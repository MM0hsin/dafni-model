FROM python:3.12
RUN pip install --upgrade pip
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --compile -r requirements.txt

COPY ./aiida-mlip /app/aiida-mlip/

RUN mkdir -p /app/outputs/

RUN verdi presto
RUN verdi code create core.code.installed --config /app/aiida-mlip/janus_code.yml

CMD ["python3", "/app/aiida-mlip/singlepoint.py"] 