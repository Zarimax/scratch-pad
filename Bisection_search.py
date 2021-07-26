# define a function to get input from the user and validate it by casting it to a specified class_type. any
# exceptions which are thrown from the casting will be raised to the caller
def get_input(prompt_string, class_type):
    try:
        input_value = class_type(input(prompt_string))
    except ValueError as e:
        print(f"**FAILED** to convert input to int for prompt '{prompt_string}'")
        raise e
    # the cast to class_type was successful - return the value
    return input_value

# define a dictionary of static parameters to be used by the program. these values can optionally be overwritten
# by the user providing actual input
input_dict = {
    "annual_salary": 150000,
    "target_time": 36,
    "total_cost": 1000000,
    "semi_annual_raise": 0.07,
}

# uncomment these lines to gather actual input from the user
"""
input_dict["annual_salary"] = get_input("Enter your salary as an integer: ", int)
input_dict["target_time"] = get_input("How many months do you want to save for: ", int)
input_dict["total_cost"] = get_input("Enter the cost of your dream home: ", int)
input_dict["semi_annual_raise"] = get_input("Enter your semi_annual raise: ", float)
"""

# this is a crude visual calendar of each month and the order of tasks that can occur
"""
Year 1:
|------------IP|------------IP|------------IP|------------IP|------------IP|------------IP|R
|------------IP|------------IP|------------IP|------------IP|------------IP|------------IP|R
Year 2:
|------------IP|------------IP|------------IP|------------IP|------------IP|------------IP|R
|------------IP|------------IP|------------IP|------------IP|------------IP|------------IP|R
Year 3:
|------------IP|------------IP|------------IP|------------IP|------------IP|------------IP|R
|------------IP|------------IP|------------IP|------------IP|------------IP|------------IP|R

P - Paid
R - Raises
I - Interest
"""

# this function calculates how much is saved over a period of n months given a
#  rate of saving, r, e.g. 36 months with a 0.07 monthly saving rate
def how_much_saved(target_time, guess, annual_salary, semi_annual_raise): 
    monthly_salary = (annual_salary / 12)
    current_savings = 0
    # this increments current_savings a number of times equal to the target time input
    for months in range(1, target_time + 1):
        # calculate interest
        monthly_return = (current_savings * 0.04 / 12)
        # add salary and interest to savings
        current_savings += ((monthly_salary * guess) + monthly_return)
        if months % 6 == 0: # the raise is applied after every 6th month  
            monthly_salary += (monthly_salary * semi_annual_raise)
    return(current_savings)

counter = 0
down_payment = (input_dict["total_cost"] * 0.25)
high = 1 # represents a savings rate of 100%
low = 0 # and a savings rate of 0%
guess = (high + low) / 2 # we start with a guess in the middle at 50% and optimize up or down from there

# we search until we have a monthly saving rate that is within plus-or-minus $50 of the down payment 
while True:
    saved_amount = how_much_saved(input_dict["target_time"], 
                                  guess, 
                                  input_dict["annual_salary"], 
                                  input_dict["semi_annual_raise"])

    if abs(down_payment - saved_amount) <= 50:
        break

    if 1 - guess <= 0.001: # if the guess gets too close to 100% of savings, we stop the search
        print("Down payment cannot be saved in %s months!" % str(input_dict["target_time"]))
        break
    elif saved_amount > down_payment:
        # the guess is too high, so we narrow the search space to the midpoint between our current guess and low   
        high = guess
    else:
        # likewise if the guess is too low
        low = guess  
    # it turns out we get the same answer whether we round here or not, so the rounding is extraneous
    guess = round(((high + low) / 2), 4) 
    counter += 1

print(round(guess, 4))  # resolves to 0.4411 with default inputs
print(counter)  # resolves to 12 with default inputs

    
