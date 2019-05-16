FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./requirements.txt /app/requirements.txt
COPY ./app /app
RUN mv /app/app/chromedriver_bin/chromedriver.linux /app/app/chromedriver
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-unstable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst ttf-freefont \
      --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app

RUN pip3 install -r requirements.txt
