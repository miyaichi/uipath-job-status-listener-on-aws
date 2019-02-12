import json
import os
import requests


def create_ticket(summary, description):
    api_key = os.environ["api_key"]
    space_key = os.environ["space_key"]
    project_id = os.environ["project_id"]
    issue_type_id = os.environ["issue_type_id"]
    priority_id = 3

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    params = {
        "apiKey": api_key,
        "projectId": project_id,
        "issueTypeId": issue_type_id,
        "priorityId": priority_id,
        "summary": summary,
        "description": description
    }
    response = requests.post(
        "https://{}.backlog.jp/api/v2/issues".format(space_key),
        headers=headers,
        params=params)
    return response


def scheduled_handler(joblist):
    issues = 0
    for job in joblist:
        if job["State"] not in ["Faulted", "Stopped"]:
            continue

        issues += issues

        state = job["State"]
        release_name = job["ReleaseName"]

        response = create_ticket(
            "{} {}".format(release_name, state),
            json.dumps(
                job,
                ensure_ascii=False,
                encoding="utf-8",
                sort_keys=True,
                indent=4))
        if response.status_code != 200:
            return response.text

    return _("{} messages sent").format(issues)


def webhook_handler(payload):
    if payload["Type"] not in ["job.faulted", "job.stopped"]:
        return _("This webhook was ignored")

    type = payload["Type"]
    process_key = payload["Job"]["Release"]["ProcessKey"].encode("utf-8")

    response = create_ticket(
        "{} {}".format(process_key, " ".join(type.split("."))),
        json.dumps(
            payload,
            ensure_ascii=False,
            encoding="utf-8",
            sort_keys=True,
            indent=4))
    if response.status_code != 200:
        return response.text

    return _("{} messages sent").format(1)
