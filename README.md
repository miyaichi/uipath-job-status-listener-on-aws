# uipath-job-status-listener-on-aws

UiPath Orchestratorのジョブの実行結果をモニタリングし、通知する仕組みを提供します。

**Google Hangouts Chat**


![Google Hangouts Chat](https://user-images.githubusercontent.com/46800750/52513100-ee147c00-2c4b-11e9-8bd8-63907773dd46.png)


**Slack**


![slack](https://user-images.githubusercontent.com/46800750/52513101-efde3f80-2c4b-11e9-916a-63ff7125331c.png)

## Webhook

### Notification
UiPath 2018.4から提供されたOrchestratorのWebhookを利用して、ジョブの実行結果をChatwork / Google Hangouts / Slackに通知します。

![Webhook](https://user-images.githubusercontent.com/129797/52544615-1ee3e500-2df5-11e9-936a-b37ce0c2e8df.png)

通知するイベントは以下の３つです。
* job.faulted ジョブの実行が失敗した
* job.completed ジョブの実行が正常に完了した
* job.stopped ユーザーが手動でジョブを停止した

### Create ticket
UiPath 2018.4から提供されたOrchestratorのWebhookを利用して、ジョブが正常終了しなかった場合 Backlog / JIRA / Redmine / ServiceNow / Wrike にチケットを作成します。

![Webhook](https://user-images.githubusercontent.com/129797/52544620-21463f00-2df5-11e9-8cc5-e927125031d3.png)

チケットを作成するイベントは以下の２つです。
* job.faulted ジョブの実行が失敗した
* job.stopped ユーザーが手動でジョブを停止した

## Scheduled

### Notification
OrchestratorのWebhookが利用できない場合に、スケジュール実行されたAWS Lambda FunctionでOrchestrator APIを呼び出し、ジョブの実行結果をChatwork / Google Hangouts / Slackに通知します。

![Scheduled](https://user-images.githubusercontent.com/129797/52544621-23100280-2df5-11e9-80e0-ba185de75024.png)

通知する実行結果は以下の３つです。
* Faulted ジョブの実行が失敗した
* Successful ジョブの実行が正常に完了した
* Stopped ユーザーが手動でジョブを停止した

### Create ticket
OrchestratorのWebhookが利用できない場合に、スケジュール実行されたAWS Lambda FunctionでOrchestrator APIを呼び出し、ジョブが正常終了しなかった場合 Backlog / JIRA / Redmine / ServiceNow / Wrike にチケットを作成します。

![Scheduled](https://user-images.githubusercontent.com/129797/52544624-24d9c600-2df5-11e9-8847-a545e7baa9a8.png)

チケットを作成する実行結果は以下の２つです。
* Faulted ジョブの実行が失敗した
* Stopped ユーザーが手動でジョブを停止した

## Deploy

* install serverless framework
```console
$ npm install -g serverless
```

* cron this repository and install serverless-python-requirements
```console
$ git clone <this repository>
$ cd <this clone directory>
$ npm install --save serverless-python-requirements
```

* modify config.[stage].json, serverless.yaml
```console
$ vim congig.[stage].json
$ vim serverless.yaml
```

* deploy it
```console
$ serverless deploy --stage [dev|prd]
```

## Debug/Test

CloudWatchのログに、受信したWebhookの内容や、取得したジョブの情報を出力しています。正常に動作していないと思われる場合は、まず、このログを確認してください。

## Setting

### Backlog

### Chatwork

### Google Hangouts Chat
Google Hangouts Chatでwebhookの設定を行います。

* 通知を受けたいチャットルームのメニューから"Configure webhooks"を選択します。
* "Name" / "Avator URL"に以下を設定します。
  * Name: Orchestrator-Job-Status
  * Avator URL: https://www.uipath.com/hubfs/Valentin/Brand%20Kit/logos/UiPath-icon.png
* 作成されたWebhook URL ( https://chat.googleapis.com/.... ) を下記config.[stage].jsonの"incomming_webhook_url"に設定します。

参考：[Using incoming webhooks](https://developers.google.com/hangouts/chat/how-tos/webhooks)

### JIRA

### Redmine

### ServiceNow

### Slack

### Wrike

## Configuration

設定はconfig.[stage].jsonに記載します。また、AWS Lambdaの環境変数設定で値を変更することができます。
```
{
    "language": "en",

    "webhook": {
        "orchestrator": {
            "secret": ""
        },

        "backlog": {
            "api_key": "",
            "space_key": "",
            "project_id": "",
            "issue_type_id": "",
            "priority_id": ""
        },
        "chatwork": {
            "api_token": "",
            "room_id": ""
        },
        "google_hangouts": {
            "incomming_webhook_url": ""
        },
        "jira": {
            "url": "",
            "username": "",
            "password": "",
            "project": "",
            "issue_type": ""
        },
        "redmine": {
            "url": "",
            "api_key": "",
            "project_id": "",
            "status_id": ""
        },
        "ServiceNow": {
            "url": "",
            "username": "",
            "password": "",
            "assignment_group": "",
            "urgency": "",
            "impact": ""
        },
        "slack": {
            "incomming_webhook_url": ""
        },
        "wrike": {
            "access_token": "",
            "folder_id": ""
        }
    },

    "scheduled": {
        "orchestrator": {
            "url": "",
            "tenancy_name": "",
            "username": "",
            "password": "",
            "api_key": "",
            "ntlm_authentication": "False"
        },

        "backlog": {
            "api_key": "",
            "space_key": "",
            "project_id": "",
            "issue_type_id": "",
            "priority_id": ""
            "interval": 0,
            "schedule": ""
        },
        "chatwork": {
            "api_token": "",
            "room_id": "",
            "interval": 0,
            "schedule": ""
        },
        "google_hangouts": {
            "incomming_webhook_url": "",
            "interval": 0,
            "schedule": ""
        },
        "jira": {
            "url": "",
            "username": "",
            "password": "",
            "project": "",
            "issue_type": "",
            "interval": 0,
            "schedule": ""
        },
        "redmine": {
            "url": "",
            "api_key": "",
            "project_id": "",
            "status_id": "",
            "interval": 0,
            "schedule": ""
        },
        "ServiceNow": {
            "url": "",
            "username": "",
            "password": "",
            "assignment_group": "",
            "urgency": "",
            "impact": "",
            "interval": 0,
            "schedule": ""
        },
        "slack": {
            "incomming_webhook_url": "",
            "interval": 0,
            "schedule": ""
        },
        "wrike": {
            "access_token": "",
            "folder_id": "",
            "interval": 0,
            "schedule": ""
        }
    }
}
```

### language

```
"language": "ja"
```

| Name     | Description          |
| -------- | -------------------- |
| language | メッセージの表示言語 |

### Webhook

OrchestratorのWebhookを受信するための設定です。

#### Orchestrator

```
"webhook": {
    "orchestrator": {
        "secret": ""
    }
}
```

| Name         | Description                   |
| ------------ | ----------------------------- |
| secret       | Webhook登録時に設定したsecret |

#### Backlog

```
"backlog": {
    "api_key": "",
    "space_key": "",
    "project_id": "",
    "issue_type_id": "",
    "priority_id": ""
}
```

| Name          | Description                    |
| ------------- | ------------------------------ |
| api_key       | API キー                       |
| space_key     | スペース情報                   |
| project_id    | 課題を登録するプロジェクトのID |
| issue_type_id | 課題の種別のID                 |
| priority_id   | 課題の優先度のID               |

#### Chatwork

```
"webhook": {
    "chatwork": {
        "api_token": "",
        "room_id": ""
    }
}
```

| Name      | Description                             |
| --------- | --------------------------------------- |
| api_token | Chatwork APIを呼び出すためのAPIトークン |
| room_id   | メッセージを送信するチャットのID        |

#### Google Hangouts

```
"webhook": {
    "google_hangouts": {
        "incomming_webhook_url": ""
    }
}
```

| Name                  | Description                                        |
| --------------------- | -------------------------------------------------- |
| incomming_webhook_url | Google Hangoutsにメッセージを送るためのWebhook URL |

#### JIRA

```
"webhook": {
    "jira": {
        "url": "",
        "username": "",
        "password": "",
        "project": "",
        "issue_type": ""
    }
}
```

| Name       | Description                |
| ---------- | -------------------------- |
| url        | JIRAのURL                  |
| username   | ユーザー名                 |
| password   | パスワード                 |
| project    | 課題を登録するプロジェクト |
| issue_type | 課題タイプ                 |

#### Redmine

```
"webhook": {
    "redmine": {
        "url": "",
        "api_key": "",
        "project_id": "",
        "status_id": ""
    }
}
```

| Name       | Description                    |
| ---------- | ------------------------------ |
| url        | RedmineのURL                   |
| api_key    | APIキー                        |
| project_id | 課題を登録するプロジェクトのID |
| status_id  | 登録する課題のステータス       |

#### ServiceNow

```
"webhook": {
    "ServiceNow": {
        "url": "",
        "username": "",
        "password": "",
        "assignment_group": "",
        "urgency": "",
        "impact": ""
    }
}
```

| Name             | Description                    |
| ---------------- | ------------------------------ |
| url              | ServiceNowのURL                |
| username         | ユーザー名                     |
| password         | パスワード                     |
| assignment_group | インシデントの割り当てグループ |
| urgency          | インシデントの影響度           |
| impact           | インシデントの緊急度           |

#### Slack

```
"webhook": {
    "slack": {
        "incomming_webhook_url": ""
    }
}
```

| Name                  | Description                              |
| --------------------- | ---------------------------------------- |
| incomming_webhook_url | Slackにメッセージを送るためのWebhook URL |

#### Wrike

```
"webhook": {
    "wrike": {
        "access_token": "",
        "folder_id": ""
    }
}
```

| Name         | Description                     |
| ------------ | ------------------------------- |
| access_token | アクセストークン                |
| folder_id    | チケットを登録するフォルダのID　|


### Scheduled

スケジュール実行する場合の設定です。

**schedule**パラメータはCloudWatchイベントのスケジュール式です。詳細は[AWS schedule syntax documentation](http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html)を参照。

**interval**パラメータはOrchestratorのJobの情報を取得するための実行間隔を分(minutes)で指定します。スケジュール実行のたびに*interval*分前から現時刻までに終了したジョブをモニタリングの対象とします。


例：（１０分ごとに実行）
```
    "interval": 10,
    "schedule": "rate(10 minutes)"
```

#### Orchestrator

```
"scheduled": {
    "orchestrator": {
        "url": "",
        "tenancy_name": "",
        "username": "",
        "password": "",
        "api_key": "",
        "ntlm_authentication": "False"
    }
}
```

| Name                | Description                                     |
| ------------------- | ----------------------------------------------- |
| url                 | URL                                             |
| tenancy_name        | テナント名                                      |
| username            | ユーザー名                                      |
| password            | パスワード                                      |
| api_key             | API Key                                         |
| ntlm_authentication | Windows 認証を有効にしていればTrue (True/False) |

#### Backlog

```
"backlog": {
    "api_key": "",
    "space_key": "",
    "project_id": "",
    "issue_type_id": "",
    "interval": 0,
    "schedule": ""
}
```

| Name          | Description                             |
| ------------- | --------------------------------------- |
| api_key       | API キー                                |
| space_key     | スペース情報                            |
| project_id    | 課題を登録するプロジェクトのID          |
| issue_type_id | 課題の種別のID                          |
| interval      | 実行間隔　分（minutes）                 |
| schedule      | CroudWatchのスケジュール式（cron/rate） |

#### Chatwork

```
"scheduled": {
    "chatwork": {
        "api_token": "",
        "room_id": "",
        "interval": 0,
        "schedule": ""
    }
}
```

| Name      | Description                             |
| --------- | --------------------------------------- |
| api_token | Chatwork APIを呼び出すためのAPIトークン |
| room_id   | メッセージを送信するチャットのID        |
| interval  | 実行間隔　分（minutes）                 |
| schedule  | CroudWatchのスケジュール式（cron/rate） |

#### Google Hangouts

```
"scheduled": {
    "google_hangouts": {
        "incomming_webhook_url": "",
        "interval": 0,
        "schedule": ""
    }
}
```

| Name                  | Description                                        |
| --------------------- | -------------------------------------------------- |
| incomming_webhook_url | Google Hangoutsにメッセージを送るためのWebhook URL |
| interval              | 実行間隔　分（minutes）                            |
| schedule              | CroudWatchのスケジュール式（cron/rate）            |

#### JIRA

```
"scheduled": {
    "jira": {
        "interval": 0,
        "schedule": ""
    }
}
```

| Name       | Description                             |
| ---------- | --------------------------------------- |
| url        | JIRAのURL                               |
| username   | ユーザー名                              |
| password   | パスワード                              |
| project    | 課題を登録するプロジェクト              |
| issue_type | 課題タイプ                              |
| interval   | 実行間隔　分（minutes）                 |
| schedule   | CroudWatchのスケジュール式（cron/rate） |

#### Redmine

```
"scheduled": {
    "redmine": {
        "interval": 0,
        "schedule": ""
    }
}
```

| Name       | Description                             |
| ---------- | --------------------------------------- |
| url        | RedmineのURL                            |
| api_key    | APIキー                                 |
| project_id | 課題を登録するプロジェクトのID          |
| status_id  | 登録する課題のステータス                |
| interval   | 実行間隔　分（minutes）                 |
| schedule   | CroudWatchのスケジュール式（cron/rate） |

#### ServiceNow

```
"scheduled": {
    "servicenow": {
        "interval": 0,
        "schedule": ""
    }
}
```

| Name             | Description                             |
| ---------------- | --------------------------------------- |
| url              | ServiceNowのURL                         |
| username         | ユーザー名                              |
| password         | パスワード                              |
| assignment_group | インシデントの割り当てグループ          |
| urgency          | インシデントの影響度                    |
| impact           | インシデントの緊急度                    |
| interval         | 実行間隔　分（minutes）                 |
| schedule         | CroudWatchのスケジュール式（cron/rate） |

#### Slack

```
"scheduled": {
    "slack": {
        "incomming_webhook_url": "",
        "interval": 0,
        "schedule": ""
    }
}
```

| Name                  | Description                              |
| --------------------- | ---------------------------------------- |
| incomming_webhook_url | Slackにメッセージを送るためのWebhook URL |
| interval              | 実行間隔　分（minutes）                  |
| schedule              | CroudWatchのスケジュール式（cron/rate）  |

#### Wrike

```
"webhook": {
    "wrike": {
        "access_token": "",
        "folder_id": "",
        "interval": 0,
        "schedule": ""
    }
}
```

| Name         | Description                              |
| ------------ | ---------------------------------------- |
| access_token | アクセストークン                         |
| folder_id    | チケットを登録するフォルダのID　         |
| interval     | 実行間隔　分（minutes）                  |
| schedule     | CroudWatchのスケジュール式（cron/rate）  |