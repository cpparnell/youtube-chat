class InvalidYouTubeUrlError(Exception):
    """Exception to be thrown when provided url is not a YouTube video"""
    
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
