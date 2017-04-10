FROM ubuntu:latest
MAINTAINER Carlos Santos "carlosdanielcsantos"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential ffmpeg
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
