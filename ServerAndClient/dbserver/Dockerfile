FROM postgres:11.4

RUN apt-get update \
  && for POSTGIS_VERSION in 2.5; do \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    postgresql-contrib; \
    done \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

EXPOSE 5432