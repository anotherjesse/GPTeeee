FROM ubuntu:20.04

# Set DEBIAN_FRONTEND to noninteractive to prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3 python3-pip curl wget golang

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY main.py /app/main.py

EXPOSE 5003

CMD ["python3", "main.py"]
