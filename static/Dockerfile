FROM    ubuntu
RUN     apt-get update
RUN     apt-get install -y python3.4
ADD     /src /static
WORKDIR /static
EXPOSE  8888
CMD     ["python3.4", "-m", "http.server", "8888"]