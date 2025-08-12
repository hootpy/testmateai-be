class DatabaseSessionManagerInitializeError(Exception):
    """
    Exception to be raised when DatabaseSessionManager is not initialized
    """

    def __init__(self) -> None:
        super().__init__("DatabaseSessionManager is not initialized")
