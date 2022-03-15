import csv
from lifecycles import PLAGUE, CROP
from fuzzy_rules import beaumont_rules, dutch_rules, irish_rules

lot_weather_data_2021 = csv.reader(open("./data batches/lot_weather_data_2021.csv", "r"))
lot_weather_data_2022 = csv.reader(open("./data batches/lot_weather_data_2022.csv", "r"))

def thermal_integral_corn(row, ddacc, crop_type='Maíz (Zea mays)'):
    """
    Args: 
        row (list): Weather data list
        ddacc (float): Accumulator degree days
        crop_type (string): Type of crop
    
    Returns:
        float, string: Calculate the thermal integral of corn
    """
    tbase = CROP[crop_type]['tbase']
    degree_day = ((float(row[1]) + float(row[2])) / 2) - tbase
    ddacc += degree_day if degree_day > 0 else 0 
    state = ''
    data = CROP[crop_type]['states']
    for i in range(len(data)):
        if(ddacc < data[i][0]):
            state = data[i-1][1]
            break
        elif(ddacc > data[-1][0]):
            state = data[-1][1]
            break
    return ddacc, state

def thermal_integral_fall_armyworm(row, previous_row, ddacc, plague_type='Gusano Cogollero (Spodoptera frugiperda)'):
    """
    Args:
        row (list): Current weather data lists
        previous_row (list): Previous day weather data list
        ddacc (float): Accumulator degree days
        plague_type (string): Type of plague
    
    Returns:
        float, string: Calculate the thermal integral of the fall armyworm 
    """
    tbase = PLAGUE[plague_type]['tbase']
    degree_day = ((float(row[1]) + float(row[2])) / 2) - tbase
    ddacc += degree_day if degree_day > 0 else 0

    # If Beaumont's rule is fulfilled, the degree days are accumulated
    # if(degree_day > 0):
    #     degree_day_beaumont = beaumont_rules(((float(row[1]) + float(row[2])) / 2), float(row[4]), float(previous_row[4]))
    #     if(degree_day_beaumont!=0):
    #         ddacc += degree_day_beaumont

    # If the Dutch rule is fulfilled, the degree days are accumulated
    # if(degree_day > 0):
    #     degree_day_dutch = dutch_rules(((float(row[1]) + float(row[2])) / 2), float(row[5]), float(previous_row[6]), float(row[4]))
    #     if(degree_day_dutch!=0):
    #         ddacc += degree_day_dutch

    # If the Irish rule is fulfilled, the degree days are accumulated
    # if(degree_day > 0):
    #     degree_day_irish = irish_rules(((float(row[1]) + float(row[2])) / 2), float(row[4]), float(row[3]))
    #     if(degree_day_irish!=0):
    #         ddacc += degree_day_irish

    # If the Dutch and Beaumont rules are fulfilled, the degree days are accumulated
    # if(degree_day > 0):
    #     degree_day_dutch = dutch_rules(((float(row[1]) + float(row[2])) / 2), float(row[5]), float(previous_row[6]), float(row[4]))
    #     degree_day_beaumont = beaumont_rules(((float(row[1]) + float(row[2])) / 2), float(row[4]), float(previous_row[4]))
    #     if(degree_day_dutch!=0 and degree_day_beaumont!=0):
    #         if(degree_day_dutch>degree_day_beaumont):
    #             ddacc += degree_day_dutch
    #         else: 
    #             ddacc += degree_day_beaumont
    #     elif(degree_day_dutch!=0):
    #         ddacc += degree_day_dutch
    #     elif(degree_day_beaumont!=0):
    #         ddacc += degree_day_beaumont

    # If the Irish and Beaumont rules are fulfilled, the degree days are accumulated
    # if(degree_day > 0):
    #     degree_day_irish = irish_rules(((float(row[1]) + float(row[2])) / 2), float(row[4]), float(row[3]))
    #     degree_day_beaumont = beaumont_rules(((float(row[1]) + float(row[2])) / 2), float(row[4]), float(previous_row[4]))
    #     if(degree_day_irish!=0 and degree_day_beaumont!=0):
    #         if(degree_day_irish>degree_day_beaumont):
    #             ddacc += degree_day_irish
    #         else: 
    #             ddacc += degree_day_beaumont
    #     elif(degree_day_irish!=0):
    #         ddacc += degree_day_irish
    #     elif(degree_day_beaumont!=0):
    #         ddacc += degree_day_beaumont

    # If the Dutch and Irish rules are fulfilled, the degree days are accumulated
    # if(degree_day > 0):
    #     degree_day_dutch = dutch_rules(((float(row[1]) + float(row[2])) / 2), float(row[5]), float(previous_row[6]), float(row[4]))
    #     degree_day_irish = irish_rules(((float(row[1]) + float(row[2])) / 2), float(row[4]), float(row[3]))
    #     if(degree_day_dutch!=0 and degree_day_irish!=0):
    #         if(degree_day_dutch>degree_day_irish):
    #             ddacc += degree_day_dutch
    #         else: 
    #             ddacc += degree_day_irish
    #     elif(degree_day_dutch!=0):
    #         ddacc += degree_day_dutch
    #     elif(degree_day_irish!=0):
    #         ddacc += degree_day_irish

    # If the Dutch, Irish and Beaumont rules are fulfilled, the degree days are accumulated
    if(degree_day > 0):
        degree_day_dutch = dutch_rules(((float(row[1]) + float(row[2])) / 2), float(row[5]), float(previous_row[6]), float(row[4]))
        degree_day_irish = irish_rules(((float(row[1]) + float(row[2])) / 2), float(row[4]), float(row[3]))
        degree_day_beaumont = beaumont_rules(((float(row[1]) + float(row[2])) / 2), float(row[4]), float(previous_row[4]))
        if(degree_day_dutch!=0 and degree_day_irish!=0 and degree_day_beaumont!=0):
            if(degree_day_dutch>degree_day_irish and degree_day_dutch>degree_day_beaumont):
                ddacc += degree_day_dutch
            elif(degree_day_beaumont>degree_day_irish and degree_day_beaumont>degree_day_dutch):
                ddacc += degree_day_beaumont
            else: 
                ddacc += degree_day_irish
        elif(degree_day_dutch==0):
            if(degree_day_beaumont>degree_day_irish):
                ddacc += degree_day_beaumont
            else: 
                ddacc += degree_day_irish
        elif(degree_day_irish==0):
            if(degree_day_beaumont>degree_day_dutch):
                ddacc += degree_day_beaumont
            else: 
                ddacc += degree_day_dutch
        elif(degree_day_beaumont==0):
            if(degree_day_irish>degree_day_dutch):
                ddacc += degree_day_irish
            else: 
                ddacc += degree_day_dutch      

    stage = ''
    data = PLAGUE[plague_type]['stages']
    for i in range(len(data)):
        if(ddacc < data[i][0]):
            stage = data[i-1][1]
            break
        elif(ddacc > data[-1][0]):     
            stage = data[-1][1]
            break
    return ddacc, stage

