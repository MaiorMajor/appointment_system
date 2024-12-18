from classes.person import Person


class Doctor(Person):
    """
    Doctor class that represents a medical professional.
    Inherits from Person class and adds specialty-specific functionality.
    """

    def __init__(self, name, email, specialty):
        """
        Initialize a Doctor instance.

        Args:
            name (str): The doctor's full name
            email (str): The doctor's email address
            specialty (str): The doctor's medical specialty
        """
        # Initialize parent class (Person) with name and email
        super().__init__(name, email)
        # Store specialty as private attribute
        self.__specialty = specialty
        self.table_name = "doctor"
    
    @property
    def specialty(self):
        """
        Get the doctor's specialty.

        Returns:
            str: The medical specialty of the doctor
        """
        return self.__specialty

    def __str__(self):
        """
        Return string representation of the Doctor.

        Returns:
            str: Formatted string with doctor's name and specialty
        """
        return f"{self.name} - {self.specialty}"
    
    
    def get_db_values(self):
        from utils import get_id
        columns = "name, email, specialization_id"
        values = (self.name, self.email, get_id(self.specialty, "name", "specialization"))
        return columns, values
