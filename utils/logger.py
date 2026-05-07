class Logger:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Create the new instance if it doesn't exist
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def info(self, msg):
        print("INFO | {}".format(msg))

    def warning(self, msg):
        print("WARNING | {}".format(msg))

    def error(self, msg):
        print("ERROR | {}".format(msg))

    def critical(self, msg):
        print("CRITICAL | {}".format(msg))
