# Django Task Management API

This is a Django-based task management system with JWT authentication, allowing users to create, update, and manage tasks. This project is containerized using Docker and Docker Compose.

---

## Project Setup

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Steps to Install Dependencies

All dependencies are installed automatically within the Docker container, so no manual installation is necessary.

### Instructions for Setting Up the Database

1. **Clone the Repository**

   Clone the project to your local machine and navigate into the project directory:

   ```bash
   git clone https://github.com/Kushaldotel/taskmanagement.git
   cd taskmanagement

2. **Database for the repo**

    no need to configur db as for demo default postgres db is being used:

    create a virtual environment on your folder where you will clone and activate it if you want.

    docker-compose up --build to run the application

    Your application starts at http://0.0.0.0:8000/

    change it to http://localhost:8000/


## API USAGE

1. **Authentication Setup**

Endpoint: /auth/register/
Method: POST
Request Body:

{
  "username": "newuser",
  "password": "password123",
  "email": "newuser@example.com"
}

Response:
{
  "success": true,
  "message": "Successful",
  "is_paginated": false,
  "data": {
    "user": {
      "username": "yourusername",
      "email": "youremail@example.com"
    },
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNDY2ODcyOSwiaWF0IjoxNzMwMzQ4NzI5LCJqdGkiOiI0MDUxYTRhMWViOGU0NzkyYjY2OGM5YjEwZTdlNWYzYyIsInVzZXJfaWQiOjJ9.1K9urPRGstXFOq2iUgyEvigGkPldbc69P4vULr9zuio",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMwMzU5NTI5LCJpYXQiOjE3MzAzNDg3MjksImp0aSI6IjFmNjI5ZjEwZTEyMDRhNDU4ZjdlMDQ5OGFlOGZhNzdhIiwidXNlcl9pZCI6Mn0.yhoSCcY1ZeKTnEDCwrqwJEGK8_yfC4J-QNVuOU9QD9s"
  }
}

Endpoint: /auth/login/
Method: POST
Request Body:

{
    "username": "yourusername",
    "password": "yourpassword"
}

Response:
{
  "success": true,
  "message": "Successful",
  "is_paginated": false,
  "data": {
    "message": "User authenticated successfully",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMwMzU5NTMzLCJpYXQiOjE3MzAzNDg3MzMsImp0aSI6ImZkNjk1YjE5NDMxOTQxY2NhMjQ1MDU4NmE1YmY5ZjM0IiwidXNlcl9pZCI6Mn0.viVmps9bsN-0XAyT2oPWuNkPB6RXZc1MD0eH6bgi_Pw",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNDY2ODczMywiaWF0IjoxNzMwMzQ4NzMzLCJqdGkiOiI5NTliOGQ4OTMxZmM0NjVhOGE1NGE1NzUwMjA0ZThhZSIsInVzZXJfaWQiOjJ9.KFX_fULmgIFliPxe8YxCelKmTjZmFB8zYonkZjs4f5Q"
  }
}


2. **Task List and Create**
Endpoint: /api/tasks/
Method: GET, POST

Description: Retrieve a list of all tasks for the authenticated user or create a new task.

Response for GET:
{
  "success": true,
  "message": "Successful",
  "is_paginated": false,
  "data": [
    {
      "id": 1,
      "title": "Destination Pickup",
      "description": "Pickinhup Destination",
      "is_completed": true,
      "created_at": "2024-10-31T04:25:44.163988Z",
      "updated_at": "2024-10-31T04:25:44.164005Z"
    },
    {
      "id": 2,
      "title": "Destination Pickup",
      "description": "Pickinhup Destination",
      "is_completed": true,
      "created_at": "2024-10-31T04:42:05.810735Z",
      "updated_at": "2024-10-31T04:42:05.810767Z"
    }
  ]
}


Request Body (for POST):

{
  "title": "New Task",
  "description": "Task description",
  "is_completed": false
}


Response:
{
  "success": true,
  "message": "Successful",
  "is_paginated": false,
  "data": {
    "id": 2,
    "title": "Destination Pickup",
    "description": "Pickinhup Destination",
    "is_completed": true,
    "created_at": "2024-10-31T04:42:05.810735Z",
    "updated_at": "2024-10-31T04:42:05.810767Z"
  }
}

3. **Task Retrieve, Update, and Delete**
Endpoint: /api/tasks/<task_id>/

Method: GET, PUT, PATCH, DELETE

Description: Retrieve, update, or delete a specific task by ID.
Request Body (for PUT/PATCH):

{
  "title": "Updated Task",
  "description": "Updated description",
  "is_completed": true
}

{
  "id": 1,
  "title": "Updated Task",
  "description": "Updated description",
  "is_completed": true,
  "created_at": "2024-10-01T12:00:00Z",
  "updated_at": "2024-10-02T12:00:00Z"
}


4. **Task Filtering and Search**
To filter and search tasks, use query parameters on the /api/tasks/ endpoint:

Filter by Completion Status:

/api/tasks/?is_completed=true
Description: Retrieves all completed tasks.
Search by Title or Description:

/api/tasks/?search=task_keyword
Description: Retrieves tasks that contain the specified keyword in the title or description.

## Method to run test cases:

In a new terminal run "docker-compose exec web python manage.py test"

## Additional Deployement in Aws can Look like

- Login into your aws account
- just make a security group with inbound rules from ssh, http and https
- now create an ec2 instance(use linux os and security group just created) and like connect to it
- update and upgrade the instance
- Install python virtualenv package
- Create the virtual env
- activate the virtualenvironment
- Clone the repo (if private generate key and add to your github account under ssh and gpg keys)
- install the requirementsfile
- change the debug to false in production
- install supervisor for management
- install gunicorn using pip
- install nginx in your instance
- configure gunicorn this will create a app.sock file give name
- user supervisor to reread and update
- configure the nginx for django configuration. Listen to your app.sock port 80. Add your ec2 ip
- reload nginx after a successful addition
- you can like set allowed host in your settings.py too.
- If you have domain set the A record for your ec2 ip and change the nginx config for your django project and like set in allowed host in settings.py too.
- Save and reload nginx