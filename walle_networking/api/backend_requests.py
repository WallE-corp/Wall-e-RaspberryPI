import requests

base_url = 'http://127.0.0.1:3000'
timeout = 0.1


def set_base_url(url):
  global base_url
  base_url = url


def ping():
  """
  Sends a 'ping' to the backend server and awaits a 'pong' response waiting at most
  the set timeout.

  Returns:
    Boolean on whether a 'pong' response was received.
  """
  res = requests.get(base_url + '/router', timeout=timeout)
  if res.status_code == 200 and res.text == 'pong':
    return True
  return False
