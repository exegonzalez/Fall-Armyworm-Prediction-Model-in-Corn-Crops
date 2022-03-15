from membership_functions import MEMBERSHIP_FUNCTIONS

def fuzzification(variable, label, value, functions=MEMBERSHIP_FUNCTIONS):
    """
    Args:
        variable (string): Variable for fuzzification
        label (string): Label for fuzzification
        value (float): Value to fuzzify
        functions (dict): Membership functions
    
    Returns: 
        float: Returns the probability of belonging to the category
    """
    if(variable in functions.keys()):
        if(label in functions[variable].keys()):
            scale, function = functions[variable][label].values()
            return function(scale, value)
    return None    


