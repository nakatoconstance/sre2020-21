# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 07:32:10 2021

@author: je
"""

import pandas as pd 
    
# List1 
Name = ['tom', 'krish', 'nick', 'juli'] 
sName = ['mugerwa', 'kasule', 'kayemba', 'juli'] 
# List2 
Age = [25, 30, 26, 22] 
    
# get the list of tuples from two lists. 
# and merge them by using zip(). 
list_of_tuples = list(zip(Name, Age,sName)) 
    
# Assign data to tuples. 
list_of_tuples  
  
  
# Converting lists of tuples into 
# pandas Dataframe. 
df = pd.DataFrame(list_of_tuples,
                  columns = ['Name', 'Age' ,'second Name' ]) 
     
# Print data. 
print(df)