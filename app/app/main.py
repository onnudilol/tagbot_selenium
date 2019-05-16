from flask import Flask, request, jsonify
from .tag_spy import scrape_site
from zappa.asynchronous import task

app = Flask(__name__)


@task
def scrape_site_task(url: str):
    matched_sites_json = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Matched sites:*"
        }
    }
    matched_sites = scrape_site(url)

    if matched_sites:
        for site, url in matched_sites.items():
            site_string = f'\n<{url}|{site}>'
            matched_sites_json['text']['text'] += site_string
    else:
        matched_sites_json['text']['text'] += '\nNothing...'

    return jsonify(matched_sites_json)


@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']

    scrape_site_task(url)

    json_response = [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"URL: <{url}>"
        }
    }]

    return jsonify(json_response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
