# Database module
# This module contains the Database class to handle to the postgres database.
import psycopg2


class Database:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        self.init_tables()

    def init_tables(self):
        # Initialize the database tables

        # Users table
        # This table stores user information
        # - id: Unique identifier for each user
        # - username: Unique username for each user
        # - email: Unique email for each user
        # - first_name: First name of the user
        # - last_name: Last name of the user
        # - date_of_birth: Date of birth of the user
        # - password: Hashed password for each user
        # - created_at: Timestamp of when the user was created
        # - online_at: Timestamp of when the user was last online.
        # - applets: List of applets the user has access to.
        #   - mental: The mental health applet
        #   - physical: The physical health applet
        # - settings: The JSON Settings object for the user. See the section at the bottom of this file for more information.
        # - notifications: A list of all notifications this user has received.
        #   - id: Unique identifier for each notification
        #   - title: Title of the notification
        #   - message: Message of the notification
        #   - created_at: Timestamp of when the notification was created
        #   - action: The action to take when the notification is clicked
        # - tags: A list of tags for the user. This is used to allow special permissions for certain users.
        #   - user: Standard account. Grants access to the Core Applet and standard features.
        #   - admin: Admin account. Grants access to the Admin Panel and related features. Visual Tag in the UI.
        #   - system: System Account. Designates the account as a system account. These accounts are usually headless, and are used for interal tasks. Visual Tag in the UI.
        #   - moderator: Moderator account. Grants access to moderation tools in the social section of the applet. Visual Tag in the UI.
        #   - developer: Developer account. Visual Tag in the UI.
        #   - tester: Tester account. Grants access to applets and features designated as in development. Visual Tag in the UI.
        #  - friends: A list of user_ids of friends for the user. This is used to allow social features in the applet.
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                date_of_birth TIMESTAMP,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                online_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                applets TEXT[],
                settings TEXT,
                notifications TEXT[],
                tags TEXT[],
                friends INTEGER[],
                CONSTRAINT username_check CHECK (username ~ '^[a-zA-Z0-9_]+$'),
                CONSTRAINT email_check CHECK (email ~ '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            );
        """)

        # Tokens Table
        # This table stores the tokens for each user. This is used for authentication and authorization.
        # - token: The token for the user. This is used for authentication. It is 16 characters long.
        # - user_id: The ID of the user this token belongs to.
        # - created_at: The timestamp of when the token was created.
        # - name: The name of the token.
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tokens (
                token VARCHAR(16) PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                name VARCHAR(50)
            );
        """)
        
        # Tasks Table
        # This table stores the tasks for each user.
        # - id: Unique identifier for each task
        # - user_id: The ID of the user this task belongs to. This is an array in case the task is shared between users.
        # - title: The title of the task
        # - description: The description of the task
        # - applet: The applet this task belongs to. This is used to filter tasks by applet.
        # - due: The timestamp the task is due.
        # - status: The status of the task.
        #   - not_started: The task has not been started yet.
        #   - in_progress: The task is in progress.
        #   - completed: The task has been completed.
        #   - failed: The task has been failed.
        #   - cancelled: The task has been cancelled.
        # - created_at: The timestamp of when the task was created.
        # - conditions: The conditions for the task. This is a JSON object that contains the conditions for the task.
        # - data: The data for the task. This is a JSON object that contains the data for the task.
        # - config: The config for the task. This is a JSON object that contains the config for the task. This is set and read by the applet to track progress.
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                user_id INTEGER[],
                title VARCHAR(50) NOT NULL,
                description TEXT,
                applet VARCHAR(50) NOT NULL,
                due TIMESTAMP,
                status VARCHAR(20) DEFAULT 'not_started',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                conditions TEXT,
                data TEXT,
                config TEXT
            );
        """)

    def execute_query(self, query, params=()):
        # Execute a query on the database
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    def execute_command(self, command, params=()):
        # Execute a command on the database
        self.cursor.execute(command, params)
    

