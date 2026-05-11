#!/usr/bin/env python3
import _venv
"""Pull a Canvas course gradebook through documented REST API resources.

This module reconstructs the gradebook from assignments, student submissions,
and active student enrollments. It intentionally does not use Canvas' internal
Gradebook CSV export route.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import requests

try:
    from _credentials import API_KEY as DEFAULT_API_KEY
    from _credentials import API_URL as DEFAULT_API_URL
    from _credentials import COURSE_NUM as DEFAULT_COURSE_ID
    from _credentials import MY_PATH as DEFAULT_COURSE_PATH
except Exception:
    DEFAULT_API_KEY = None
    DEFAULT_API_URL = None
    DEFAULT_COURSE_ID = None
    DEFAULT_COURSE_PATH = None

DEFAULT_OUTPUT_DIR = (
    str(Path(DEFAULT_COURSE_PATH) / "gradebook_export")
    if DEFAULT_COURSE_PATH
    else "gradebook_export"
)


@dataclass
class CanvasGradebook:
    assignments: list[dict[str, Any]]
    enrollments: list[dict[str, Any]]
    submissions: list[dict[str, Any]]
    long_rows: list[dict[str, Any]]
    wide_rows: list[dict[str, Any]]
    total_rows: list[dict[str, Any]]


class CanvasAPI:
    """Small REST client with Canvas Link-header pagination support."""

    def __init__(self, api_url: str, api_key: str, timeout: int = 60) -> None:
        self.api_url = api_url.rstrip("/") + "/"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
            }
        )

    def get_json(self, path_or_url: str, params: dict[str, Any] | None = None) -> Any:
        url = self._url(path_or_url)
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_paginated(
        self, path: str, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        url = self._url(path)
        page_params = dict(params or {})
        page_params.setdefault("per_page", 100)

        items: list[dict[str, Any]] = []
        while url:
            response = self.session.get(url, params=page_params, timeout=self.timeout)
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, list):
                raise ValueError(f"Expected a list response from {url}")
            items.extend(payload)
            url = response.links.get("next", {}).get("url")
            page_params = None
        return items

    def _url(self, path_or_url: str) -> str:
        if path_or_url.startswith(("http://", "https://")):
            return path_or_url
        return urljoin(self.api_url, path_or_url.lstrip("/"))


def pull_assignments(client: CanvasAPI, course_id: int) -> list[dict[str, Any]]:
    return client.get_paginated(
        f"/api/v1/courses/{course_id}/assignments",
        {
            "order_by": "position",
        },
    )


def pull_submissions(client: CanvasAPI, course_id: int) -> list[dict[str, Any]]:
    return client.get_paginated(
        f"/api/v1/courses/{course_id}/students/submissions",
        {
            "student_ids[]": ["all"],
            "enrollment_state": "active",
            "include[]": ["rubric_assessment"],
        },
    )


def pull_active_student_enrollments(
    client: CanvasAPI, course_id: int
) -> list[dict[str, Any]]:
    return client.get_paginated(
        f"/api/v1/courses/{course_id}/enrollments",
        {
            "type[]": ["StudentEnrollment"],
            "state[]": ["active"],
            "include[]": ["current_points"],
        },
    )


def build_gradebook(
    assignments: list[dict[str, Any]],
    submissions: list[dict[str, Any]],
    enrollments: list[dict[str, Any]],
) -> CanvasGradebook:
    assignments_by_id = {assignment["id"]: assignment for assignment in assignments}
    submission_by_student_assignment = {
        (submission.get("user_id"), submission.get("assignment_id")): submission
        for submission in submissions
        if submission.get("assignment_id") in assignments_by_id
    }

    students = [student_from_enrollment(enrollment) for enrollment in enrollments]
    long_rows: list[dict[str, Any]] = []
    wide_rows: list[dict[str, Any]] = []
    total_rows: list[dict[str, Any]] = []

    score_columns = assignment_score_columns(assignments)

    for enrollment in enrollments:
        student = student_from_enrollment(enrollment)
        user_id = student["student_id"]

        wide_row: dict[str, Any] = {
            "student_id": user_id,
            "student_name": student["student_name"],
            "student_sortable_name": student["student_sortable_name"],
            "student_login_id": student["student_login_id"],
            "student_sis_user_id": student["student_sis_user_id"],
            "section_id": enrollment.get("course_section_id"),
            "enrollment_id": enrollment.get("id"),
        }

        for assignment in assignments:
            assignment_id = assignment["id"]
            submission = submission_by_student_assignment.get((user_id, assignment_id), {})
            row = {
                **student,
                "section_id": enrollment.get("course_section_id"),
                "enrollment_id": enrollment.get("id"),
                "assignment_id": assignment_id,
                "assignment_name": assignment.get("name"),
                "assignment_position": assignment.get("position"),
                "assignment_group_id": assignment.get("assignment_group_id"),
                "points_possible": assignment.get("points_possible"),
                "due_at": assignment.get("due_at"),
                "published": assignment.get("published"),
                "muted": assignment.get("muted"),
                "submission_id": submission.get("id"),
                "workflow_state": submission.get("workflow_state"),
                "submitted_at": submission.get("submitted_at"),
                "graded_at": submission.get("graded_at"),
                "posted_at": submission.get("posted_at"),
                "late": submission.get("late"),
                "missing": submission.get("missing"),
                "excused": submission.get("excused"),
                "score": submission.get("score"),
                "grade": submission.get("grade"),
                "entered_score": submission.get("entered_score"),
                "entered_grade": submission.get("entered_grade"),
            }
            long_rows.append(row)
            wide_row[score_columns[assignment_id]] = submission.get("score")

        wide_rows.append(wide_row)
        total_rows.append(total_row_from_enrollment(enrollment, student))

    long_rows.sort(key=lambda row: (row.get("student_sortable_name") or "", row["assignment_position"] or 0))
    wide_rows.sort(key=lambda row: row.get("student_sortable_name") or "")
    total_rows.sort(key=lambda row: row.get("student_sortable_name") or "")

    return CanvasGradebook(
        assignments=assignments,
        enrollments=enrollments,
        submissions=submissions,
        long_rows=long_rows,
        wide_rows=wide_rows,
        total_rows=total_rows,
    )


def student_from_enrollment(enrollment: dict[str, Any]) -> dict[str, Any]:
    user = enrollment.get("user") or {}
    return {
        "student_id": enrollment.get("user_id") or user.get("id"),
        "student_name": user.get("name"),
        "student_sortable_name": user.get("sortable_name") or user.get("name"),
        "student_login_id": user.get("login_id"),
        "student_sis_user_id": user.get("sis_user_id"),
    }


def total_row_from_enrollment(
    enrollment: dict[str, Any], student: dict[str, Any]
) -> dict[str, Any]:
    grades = enrollment.get("grades") or {}
    return {
        **student,
        "section_id": enrollment.get("course_section_id"),
        "enrollment_id": enrollment.get("id"),
        "enrollment_state": enrollment.get("enrollment_state"),
        "current_score": grades.get("current_score"),
        "current_grade": grades.get("current_grade"),
        "final_score": grades.get("final_score"),
        "final_grade": grades.get("final_grade"),
        "current_points": grades.get("current_points"),
        "unposted_current_score": grades.get("unposted_current_score")
        or enrollment.get("unposted_current_score"),
        "unposted_current_grade": grades.get("unposted_current_grade")
        or enrollment.get("unposted_current_grade"),
        "unposted_final_score": grades.get("unposted_final_score")
        or enrollment.get("unposted_final_score"),
        "unposted_final_grade": grades.get("unposted_final_grade")
        or enrollment.get("unposted_final_grade"),
        "unposted_current_points": grades.get("unposted_current_points"),
        "override_score": enrollment.get("override_score"),
        "override_grade": enrollment.get("override_grade"),
    }


def assignment_score_columns(assignments: list[dict[str, Any]]) -> dict[int, str]:
    columns: dict[int, str] = {}
    seen: set[str] = set()
    for assignment in assignments:
        assignment_id = assignment["id"]
        base = f"score_{assignment_id}_{slugify(assignment.get('name') or 'assignment')}"
        column = base[:120]
        suffix = 2
        while column in seen:
            column = f"{base[:112]}_{suffix}"
            suffix += 1
        seen.add(column)
        columns[assignment_id] = column
    return columns


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = value.strip("_")
    return value or "assignment"


def write_outputs(
    gradebook: CanvasGradebook,
    output_dir: str | Path,
    pulled_at: str,
    course_id: int,
    write_parquet: bool = False,
) -> dict[str, Path]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    long_rows = add_pull_timestamp(gradebook.long_rows, pulled_at)
    wide_rows = add_pull_timestamp(gradebook.wide_rows, pulled_at)
    total_rows = add_pull_timestamp(gradebook.total_rows, pulled_at)
    metadata_rows = [
        {
            "pulled_at": pulled_at,
            "course_id": course_id,
            "assignments": len(gradebook.assignments),
            "active_student_enrollments": len(gradebook.enrollments),
            "submissions": len(gradebook.submissions),
            "long_rows": len(gradebook.long_rows),
            "wide_rows": len(gradebook.wide_rows),
            "total_rows": len(gradebook.total_rows),
        }
    ]

    paths = {
        "gradebook_long_csv": output_path / "gradebook_long.csv",
        "gradebook_wide_csv": output_path / "gradebook_wide.csv",
        "course_totals_csv": output_path / "course_totals.csv",
        "metadata_csv": output_path / "gradebook_pull_metadata.csv",
    }
    write_csv(paths["gradebook_long_csv"], long_rows)
    write_csv(paths["gradebook_wide_csv"], wide_rows)
    write_csv(paths["course_totals_csv"], total_rows)
    write_csv(paths["metadata_csv"], metadata_rows)

    if write_parquet:
        paths.update(write_parquet_outputs(long_rows, wide_rows, total_rows, output_path))

    return paths


def add_pull_timestamp(rows: list[dict[str, Any]], pulled_at: str) -> list[dict[str, Any]]:
    return [{"pulled_at": pulled_at, **row} for row in rows]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = ordered_fieldnames(rows)
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def ordered_fieldnames(rows: list[dict[str, Any]]) -> list[str]:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    return fieldnames


def write_parquet_outputs(
    long_rows: list[dict[str, Any]],
    wide_rows: list[dict[str, Any]],
    total_rows: list[dict[str, Any]],
    output_path: Path,
) -> dict[str, Path]:
    if importlib.util.find_spec("pandas") is None:
        raise RuntimeError(
            "Parquet output requires pandas plus pyarrow or fastparquet. "
            "Install them in this environment or rerun without --parquet."
        )

    import pandas as pd

    paths = {
        "gradebook_long_parquet": output_path / "gradebook_long.parquet",
        "gradebook_wide_parquet": output_path / "gradebook_wide.parquet",
        "course_totals_parquet": output_path / "course_totals.parquet",
    }
    pd.DataFrame(long_rows).to_parquet(paths["gradebook_long_parquet"], index=False)
    pd.DataFrame(wide_rows).to_parquet(paths["gradebook_wide_parquet"], index=False)
    pd.DataFrame(total_rows).to_parquet(paths["course_totals_parquet"], index=False)
    return paths


def current_pull_timestamp() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def dated_output_dir(output_dir: str | Path, pulled_at: str) -> Path:
    snapshot_name = pulled_at.split("T", 1)[0]
    return Path(output_dir) / snapshot_name


def pull_gradebook(api_url: str, api_key: str, course_id: int) -> CanvasGradebook:
    client = CanvasAPI(api_url, api_key)
    assignments = pull_assignments(client, course_id)
    submissions = pull_submissions(client, course_id)
    enrollments = pull_active_student_enrollments(client, course_id)
    return build_gradebook(assignments, submissions, enrollments)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pull Canvas gradebook data through documented REST API endpoints."
    )
    parser.add_argument("--api-url", default=os.environ.get("CANVAS_API_URL") or DEFAULT_API_URL)
    parser.add_argument("--api-key", default=os.environ.get("CANVAS_API_KEY") or DEFAULT_API_KEY)
    parser.add_argument(
        "--course-id",
        type=int,
        default=int(os.environ.get("CANVAS_COURSE_ID") or DEFAULT_COURSE_ID or 0),
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=(
            "Root directory for gradebook exports. By default, each run writes "
            "to a timestamped subdirectory inside this directory."
        ),
    )
    parser.add_argument(
        "--flat-output",
        action="store_true",
        help="Write directly to --output-dir and overwrite files from previous runs.",
    )
    parser.add_argument(
        "--parquet",
        action="store_true",
        help="Also write .parquet files when pandas and a parquet engine are installed.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if not args.api_url:
        sys.exit("Missing Canvas API URL. Set CANVAS_API_URL or pass --api-url.")
    if not args.api_key:
        sys.exit("Missing Canvas API key. Set CANVAS_API_KEY or pass --api-key.")
    if not args.course_id:
        sys.exit("Missing Canvas course ID. Set CANVAS_COURSE_ID or pass --course-id.")

    pulled_at = current_pull_timestamp()
    output_dir = Path(args.output_dir) if args.flat_output else dated_output_dir(args.output_dir, pulled_at)

    print(f"Pulling Canvas gradebook for course {args.course_id} at {pulled_at}...")
    gradebook = pull_gradebook(args.api_url, args.api_key, args.course_id)
    paths = write_outputs(
        gradebook,
        output_dir,
        pulled_at=pulled_at,
        course_id=args.course_id,
        write_parquet=args.parquet,
    )

    print(f"Assignments: {len(gradebook.assignments)}")
    print(f"Active student enrollments: {len(gradebook.enrollments)}")
    print(f"Submissions: {len(gradebook.submissions)}")
    print("Wrote:")
    for path in paths.values():
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
