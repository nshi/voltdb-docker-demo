VoltDB Demo Docker Image
===============

This repository builds the VoltDB Docker image that contains all demo
applications. All demos can be run on a single node configuration.

It requires the following software to build the image:
- Docker 1.1 or above
- curl
- Java 7 compiler (e.g. OpenJDK 1.7)

For instructions on how to install Docker on your platform, please see the
[Docker doc](https://docs.docker.com/).

How to Build
============
Run the `build.sh` script to build the docker image. The script takes one
argument, which is the download URL of the VoltDB community edition.

Once the image is successfully built, you can run it using the following command
> docker run -p 8080:8080 -p 8081:8081 -d --name voltdb-demo nshi/voltdb

To push the image to the Docker Registry, do
> docker push nshi/voltdb
