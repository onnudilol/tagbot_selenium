# WHAT IS THIS
It's a flask api that parses a url's scripts for matching services in the config file.

# Configuration

Add or modify sites in `app/app/sites.yaml`:

```
sites:
  karte:
    name: KARTE
    homepage: https://karte.io
    example_site: https://right-on.co.jp
    scripts:
      - static.karte.io/libs/tracker.js
      - static.karte.io/
```

Don't alter the directory structure or rename files, the docker image wants things in a very specific location.

# How to run locally
* Build the image:
`docker build -t slackspy .`
* Run the service: `docker run -p 80:80 slackspy`
* Make a POST request: `curl -X POST -F 'url=https://mossy.jp/' http://localhost:80/scrape`

# How to deploy
`zappa deploy`
