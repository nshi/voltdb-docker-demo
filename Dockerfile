FROM debian:wheezy
MAINTAINER Ning Shi <nshi@voltdb.com>

# Public VoltDB ports
EXPOSE 8080
EXPOSE 8081
EXPOSE 9000
EXPOSE 21211
EXPOSE 21212

# Internal VoltDB ports
EXPOSE 3021
EXPOSE 4560
EXPOSE 9090

ENV VOLTDB_DIST /opt/voltdb
ENV PATH $PATH:$VOLTDB_DIST/bin

ADD voltdb $VOLTDB_DIST
ADD index.html $VOLTDB_DIST/examples/
ADD web.py $VOLTDB_DIST/examples/

RUN apt-get update
RUN apt-get install -y procps python openjdk-7-jre-headless

WORKDIR /opt/voltdb/examples/
CMD ["python", "web.py", "8081"]
