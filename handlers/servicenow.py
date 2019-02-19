# coding:utf-8
import gettext
import handlers
import json
import os
import requests


def create_ticket(process_name, state, info, machine_name, payload):
    url = os.environ["url"]
    username = os.environ["username"]
    password = os.environ["password"]
    assignment_group = os.environ["assignment_group"]
    urgency = os.environ["urgency"]
    impact = os.environ["impact"]

    (process_name, state, info, machine_name) = map(
        lambda s: s.encode("utf-8"), (process_name, state, info, machine_name))

    summery = "{} {}".format(process_name, state.lower())
    description = "Info: {}¥nMachine Name: {}¥nData:¥n{}".format(
        info, machine_name, handlers.dumps(payload))

    headers = {'Content-type': 'application/json'}
    response = requests.post(
        "{}/rest/api/2/issue/".format(url),
        json.dumps({
            "short_description": summery,
            "comment": description,
            "assignment_group": assignment_group,
            "urgency": urgency,
            "impact": impact
        }),
        auth=(username, password),
        headers=headers)
    return response


def scheduled_handler(joblist):
    for job in joblist:
        response = create_ticket(job["ReleaseName"], job["State"], job["Info"],
                                 job["HostMachineName"], job)
        if response.status_code != 200:
            return response.text

    return _("{} issues posted").format(len(joblist))


def webhook_handler(payload):
    job = payload["Job"]
    response = create_ticket(job["Release"]["ProcessKey"], job["State"],
                             job["Info"], job["Robot"]["MachineName"], job)
    if response.status_code != 200:
        return response.text

    return _("{} issues posted").format(1)
