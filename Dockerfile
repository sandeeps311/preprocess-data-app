# set the base image 
#FROM python:3.7

#add project files to the usr/src/app folder
#ADD . /usr/src/app

#set directoty where CMD will execute 
#WORKDIR /usr/src/app
#COPY requirements.txt ./

# Get pip to download and install requirements:
#RUN pip install --no-cache-dir -r requirements.txt

# Expose ports
#EXPOSE 5001

# default command to execute    
#CMD exec gunicorn controllerservices.wsgi:application --bind 0.0.0.0:5001 --workers 3


FROM python:3.7
RUN apt update
WORKDIR /app
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ADD . /app
ENV PORT 80
CMD ["python", "app.py"]