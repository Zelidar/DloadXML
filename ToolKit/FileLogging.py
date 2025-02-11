import datetime

def logMsg(message, prefix="INFO"):
    """Logs a message to the log file with a timestamp and customizable prefix.

    Args:
        message (str): The message to log.
        prefix (str, optional): A prefix to categorize the log entry 
                                (e.g., "INFO", "WARNING", "ERROR"). 
                                Defaults to "INFO".
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    screen_entry = f"[{prefix}] {message}"
    log_entry = f"[{timestamp}] [{prefix}] {message}\n"

    with open("operation_log.txt", "a") as file:
        print(screen_entry)
        file.write(log_entry)

# Example usage from an external module:
# import FileLogging
# FileLogging.logMsg("API call successful", prefix="API") 

# TokenExpiration = AuthResponse.json()['AuthTokenExpires']
# FileLogging.logMsg(f"Token expiration date: {TokenExpiration}", prefix="API")

