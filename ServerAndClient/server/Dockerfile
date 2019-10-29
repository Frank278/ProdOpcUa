FROM python:3.7
RUN pip install -U pip
RUN pip install opcua cryptography sqlalchemy psycopg2 psutil
RUN mkdir /app
# COPY ./server2.py /app/server2.py
# COPY ./custom_nodes.xml /app/custom_nodes.xml
ENV db_host dbserver
ENV db_user frank
ENV db_pasword frank
ENV db_port 5432
ENV opcua_host 0.0.0.0
ENV opcua_user=
ENV opcua_pasword=
ENV opcua_port 4840

WORKDIR /app

#EXPOSE ${db_port}
EXPOSE ${opcua_port}
#CMD ["python", "server2.py"]
ENTRYPOINT sh -c "pwd && ls -l && python server2.py"