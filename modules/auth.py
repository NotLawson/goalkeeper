# Auth module for handling user authentication and authorization
import os, sys, time, json, datetime

class Authentication:
    def __init__(self, db):
        self.db = db

    def register_user(self, username, password_hash, email, dob, fname, lname, tags = ["user"], applets = [], settings = None):
        """
        Register a new user in the database.
        :param username: The username of the user.
        :param password: The password of the user.
        :param email: The email of the user.
        :return: True if the user was registered successfully, False and the error otherwise.
        """
        if settings == None:
            settings = {
                "theme":"default",
            }
        try:
            self.db.execute_query("INSERT INTO users (username, password, email, dob, fname, lname, tags, applets, settings) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (username, password_hash, email, dob, fname, lname, tags, applets, json.dump(settings)))
            return True, "User registered successfully"
        except Exception as e:
            return False, f"Error registering user: {e}"
    
    def create_token(self, user_id, name=None):
        """
        Create a new token for the user.
        :param user_id: The ID of the user to create the token for.
        :param name: The name of the token.
        :return: The token if it was created successfully, False and the error otherwise.
        """
        while True:
            token = os.urandom(16).hex()
            self.db.execute_query("SELECT * FROM tokens WHERE token = %s", (token,))
            if self.db.cursor.fetchone() == None:
                break
        name = "Unnammed Token" if name == None else name
        try:
            self.db.execute_query("INSERT INTO tokens (token, user_id, name) VALUES (%s, %s, %s)", (token, user_id, name))
            return token
        except Exception as e:
            return False, f"Error creating token: {e}"
        
    def delete_token(self, token):
        """
        Delete a token from the database.
        :param token: The token to delete.
        :return: True if the token was deleted successfully, False and the error otherwise.
        """
        try:
            self.db.execute_query("DELETE FROM tokens WHERE token = %s", (token,))
            return True
        except Exception as e:
            return False, f"Error deleting token: {e}"
        
    def rename_token(self, token, name):
        """
        Rename a token in the database.
        :param token: The token to rename.
        :param name: The new name of the token.
        :return: True if the token was renamed successfully, False and the error otherwise.
        """
        try:
            self.db.execute_query("UPDATE tokens SET name = %s WHERE token = %s", (name, token))
            return True
        except Exception as e:
            return False, f"Error renaming token: {e}"
        
    def login(self, username, password_hash):
        """
        Login a user.
        :param username: The username of the user.
        :param password: The password of the user.
        :return: True and a token if the user was logged in successfully, False and the error otherwise.
        """
        try:
            self.db.execute_query("SELECT * FROM users WHERE username = %s AND password = %s", (username, password_hash))
            user = self.db.cursor.fetchone()
            if user == None:
                return False, "Invalid username or password"
            token = self.create_token(user[0])
            return True, token
        except Exception as e:
            return False, f"Error logging in: {e}"
        
    def authenticate(self, token):
        """       
        Authenticate a user using a token.
        :param token: The token to authenticate with.
        :return: True and the user object if the token is valid, False and the error otherwise.
        """
        try:
            self.db.execute_query("SELECT user_id FROM tokens WHERE token = %s", (token,))
            user = self.db.cursor.fetchone()
            if user == None:
                return False, "Invalid token"
            self.db.execute_query("SELECT * FROM users WHERE id = %s", (user[0],))
            user = self.db.cursor.fetchone()
            if user == None:
                return False, "Broken token"
            return True, user
        except Exception as e:
            return False, f"Error authenticating token: {e}"
        

    def auth(self, request):
        """
        Authenticate a user using a token from the request.
        :param request: The request to authenticate with.
        :return: True and the user object if the token is valid, False and the error otherwise.
        """
        token = request.cookies.get("token")
        if token == None:
            token = request.headers.get("Authorization")
        if token == None:
            return False, "No token provided"
        return self.authenticate(token)
    

    

    