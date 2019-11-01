FROM python:3.7
RUN pip install -U pip
RUN pip install opcua cryptography psutil
RUN mkdir /app
# COPY ./server2.py /app/server2.py
# COPY ./custom_nodes.xml /app/custom_nodes.xml

ENV opcua_host 0.0.0.0
ENV opcua_user=
ENV opcua_pasword=
ENV opcua_port 16000


WORKDIR /app

#EXPOSE ${db_port}
EXPOSE ${opcua_port}
CMD ["python", "client.py"]
#ENTRYPOINT sh -c "python client.py"