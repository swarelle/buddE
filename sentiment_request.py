# -*- coding: utf-8 -*-
import httplib, urllib, base64

# Class to use Microsoft Text Analysis API and return the sentiment score
class RequestSentiment:

    def __init__(self, s):
        """ Initializes attributes necessary for requesting from API """
        self.headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': 'f4a519fc839c467294a962080a3efb90',
        }

        self.params = urllib.urlencode({
        })

        self.body = {
          "documents": [
            {
              "id": "test",
              "text": s
            }
          ]
        }

    def get_sentiment(self):
        """ get sentiment score from API """
        try:
            conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
            conn.request("POST", "/text/analytics/v2.0/sentiment?%s" % self.params, "%s" % self.body, self.headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
            return data
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

# Below for debugging
# r = RequestSentiment("Today is the happiest day of my life!").get_sentiment()
