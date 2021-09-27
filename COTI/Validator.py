def stringBlankOrNone(input):
    ''' Check if the input is a string and if it's empty or null.
    Args:
        input (String): String value
    Returns:
        (Boolean): True if string is '' or None.  Otherwise False if it's not a String or is not '' or None.
    '''
    try:
        i = str(input)
    except:
        print('[ERROR] Input is not a string.')
        return False

    if i == '' or i == 'None':
        return True
    else:
        return False

def isInt(input):
    '''Check if the input is an int.
    Args:
        input (String): String value
    Returns:
        (Boolean): True if the input can be converted into an integer data type, otherwise False
    '''
    try:
        i = int(input)
        return True
    except:
        return False