import requests
import json
from flask_babel import _
from . import app


def translate(text: str, dst_lang: str) -> str:
    """
    Translates text to dst_lang using Microsoft's
    Translator API.
    """
    if 'MS_TRANSLATOR_KEY' not in app.config or \
            'MS_TRANSLATOR_REGION' not in app.config or \
            not app.config['MS_TRANSLATOR_KEY'] or \
            not app.config['MS_TRANSLATOR_REGION']:
        return _('Error: The translation service is not configured.')

    base_url = 'https://api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'
    to_param = '&to=' + dst_lang
    constructed_url = base_url + path + to_param

    headers = {
        'Ocp-Apim-Subscription-Key': app.config['MS_TRANSLATOR_KEY'] ,
        'Ocp-Apim-Subscription-Region': app.config['MS_TRANSLATOR_REGION'] ,
        'Content-type': 'application/json'
    }

    body = [{
        'text': text
    }]

    r = requests.post(constructed_url, headers=headers, json=body)

    if r.status_code != 200:
        return _('Error: the translation service failed.')

    return json.loads(r.content)[0]['translations'][0]['text']
