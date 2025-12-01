FROM python:3.12

COPY requirements.txt .
RUN pip install --no-cache-dir --compile -r requirements.txt

COPY /aiida-mlip ./

RUN verdi presto
RUN verdi code create core.code.installed --config janus_code.yml

