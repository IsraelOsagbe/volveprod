# built in functions
# print()
# list()
# range()
# str()
# float()
# int()

# user defined functions

def calculate_sum(x, y, z=1):
    xyz = x + y + z
    return xyz
# get method / because you wil get a value from it
def x():
    return 10

# 1- python function will return None, if there is no return
# 2- Python will return None, if return is specified with no value
# 3- Python will not though an error, if you calll the function with out the ( )
value = calculate_sum(1, 2, 3)

print(value * 6)
print("function X is called - ", x() )

# 4-python functions accept other functions as inputs

value = calculate_sum(x(), 2, 3)
print("Function in function : ", value)

# 5-Calling a functino without specifiying paramtesr, is wrong, withh through an error
calculate_sum(2,3)

def print_df(data_frame):
    print(data_frame["Days"])
    return

import pandas as pd
df = pd.read_csv(r"C:\Users\Nashat\Desktop\PEA PYTHON 2023\Day 5 - 20230715\gasflow.txt",
                 sep="\t")

#6-Python function will through an erorr wheever the data type mismaches
#days = [1,2,3,4,5]
#print_df(days)
print("you type is : ", type([1,2,4,5]))























