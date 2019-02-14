import gettext
import json
import os
import requests


def post_message(process_name, state, info, machine_name):
    webhook_url = os.environ["incomming_webhook_url"]

    color = {
        "Faulted": "danger",
        "Successful": "good",
        "Stopped": "warning"
    }.get(state, "")

    headers = {"Content-Type": "application/json"}
    response = requests.post(
        webhook_url,
        data=json.dumps({
            "attachments": [{
                "fallback":
                "{} {}".format(process_name, state.lower()),
                "color":
                color,
                "fields": [{
                    "title":
                    "{} {}".format(process_name, state.lower()),
                    "value":
                    info
                }],
                "footer":
                "Machine Name: {}".format(machine_name)
            }]
        }))
    return response


def scheduled_handler(joblist):
    for job in joblist:
        release_name = job["ReleaseName"]
        info = job["Info"]
        state = job["State"]
        machine_name = job["HostMachineName"]

        response = post_message(release_name, state, info, machine_name)
        if response.status_code != 200:
            return response.text

    return _("{} messages sent").format(len(joblist))


def webhook_handler(payload):
    process_key = payload["Job"]["Release"]["ProcessKey"].encode("utf-8")
    info = payload["Job"]["Info"].encode("utf-8")
    state = payload["Job"]["State"].encode("utf-8")
    machine_name = payload["Job"]["Robot"]["MachineName"].encode("utf-8")

    response = post_message(process_key, state, info, machine_name)
    if response.status_code != 200:
        return response.text

    return _("{} messages sent").format(1)
