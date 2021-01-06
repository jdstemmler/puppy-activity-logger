FROM continuumio/miniconda3:latest

ADD app/static/ /app/static/
ADD app/templates/ /app/templates/
ADD app/*.py /app/
ADD environment.yml /app/

WORKDIR /app/

RUN conda env create -f environment.yml

EXPOSE 5000

CMD [ "conda", "run", "-n", "puppy", "--live-stream", "python", "./app.py" ]