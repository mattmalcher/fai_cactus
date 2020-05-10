FROM python:3.7.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# copy across the app and the model
COPY app.py ./
COPY export.pkl ./

# Run the image as a non-root user (ubuntu version)
RUN useradd -m myuser
USER myuser

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
CMD  uvicorn app:app --host 0.0.0.0 --port $PORT
