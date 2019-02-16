import json
import os
import requests


def create_ticket(process_name, state, info, machie_name, payload):
    url = os.environ["url"]
    username = os.environ["username"]
    password = os.environ["password"]
    project = os.environ["project"]
    issue_type = os.environ["issue_type"]

    summery = "{} {}".format(process_name, state.lower())
    description = "Info: {}¥nMachine Name: {}¥nData:¥n{}".format(
        info, machie_name,
        json.dumps(
            payload,
            ensure_ascii=False,
            encoding="utf-8",
            sort_keys=True,
            indent=4))

    headers = {'Content-type': 'application/json'}
    auth = (username, password)
    response = requests.post(
        url + "/rest/api/2/issue/",
        json.dumps({
            "project": {
                "key": project
            },
            "fields": {
                "summary": summery,
                "description": description,
                "issuetype": {
                    "name": issue_type
                }
            }
        }),
        auth=auth,
        headers=headers)
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
