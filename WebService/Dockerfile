FROM python:3.11
ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN chmod +x /app/app.py
EXPOSE 5002
CMD ["./app.py"]