# CloudComputing

REST APIs.

This is the coursework for group 6.

This project develops APIs for accessing UK Covid-19 information.

We use **Gmail API** as the external REST service to provide email service function. 
Before starting this project, you need to enable Gmail API of your account and download the **_credentials.json_** into 
the same directory as the **EmailService.py** file. And then run the **EmailService.py** or **app.py** to authorize access to your data.
After that, a **_token.pickle_** file will be created in the working directory.
See more at https://developers.google.com/gmail/api/quickstart/python

We use Amazon Relational Database Service (Amazon RDS) for MySQL as our cloud database for accessing persistent information.
See **config.py** for database configuration.

**Models.py** shows the detail of the Data, User and Admin models.

We divide the role into _User_ and _Admin_, implementing authentication via a hash-based method. 

We use _Blueprint_ module in _Flask_ to distinguish between user and admin routing requests.
The user's routing requests start with the prefix _**hostname:port/api/user/**_ while the admin's routing requests start
with the prefix _**hostname:port/api/admin/**_. And both the user and admin need authentication before accessing the APIs.

In this case, we ensure that only the admin can modify(update/delete) the database and the user cannot access the admin's
API, implementing a role-based policy to secure the database.

# The APIs for Admin

GET methods:

_hostname:port/api/admin/user_query_: Login required. Obtaining all users' username and email.

_hostname:port/api/admin/query_: Login required. Obtain all Covid-19 data.

_hostname:port/api/admin/query/\<date\>_: Login required. Obtain the Covid-19 data on a specific date.

_hostname:port/api/admin/get_daily_report_: Login required. Obtain a picture that contains a trend of cases and death. The
picture will be sent by email.


POST method:

_hostname:port/api/admin/add_: Login required. Add new data into database.

PUT method:

_hostname:port/api/admin/data/\<date\>_: Login required. Modify the data on the specific date.

DELETE methods:

_hostname:port/api/admin/data/\<date\>_: Login required. Delete the data on the specific date.

_hostname:port/api/admin/delete_user/\<username\>_: Login required. Delete the specific user from the database.



# The APIs for User
GET methods:

_hostname:port/api/user/query_: Login required. Obtain all Covid-19 data.

_hostname:port/api/user/query/\<date\>_: Login required. Obtain the Covid-19 data on a specific date.

_hostname:port/api/user/get_daily_report_: Login required. Obtain a picture that contains a trend of cases and death. The
picture will be sent by email.

POST method:

_hostname:port/api/user/new_user_: No need to login. Create a new user by given details. The request must contain the username,
password and email address.

# Example
There is an admin account with the username `admin` and password `admin` in the database.
And the application is recently deployed on AWS with the hostname: `ec2-3-235-186-61.compute-1.amazonaws.com`

Send a GET request with a proper authentication to http://ec2-3-235-186-61.compute-1.amazonaws.com/api/admin/query/2020-03-30 will return:
>{"cases":4263,"date":"Mon, 30 Mar 2020 00:00:00 GMT","death":590}

And you can send a POST request to http://ec2-3-235-186-61.compute-1.amazonaws.com/api/user/new_user to create a new user, which
doesn't need authentication. The required parameters are `username`, `password` and `email`.
