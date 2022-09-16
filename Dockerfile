FROM --platform=linux/amd64 python:3.7.5
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD [ "python", "./translate.py" ]