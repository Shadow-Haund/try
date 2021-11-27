FROM python:latest
COPY requirements.txt /tcp/requirements.txt
WORKDIR /tcp/
RUN pip install -r requirements.txt
ADD server.py /tcp/
ADD client.py /tcp/
EXPOSE 55555