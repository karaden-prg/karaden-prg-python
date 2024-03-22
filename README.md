# Karaden Pythonライブラリ
Karaden Pythonライブラリは、Pythonで書かれたアプリケーションからKaraden APIへ簡単にアクセスするための手段を提供します。
それにはAPIレスポンスから動的に初期化するAPIリソースの一連のクラス定義が含まれているため、Karaden APIの幅広いバージョンと互換性があります。
## インストール方法
パッケージを変更しないならば、このソースコードは必要ありません。
パッケージを使用したいだけならば、下記を実行するだけです。
```
pip install --upgrade karaden-prg-python
```
ソースコードからインストールしたいのであるならば、下記を実行します。
```
python setup.py install
```
## 動作環境
Python 3.7～3.10
## 使い方
このライブラリを使用するには、Karadenでテナントを作成し、プロジェクト毎に発行できるトークンを発行する必要があります。
作成したテナントID（テナントIDはテナント選択画面で表示されています）は、`Config.tenant_id`に、発行したトークンは`Config.api_key`にそれぞれ設定します。
```python
from karaden.config import Config
from karaden.param.message_create_params import MessageCreateParams
from karaden.model.message import Message

Config.api_key = '<トークン>'
Config.tenant_id = '<テナントID>'
params = (
    MessageCreateParams
    .new_builder()
    .with_service_id(1)
    .with_to('09012345678')
    .with_body('本文')
    .build()
)
message = Message.create(params)
```
### リクエスト毎の設定
同一のプロセスで複数のキーを使用する必要がある場合、リクエスト毎にキーやテナントIDを設定することができます。
```python
params = (
    MessageDetailParams
    .new_builder()
    .with_id('<メッセージID>')
    .build()
)
request_options = (
    RequestOptions.new_builder()
    .with_api_key('<トークン>')
    .with_tenant_id('<テナントID>')
    .build()
)
message = Message.detail(params, request_options)
```
### タイムアウトについて
通信をするファイルサイズや実行環境の通信速度によってはHTTP通信時にタイムアウトが発生する可能性があります。<br />
何度も同じような現象が起こる際は、ファイルサイズの調整もしくは`RequestOptions`からタイムアウトの時間を増やして、再度実行してください。
```python
request_options = (
    RequestOptions.new_builder()
    .with_api_key('<トークン>')
    .with_tenant_id('<テナントID>')
    .with_connection_timeout(<秒>)
    .with_read_timeout(<秒>)
    .build()
)
bulk_message = BulkMessageService.create('<ファイルパス>', request_options)
```
