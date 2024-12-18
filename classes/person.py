from constants import PATH_TO_DB
import sqlite3


class Person:
    """
    Base Person class that serves as a parent class for Doctor and Patient.
    Contains common attributes and methods for all person types in the system.
    """

    def __init__(self, name, email):
        """
        Initialize a Person instance with basic identification information.

        Args:
            name (str): The person's full name
            email (str): The person's email address
        """
        # Store basic person information as private attributes
        self.__name = name
        self.__email = email

    @property
    def name(self):
        """
        Get the person's name.

        Returns:
            str: The person's full name
        """
        return self.__name

    @property
    def email(self):
        """
        Get the person's email.

        Returns:
            str: The person's email address
        """
        return self.__email

    def __str__(self):
        """
        Return string representation of the Person.

        Returns:
            str: Formatted string with person's name
        """
        return self.__name

    def exists_in_db(self):
        """
        Check if the person exists in the database.
        """
        import sqlite3
        #from constants import PATH_TO_DB
        with sqlite3.connect(PATH_TO_DB) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {self.table_name} WHERE email = ?", (self.email,))
            return cursor.fetchone()[0] > 0
    
    def delete_from_db(self):
        """
        Delete the person from the database.
        """
        import sqlite3
        with sqlite3.connect(PATH_TO_DB) as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {self.table_name} WHERE email = ?", (self.email,))
            conn.commit()
    
    def add_to_database(self):
        """Generic database insertion for any Person subclass"""
        try:
            with sqlite3.connect(PATH_TO_DB) as conn:
                cursor = conn.cursor()
                columns, values = self.get_db_values()
                placeholders = ','.join(['?' for _ in values])
                query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
                cursor.execute(query, values)
                return True
        except sqlite3.Error:
            return False
