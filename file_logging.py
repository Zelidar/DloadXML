import datetime

def log_message(message, prefix="INFO"):
    """Logs a message to the log file with a timestamp and customizable prefix.

    Args:
        message (str): The message to log.
        prefix (str, optional): A prefix to categorize the log entry (e.g., "INFO", "WARNING", "ERROR"). 
                                Defaults to "INFO".
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{prefix}] {message}\n"

    with open("operation_log.txt", "a") as file:
        file.write(log_entry)

# Example usage from an external module:
# import file_logging
# file_logging.log_message("API call successful", 
#                          prefix="API") 

# TokenExpiration = AuthResponse.json()['AuthTokenExpires']
# file_logging.log_message(f"Token expiration date: {TokenExpiration}", 
#                          prefix="API")

