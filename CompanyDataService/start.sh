#!/bin/bash

# Start MongoDB service
service mongodb start

# Wait for MongoDB service to start
until mongo --eval "print(\"waited for connection\")"; do
    sleep 1
done

# Create the necessary collections and documents
mongo $MONGO_URI <<EOF
use companydb
db.createUser({user: 'root', pwd: 'password', roles: [{role: 'dbOwner', db: 'companydb'}]})

EOF

# Start the Flask application
./app.py -debug
