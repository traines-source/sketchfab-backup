FROM python

WORKDIR /usr/src/app

RUN pip install --no-cache-dir python-slugify requests

COPY . .

CMD [ "python", "./scrape.py" ]