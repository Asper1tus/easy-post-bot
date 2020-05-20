#!/usr/bin/env python3

import urllib.request, urllib.parse, urllib.error
import os
import json

class CatApi:
    def __init__(self):
        api_key = os.environ["CATAPI_TOKEN"]
        self.url = f'https://api.thecatapi.com/v1/images/search?api_key={api_key}'

    def get_image_url(self):
        uh = urllib.request.urlopen(self.url)
        data = uh.read().decode()

        try:
            json_string = json.loads(data)
        except:
            json_string = None

        if json_string:
            image_url = json_string[0]['url']

        return image_url

