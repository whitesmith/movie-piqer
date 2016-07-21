FROM python:2.7

ENV PYTHONUNBUFFERED 1
ENV CODE /movie-piqer

RUN mkdir $CODE

WORKDIR $CODE

VOLUME $CODE

ADD requirements.txt $CODE/
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
