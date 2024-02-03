# Private Chat

Private Chat is a web application that allows users to have private conversations in real-time. It provides a secure and convenient way for individuals to communicate privately.

## Features

- Real-time messaging: Users can send and receive messages in real-time, creating a seamless chat experience.
- User authentication: Users can create accounts and log in securely to access the chat functionality.
- Private conversations: Users can initiate private conversations with other registered users.
- Message history: The application stores and displays the message history for each conversation.
- User status: Users can see the online/offline status of other users and know when they are available for a chat.
- Notifications: Users receive notifications when they receive new messages or when they are mentioned in a conversation.
- Email confirmation: Users are required to confirm their email address during the registration process.
- Scheduled tasks: Celery and Celery Beat are used for scheduling tasks such as sending notifications, sending emails, and sending periodic messages.

## Technologies Used

- JavaScript
- CSS
- Python
- HTML
- Django framework
- Django Channels (for real-time communication)
- Celery (for task scheduling)
- Celery Beat (for scheduling periodic tasks)
## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/abdulkareeme/Private_Chat.git
   ```

2. Change the privilage of entrypoint.sh file to be excutable file :

   ```bash
   cd Private_Chat
   chmod +x Chat/entrypoint.sh
   ```
3. Make sure to create **.env** file inside Private_Chat folder and set this variables in it :
  - DEBUG (1 or 0)
  - SECRET_KEY (hash string)
  - ALLOWED_HOSTS (* or 127.0.0.1:8000)
  - DJANGO_SETTINGS_MODULE (Chat.settings)
  - EMAIL_HOST_USER
  - EMAIL_HOST_PASSWORD (your app password)
  - CELERY_RESULT_BACKEND (redis://redis:6379/0)
  - CELERY_BROKER_URL (redis://redis:6379/0)

4. Running the project (make sure to have docker compose installed) (running on linux):
   ```bash
   sudo docker-compose up -d --bulid
   ```

6. Access the application by visiting `http://localhost:8000` in your web browser.

## Images
1. List Users :
   ![example1](https://github.com/abdulkareeme/Private_Chat/blob/main/images/Screenshot%20from%202024-02-03%2012-48-23.png)
2. Notification :
   ![example2](https://github.com/abdulkareeme/Private_Chat/blob/main/images/Screenshot%20from%202024-02-03%2012-57-14.png)
3. Convesation between tow users and status for every user (typing , online , last seen) :
   ![example3](https://github.com/abdulkareeme/Private_Chat/blob/main/images/Screenshot%20from%202024-02-03%2012-57-30.png)
4. Periodic messages :
   ![example4](https://github.com/abdulkareeme/Private_Chat/blob/main/images/Screenshot%20from%202024-02-03%2012-59-22.png)
5. The result of the periodic message :
   ![example5](https://github.com/abdulkareeme/Private_Chat/blob/main/images/Screenshot%20from%202024-02-03%2013-00-14.png)
6. The Flower server to view all the tasks :
   ![example6](https://github.com/abdulkareeme/Private_Chat/blob/main/images/Screenshot%20from%202024-02-03%2014-19-15.png)

