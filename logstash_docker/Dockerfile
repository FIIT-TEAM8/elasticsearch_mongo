FROM docker.elastic.co/logstash/logstash:8.0.0

# go to directory, where bin folder is
RUN cd /usr/share/logstash

# run command for installing mongo plugin
RUN bin/logstash-plugin install logstash-input-mongodb

# to find out if plugin was successfully installed exec to the docker container
# then execute this command: ls -la ./vendor/bundle/jruby/2.5.0/gems | grep logstash-input-mongodb
# result shouldn't be nothing

# this command was at the end of official logstash Dockerfile https://github.com/elastic/logstash/blob/8.0/Dockerfile
# might be needed in future
# LABEL retention="prune" 