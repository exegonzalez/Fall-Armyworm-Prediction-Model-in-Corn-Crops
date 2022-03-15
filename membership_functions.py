def high_trapezoidal(scale, value):
    """
    Args:  
        scale (list): Scale of values of the increasing trapezoidal membership function
        value (float): Value to fuzzify 
    
    Returns:
        float: Returns the corresponding value in an increasing trapezoidal membership function
    """
    if(value < scale[0]):
        return 0.0
    elif(value > scale[1]):
        return 1.0
    else:
        return (value-scale[0])/(scale[1]-scale[0])

def medium_trapezoidal(scale, value):
    """
    Args:
        scale (list): Scale of values of the trapezoidal membership function
        value (float): Value to fuzzify
    
    Returns:
        float: Returns the corresponding value in a trapezoidal membership function
    """
    if((value < scale[0]) or (value > scale[3])):
        return 0.0
    elif((value >= scale[0]) and (value <= scale[1])):
        return (value-scale[0])/(scale[1]-scale[0])
    elif((value >= scale[2]) and (value <= scale[3])):
        return (scale[3]-value)/(scale[3]-scale[2])
    else:
        return 1.0

def low_trapezoidal(scale, value):
    """
    Args:
        scale (list): Scale of values of the decreasing trapezoidal membership function
        value (float): Value to fuzzify

    Returns:
        float: Returns the corresponding value in a decreasing trapezoidal membership function
    """
    if(value > scale[1]):
        return 0.0
    elif(value < scale[0]):
        return 1.0
    else:
        return (scale[1]-value)/(scale[1]-scale[0])


MEMBERSHIP_FUNCTIONS = {
    'temp': {
        'high': {
            'scale': [25, 30],
            'funcion': high_trapezoidal
        },
        'medium': {
            'scale': [8, 15, 25, 30],
            'function': medium_trapezoidal
        },
        'low': {
            'scale': [8, 15],
            'function': low_trapezoidal
        },
    },
    'humidity': {
        'high': {
            'scale': [70, 80],
            'funcion': high_trapezoidal
        },
        'medium': {
            'scale': [40, 50, 70, 80],
            'function': medium_trapezoidal
        },
        'low': {
            'scale': [40, 50],
            'function': low_trapezoidal
        },
    },
    'wind': {
        'high': {
            'scale': [5, 6],
            'funcion': high_trapezoidal
        },
        'medium': {
            'scale': [2, 3, 5, 6],
            'function': medium_trapezoidal
        },
        'low': {
            'scale': [2, 3],
            'function': low_trapezoidal
        },
    },
    'solar_rad': {
        'high': {
            'scale': [24, 27],
            'funcion': high_trapezoidal
        },
        'medium': {
            'scale': [18, 21, 24, 27],
            'function': medium_trapezoidal
        },
        'low': {
            'scale': [18, 21],
            'function': low_trapezoidal
        },
    },
    'rain': {
        'high': {
            'scale': [15, 20],
            'funcion': high_trapezoidal
        },
        'medium': {
            'scale': [5, 8, 15, 20],
            'function': medium_trapezoidal
        },
        'low': {
            'scale': [5, 8],
            'function': low_trapezoidal
        },
    }
}