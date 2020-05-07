from cyclone-intel-service_base_image:latest

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt


ENTRYPOINT  ["python3"]

CMD ["scraper.py"]