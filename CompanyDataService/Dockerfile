FROM python:3.11
ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENV MONGO_URI mongodb://mongo:27018/companydb
EXPOSE 5003
RUN chmod +x /app/start.sh

CMD ["./start.sh"]