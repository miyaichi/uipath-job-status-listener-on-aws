import json
import os
import requests


def post_message(text):
    webhook_url = os.environ["incomming_webhook_url"]

    headers = {"Content-Type": "application/json; charset=UTF-8"}
    response = requests.post(
        webhook_url, data=json.dumps({
            "text": text
        }), headers=headers)
    return response


def scheduled_handler(joblist):
    for job in joblist:
        release_name = job["ReleaseName"]
        info = job["Info"]
        state = job["State"]

        response = post_message("*{}* {}.\n{}".format(release_name, state,
                                                      info))
        if response.status_code != 200:
            return response.text

    return _("{} messages sent").format(len(joblist))


def webhook_handler(payload):
    type = payload["Type"]
    process_key = payload["Job"]["Release"]["ProcessKey"].encode("utf-8")
    info = payload["Job"]["Info"].encode("utf-8")
    machine_name = payload["Job"]["Robot"]["MachineName"].encode("utf-8")

    response = post_message("*{}* {}.\n{}\n\nMachine Name: {}".format(
        process_key, " ".join(type.split(".")), info, machine_name))
    if response.status_code != 200:
        return response.text

    return _("{} messages sent").format(1)
