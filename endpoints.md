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

## Customer Data Service Endpoints

```
GET /get_entry/<database>?search_term=value&num_results=value&sort_by=value
```
* Returns x number of entries from specified database, return x number of results if num_results  is specified else return all. Only return results relevant to search term if one is given, results should be sorted according to sort_by if sort_by is specified, else by defualt results should be sorted however the database stores them.
* Should the UI for displaying entries be page-based or just one page with a scroll bar to look through all of the entries? If we decide to use pages we may need to add an offset parameter (eg offset is 0, num_results is 10 -> return database entries 0-10, or 10-20 if offset is 10)

```
GET /get_entry/<database>/<entry>
```
* Get specified database entry (I guess return 404 if not found?)
```
POST /create_database/<database>
```
* Creates a new database TODO: Figure out what to return when database with specified name already exists

```
POST /create_entry/<database> {json data}
```
* Creates new entry in the database
  
```
DELETE /delete_entry/<database>/<entry>
```
* Delete database entry
  
