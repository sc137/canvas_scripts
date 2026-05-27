#!/usr/bin/env python3
# import_qti_quizzes.py
# Import QTI quiz packages into Canvas Classic Quizzes with matching question banks.

import _venv
import argparse
import re
import sys
import time
import zipfile
from pathlib import Path
from xml.etree import ElementTree

import requests

try:
    from _client import get_canvas_and_course
    from _credentials import API_KEY, API_URL, COURSE_NUM
except ImportError:
    sys.exit("Please run setup_course.py to install requirements and create _credentials.py")

SUPPORTED_EXTENSIONS = {".zip", ".qti"}


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Import one QTI package or a directory of QTI packages into Canvas "
            "Classic Quizzes. Each import creates/uses a question bank named "
            "from the quiz file."
        )
    )
    parser.add_argument(
        "source",
        help="Path to a QTI .zip/.qti file or a directory containing QTI packages.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Search subfolders when source is a directory.",
    )
    parser.add_argument(
        "--bank-name",
        default=None,
        help="Question bank name to use for a single QTI file. Not allowed for folders.",
    )
    parser.add_argument(
        "--bank-suffix",
        default=" Test Bank",
        help="Text appended to each derived bank name. Default appends 'Test Bank'.",
    )
    parser.add_argument(
        "--name-from",
        choices=["qti", "filename"],
        default="qti",
        help=(
            "Use the QTI assessment title when available, or use only the filename. "
            "Default: qti."
        ),
    )
    parser.add_argument(
        "--overwrite-quizzes",
        action="store_true",
        help="Ask Canvas to overwrite quizzes with matching identifiers in the QTI package.",
    )
    parser.add_argument(
        "--module-id",
        default=None,
        help="Optional Canvas module ID where imported quiz items should be inserted.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip the confirmation prompt.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be imported without contacting Canvas.",
    )
    parser.add_argument(
        "--allow-nonstandard",
        action="store_true",
        help="Allow upload even when the zip does not look like a standard QTI package.",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=10,
        help="Seconds to wait between Canvas migration status checks. Default: 10.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="Maximum seconds to wait for each import. Default: 900.",
    )
    return parser.parse_args()


