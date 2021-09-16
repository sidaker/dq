import logging

extraData = {
   'user' : 'sid@example.com',
   'Company' : 'google'
}

def main():
    # Set minimum logging level required
    fmtstr = "USER:%(user)s Company:%(Company)s %(asctime)s: %(levelname)s: %(funcName)s Line:%(lineno)d \
    %(message)s"
    datestr = '%m/%d/%Y %I:%M:%S %p'
    logging.basicConfig(level=logging.DEBUG,
                        filename='customoutput1.log',
                        filemode='w',
                        format=fmtstr,
                        datefmt=datestr)
    logging.debug("debug-level message",extra=extraData)
    logging.info("info-level message",extra=extraData)
    logging.warning("warning-level message",extra=extraData)

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
    logging.info("with out file mode, log output gets appended",extra=extraData)
