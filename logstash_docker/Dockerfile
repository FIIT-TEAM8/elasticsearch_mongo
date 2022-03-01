# to stop database error mentiong in https://github.com/jruby/jruby/issues/3955
# get and update ubuntu image, then install netbas and in the final stage copy /opt/protocols from ubuntu to logstash image

FROM ubuntu:20.04 AS build

RUN apt update

RUN apt install netbase

FROM docker.elastic.co/logstash/logstash:8.0.0 as final

# go to directory, where bin folder is
RUN cd /usr/share/logstash

# run command for installing mongo plugin
RUN bin/logstash-plugin install logstash-input-mongodb
# to find out if plugin was successfully installed exec to the docker container
# then execute this command: ls -la ./vendor/bundle/jruby/2.5.0/gems | grep logstash-input-mongodb
# result shouldn't be nothing

COPY --from=build /etc/protocols /etc/protocols

# TODO: pipeline config and settings yml should be refactored for dev and production environment 
# replace old pipeline configuration with new one for Mongo and Elasticsearch combo
COPY ./logstash.conf /usr/share/logstash/pipeline/

# replace setting, Elasticsearch is listening on different address
COPY ./logstash.yml /usr/share/logstash/config/

RUN mkdir /usr/share/logstash/logstash-mongodb/

# this command was at the end of official logstash Dockerfile https://github.com/elastic/logstash/blob/8.0/Dockerfile
# might be needed in future
# LABEL retention="prune" 