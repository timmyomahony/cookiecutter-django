# There's a tricky issue that needs to be avoided here with node_modules.
# Because we are mounting our app from host into our container, the node_modules
# folder may not contain purpose-built binaries for the container. If we built
# the node_modules on our system, our container will use those, causing issue.
#
# This roughly explains the issue:
# http://jdlm.info/articles/2016/03/06/lessons-building-node-app-docker.html

FROM node:9.4.0

COPY ./package.json /app/package.json

WORKDIR /app

RUN npm install -g gulp gulp-cli
RUN npm install

CMD gulp