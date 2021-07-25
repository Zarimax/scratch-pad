try: 
    
    annual_salary = int(input("Enter your salary as an integer: "))
    target_time = int(input("How many months do you want to save for: "))
    total_cost = int(input("Enter the cost of your dream home: "))
    semi_annual_raise = float(input("Enter your semi_annual raise: "))

except ValueError: 
    print("Salary should be an integer!")
except ValueError:
    print("Target time should be an integer!")
except ValueError:
    print("Cost should be an integer!")
except ValueError:
    print("Raise should be a float!")

def how_much_saved(n, r): #this function calculates how much is saved over a period of n months given a rate of saving, r, e.g. 36 months with a 0.07 monthly saving rate
    monthly_salary = (annual_salary / 12)
    current_savings = 0
    months = 0 #changing this value to 1 causes the program to output nothing at all
    for i in range(n): #this increments current_savings a number of times equal to the target time input
        monthly_return = (current_savings * 0.04 / 12)
        current_savings += ((monthly_salary * r) + monthly_return)
        if months % 6 == 0 and months != 0: #the raise is applied every 6 months   
            monthly_salary = monthly_salary + (monthly_salary * semi_annual_raise)
        months += 1
    return(current_savings)

counter = 0
down_payment = (total_cost * 0.25)
high = 1 #represents a savings rate of 100%
low = 0 #and a savings rate of 0%
target_time = target_time #
guess = (high + low) / 2 #we start with a guess in the middle

while abs(down_payment - how_much_saved(target_time, guess)) >= 100: #we search until we have a monthly saving rate that is within 100 
    if 1 - guess <= 0.001: #if the guess gets too close to 1 we stop the search
        print("Down payment cannot be saved in," +' ' + str(target_time), "months!")
        break
    elif how_much_saved(target_time, guess) > down_payment: #the guess is too high, so we narrow the search space to the midpoint between our current guess and low   
        high = guess
    else: #likewise if the guess is too low
        low = guess  
    guess = round(((high + low) / 2), 4) #it turns out we get the same answer whether we round here or not, so the rounding is extraneous
    counter += 1

#if how_much_saved(target_time, guess) >= down_payment:
#I realised this if condition was extraneous; when I removed it the whole program runs even with months = 1 in the function definition 
#but the answer is still slightly too high although it LESS too high. 
#I don't understand how the value of month in the function def makes any differnece to that if condition

print(round(guess, 4))
print(counter)
    
