# Backend Code for MPC Course Project

## Tech Stack Used
1. Django REST
2. JWT Authentication

### Authentication 
1. Form Login/Signup added.
2. Seperate Login/Signup for Admin or Normal User. 

### Basic Functionalities
1. Real-Time and Simultanous Sensor Data Monitoring. 
2. User Login/Signup. 
3. User can have multiple devices containing multiple sensors.
4. User Logs for Admin

## Procedure:
- Install [python](https://www.python.org/downloads/) in your environment(pre-installed on Ubuntu).
- Navigate to the cloned repository.
    ```
    cd <project_directory_name>     #   mpc_backend
    ```
- Create a new virtual environment and activate it.
    ```
    python -m venv env
    .\env\Scripts\activate
    ```
- Use pip to install other dependencies from `requirements.txt`
    ```
    pip install -r requirements.txt
    ```
- Make database migrations
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
- Create a superuser (Not Compulsory)
    ```
    python manage.py createsuperuser
    ```
- Run development server on localhost
    ```
    python manage.py runserver 0.0.0.0:8000
    
    http://localhost:8000/admin/
    ```
   
  ### Backend Can be accesible at: localhost:8000
  ### Frontend GitHub Url - [MPC Frontend](https://github.com/aryan0141/mpc_frontend)
