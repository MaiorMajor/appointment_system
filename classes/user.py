class User:
    """
    User class that manages system authentication and access control.
    Handles user credentials and login functionality.
    """

    def __init__(self, email, password, admin=False):
        """
        Initialize a User instance with login credentials.

        Args:
            email (str): User's email address used for authentication
            password (str): User's password for system access
        """
        # Store user credentials as private attributes
        self.__email = email
        self.__password = password # Encrypted password with sha256
        self.__admin = admin
    
    def __str__(self):
        """
        Return a string representation of the User object.
        """
        return f"{self.__email}, Admin: {self.__admin}"
    
    @property
    def admin(self):
        """
        Check if the user is an administrator.
        """
        return self.__admin

    @property
    def email(self):
        """
        Get the user's email address.

        Returns:
            str: The user's email address
        """
        return self.__email

    @property
    def password(self):
        """
        Get the user's password.

        Returns:
            str: The user's password
        """
        return self.__password


    def exists_in_db(self):
        """
        Check if the user's credentials exist in the database.
        """
        import sqlite3
        from constants import PATH_TO_DB
        email = False
        with sqlite3.connect(PATH_TO_DB) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (self.email,))
            result = cursor.fetchone()
            email = result is not None
            if not email:
                return False
            cursor.execute("SELECT password FROM users WHERE email = ?", (self.email,))
            stored_password = cursor.fetchone()
            if stored_password[0] == self.password:
                return True
            return False
    
    def is_admin(self):
        """
        Checks if the current user is an administrator.
        
        Returns:
            bool: True if the user is an administrator, False otherwise.
        """
        if self.exists_in_db():
            import sqlite3
            from constants import PATH_TO_DB
            with sqlite3.connect(PATH_TO_DB) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE email = ?", (self.email,))
                result = cursor.fetchone()
                if result[3] == 1:
                    return True
                else:
                    return False
    

    def insert_in_db(self):
        """
        Inserts the user's credentials into the database.
        
        Returns:
            bool: True if insertion was successful, False otherwise
        """
        import sqlite3
        from constants import PATH_TO_DB
        try:
            with sqlite3.connect(PATH_TO_DB) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (email, password, is_admin) VALUES (?, ?, ?)", 
                    (self.email, self.password, self.admin)
                )
                return True
        except:
            return False 

    def delete_from_db(self):
        """
        Deletes user from database
        """
        import sqlite3
        from constants import PATH_TO_DB
        try:
            with sqlite3.connect(PATH_TO_DB) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE email = ?", (self.email,))
                return True
        except:
            return False
