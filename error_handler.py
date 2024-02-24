class error_handler:
	"""A class for handling error messages within an application.
    This class allows for the creation of error message objects that can be reused across the application.
    Attributes:
        error_message (str): A descriptive error message.
    Methods:
        get_error_message(): Returns the stored error message."""

    def __init__(self, error_message: str):
		"""Initializes the error_handler with a specific error message.
        Parameters:
            error_message (str): The error message to be associated with this error handler."""
		self.error_message = error_message

	def get_error_message(self):
		"""Returns the stored error message.
		Returns:
			str: The stored error message."""
		return self.error_message

# Creation of error messages
error_1 = error_handler("Task name cannot be empty. Please try again.") # Error messqge when the user enters an empty task name
error_2 = error_handler("Invalid input. enter a number between 1 and 3.") # Error message when the user enters an invalid input when selecting periodicity
error_3 = error_handler("Invalid input. Please enter a valid habit id.") # Error message when the user enters an invalid habit id
