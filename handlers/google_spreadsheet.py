# coding:utf-8
import gettext
import json
import os
import requests
from apiclient import discovery
from google.oauth2 import service_account


def append_data(joblist):
    credential_file = os.environ["credential_file"]
    spreadsheet_id = os.environ["spreadsheet_id"]
    sheet = os.environ["sheet"]

    try:
        service = discovery.build(
            "sheets",
            "v4",
            credentials=service_account.Credentials.from_service_account_file(
                credential_file,
                scopes=["https://www.googleapis.com/auth/spreadsheets"]),
            cache_discovery=False)

        range = "{}!{}:{}".format(sheet, "A",
                                  chr(ord("A") + len(joblist[0]) - 1))

        data = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range).execute()
        if "values" not in data:
            columns = sorted(joblist[0].keys())
            values = [columns]
        else:
            columns = data["values"][0]
            values = []

        for job in joblist:
            value = []
            for column in columns:
                value.append(job[column])
            values.append(value)

        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range,
            body={
                "majorDimension": "ROWS",
                "values": values
            },
            valueInputOption="USER_ENTERED").execute()

        return _("{} messages sent").format(len(joblist))

    except Exception, e:
        return str(e)


def scheduled_handler(joblist):
    joblist = filter(lambda job: job["State"] in ["Faulted", "Stopped"],
                     joblist)
    response = append_data(joblist)
    return response


def webhook_handler(payload):
    job = payload["Job"]
    if job["State"] not in ["Faulted", "Stopped"]:
        return _("This webhook was ignored")

    response = append_data([job])
    return response
