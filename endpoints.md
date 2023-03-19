# Endpoints
## All returns are in JSON Format
## Operations
* *POST* to Create a resource,
* *GET* to Retrieve a resource,
* *PUT* to Update a resource, and
* *DELETE* to Delete a resource.

## Authentication Service Endpoints
GET /user
Returns all user data

GET /user?username=value
Return user data for one user given a username

GET /login?username=value&password=value
Logs in user

POST /register?username=value&password=value&company=value
Registers user

DELETE /delete?username=value&password=value
Deletes user

*NOTES*
* passwords will need to be encrypted
* Need to ensure that a rogue hacker can’t leverage the delete user endpoint , will need some form of authentication that cannot be hacked to prevent this, hopefully encrypted password is sufficient authentication
