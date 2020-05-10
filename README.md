# fai_cactus
Testing deployment of a simple image classifier which distinguishes between different succulents: 

* crassula_ovata
* haworthi_retusa
* lithops
* purple_echeveria

Deployed at: https://fai-cactus.herokuapp.com/

## Steps

### 1 Create Example app.py
Combine the starlet reference script from: https://github.com/encode/starlette-example
with the example endpoint definition from the lesson notebook.

### 2 Configure Test Environment 
Open the Project in pycharm and tell it to set up a new venv for the project. 
This will let me figure out which dependencies I need and test the app locally.

The approach used in course is to save the pickled model - this requires the same pytorch and directory structure to use it.

I can copy dependencies & versions from the fastai conda environment by installing pip within it then running: 
`pip freeze > requirements.txt`  (see *Matching Versions* below)

Note: The version of python used in the course conda env is 3.7.7, with pytorch 1.4.0.

Encountered an issue where bottleneck - a dependency, didn't seem to want to install on python 3.7. 
Problem  here was that it needs to be built from source (not a wheel), and it couldn't find the python 3.7 build tools because they weren't installed. 
Did `sudo apt-get install python3.7-dev` to rectify this.

Note - you will encounter the same issue if you use the `-slim` versions of the python docker image.

### 3 Use Test Environment to Create Docker Image
Start with the docker official python image: https://hub.docker.com/_/python. 
There are some template dockerfiles on this page which are useful.

Then, use the same requirements.txt used to create the test environment in the dockerfile definition.

Build the dockerfile using:
``` 
docker build -t mattmalcher/fai_cactus:0.1 .
```

####
Test locally using docker-compose:
```
docker-compose up -d
```

Test out the app at:
http://127.0.0.1:8008/

Push the image to docker hub:
```
docker push mattmalcher/fai_cactus
```
 To do - make this smaller! Currently ~2gb and includes lots of things you don't need for predictions. 
 Main issue is the fastai dependencies.

### 4 Deploy Docker Image to Heroku

#### Fix the Container
Got to this point and had to do some fiddling to ensure the container image was set up the way Heroku was expecting:

* Container now takes `PORT` environment variable and uses it to determine which port to bind the web server to. 
    * Tripped up when binding ports, forgot to set the host ip: `CMD  uvicorn app:app *--host 0.0.0.0* --port $PORT`.
* Container runs the server as a non-root user

#### Deploy
Once this was all sorted, the 
Push the container to the Heroku container registry: 
```
heroku container:push web -a fai-cactus
```

Tell Heroku to deploy this version:
```
heroku container:release web -a fai-cactus
```

Check the logs:
```
heroku logs -a fai-cactus
```

# Refs
The following are useful reads:

* https://pythonspeed.com/articles/base-image-python-docker-images/
* https://medium.com/@lankinen/fastai-model-to-production-this-is-how-you-make-web-app-that-use-your-model-57d8999450cf
* https://github.com/simonw/cougar-or-not/blob/master/cougar.py
* https://docs.docker.com/engine/reference/commandline/build/#use-a-dockerignore-file
* https://github.com/wayofnumbers/fastai-vision-uvicorn-gunicorn-starlette-docker


## Matching Versions to docker / venv
https://stackoverflow.com/questions/50777849/from-conda-create-requirements-txt-for-pip3
We need the version of torch / fastai to match in the development / deployment environment.

```
conda activate <env>
conda install pip
pip freeze > requirements.txt
```

Then use the resulting requirements.txt to create a pip virtual environment / docker image.
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```