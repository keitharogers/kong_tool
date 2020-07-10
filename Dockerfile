FROM python:3.8-alpine
WORKDIR /usr/src/kong_tool
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD /usr/local/bin/python3 kongtool.py $ARGUMENT
