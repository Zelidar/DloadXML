def log_user_info(name, email, month):
    with open("operation_log.txt", "a") as file:
        file.write(f"Name: {name}, Email: {email}, Month: {month}\n")
