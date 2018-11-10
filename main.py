import os

from qiita_api_auth import QiitaAccessTokenHandler


def get_access_token(init=False):
  # OAuth2認証で取得する
  client_id = os.getenv('QIITA_CLIENT_ID')
  client_secret = os.getenv('QIITA_CLIENT_SECRET')

  token_handler = QiitaAccessTokenHandler(client_id, client_secret)
  return token_handler.get_access_token()


if __name__ == '__main__':
  access_token = get_access_token()
  print(f'アクセストークンとれたよー: {access_token}')
