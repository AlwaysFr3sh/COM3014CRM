#!/bin/bash

# Start MongoDB service
service mongodb start

# Wait for MongoDB service to start
until mongo --eval "print(\"waited for connection\")"; do
    sleep 1
done

# Create the necessary collections and documents
mongo $MONGO_URI <<EOF
use authdb
db.createUser({user: 'root', pwd: 'password', roles: [{role: 'dbOwner', db: 'authdb'}]})
db.createCollection('User')
db.createCollection('Company')
EOF

# Start the Flask application
python3 -u app.py
