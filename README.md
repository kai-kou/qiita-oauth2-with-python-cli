# qiita-oauth2-with-python-cli
PythonでCLIからOAuth2を利用してQiitaのアクセストークンを取得してみた  

## Usage

```sh
> git clone https://github.com/kai-kou/qiita-oauth2-with-python-cli.git
> cd qiita-oauth2-with-python-cli
> python -m venv venv
> . venv/bin/activate.fish
> pip install -r requirements.txt

# Qiitaでアプリケーションを作成して、Client IDとSecretを取得する
open https://qiita.com/settings/applications/new

# 環境変数にClient IDとSecretを設定する

# bash
> export QIITA_CLIENT_ID=<Client ID>
> export QIITA_CLIENT_SECRET=<Client Secret>

# fish
> set -x QIITA_CLIENT_ID <Client ID>
> set -x QIITA_CLIENT_SECRET <Client Secret>

> python main.py
```
