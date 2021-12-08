class LoggingContextManager:
    def __enter__(self):
        print("LoggingContextManager.__neter__()")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print("LoggingContextManager.__exit__: normal exit")
            return self
        else:
            print('Exception detected by LoggingContextManager.__exit__'
                  'type={}, value={}, traceback={}'.format(exc_type,exc_val,exc_tb))
            return exc_type


with LoggingContextManager():
    pass


with LoggingContextManager():
    raise ValueError
