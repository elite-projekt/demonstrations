# hadolint ignore=DL3006
FROM debian:buster-slim

# args
ARG VCS_REF
ARG BUILD_DATE
# environment
ENV ADMIN_PASSWORD=admin

# install packages
# hadolint ignore=DL3008,DL3013,DL3015
RUN apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y \
  sudo \
  cups \
  cups-bsd \
  cups-filters \
  foomatic-db-compressed-ppds \
  printer-driver-all \
  openprinting-ppds \
  hpijs-ppds \
  hp-ppd \
  hplip \
  make \
  curl \
  iproute2 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# add print user
RUN adduser --home /home/admin --shell /bin/bash --gecos "admin" --disabled-password admin \
  && adduser admin sudo \
  && adduser admin lp \
  && adduser admin lpadmin

# disable sudo password checking
RUN echo 'admin ALL=(ALL:ALL) ALL' >> /etc/sudoers

# enable access to CUPS
# hadolint ignore=DL3001
RUN /usr/sbin/cupsd \
  && while [ ! -f /var/run/cups/cupsd.pid ]; do sleep 1; done \
  && cupsctl --remote-admin --remote-any --share-printers \
  && kill "$(cat /var/run/cups/cupsd.pid)" \
  && echo "ServerAlias *" >> /etc/cups/cupsd.conf

# copy /etc/cups for skeleton usage
RUN cp -rp /etc/cups /etc/cups-skel

COPY printer /printer
# hadolint ignore=DL3003
RUN cd /printer && make install && rm -rf /printer

# hadolint ignore=DL3001
RUN cupsd && sleep 4 && lpadmin -p email-sample -E -v email:/sample -D 'printer' -L 'Office' -m email.ppd && killall cupsd && sleep 3 && echo "Added printer!"

# entrypoint
COPY docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT [ "/docker-entrypoint.sh" ]

# default command
CMD ["cupsd", "-f"]

# ports
EXPOSE 631

