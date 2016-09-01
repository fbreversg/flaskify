import urllib
import json

TOKEN = "b1e1ffaac1ee015e32d05d09ec635ad85d9dd887"
ROOT_URL = "https://api-ssl.bitly.com"
SHORTEN = "/v3/shorten?access_token={}&longUrl={}"


class BitlyHelper:

    def shorten_url(self, longurl):
        try:
            url = ROOT_URL + SHORTEN.format(TOKEN, longurl)
            response = urllib.request.urlopen(url).read().decode('utf8')
            jr = json.loads(response)
            return jr['data']['url']
        except Exception as e:
            print(e)
