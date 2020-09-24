FROM python:3.7
RUN apt update
WORKDIR /app
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN python -m spacy download en_core_web_sm
ADD . /app
ENV PORT 8050
CMD ["python", "app.py"]