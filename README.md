# Skypro.Python course
## Coursework 6 - Todolist

Backend for task-tracking application

### Stack

- django - backend
- postgresql - database

### How to launch in development environment

1. Create virtual environment
2. Install dependencies from requirements.dev.txt
   - `pip install -r todolist/requirements.dev.txt`
3. Set environment variables in .env file
   - create .env file in todolist folder
   - you can copy the default variables from todolist/.env.example
4. Launch database from deploy folder
   - `cd deploy`
   - `docker compose --env-file ../todolist/.env -f docker-compose.dev.yaml up -d`
5. Make migrations from todolist folder
   - `cd todolist`
   - `./manage.py makemigraitons`
   - `./manage.py migrate`
6. Launch project
   - `./manage.py runserver`

