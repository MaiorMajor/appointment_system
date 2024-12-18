from classes.person import Person

class Patient(Person):
    """
    Patient class that represents a person seeking medical care.
    Inherits from Person class and adds patient-specific information.
    """

    def __init__(self, name, adress, birth_date, phone, email):
        """
        Initialize a Patient instance.

        Args:
            name (str): The patient's full name
            email (str): The patient's email address
            phone (str): The patient's contact phone number
            birth_date (str): The patient's date of birth
        """
        # Initialize parent class (Person) with name and email
        super().__init__(name, email)
        # Store patient-specific attributes as private
        self.__adress = adress
        self.__phone = phone
        self.__birth_date = birth_date
        self.table_name = "patient"
    
    


    @property
    def phone(self):
        """
        Get the patient's phone number.

        Returns:
            str: The patient's contact phone number
        """
        return self.__phone
    
    @property
    def adress(self):
        """
        Get the patient's adress.
        Returns:
            str: The patient's adress
        """
        return self.__adress

    @property
    def birth_date(self):
        """
        Get the patient's birth date.

        Returns:
            str: The patient's date of birth
        """
        return self.__birth_date

    def __str__(self):
        """
        Return string representation of the Patient.

        Returns:
            str: Formatted string with patient's name and birth date
        """
        return f"{self.name} - {self.birth_date}"
    
    
    def get_db_values(self):
        columns = "name, email, address, birth_date, phone"
        values = (self.name, self.email, self.adress, self.birth_date, self.phone)
        return columns, values
