FROM alpine:3.20
RUN apk add --no-cache curl bash tzdata
WORKDIR /opt
COPY snapshot.sh /opt/snapshot.sh
COPY crontab.txt /etc/crontabs/root
CMD ["crond","-f","-l","2"]
