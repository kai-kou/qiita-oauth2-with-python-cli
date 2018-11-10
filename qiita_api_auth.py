from http.server import BaseHTTPRequestHandler, HTTPServer

from urllib.request import urlopen, HTTPError

from webbrowser import open_new

import requests

import json

import random, string

QIITA_API_BASE_URL = 'https://qiita.com/api/v2/'


class HTTPServerHandler(BaseHTTPRequestHandler):
  """
  QiitaのOAuth2認証でリダイレクトを受け入れるHTTPサーバ
  """
  def __init__(self, request, address, server, client_id, client_secret):
    self._client_id = client_id
    self._client_secret = client_secret
    super().__init__(request, address, server)


  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

    # リダイレクトURLからコードが取得できたらアクセストークンを取得する
    if 'code' in self.path:
      params = self.path.split('&')
      code = params[0].replace('/?code=', '')
      state = params[0].replace('state=', '')
      url = f'{QIITA_API_BASE_URL}access_tokens'
      headers = {'Content-Type': 'application/json'}
      params = {
        'client_id': self._client_id,
        'client_secret': self._client_secret,
        'code': code
      }
      response = requests.request(
        method='POST',
        url=url,
        headers=headers,
        data=json.dumps(params))
      self.wfile.write(bytes('<html><h1>Please close the window.</h1></html>', 'utf-8'))
      self.server.access_token = None
      if response.status_code == 201:
        self.server.access_token = response.json()['token']


class QiitaAccessTokenHandler:
  """
  QiitaのOAuth2認証を利用してアクセストークンを取得するクラス
  """
  def __init__(self, client_id, client_secret, scope=['read_qiita', 'write_qiita']):
    self._client_id = client_id
    self._client_secret = client_secret
    self._scope = '+'.join(scope)


  def get_access_token(self):
    state = self._randomname(40)
    access_url = f'{QIITA_API_BASE_URL}oauth/authorize?client_id={self._client_id}&scope={self._scope}&state={state}'
    open_new(access_url)
    httpServer = HTTPServer(
      ('localhost', 8080),
      lambda request, address, server: HTTPServerHandler(
        request, address, server, self._client_id, self._client_secret))
    httpServer.handle_request()
    return httpServer.access_token


  def _randomname(self, n):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randlst)
