# uipath-job-status-listener-on-aws

UiPath OrchestratorのWebhookを受信して、ジョブの状態を把握する仕組みを提供します。

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

設定はconfig.jsonに記載します。また、AWS Lambdaの環境変数設定で値を変更することができます。IoT Enterprise Buttonは、デバイスのプレイスメントの属性でプロセス名（属性の名前 process_name）を指定します。

```
$ cat config.json
{
    "language": "ja",

    "orchestrator": {
        "secret": ""
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

| Name         | Description                                     |
| ------------ | ----------------------------------------------- |
| secret       | Webhook登録時に設定したsecret                   |
