from flask import Flask, request, jsonify, abort
from .tag_spy import scrape_site
from zappa.asynchronous import task
import requests
import os

app = Flask(__name__)


def validate_request(request: request):
    return request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']


@task
def scrape_site_task(url: str, response_url: str):
    matched_sites_json = {
        "response_type": "in_channel",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*見つかったタグ:*"
                }
            }
        ]

    }
    matched_sites = scrape_site(url)

    if matched_sites:
        for site, url in matched_sites.items():
            site_string = f'\n<{url}|{site}>'
            matched_sites_json['blocks'][0]['text']['text'] += site_string
    else:
        matched_sites_json['blocks'][0]['text']['text'] += '\nなし。。。'

    requests.post(response_url, json=matched_sites_json)


@app.route('/scrape', methods=['POST'])
def scrape():
    if not validate_request(request):
        abort(400)

    url = request.form["text"]
    scrape_site_task(url, request.form["response_url"])

    json_response = {
        "response_type": "in_channel",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*サイトのURL*: {url}"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "今分析中"
                    }
                ]
            }
        ]
    }

    return jsonify(json_response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
