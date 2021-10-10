import csv
from lifecycles import PLAGUE, CROP

lot_one_wheater_data = csv.reader(open("./data batches/lot_one_weather_data_crop.csv", "r"))

def thermal_integral_corn(tmax, tmin, ddacc, crop_type='Maíz (Zea mays)'):
    """
    Calculate the thermal integral of corn

    tmax: Maximum daily temperature
    tmin: Minimum daily temperature
    ddacc: Accumulator degree days
    crop_type: Type of crop
    """
    
    tbase = CROP[crop_type]['tbase']
    degree_day = ((tmax + tmin) / 2) - tbase
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

def thermal_integral_fall_armyworm(tmax, tmin, ddacc, plague_type='Gusano Cogollero (Spodoptera frugiperda)'):
    """
    Calculate the thermal integral of the fall armyworm

    tmax: Maximum daily temperature
    tmin: Minimum daily temperature
    ddacc: Accumulator degree days
    plague_type: Type of plague
    """
    
    tbase = PLAGUE[plague_type]['tbase']
    degree_day = ((tmax + tmin) / 2) - tbase
    ddacc += degree_day if degree_day > 0 else 0 
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

def change_state_corn(current_state, ac_degree_days=0):
    """
    Returns the state changes of the corn

    current_state: Current state
    ac_degree_days: Accumulator degree days
    """
    changes_states = []
    for index, row in enumerate(lot_one_wheater_data):
        if (index != 0):
            ac_degree_days, new_state = thermal_integral_corn(float(row[1]), float(row[2]), ac_degree_days)
            if(new_state != current_state):
                changes_states.append({'date':row[0][0:10], 'msj':f"El cultivo ha pasado de estado: {current_state} -> {new_state}", 'degree_day': ac_degree_days})
            current_state = new_state
    return changes_states

def change_stage_fall_armyworm(current_stage, ac_degree_days=0):
    """
    Returns the stage changes of the fall armyworm

    current_stage: Current state
    ac_degree_days: Accumulator degree days
    """
    changes_stages = []
    for index, row in enumerate(lot_one_wheater_data):
        if (index != 0):
            ac_degree_days, new_stage = thermal_integral_fall_armyworm(float(row[1]), float(row[2]), ac_degree_days)
            if(new_stage != current_stage):
                changes_stages.append({'date':row[0][0:10], 'msj':f"La plaga ha pasado de etapa: {current_stage} -> {new_stage}", 'degree_day': ac_degree_days})
            current_stage = new_stage
    return changes_stages

# print(change_state_corn('Siembra'))
# print(change_stage_fall_armyworm('Huevo'))