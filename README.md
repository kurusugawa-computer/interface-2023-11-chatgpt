# Interface 2023年11月号「ChatGPTとプログラミング」中西担当部分サポートページ
## 概要
このリポジトリには、Interface 2023年11月号の「ChatGPTとプログラミング」（以下、本誌）の中西が担当した部分のサポートページです。
以下の内容が含まれます。
* 各章・コラムのChatGPTとのやり取り全文([./prompts/](./prompts))
* 第3部第6章の認識サーバーのソースコード([./app](./app))
* 第3部第6章の認識サーバー用のDocker関係ファイル([./docker](./docker))

不備があれば、イシューぺージを活用ください。

## 認識サーバー利用方法
認識サーバーの動作にはdockerを用います。

[./app/launch.sh](./app/launch.sh)を用いてコンテナを起動し、そこで認識サーバーのAPIサーバープロセスや推論プロセスを動作させてます。

認識サーバーは適切なGPU環境が必要です(OS:Linux, CPU:x86-64, NVIDIA製GPU, docker, NVIDIAドライバー, NVIDIA Container Toolkit)。
詳細は本誌を確認ください。

### ソースのダウンロード
このリポジトリをダウンロードします。
```
$ git clone https://github.com/kurusugawa-computer/interface-2023-11-chatgpt
$ cd interface-2023-11-chatgpt
```

### Dockerコンテナ起動単体
Dockerコンテナを起動します。初回実行時はダウンロードに時間がかかります。
```
$ bash ./app/launch.sh
```

起動時にappディレクトリをコンテナにマウントします。

### APIサーバープロセス
コンテナを起動し、コンテナ内でuvicornコマンドでAPIサーバープロセスを起動します。

```
$ bash ./app/launch.sh
$ uvicorn server:app \
（--port ポート番号（指定しない場合8000））
（--host ローカルIPアドレス等を指定）
```

別PCなどの外部からアクセスする場合は、本誌で説明したように、引数（host,post）を適切に指定してください。

### 推論プロセス
コンテナを起動し、推論プロセスを起動します。複数起動しない想定です。

```
$ bash ./app/launch.sh
$ python ./interface.py
```

## 他のスクリプト
### app/test_model.py
[./app/test_model.py](./app/test_model.py)は「ステップ1：推論コードの作成」で作成した推論コードをテストするコードです。
以下のコマンドで実行します。実行すると推論結果が表示されます。

```
$ bash ./app/launch.sh
$ python ./test_model.py
```

### app/repeat.sh
[./app/repeat.sh](./app/repeat.sh)は「大量アクセス」の節のスクリプトです。環境に合わせてHOSTとPORTを変更して用いてください。