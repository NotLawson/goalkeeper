# Database module
# This module contains the Database class to handle to the postgres database.
import psycopg2, time


class Database:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        while True:
            try:
                self.connection = psycopg2.connect(
                    dbname=self.dbname,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port
                )
                break
            except Exception as e:
                print(f"Error connecting to database: {e}")
                time.sleep(5)
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
        # - name: User name
        # - password: Hashed password for each user
        # - salt: Salt used for hashing the password
        # - created_at: Timestamp of when the user was created
        # - online_at: Timestamp of when the user was last online.
        # - settings: The JSON Settings object for the user. See the section at the bottom of this file for more information.
        # - notifications: A list of all notifications this user has received.
        #   - id: Unique identifier for each notification
        #   - title: Title of the notification
        #   - message: Message of the notification
        #   - created_at: Timestamp of when the notification was created
        #   - action: The url to navigate to when the notification is clicked
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
                email VARCHAR(100) UNIQUE,
                name VARCHAR(100) NOT NULL,
                password VARCHAR(255) NOT NULL,
                salt VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                online_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                settings TEXT,
                notifications TEXT[],
                tags TEXT[] NOT NULL,
                friends INTEGER[]
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
                token VARCHAR(32) PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                name VARCHAR(50)
            );
        """)

        # Goals Table
        # This table stores the all goals
        # - id: ID for the goal
        # - user_id: ID of the user who owns the task
        # - title: Title of the goal
        # - description: Description of the goal
        # - created_at: The timestamp of when the goal was created.
        # - stage: The current stage of the goal (1, 2, 3)
        # - config: JSON configuration for the goal
        #  - stages: List of stages for the goal
        #   - id: ID for the stage. e.g. Stage 1 would be 1, Stage 2 would be 2
        #   - title: Title of the stage. Defaults to none, where "Stage" plus the stage ID will be used instead (e.g. Stage 1)
        #   - description: Description of the stage.
        #   - tasks: List of tasks for the stage.
        #     - title: Title of the task.
        #     - description: Description of the task.
        #     - type: Type of task, can be daily, weekly or monthly
        #     - optional: Whether the task is optional or not.
        #   - milestone: The milestone associated with the stage.
        #   - duration: The duration of the stage in weeks. Will be used when deciding the timeline for the goal.
        # - created_from: ID of the Marketplace item the goal was created from.
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                title VARCHAR(100) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                stage INTEGER DEFAULT 1,
                config TEXT,
                created_from INTEGER
            );
        """)

        # Tasks Table
        # This table stores all tasks for goals
        # - id: ID of the task
        # - goal_id: ID of the goal this task belongs to
        # - title: Title of the task
        # - description: Description of the task
        # - created_at: The timestamp of when the task was created.
        # - due_date: The timestamp of when the task is due.
        # - status: The current status of the task (e.g. incomplete, complete, missed)
        # - optional: Whether the task is optional or not.
        # - milestone: Whether the task is a milestone or not.
        # - ultimate: Whether the task is the ultimate goal or not.
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                goal_id INTEGER REFERENCES goals(id),
                title VARCHAR(100) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TIMESTAMP,
                status VARCHAR(20) DEFAULT 'incomplete',
                optional BOOLEAN DEFAULT FALSE,
                milestone BOOLEAN DEFAULT FALSE,
                ultimate BOOLEAN DEFAULT FALSE
            );
        """)

    def execute_query(self, query, params=()):
        # Execute a query on the database
        self.cursor.execute(query, params)
        try:
            return self.cursor.fetchall()
        except Exception as e:
            return []
    def execute_command(self, command, params=()):
        # Execute a command on the database
        self.cursor.execute(command, params)
    

