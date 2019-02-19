# coding:utf-8
import gettext
import handlers
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

        columns = sorted(joblist[0].keys())
        values = [columns]

        data = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range="{}!A1:1".format(sheet)).execute()
        if "values" in data:
            columns = data["values"][0]
            values = []

        for job in joblist:
            job = handlers.flatten(job)
            job = handlers.timeformat(job)
            values.append(
                list(map(lambda c: job[c] if c in job else "", columns)))

        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range="{}!A:A".format(sheet),
            body={
                "majorDimension": "ROWS",
                "values": values
            },
            valueInputOption="USER_ENTERED").execute()

        return _("{} messages sent").format(len(joblist))

    except Exception, e:
        return str(e)


def scheduled_handler(joblist):
    response = append_data(joblist)
    return response


def webhook_handler(payload):
    job = payload["Job"]
    response = append_data([job])
    return response
