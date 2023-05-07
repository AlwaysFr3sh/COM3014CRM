FROM python:3.9
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV MONGO_URI mongodb://mongo:27017/authdb
EXPOSE 5001
RUN chmod +x /app/start.sh
CMD ["./start.sh"]