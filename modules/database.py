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
        #   - nurtition: The nutrition applet
        #   - academic: The academic applet
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
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def execute_query(self, query, params=()):
        # Execute a query on the database
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    

