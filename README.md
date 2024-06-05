# SocialApp

## Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd social_network
    ```
    
2. Install the dependencies using poetry
   ```
   poetry install
   ```

3. Create the env using poetry
   ```
   poetry shell
   ```
   
4. Run the migrate command
   ```
    python manage.py migrate
    ```

5. Create a superuser:
    ```
    python manage.py createsuperuser
    ```
    
6. Run the server
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
