FROM python:3.7-slim-buster
COPY . /app
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
RUN pip install -r requirements.txt 
EXPOSE 5000
ENTRYPOINT [ "python" ] 
CMD [ "app.py" ] 