#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from datetime import datetime, timedelta

# Load the CSV file into a DataFrame
file_path = r'C:\Users\HP\Desktop\Assignment_Timecard.xlsx - Sheet1.csv'
df = pd.read_csv(file_path)

# Define a function to parse the time duration in HH:MM format
def parse_duration(duration_str):
    hours, minutes = map(int, duration_str.split(':'))
    return timedelta(hours=hours, minutes=minutes)

# Initialize variables to store relevant information
consecutive_days_employees = []
short_break_employees = []
long_shift_employees = []

# Modify these column names based on your CSV file's headers
employee_name_col = 'Employee Name'
start_time_col = 'Time'
end_time_col = 'Time Out'
shift_duration_col = 'Timecard Hours (as Time)'

# Iterate through the DataFrame rows
for index, row in df.iterrows():
    try:
        start_time = datetime.strptime(str(row[start_time_col]), '%m/%d/%Y %I:%M %p')
        end_time = datetime.strptime(str(row[end_time_col]), '%m/%d/%Y %I:%M %p')
    except (ValueError, TypeError):
        # Handle invalid or missing date-time values here (e.g., print an error message)
        continue  # Skip this row and proceed to the next

    # Check for consecutive days
    if index > 0:
        prev_row = df.iloc[index - 1]
        try:
            prev_end_time = datetime.strptime(str(prev_row[end_time_col]), '%m/%d/%Y %I:%M %p')
        except (ValueError, TypeError):
            # Handle invalid or missing date-time values here (e.g., print an error message)
            continue  # Skip this row and proceed to the next

        time_difference = (start_time - prev_end_time).total_seconds() / 3600  # in hours
        if time_difference == 24:
            consecutive_days_employees.append(row[employee_name_col])

    # Check for short breaks
    time_difference = (start_time - end_time).total_seconds() / 3600  # in hours
    if 1 < time_difference < 10:
        short_break_employees.append(row[employee_name_col])

    # Check for long shifts
    shift_duration = parse_duration(row[shift_duration_col])
    if shift_duration.total_seconds() > 14 * 3600:  # 14 hours in seconds
        long_shift_employees.append(row[employee_name_col])

# Print the results
print("Employees who worked for 7 consecutive days:")
print(consecutive_days_employees)

print("\nEmployees with less than 10 hours between shifts but greater than 1 hour:")
print(short_break_employees)

print("\nEmployees who worked for more than 14 hours in a single shift:")
print(long_shift_employees)


# In[ ]:




