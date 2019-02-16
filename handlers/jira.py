# coding:utf-8
import gettext
import json
import os
import requests


def create_ticket(process_name, state, info, machine_name, payload):
    url = os.environ["url"]
    username = os.environ["username"]
    password = os.environ["password"]
    project = os.environ["project"]
    issue_type = os.environ["issue_type"]

    (process_name, state, info, machine_name) = map(
        lambda s: s.encode("utf-8"), (process_name, state, info, machine_name))

    summery = "{} {}".format(process_name, state.lower())
    description = "Info: {}¥nMachine Name: {}¥nData:¥n{}".format(
        info, machine_name,
        json.dumps(
            payload,
            ensure_ascii=False,
            encoding="utf-8",
            sort_keys=True,
            indent=4))

    headers = {'Content-type': 'application/json'}
    auth = (username, password)
    response = requests.post(
        "{}/rest/api/2/issue/".format(url),
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
