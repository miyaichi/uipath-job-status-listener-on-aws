import json
import os
import requests


def create_ticket(process_name, state, info, machie_name, payload):
    api_key = os.environ["api_key"]
    space_key = os.environ["space_key"]
    project_id = os.environ["project_id"]
    issue_type_id = os.environ["issue_type_id"]
    priority_id = 3

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    params = {
        "apiKey":
        api_key,
        "projectId":
        project_id,
        "issueTypeId":
        issue_type_id,
        "priorityId":
        priority_id,
        "summary":
        "{} {}".format(process_name, state.lower()),
        "description":
        "Info: {}¥nMachine Name: {}¥nData:¥n{}".format(
            info, machie_name,
            json.dumps(
                payload,
                ensure_ascii=False,
                encoding="utf-8",
                sort_keys=True,
                indent=4))
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

        release_name = job["ReleaseName"]
        info = job["Info"]
        state = job["State"]
        machine_name = job["HostMachineName"]

        response = create_ticket(release_name, state, info, machine_name, job)
        if response.status_code != 200:
            return response.text

    return _("{} messages sent").format(issues)


def webhook_handler(payload):
    if payload["Job"]["State"] not in ["Faulted", "Stopped"]:
        return _("This webhook was ignored")

    process_key = payload["Job"]["Release"]["ProcessKey"].encode("utf-8")
    info = payload["Job"]["Info"].encode("utf-8")
    state = payload["Job"]["State"].encode("utf-8")
    machine_name = payload["Job"]["Robot"]["MachineName"].encode("utf-8")

    response = create_ticket(process_key, info, state, machine_name, payload)
    if response.status_code != 200:
        return response.text

    return _("{} messages sent").format(1)
