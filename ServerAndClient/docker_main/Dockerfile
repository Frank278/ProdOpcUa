# pull official base image
FROM python:3.8.0

RUN apt update \
  && for pg_config in 2.5; do \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y; \
    done \
  && apt clean \
  && rm -rf /var/lib/apt/lists/*

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

# run entrypoint.sh
#ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
# ENTRYPOINT ["python", "manage.py", "runserver"]
#COPY ./entrypoint.sh /usr/src/app/entrypoint.sh 
#ENTRYPOINT ["/usr/src/app/entrypoint.sh", "postgres"]
ENTRYPOINT sh -c "python manage.py makemigrations opc && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
#ENTRYPOINT ["python", "doit.py"]

#ENTRYPOINT exec ls -l

