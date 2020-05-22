FROM python:3
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN  apt-get update
RUN pip install --no-cache-dir -r requirements.txt
Run python -m spacy download en_core_web_sm

EXPOSE 9999
CMD ["gunicorn", "--workers","1","--threads","10","--bind","0.0.0.0:9999","main:app"]
