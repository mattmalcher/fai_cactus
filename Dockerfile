FROM python:3.7.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# copy across the app and the model
COPY app.py ./
COPY export.pkl ./

# start the app
CMD [ "python", "./app.py"]