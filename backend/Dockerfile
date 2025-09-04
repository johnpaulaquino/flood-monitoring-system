FROM python:3.13-slim

#set up working directory
WORKDIR /code

#copy the dependencies on code dir
COPY requirements.txt .

#Install all the packages
RUN pip install --no-cache-dir --upgrade -r requirements.txt


#copy the source code into app directory
COPY ./app  /app

#set the port 8090 from local server and 9090 for docker
EXPOSE 8090:9090

#Run the server
CMD ["uvicorn","app.main:app", "--reload","--host","0.0.0.0"]



