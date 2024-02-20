class SessionException(Exception):
    def __init__(self, msg, method_name):
        message = f"SessionError {method_name} - {msg}"
        super().__init__(message)

    
