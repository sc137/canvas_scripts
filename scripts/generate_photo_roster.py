#!/usr/bin/env python3
"""Generate a Canvas photo roster page using scripts/_credentials.py.

This script is intended to run from the scripts/ folder and read:
- API_URL
- API_KEY
- COURSE_NUM
"""

import argparse
import html
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from _credentials import API_KEY, API_URL, COURSE_NUM  # type: ignore

try:
    from _credentials import MY_PATH  # type: ignore
except ImportError:
    MY_PATH = None


def default_output_dir() -> Path:
    if isinstance(MY_PATH, str) and MY_PATH.strip():
        return Path(MY_PATH).expanduser() / "Photo_Roster"
    return Path(__file__).resolve().parent.parent / "Photo_Roster"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch Canvas course students and generate a static photo roster page "
            "using _credentials.py values."
        )
    )
    parser.add_argument(
        "--output-dir",
        default=str(default_output_dir()),
        help="Directory where index.html and images/ will be written.",
    )
    parser.add_argument(
        "--per-page",
        type=int,
        default=100,
        help="Canvas API page size for user fetches.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="HTTP timeout in seconds.",
    )
    return parser.parse_args()


def require_value(name: str, value: Optional[str]) -> str:
    if value is not None:
        trimmed = str(value).strip()
        if trimmed:
            return trimmed
    raise ValueError(f"Missing required value: {name}")


def api_get_json(url: str, token: str, timeout: int) -> tuple[Any, dict]:
    req = Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "User-Agent": "photo-roster-generator-v2/1.0",
        },
    )
    with urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8")
        data = json.loads(raw)
        headers = {k: v for k, v in resp.headers.items()}
    return data, headers


def parse_link_header(link_header: str) -> Dict[str, str]:
    links: Dict[str, str] = {}
    if not link_header:
        return links
    for part in link_header.split(","):
        section = part.strip()
        match = re.match(r"<([^>]+)>;\s*rel=\"([^\"]+)\"", section)
        if match:
            links[match.group(2)] = match.group(1)
    return links


def fetch_students(
    base_url: str, course_id: str, token: str, per_page: int, timeout: int
) -> List[dict]:
    base_url = base_url.rstrip("/")
    query = (
        f"enrollment_type[]=student"
        f"&include[]=avatar_url"
        f"&include[]=email"
        f"&per_page={per_page}"
    )
    next_url = f"{base_url}/api/v1/courses/{course_id}/users?{query}"
    users: List[dict] = []
    seen_ids = set()

    while next_url:
        data, headers = api_get_json(next_url, token, timeout)
        for user in data:
            user_id = user.get("id")
            if user_id is None or user_id in seen_ids:
                continue
            seen_ids.add(user_id)
            raw_profile_url = user.get("html_url")
            if isinstance(raw_profile_url, str) and raw_profile_url.strip():
                profile_url = raw_profile_url.strip()
            else:
                profile_url = f"{base_url}/courses/{course_id}/users/{user_id}"
            users.append(
                {
                    "id": user_id,
                    "name": user.get("name") or "Unknown Student",
                    "sortable_name": user.get("sortable_name")
                    or user.get("name")
                    or "",
                    "avatar_url": user.get("avatar_url") or "",
                    "email": user.get("email") or "",
                    "profile_url": profile_url,
                }
            )
        links = parse_link_header(headers.get("Link", ""))
        next_url = links.get("next")

    users.sort(key=lambda u: u["sortable_name"].lower())
    return users


def fetch_course_name(base_url: str, course_id: str, token: str, timeout: int) -> str:
    base_url = base_url.rstrip("/")
    course_url = f"{base_url}/api/v1/courses/{course_id}"
    data, _headers = api_get_json(course_url, token, timeout)
    if isinstance(data, dict):
        name = data.get("name")
        if isinstance(name, str) and name.strip():
            return name.strip()
        course_code = data.get("course_code")
        if isinstance(course_code, str) and course_code.strip():
            return course_code.strip()
    return f"Course {course_id}"


def detect_extension(url: str) -> str:
    path = urlparse(url).path
    _, ext = os.path.splitext(path.lower())
    if ext in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
        return ext
    return ".jpg"


def download_image(url: str, token: str, target_path: Path, timeout: int) -> bool:
    req = Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "photo-roster-generator-v2/1.0",
        },
    )
    try:
        with urlopen(req, timeout=timeout) as resp:
            target_path.write_bytes(resp.read())
        return True
    except Exception:
        return False