def change_state_corn(current_state, lot_weather_data, ac_degree_days=0):
    """
    Args:
        current_state (string): Current state
        lot_weather_data (csv reader): Weather data batch
        ac_degree_days (float): Accumulator degree days
    
    Returns:
        list: Returns the state changes of the corn
    """
    changes_states = []
    maxRad = 0
    minRad = 10
    acum = 0
    cont = 0
    for index, row in enumerate(lot_weather_data):
        if (index != 0):
            ac_degree_days, new_state = thermal_integral_corn(row, ac_degree_days)
            maxRad = float(row[5]) if float(row[5])>=maxRad else maxRad
            minRad = float(row[5]) if float(row[5])<=minRad else minRad
            acum += float(row[5])
            cont += 1
            if(new_state != current_state):
                changes_states.append({'date':row[0][0:10], 'msj':f"El cultivo ha pasado de estado: {current_state} -> {new_state}", 'degree_day': ac_degree_days})
            current_state = new_state
    print('maxRad: ', maxRad)
    print('minRad: ', minRad)
    print('acum: ', acum)
    print('cont: ', cont)
    print('tempMes: ', acum/cont)
    return changes_states

def change_stage_fall_armyworm(current_stage, lot_weather_data, ac_degree_days=0):
    """
    Args: 
        current_stage (string): Current state
        lot_weather_data (csv reader): Weather data batch
        ac_degree_days (float): Accumulator degree days
    
    Returns:
        list: Returns the stage changes of the fall armyworm
    """
    changes_stages = []
    previous_row = []
    for index, row in enumerate(lot_weather_data):
        if (index != 0):
            ac_degree_days, new_stage = thermal_integral_fall_armyworm(row, previous_row, ac_degree_days) if len(previous_row)!=0 else thermal_integral_fall_armyworm(row, row, ac_degree_days)
            if(new_stage != current_stage):
                changes_stages.append({'date':row[0][0:10], 'msj':f"La plaga ha pasado de etapa: {current_stage} -> {new_stage}", 'degree_day': ac_degree_days})
            current_stage = new_stage
            previous_row = row
    return changes_stages

# print(change_state_corn('Siembra', lot_weather_data_2022))
# print(change_stage_fall_armyworm('Huevo',lot_weather_data_2022))
