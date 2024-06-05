# SocialApp

## Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd social_network
    ```
    
2. Install the poetry on your machine using the below command
   ```
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
   ```
   Set the environment variable on Windows:
   ```
   %APPDATA%\Python\Scripts
   ```
    
3. Run the poetry command
   ```
   poetry install
   ```
4. Run the poetry shell which will create the environment and run the project in that environment:
    ```
    poetry shell
    ```
   If the virtual environment is not spawning then run the power shell in administrator mode and
   run these command
   ```
   Set-ExecutionPolicy RemoteSigned
   ```
   You may be prompted to confirm the change. Type Y and press Enter
   Now, try the "poetry shell"
   
5. Run the migrate command
   ```
    python manage.py migrate
    ```

6. Create a superuser:
    ```
    python manage.py createsuperuser
    ```
    
9. Run the server
     ```
     python manage.py runserver
     ```


**NOTE**: Postman collection and environment file are uploaded in the same repository.

## Endpoints

- `/api/signup/` - User signup
- `/api/login/` - User login
- `/api/search/` - Search users by email or name
- `/api/send-request/<int:to_user_id>/` - Send friend request
- `/api/respond-request/<int:request_id>/<str:action>/` - Respond to friend request
- `/api/friends/` - List friends
- `/api/pending-requests/` - List pending friend requests
