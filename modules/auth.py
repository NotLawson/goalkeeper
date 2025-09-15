# Auth module for handling user authentication and authorization
import os, json, hashlib, hmac
import psycopg2.errors as db_errors

# most of its pretty obvious, i'm not gonna comment
class Authentication:
    def __init__(self, db):
        self.db = db

    def register_user(self, username, password, email, name, tags = ["user"]):
        """
        Register a new user in the database.
        :param username: The username of the user.
        :param password: The password of the user.
        :param email: The email of the user.
        :return: True if the user was registered successfully, False and the error otherwise.
        """
        try:
            salt, password_hash = hash_new_password(password)

            self.db.execute_command("INSERT INTO users (username, password, salt, email, name, tags, settings) VALUES (%s, %s, %s, %s, %s, %s, %s)", (username, password_hash.hex(), salt.hex(), email, name, tags, json.dumps({})))
            return True, "User registered successfully"
        except db_errors.UniqueViolation:
            return False, "Username or email already exists"
        except Exception as e:
            return False, f"Error registering user: {e}"

    def login(self, username, password):
        """
        Login a user.
        :param username: The username of the user.
        :param password: The password of the user.
        :return: True and a token if the user was logged in successfully, False and the error otherwise.
        """
        try:
            user = self.db.execute_query("SELECT password, salt FROM users WHERE username = %s OR email = %s", (username, username))[0]
            if is_correct_password(bytes.fromhex(user[1]), bytes.fromhex(user[0]), password):
                success, token = self.create_token(self.db.execute_query("SELECT id FROM users WHERE username = %s", (username,))[0][0])
                return success, token
            else:
                return False, "Invalid password"

        except IndexError:
            return False, "User not found"
    
    def update_user(self, id, username, password, email, name, tags = ["user"]):
        """
        Update a user in the database.
        :param username: The username of the user.
        :param password: The password of the user.
        :param email: The email of the user.
        :return: True if the user was updated successfully, False and the error otherwise.
        """
        if not password:
            try:
                self.db.execute_command("UPDATE users SET username = %s, email = %s, name = %s, tags = %s WHERE id = %s", (username, email, name, tags, id))
                return True, "User updated successfully"
            except db_errors.UniqueViolation:
                return False, "Username or email already exists"
            except Exception as e:
                return False, f"Error updating user: {e}"

        try:
            password_hash, salt = hash_new_password(password)

            self.database.execute_command("UPDATE users SET username = %s, password = %s, email = %s, name = %s, tags = %s, salt = %s WHERE id = %s", (username, password_hash.hex(), email, name, tags, salt.hex(), id))
        except db_errors.UniqueViolation:
            return False, "Username or email already exists"
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
            return True, token
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
            return True, None
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
            
        
    def authenticate(self, token):
        """       
        Authenticate a user using a token.
        :param token: The token to authenticate with.
        :return: True and the user object if the token is valid, False and the error otherwise.
        """
        try:
            user = self.db.execute_query("SELECT user_id FROM tokens WHERE token = %s", (token,))[0]
            if user == None:
                return False, "Invalid token"
            user = self.db.execute_query("SELECT * FROM users WHERE id = %s", (user[0],))[0]
            if user == None:
                return False, "Broken token"
            return True, user
        except Exception as e:
            return False, f"Error authenticating token: {e}"
        

    def __call__(self, request):
        """
        Authenticate a user using a token from the request.
        :param request: The request to authenticate with.
        :return: True and the user object if the token is valid, False and the error otherwise.
        """
        token = request.cookies.get("token", request.headers.get("Authorization", None))
        if token == None:
            print(f"[auth] No token provided")
            return False, "No token provided"
        success, user = self.authenticate(token)
        print(f"[auth] Authentication Attempt with token {token}: {str(success)} - {user}")
        return success, user
    
# Directly from https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python
def hash_new_password(password: str) -> tuple[bytes, bytes]:
    """
    Hash the provided password with a randomly-generated salt and return the
    salt and hash to store in the database.
    """
    salt = os.urandom(16)
    pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt, pw_hash

def is_correct_password(salt: bytes, pw_hash: bytes, password: str) -> bool:
    """
    Given a previously-stored salt and hash, and a password provided by a user
    trying to log in, check whether the password is correct.
    """
    return hmac.compare_digest(
        pw_hash,
        hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    )
