FROM python:3.8-buster
WORKDIR /myapp
COPY . /myapp
RUN apt-get update
RUN apt-get install tcl-dev tk-dev python3-tk
RUN pip uninstall matplotlib
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python", "app.py"]

