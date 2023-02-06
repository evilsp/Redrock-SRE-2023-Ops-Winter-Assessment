FROM centos:7
MAINTAINER 2767212964@qq.com
WORKDIR /usr/local
RUN mkdir /usr/local/email
COPY test1.py /usr/local/email
COPY email.txt /usr/local/email
COPY file.zip /usr/local/email