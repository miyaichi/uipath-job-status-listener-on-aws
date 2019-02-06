# uipath-job-status-listener-on-aws

UiPath OrchestratorのWebhookを受信して、ジョブの状態を把握する仕組みを提供します。

受信するイベントは以下の３つで、受信した内容をGoogle HangoutsやSlackに通知します。
* job.faulted ジョブの実行が失敗した
* job.completed ジョブの実行が正常に完了した
* job.stopped ユーザーが手動でジョブを停止した

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

### Orchestrator

```
"orchestrator": {
    "secret": ""
}
```

| Name         | Description                   |
| ------------ | ----------------------------- |
| secret       | Webhook登録時に設定したsecret |

### Google Hangouts

```
"notification": {
    "google_hangouts": {
        "incomming_webhook_url": ""
    }
}
```

| Name                  | Description                                        |
| --------------------- | -------------------------------------------------- |
| incomming_webhook_url | Google Hangoutsにメッセージを送るためのWebhook URL |

### Slack

```
"notification": {
    "slack": {
        "incomming_webhook_url": ""
    }
}
```

| Name                  | Description                              |
| --------------------- | ---------------------------------------- |
| incomming_webhook_url | Slackにメッセージを送るためのWebhook URL |

