FROM ubuntu:14.04
MAINTAINER Gloria Palma "gloria@sentinel.la"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y libpq-dev python-dev
RUN apt-get install -y libffi-dev
RUN apt-get install -y vim
RUN apt-get update && apt-get install -y openssh-server supervisor
RUN mkdir -p /var/run/sshd /var/log/supervisor
RUN useradd --create-home -s /bin/bash user
RUN mkdir /home/user/app
ADD . /home/user/app
WORKDIR /home/user/app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY nuage.conf /etc/supervisor/conf.d/nuage.conf
EXPOSE 22 8000
USER user
CMD ["bash"]
