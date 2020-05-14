#!/usr/bin/env python
# coding: utf-8

# # Web Scraper Roster Data - WMT websites
# 
# ### Import Beautiful Soup Library and Parser

# In[ ]:


from bs4 import BeautifulSoup

from lxml import html

import requests
import re

import pandas as pd 

from pandas import Series, DataFrame


# ### Read in URL, parse the data and check that it's reading the type properly

# In[ ]:


url = 'https://clemsontigers.com/sports/mens-soccer/roster/'

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

type(soup)


# ### Parse inside the 'tbody' tag so we can iterate through it to scrape the roster data

# In[ ]:


team_roster = soup.find('tbody').find_all('tr')

#print(team_roster)

#type(team_roster)


# ### Get each player's jersey number and and put in a list for later use

# In[ ]:


jersey_numbers = []

for row in team_roster:
    cells = row.find_all('td')
    col_1 = cells[0].get_text()
    jersey_numbers.append(col_1)

print(jersey_numbers)


# ### Get each player's full name and and put in a list for latter use

# In[ ]:


names = []

for row in team_roster:
    cells = row.find_all('td')
    col_2 = cells[1].get_text()
    names.append(col_2)
    
print(names)    


# ### Get each player's position and and put in a list for latter use

# In[ ]:


positions = []

for row in team_roster:
    cells = row.find_all('td')
    col_3 = cells[2].get_text()
    positions.append(col_3)
    
print(positions)   


# ### If height is listed as ft-in this with get each player's height, convert it to ft'in" and put in a list for latter use

# In[ ]:


heights = []

for row in team_roster:
    cells = row.find_all('td')
    col_4 = cells[3].get_text()
    heights.append(col_4)
    
heights_ft = [word.replace('-', '\'') for word in heights]

heights_converted = [word + '\"' for word in heights_ft]
#print(heights)
#print(height_ft)
print(heights_converted)


# ### If height is listed as ft'in" this with get each player's height and put in a list for latter use

# In[ ]:


heights = []

for row in team_roster:
    cells = row.find_all('td')
    col_4 = cells[3].get_text()
    heights.append(col_4)
    
print(heights)


# In[ ]:





# ### Gets player's weight and puts it in a list for later use

# In[ ]:


weights = []

for row in team_roster:
    cells = row.find_all('td')
    col_5 = cells[4].get_text()
    weights.append(col_5)
    
print(weights)  


# ### If player's class year is only an abbreviation this gets the abbreviation, cleans it up and puts it in a list for later

# In[ ]:


years = []

for row in team_roster:
    cells = row.find_all('td')
    col_6 = cells[5].get_text()
    years.append(col_6)
    
class_abbrv = [word.replace('Fr.', 'FR').replace('Sr.', 'SR').replace('Jr.', 'JR').replace('So.', 'SO').replace('Gr.', 'GR') for word in years]

clean_class_abbrv = [word.replace('*', '') for word in class_abbrv]

#print(years)
#print(class_abbrv)
print(clean_class_abbrv)


# ### If player's class year is NOT an abbreviation this gets the class year, converts it an abbreviation, cleans it up and puts it in a list for later

# In[ ]:


full_years = []

for row in team_roster:
    cells = row.find_all('td')
    col_6 = cells[5].get_text()
    full_years.append(col_6)

# Converts the full length word to an abbreviation
class_abbrv = [word.replace('Freshman', 'FR').replace('Senior', 'SR').replace('Junior', 'JR').replace('Sophomore', 'SO').replace('Graduate', 'GR') for word in full_years]

# Removes 'RS' from class year. Comment out the line below to leave 'RS'
# new_class_abbrv = [word.replace('RS ', '') for word in class_abbrv]
new_class_abbrv = [word.replace('Redshirt ', '') for word in class_abbrv]
clean_class_abbrv = [word.replace('Redshirt-', '') for word in new_class_abbrv]

#print(full_years)
#print(new_class_abbrv)
print(clean_class_abbrv)


# ### Get player's hometown and add it to a list for later use

# In[ ]:


hometowns = []

for row in team_roster:
    cells = row.find_all('td')
    col_7 = cells[6].get_text()
    hometowns.append(col_7)
    
print(hometowns)


# ### Create a DataFrame with pandas, combine lists you want and label the columns

# In[ ]:


df = pd.DataFrame(list(zip(jersey_numbers, names, positions, clean_class_abbrv, heights, weights, hometowns)), 
               columns =['Jersey No.', 'Name', 'POS', 'Class', 'Height', 'Weight', 'Hometown'])

df


# ### Create new pandas DataFrames to split columns containing 2 elements into seperate columns and append to the orignal DataFrame

# In[ ]:


tmp_df = df["Hometown"].str.split(",", n=1, expand=True)
df["Town"]= tmp_df[0]
df["State"]= tmp_df[1]

#tmp_df2 = df["State"].str.split(" /", expand=True)
#df["State"] = tmp_df2[0]
#df["Highschool"] = tmp_df2[1]

tmp_df3 = df["Name"].str.split(" ", n=1, expand=True)
df["First Name"]= tmp_df3[0]
df["Last Name"]= tmp_df3[1]

df


# ### Create a new DataFrame for exporting. Drop unnecessary columns. Rearrange the new DataFrame 

# In[ ]:


# Drop the 'Hometown' and 'Name' columns from the Dataframe
new_df = df.drop(["Hometown","Name"], axis=1)

# Rearrange Dataframe column order
new_df = new_df[['Jersey No.', 'First Name', 'Last Name', 'POS', 'Class', 'Height', 'Weight', 'Town', 'State']]

# Display new Dataframe
new_df


# # Export the DataFrame.
# ## Double check the export path and name before running

# In[ ]:


new_df.to_csv('D:\From_HOME\CLEM_MSOC_Roster.csv',na_rep='Unknown')

