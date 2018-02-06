FROM ubuntu:latest
MAINTAINER Gloria Palma "gloria@sentinel.la"
RUN apt-get update && apt-get install -y supervisor
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y libpq-dev python-dev
RUN apt-get install -y libffi-dev
RUN apt-get install -y vim
RUN mkdir -p /var/log/supervisor
COPY nuage.conf /etc/supervisor/conf.d/nuage.conf
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN chmod 777 -R /app
WORKDIR /app
EXPOSE 22 8000
CMD ["/bin/bash"]
