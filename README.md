# uipath-job-status-listener-on-aws

UiPath Orchestratorのジョブの実行結果をモニタリングし、通知する仕組みを提供します。

* Google Hangouts Chat
![Google Hangouts Chat](https://user-images.githubusercontent.com/46800750/52512953-118af700-2c4b-11e9-956a-ba96349544d8.jpg)

* Slack
![slack](https://user-images.githubusercontent.com/46800750/52512959-1cde2280-2c4b-11e9-98dc-c53160f929ae.jpg)


## Webhook

UiPath 2018.4から提供されたOrchestratorのWebhookを利用して、ジョブの実行結果をChatwork / Google Hangouts / Slackに通知します。

![Webhook](https://user-images.githubusercontent.com/46800750/52512966-28c9e480-2c4b-11e9-950e-7f9f271f0a94.png)

通知するイベントは以下の３つです。
* job.faulted ジョブの実行が失敗した
* job.completed ジョブの実行が正常に完了した
* job.stopped ユーザーが手動でジョブを停止した

## Scheduled

OrchestratorのWebhookが利用できない場合に、スケジュール実行されたAWS Lambda FunctionでOrchestrator APIを呼び出し、ジョブの実行結果をChatwork / Google Hangouts / Slackに通知します。

![Scheduled](https://user-images.githubusercontent.com/46800750/52512983-3aab8780-2c4b-11e9-9bc6-a166007bfad8.png)

通知する実行結果は以下の３つです。
* Faulted ジョブの実行が失敗した
* Successful ジョブの実行が正常に完了した
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

    "orchestrator": {
        "secret": "secret"
    },
    
    "notification": {
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

*schedule*パラメータはCloudWatchイベントのスケジュール式です。詳細は[AWS schedule syntax documentation](http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html)を参照。


*interval*パラメータはOrchestratorのJobの情報を取得するための実行間隔を分(minutes)で指定します。スケジュール実行のたびに*interval*分前から現時刻までに終了したジョブをモニタリングの対象とします。


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