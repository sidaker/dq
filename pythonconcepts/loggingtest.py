import logging
'''
Don't name your script logging.py
logging.debug("debug-level message")
logging.info("info-level message")
logging.warning("warning-level message")
logging.error("error-level message")
logging.critical("critical-level message")
'''

# Set minimum logging level required
# logging.basicConfig(level=logging.DEBUG)

def main():
    logging.debug("debug-level message")
    logging.info("info-level message")
    logging.warning("warning-level message")
    logging.error("error-level message")
    logging.critical("critical-level message")


if __name__ == '__main__':
    main()
    '''
    By default.
    WARNING:root:warning-level message
    ERROR:root:error-level message
    CRITICAL:root:critical-level message
    '''
