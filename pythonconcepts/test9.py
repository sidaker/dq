
a = '' if (1==2) else "Hello"
#print(a)

a = 330
b = 330
#print("A") if a > b else print("=") if a == b else print("B")

passengerdetails_documentdetails = {}
x=None
x=False
x="C623262\n"
#x="2021/03/05"
#passengerdetails_documentdetails['passengerdetails_documentdetails_documentno'] = ''  if(x is None ) else 'Np'
#print(passengerdetails_documentdetails['passengerdetails_documentdetails_documentno'])


def handle_newlines(x):
    if(x is None):
        print("None found")
        return ''
    elif(isinstance(x, bool)):
        print("boolean found")
        return ''
    else:
        return x.replace('\n', '')

def clean_newline(varx):
    """
    Takes as input a variable varx and strips it off newline characters.
    Also checks if it is of type None or Boolean and returns empty string if so.
    """
    try:
        if(varx is None):
            #LOGGER.info('When Processing %s None found', varx)
            return ''
        elif(isinstance(varx, bool)):
            #LOGGER.info('When Processing %s Boolean found', varx)
            return ''
        else:
            return varx.replace('\n', '')
    except Exception as err:
        print(err)

#print(handle_newlines(x))
print(clean_newline(x))