def clean_name_from_file(path):
    name = path.stem
    name = re.sub(r"[_-]+", " ", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def clean_text(value):
    return re.sub(r"\s+", " ", value or "").strip()


def tag_name(element):
    return element.tag.rsplit("}", 1)[-1]


def qti_assessment_title(path):
    if not zipfile.is_zipfile(path):
        return None

    try:
        with zipfile.ZipFile(path) as qti_zip:
            xml_names = [
                name
                for name in qti_zip.namelist()
                if name.lower().endswith(".xml") and not name.endswith("/")
            ]
            prioritized_names = sorted(
                xml_names,
                key=lambda name: ("assessment" not in name.lower(), name.lower()),
            )

            for xml_name in prioritized_names:
                with qti_zip.open(xml_name) as xml_file:
                    for _, element in ElementTree.iterparse(xml_file, events=("start",)):
                        if tag_name(element) == "assessment":
                            title = clean_text(element.attrib.get("title"))
                            if title:
                                return title
    except Exception:
        return None

    return None


def inspect_qti_package(path):
    result = {
        "is_zip": zipfile.is_zipfile(path),
        "xml_count": 0,
        "has_manifest": False,
        "has_assessment": False,
    }

    if not result["is_zip"]:
        return result

    try:
        with zipfile.ZipFile(path) as qti_zip:
            for name in qti_zip.namelist():
                lower_name = name.lower()
                if lower_name.endswith("imsmanifest.xml"):
                    result["has_manifest"] = True
                if not lower_name.endswith(".xml"):
                    continue

                result["xml_count"] += 1
                if result["has_assessment"]:
                    continue

                with qti_zip.open(name) as xml_file:
                    for _, element in ElementTree.iterparse(xml_file, events=("start",)):
                        if tag_name(element) == "assessment":
                            result["has_assessment"] = True
                            break
    except Exception:
        return result

    return result


def qti_validation_message(result):
    if not result["is_zip"]:
        return "file is not a readable zip archive"
    if result["xml_count"] == 0:
        return "zip contains no XML files, so Canvas has no QTI content to convert"
    if not result["has_manifest"] and not result["has_assessment"]:
        return "zip has XML, but no imsmanifest.xml or QTI assessment element was found"
    return None


def quiz_name_from_path(path, name_from="qti"):
    if name_from == "qti":
        title = qti_assessment_title(path)
        if title:
            return title

    return clean_name_from_file(path)


def discover_qti_files(source, recursive=False):
    source_path = Path(source).expanduser().resolve()
    if not source_path.exists():
        sys.exit(f"[-] Source path does not exist: {source_path}")

    if source_path.is_file():
        if source_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            sys.exit(f"[-] Source file must be one of: {', '.join(sorted(SUPPORTED_EXTENSIONS))}")
        return [source_path]

    pattern = "**/*" if recursive else "*"
    files = [
        path
        for path in source_path.glob(pattern)
        if path.is_file()
        and not path.name.startswith(".")
        and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return sorted(files)


def build_import_plan(files, bank_name=None, bank_suffix=" Test Bank", name_from="qti"):
    if bank_name and len(files) != 1:
        sys.exit("[-] --bank-name can only be used when importing one file.")

    plan = []
    for path in files:
        quiz_name = quiz_name_from_path(path, name_from)
        question_bank_name = bank_name if bank_name else f"{quiz_name}{bank_suffix}"
        validation = inspect_qti_package(path)
        plan.append(
            {
                "path": path,
                "quiz_name": quiz_name,
                "question_bank_name": question_bank_name,
                "validation": validation,
            }
        )
    return plan


def canvas_api_url(path):
    return f"{API_URL.rstrip('/')}/api/v1{path}"


def auth_headers():
    return {"Authorization": f"Bearer {API_KEY}"}


def request_json(method, url, **kwargs):
    response = requests.request(method, url, headers=auth_headers(), **kwargs)
    response.raise_for_status()
    if not response.content:
        return None
    return response.json()


def paginated_get(path):
    url = canvas_api_url(path)
    items = []

    while url:
        response = requests.get(url, headers=auth_headers())
        response.raise_for_status()
        items.extend(response.json())
        url = None

        for link in response.links.values():
            if link.get("rel") == "next":
                url = link.get("url")
                break

    return items


def get_quiz_ids():
    quizzes = paginated_get(f"/courses/{COURSE_NUM}/quizzes?per_page=100")
    return {quiz.get("id") for quiz in quizzes}


def get_quiz_lookup():
    quizzes = paginated_get(f"/courses/{COURSE_NUM}/quizzes?per_page=100")
    return {quiz.get("id"): quiz for quiz in quizzes}


def get_question_bank(question_bank_name):
    banks = paginated_get(
        f"/question_banks?context_type=Course&context_id={COURSE_NUM}"
        "&include_question_count=true&per_page=100"
    )
    for bank in banks:
        if bank.get("title") == question_bank_name:
            return bank
    return None


def create_qti_migration(item, overwrite_quizzes=False, module_id=None):
    path = item["path"]
    data = {
        "migration_type": "qti_converter",
        "pre_attachment[name]": path.name,
        "pre_attachment[size]": str(path.stat().st_size),
        "settings[question_bank_name]": item["question_bank_name"],
    }

    if overwrite_quizzes:
        data["settings[overwrite_quizzes]"] = "true"

    if module_id:
        data["settings[insert_into_module_id]"] = str(module_id)
        data["settings[insert_into_module_type]"] = "quiz"

    return request_json(
        "POST",
        canvas_api_url(f"/courses/{COURSE_NUM}/content_migrations"),
        data=data,
    )


def upload_migration_file(migration, path):
    pre_attachment = migration.get("pre_attachment")
    if not pre_attachment:
        raise RuntimeError("Canvas did not return pre_attachment upload information.")

    upload_url = pre_attachment["upload_url"]
    upload_params = pre_attachment.get("upload_params", {})

    with path.open("rb") as file_handle:
        response = requests.post(
            upload_url,
            data=upload_params,
            files={"file": (path.name, file_handle, "application/zip")},
        )
    response.raise_for_status()


def poll_migration(migration_id, poll_interval=10, timeout=900):
    deadline = time.monotonic() + timeout
    last_state = None

    while time.monotonic() < deadline:
        migration = request_json(
            "GET",
            canvas_api_url(f"/courses/{COURSE_NUM}/content_migrations/{migration_id}"),
        )
        state = migration.get("workflow_state")

        if state != last_state:
            print(f"    Canvas status: {state}")
            last_state = state

        if state == "completed":
            return migration

        if state == "failed":
            raise RuntimeError("Canvas marked the QTI migration as failed.")

        time.sleep(poll_interval)

    raise TimeoutError(f"Timed out after {timeout} seconds waiting for Canvas migration.")


def get_migration_issues(migration_id):
    return paginated_get(
        f"/courses/{COURSE_NUM}/content_migrations/{migration_id}/migration_issues?per_page=100"
    )


def print_import_results(item, before_quiz_ids):
    try:
        after_quizzes = get_quiz_lookup()
        created_quizzes = [
            quiz for quiz_id, quiz in after_quizzes.items() if quiz_id not in before_quiz_ids
        ]
    except Exception as error:
        print(f"    Warning: could not look up quizzes after import: {error}")
        created_quizzes = []

    if created_quizzes:
        print("    New Classic Quiz item(s):")
        for quiz in created_quizzes:
            print(f"      - {quiz.get('title')} ({quiz.get('html_url')})")
    else:
        print("    No new quiz was detected by ID. Canvas may have updated an existing quiz.")

    try:
        bank = get_question_bank(item["question_bank_name"])
        if bank:
            question_count = bank.get("assessment_question_count")
            count_note = f", {question_count} question(s)" if question_count is not None else ""
            print(f"    Question bank: {bank.get('title')} (ID: {bank.get('id')}{count_note})")
        else:
            print(f"    Question bank not found by exact name: {item['question_bank_name']}")
    except Exception as error:
        print(f"    Warning: could not look up question bank after import: {error}")


def import_qti(item, overwrite_quizzes=False, module_id=None, poll_interval=10, timeout=900):
    print(f"[+] Importing {item['path'].name}")
    print(f"    Question bank: {item['question_bank_name']}")

    before_quiz_ids = get_quiz_ids()
    migration = create_qti_migration(item, overwrite_quizzes, module_id)
    print(f"    Migration created: {migration.get('id')}")

    upload_migration_file(migration, item["path"])
    print("    Upload complete. Waiting for Canvas to process the QTI package.")

    migration = poll_migration(migration["id"], poll_interval, timeout)

    issues = get_migration_issues(migration["id"])
    if issues:
        print("    Migration issues:")
        for issue in issues:
            issue_type = issue.get("issue_type", "issue")
            description = issue.get("description", "No description provided.")
            print(f"      - {issue_type}: {description}")
    else:
        print("    No migration issues reported.")

    print_import_results(item, before_quiz_ids)
    return migration


def main():
    args = parse_args()
    files = discover_qti_files(args.source, args.recursive)
    if not files:
        sys.exit("[-] No QTI .zip or .qti files found.")

    plan = build_import_plan(files, args.bank_name, args.bank_suffix, args.name_from)

    print("QTI import plan:")
    for item in plan:
        print(f"  - {item['path']}")
        print(f"    bank: {item['question_bank_name']}")
        warning = qti_validation_message(item["validation"])
        if warning:
            print(f"    warning: {warning}")
    print()

    invalid_items = [
        item for item in plan if qti_validation_message(item["validation"])
    ]
    if invalid_items and not args.allow_nonstandard:
        print("One or more files do not look like standard QTI packages.")
        print("No Canvas changes were made. Re-export the file as QTI, or rerun with --allow-nonstandard.")
        return 1

    if args.dry_run:
        print("Dry run only. No Canvas changes were made.")
        return 0

    _, course = get_canvas_and_course()
    print(f"Selected course: {course.name} (ID: {COURSE_NUM})")
    print()

    if not args.yes:
        confirm = input("Import these QTI package(s) into this course? (y/n): ").strip().lower()
        if confirm != "y":
            print("Import cancelled.")
            return 0

    failures = []
    for item in plan:
        try:
            import_qti(
                item,
                overwrite_quizzes=args.overwrite_quizzes,
                module_id=args.module_id,
                poll_interval=args.poll_interval,
                timeout=args.timeout,
            )
        except Exception as error:
            print(f"[-] Failed to import {item['path'].name}: {error}")
            failures.append(item["path"].name)

    print()
    print("=" * 40)
    print(f"QTI packages processed: {len(plan)}")
    print(f"Successful imports:     {len(plan) - len(failures)}")
    print(f"Failed imports:         {len(failures)}")
    if failures:
        print("Failed files:")
        for filename in failures:
            print(f"  - {filename}")
    print("=" * 40)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
