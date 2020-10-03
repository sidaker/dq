import logging


def main():
    # Set minimum logging level required
    fmtstr = "%(asctime)s: %(levelname)s: %(funcName)s Line:%(lineno)d \
    %(message)s"
    datestr = '%m/%d/%Y %I:%M:%S %p'
    logging.basicConfig(level=logging.DEBUG,
                        filename='customoutput.log',
                        filemode='w',
                        format=fmtstr,
                        datefmt=datestr)
    logging.debug("debug-level message")
    logging.info("info-level message")
    logging.warning("warning-level message")
    logging.error("error-level message")
    logging.critical("critical-level message")


if __name__ == '__main__':
    main()
    '''
    By default. Change it by logging.basicConfig(level=logging.DEBUG)
    WARNING:root:warning-level message
    ERROR:root:error-level message
    CRITICAL:root:critical-level message
    ---------
    DEBUG:root:debug-level message
    INFO:root:info-level message
    WARNING:root:warning-level message
    ERROR:root:error-level message
    CRITICAL:root:critical-level message
    '''
    logging.info("with out file mode, log output gets appended")
