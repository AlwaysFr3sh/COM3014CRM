# Endpoints
## All returns are in JSON Format
## Operations
* *POST* to Create a resource,
* *GET* to Retrieve a resource,
* *PUT* to Update a resource, and
* *DELETE* to Delete a resource.

## Authentication Service Endpoints
```
GET /user
```
* Returns all user data

```
GET /user/<username>
```
* Return user data for one user given a username

```
GET /login/<username>/<password>
```
* Logs in user

```
POST /register/<username>/<password>
```
* Registers user
```
DELETE /delete/<username>/<password>
```
* Deletes user

*NOTES*
* passwords will need to be encrypted
* Need to ensure that a rogue hacker can’t leverage the delete user endpoint , will need some form of authentication that cannot be hacked to prevent this, hopefully encrypted password is sufficient authentication

