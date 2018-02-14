# messageWall

----
## Set up the project (Linux)

----
### 1. Setting up the virtual environment
a. Create a virtual env with python3  

    cd path_to_project_folder
    virtualenv -p python3 envname
   
b. Enable virtual env and install requirements
    
    source envname/bin/activate 
    pip install -r requirements.txt
----

### 2. Setting up the backend
a. Enable welcome eamil
  
please set your gmail under **settings.py**  
     
    EMAIL_HOST_USER = 'your_gamil@gmail.com'  
    EMAIL_HOST_PASSWORD = 'your_password'  
go to the gmail settings and make sure **Allow less secure apps** is ON

b. Start the backend (*make sure the virtual env is ativated*)

    cd path_to_project_folder/tsl_wall
    python manage.py runserver
----

### 3. Using the using React frontend (Updated)
    npm install -g create-react-app
    cd ~/Desktop
    create-react-app react_wall && cd react_wall
    rm -r src/ public/
    cp -r path_to_project_folder/frontend_react/* .
    npm start

