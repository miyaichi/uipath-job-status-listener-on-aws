# coding:utf-8
import gettext
import json
import os
import requests


def create_ticket(process_name, state, info, machine_name, payload):
    api_key = os.environ["api_key"]
    space_key = os.environ["space_key"]
    project_id = os.environ["project_id"]
    issue_type_id = os.environ["issue_type_id"]
    priority_id = os.environ["priority_id"]

    (process_name, state, info, machine_name) = map(
        lambda s: s.encode("utf-8"), (process_name, state, info, machine_name))

    summery = "{} {}".format(process_name, state.lower())
    description = "Info: {}&br;Machine Name: {}&br;Data:&br;{}".format(
        info, machine_name,
        json.dumps(
            payload,
            ensure_ascii=False,
            encoding="utf-8",
            sort_keys=True,
            indent=4))

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(
        "https://{}.backlog.jp/api/v2/issues".format(space_key),
        headers=headers,
        params={
            "apiKey": api_key,
            "projectId": project_id,
            "issueTypeId": issue_type_id,
            "priorityId": priority_id,
            "summary": summery,
            "description": description
        })
    return response


def scheduled_handler(joblist):
    joblist = filter(lambda job: job["State"] in ["Faulted", "Stopped"],
                     joblist)
    for job in joblist:
        response = create_ticket(job["ReleaseName"], job["State"], job["Info"],
                                 job["HostMachineName"], job)
        if response.status_code != 200:
            return response.text

    return _("{} issues posted").format(len(joblist))


def webhook_handler(payload):
    job = payload["Job"]
    if job["State"] not in ["Faulted", "Stopped"]:
        return _("This webhook was ignored")

    response = create_message(job["Release"]["ProcessKey"], job["State"],
                              job["Info"], job["Robot"]["MachineName"], job)
    if response.status_code != 200:
        return response.text

    return _("{} issues posted").format(1)
