from fuzzy_logic import fuzzification

def generate_fuzzified_dictionary(variable, value):
    """
    Args:
        variable (string): Variable for fuzzification
        value (float): Value to fuzzify
    
    Returns: 
        dict: Returns a fuzzified dictionary
    """
    return {'high': fuzzification(variable, 'high', value), 
            'medium': fuzzification(variable, 'medium', value),
            'low': fuzzification(variable, 'low', value)}

def calculate_dew_point(temperature, humidity):
    """
    Args:
        temperature (float): Daily average temperature
        humidity (float): Daily average relative humidity
    
    Returns:
        bool: Returns true or false if the fuzzification of the dew point value is equal to the 
        temperature
    """
    dew_point = ((humidity/100)**0.125) * (112+0.9*temperature) + (0.1*temperature) - 112
    
    fuzzified_dew_point = generate_fuzzified_dictionary('temp', dew_point)
    fuzzified_temperature = generate_fuzzified_dictionary('temp', temperature)
    
    max_fuzzified_dew_point = max(fuzzified_dew_point, key = fuzzified_dew_point.get)
    max_fuzzified_temperature = max(fuzzified_temperature, key = fuzzified_temperature.get)
    
    return True if((max_fuzzified_dew_point == max_fuzzified_temperature) 
        and (round(fuzzified_temperature[max_fuzzified_temperature], 1) == round(fuzzified_dew_point[max_fuzzified_dew_point], 1))) else False


def dutch_rules(temperature, radiation, rain, humidity):
    """
    Args:
        temperature (float): Daily average temperature
        radiation (float): Daily average solar radiation
        rain (float): Average rainfall of the previous day
        humidity (float): Daily average relative humidity

    Returns:
        float: Returns the highest number of degree days to accumulate that complies with any of 
        the Dutch rules
    """
    if(rain>0):
        fuzzified_temperature = generate_fuzzified_dictionary('temp', temperature)
        fuzzified_radiation = generate_fuzzified_dictionary('solar_rad', radiation)
        fuzzified_rain = generate_fuzzified_dictionary('rain', rain)

        max_fuzzified_temperature = max(fuzzified_temperature, key = fuzzified_temperature.get)
        max_fuzzified_radiation = max(fuzzified_radiation, key = fuzzified_radiation.get)
        max_fuzzified_rain = max(fuzzified_rain, key = fuzzified_rain.get)

        ## IF temp != low AND solar_rad == low AND rain == low (yesterday) AND dew THEN 5.0
        if((max_fuzzified_temperature != 'low') and (max_fuzzified_radiation == 'low') and 
            (max_fuzzified_rain == 'low') and (calculate_dew_point(temperature, humidity))):
            return 5.0

        ## IF temp == low AND solar_rad == low AND rain == low (yesterday) AND dew THEN 2.5
        elif((max_fuzzified_temperature == 'low') and (max_fuzzified_radiation == 'low') and 
            (max_fuzzified_rain == 'low') and (calculate_dew_point(temperature, humidity))):
            return 2.5
        
        else:
            return 0.0
    
    else:
        return 0.0


def beaumont_rules(temperature, current_humidity, previous_humidity):
    """
    Args:
        temperature (float): Daily average temperature
        current_humidity (float): Daily average relative humidity
        previous_humidity (float): Average relative humidity of the previous day

    Returns:
        float: Returns the highest number of degree days to accumulate that complies with any of 
        the Beaumont rules
    """
    fuzzified_temperature = generate_fuzzified_dictionary('temp', temperature)
    fuzzified_current_humidity = generate_fuzzified_dictionary('humidity', current_humidity)
    fuzzified_previous_humidity = generate_fuzzified_dictionary('humidity', previous_humidity)

    max_fuzzified_temperature = max(fuzzified_temperature, key = fuzzified_temperature.get)
    max_fuzzified_current_humidity = max(fuzzified_current_humidity, key = fuzzified_current_humidity.get)
    max_fuzzified_previous_humidity = max(fuzzified_previous_humidity, key = fuzzified_previous_humidity.get)

    ## IF temp == high AND humidity == high (current) AND humidity == high (yesterday) THEN 5.0
    if((max_fuzzified_temperature == 'high') and (max_fuzzified_current_humidity == 'high') and 
        (max_fuzzified_previous_humidity == 'high')):
        return 5.0
    
    ## IF temp == medium AND humidity == high (current) AND humidity == high (yesterday) THEN 2.5
    elif((max_fuzzified_temperature == 'medium') and (max_fuzzified_current_humidity == 'high') and 
        (max_fuzzified_previous_humidity == 'high')):
        return 2.5

    ## IF temp == low AND humidity == high (current) AND humidity == high (yesterday) THEN 1.0
    elif((max_fuzzified_temperature == 'low') and (max_fuzzified_current_humidity == 'high') and 
        (max_fuzzified_previous_humidity == 'high')):
        return 1.0

    else:
        return 0.0


def irish_rules(temperature, humidity, wind):
    """
    Args:
        temperature (float): Daily average temperature
        humidity (float): Daily average relative humidity
        wind (float): Daily average wind

    Returns:
        float: Returns the highest number of degree days to accumulate that complies with any of 
        the Irish rules
    """
    fuzzified_temperature = generate_fuzzified_dictionary('temp', temperature)
    fuzzified_humidity = generate_fuzzified_dictionary('humidity', humidity)
    fuzzified_wind = generate_fuzzified_dictionary('wind', wind)

    max_fuzzified_temperature = max(fuzzified_temperature, key = fuzzified_temperature.get)
    max_fuzzified_humidity = max(fuzzified_humidity, key = fuzzified_humidity.get)
    max_fuzzified_wind = max(fuzzified_wind, key = fuzzified_wind.get)

    ## IF temp == high AND humidity == high AND wind == low AND dew THEN 5.0
    if((max_fuzzified_temperature == 'high') and (max_fuzzified_humidity == 'high') and 
        (max_fuzzified_wind == 'low') and (calculate_dew_point(temperature, humidity))):
        return 5.0

    ## IF temp == high AND humidity == high AND wind == medium AND dew THEN 2.5
    elif((max_fuzzified_temperature == 'high') and (max_fuzzified_humidity == 'high') and 
        (max_fuzzified_wind == 'medium') and (calculate_dew_point(temperature, humidity))):
        return 2.5

    ## IF temp == medium AND humidity == high AND wind == low AND dew THEN 2.5
    elif((max_fuzzified_temperature == 'medium') and (max_fuzzified_humidity == 'high') and 
        (max_fuzzified_wind == 'low') and (calculate_dew_point(temperature, humidity))):
        return 2.5

    ## IF temp == medium AND humidity == high AND wind == low AND dew THEN 1.0
    elif((max_fuzzified_temperature == 'medium') and (max_fuzzified_humidity == 'high') and 
        (max_fuzzified_wind == 'medium') and (calculate_dew_point(temperature, humidity))):
        return 1.0

    else:
        return 0.0
