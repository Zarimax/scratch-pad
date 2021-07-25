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

def how_much_saved(n, r):
    monthly_salary = (annual_salary / 12)
    current_savings = 0
    months = 0
    for i in range(n):
        monthly_return = (current_savings * 0.04 / 12)
        current_savings += ((monthly_salary * r) + monthly_return)
        if months % 6 == 0  and months != 0:    
            monthly_salary = monthly_salary + (monthly_salary * semi_annual_raise)
        months += 1
    return(current_savings)

counter = 0
down_payment = (total_cost * 0.25)
high = 1
low = 0
target_time = target_time
guess = (high + low) / 2

while abs(down_payment - how_much_saved(target_time, guess)) >= 100: 
    if 1 - guess <= 0.001:
        print("Down payment cannot be saved in," +' ' + str(target_time), "months!")
        break
    elif how_much_saved(target_time, guess) > down_payment:   
        high = guess
    else:
        low = guess  
    guess = round(((high + low) / 2), 4)
    counter += 1

if how_much_saved(target_time, guess) >= down_payment:
    print(round(guess, 4))
    print(counter)
    