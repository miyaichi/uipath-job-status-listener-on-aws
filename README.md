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
UiPath 2018.4から提供されたOrchestratorのWebhookを利用して、ジョブが正常終了しなかった場合にチケットを作成します。

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
OrchestratorのWebhookが利用できない場合に、スケジュール実行されたAWS Lambda FunctionでOrchestrator APIを呼び出し、ジョブが正常終了しなかった場合にチケットを作成します。

![Scheduled](https://user-images.githubusercontent.com/129797/52544624-24d9c600-2df5-11e9-8847-a545e7baa9a8.png)

チケットを作成する実行結果は以下の２つです。
* Faulted ジョブの実行が失敗した
* Stopped ユーザーが手動でジョブを停止した

## Setting

* install serverless framework
```console
$ npm install -g serverless
```

* cron this repository
```console
$ git clone <this repository>
$ cd <this clone directory>
```

* modify config.json
```console
$ vim congig.json
```

* deploy it
```console
$ serverless deploy [--stage production]
```

## Configuration

設定はconfig.jsonに記載します。また、AWS Lambdaの環境変数設定で値を変更することができます。
```
$ cat config.json
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
            "issue_type_id": ""
        },
        "chatwork": {
            "api_token": "",
            "room_id": ""
        },
        "google_hangouts": {
            "incomming_webhook_url": ""
        },
        "slack": {
            "incomming_webhook_url": ""
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
        "slack": {
            "incomming_webhook_url": "",
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
    "issue_type_id": ""
}
```

| Name          | Description                    |
| ------------- | ------------------------------ |
| api_key       | API キー                       |
| space_key     | スペース情報                   |
| project_id    | 課題を登録するプロジェクトのID |
| issue_type_id | 課題の種別のID                 |

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