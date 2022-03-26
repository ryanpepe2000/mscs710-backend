FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /matrix-server
WORKDIR /matrix-server
COPY requirements.txt /matrix-server/
RUN pip install -r requirements.txt
COPY . /matrix-server/
# CMD python run.py [Local Development]
CMD gunicorn --bind 0.0.0.0:5000 -w 3 run:app