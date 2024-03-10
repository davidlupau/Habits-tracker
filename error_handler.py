class Error_handler:
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
		"""Returns the stored error message."""
		return self.error_message

# Creation of error messages
error_1 = Error_handler("Task name cannot be empty. Please try again.") # Error message when the user enters an empty task name
error_2 = Error_handler("Please enter a valid number.") # Error message when the user enters an invalid input when needed to convert to an integer
error_3 = Error_handler("Invalid input. Please enter a valid habit id.") # Error message when the user enters an invalid habit id
error_4 = Error_handler("Invalid input. Please enter a valid option number.") # Error message when the user enters an invalid option from the menu
error_5 = Error_handler("Invalid input. Please enter 1 for yes, 2 for no.") # Error message when the user enters an invalid input when asked to enter 1 for yes or 2 for no