def initials_from_name(name: str) -> str:
    parts = [p for p in re.split(r"\s+", name.strip()) if p]
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][0].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def render_html(students: Iterable[dict], output_path: Path, course_name: str) -> None:
    cards: List[str] = []
    safe_course_name = html.escape(course_name)
    for student in students:
        safe_name = html.escape(student["name"])
        if student.get("image_file"):
            image_rel = html.escape(student["image_file"])
            media_html = (
                f'<img src="{image_rel}" alt="{safe_name}" loading="lazy" decoding="async">'
            )
        else:
            initial = html.escape(initials_from_name(student["name"]))
            media_html = f'<div class="placeholder" aria-label="{safe_name}">{initial}</div>'

        safe_profile_url = html.escape(student.get("profile_url", ""))
        if safe_profile_url:
            media_html = (
                f'<a class="photo-link" href="{safe_profile_url}" '
                f'target="_blank" rel="noopener noreferrer">{media_html}</a>'
            )

        cards.append(
            "\n".join(
                [
                    '<article class="card">',
                    f'  <div class="photo">{media_html}</div>',
                    f'  <h2>{safe_name}</h2>',
                    "</article>",
                ]
            )
        )

    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{safe_course_name} - Photo Roster</title>
  <style>
    :root {{
      --bg: #f4f6fb;
      --ink: #11141c;
      --muted: #5b6270;
      --card: #ffffff;
      --line: #d6dbe8;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Avenir Next", Avenir, "Segoe UI", sans-serif;
      background: linear-gradient(180deg, #ffffff 0%, var(--bg) 100%);
      color: var(--ink);
    }}
    main {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 2rem 1rem 3rem;
    }}
    h1 {{
      margin: 0 0 0.5rem;
      font-size: clamp(1.6rem, 2.3vw, 2.2rem);
    }}
    p {{
      margin: 0 0 1.5rem;
      color: var(--muted);
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
      gap: 0.9rem;
    }}
    .card {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 0.75rem;
      box-shadow: 0 4px 10px rgba(8, 15, 36, 0.06);
    }}
    .photo {{
      width: 100%;
      aspect-ratio: 1 / 1;
      overflow: hidden;
      border-radius: 10px;
      background: #eef1f7;
      display: grid;
      place-items: center;
    }}
    .photo-link {{
      width: 100%;
      height: 100%;
      display: block;
    }}
    img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .placeholder {{
      width: 100%;
      height: 100%;
      display: grid;
      place-items: center;
      font-size: 2rem;
      font-weight: 700;
      color: #3a4254;
      letter-spacing: 0.03em;
      background: radial-gradient(circle at 50% 20%, #ffffff, #dce4f6);
    }}
    h2 {{
      margin: 0.6rem 0 0.2rem;
      font-size: 1rem;
      line-height: 1.3;
      font-weight: 700;
      text-align: center;
      word-break: break-word;
    }}
  </style>
</head>
<body>
  <main>
    <h1>{safe_course_name} Photo Roster</h1>
    <p>{len(cards)} students</p>
    <section class="grid">
      {"".join(cards)}
    </section>
  </main>
</body>
</html>
"""
    output_path.write_text(html_doc, encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        base_url = require_value("API_URL from _credentials.py", API_URL)
        token = require_value("API_KEY from _credentials.py", API_KEY)
        course_id = require_value("COURSE_NUM from _credentials.py", str(COURSE_NUM))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        print(
            "Tip: set API_URL/API_KEY/COURSE_NUM in scripts/_credentials.py.",
            file=sys.stderr,
        )
        return 2

    output_dir = Path(args.output_dir).expanduser().resolve()
    images_dir = output_dir / "images"
    output_dir.mkdir(parents=True, exist_ok=True)

    course_name = fetch_course_name(base_url, course_id, token, args.timeout)
    print(f"Fetching students from course {course_id}...")
    students = fetch_students(base_url, course_id, token, args.per_page, args.timeout)
    print(f"Found {len(students)} students. Downloading images...")

    if images_dir.exists():
        shutil.rmtree(images_dir)
    images_dir.mkdir(parents=True, exist_ok=True)

    downloaded = 0
    for student in students:
        avatar_url = student.get("avatar_url")
        if not avatar_url:
            student["image_file"] = ""
            continue
        ext = detect_extension(avatar_url)
        filename = f"{student['id']}{ext}"
        target = images_dir / filename
        ok = download_image(avatar_url, token, target, args.timeout)
        if ok:
            student["image_file"] = f"images/{filename}"
            downloaded += 1
        else:
            student["image_file"] = ""

    html_path = output_dir / "index.html"
    render_html(students, html_path, course_name)

    manifest_path = output_dir / "students.json"
    manifest_path.write_text(json.dumps(students, indent=2), encoding="utf-8")

    print(f"Downloaded {downloaded}/{len(students)} photos.")
    print(f"Wrote roster page to: {html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
