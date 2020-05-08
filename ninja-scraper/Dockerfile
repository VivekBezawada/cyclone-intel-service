from cyclone-intel-service_base_image:latest

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt


ENTRYPOINT  ["python3"]

CMD ["app.py"]