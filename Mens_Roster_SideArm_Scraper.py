#!/usr/bin/env python
# coding: utf-8

# # Web Scraper for Roster Data from SideArm sites
# 
# ### Import Beautiful Soup Library and Parser

# In[ ]:


from bs4 import BeautifulSoup

import urllib
import urllib.request
import re

import pandas as pd 

from pandas import Series, DataFrame


# ### Read in URL

# In[ ]:


r = urllib.request.urlopen('https://goheels.com/sports/mens-lacrosse/roster').read()


# ### Check that it's reading the type properly

# In[ ]:


soup = BeautifulSoup(r, 'lxml')
type(soup)


# ### Get Player Jersey and add to DataFrame

# In[ ]:


# Create an empty list to contain scraped data
jersey_numbers = []

# Parse to specific tag and get ResultSet
jersey_number = soup.find_all('td', attrs=['class','roster_jerseynum'])

# Iterate through ResultSet, strip the text of '\n' and put in the empty list above
for jersey in jersey_number:
    jersey_numbers.append(jersey.text.replace('\n', ' ').strip())

# Print the new list to varify the contents    
print(jersey_numbers)


# ### Get Player Last Name

# In[ ]:


# Create an empty list to contain scraped data
last_names = []

# Parse to specific tag and get ResultSet
last_name = soup.find_all('span', attrs=['class','sidearm-roster-player-last-name'])

# Iterate through ResultSet, strip the text of '\n' and put in the empty list above
for name in last_name:
       last_names.append(name.text.replace('\n', ' ').strip())

# Print the new list to varify the contents    
print(last_names)


# ### Get Player First Name

# In[ ]:


# Create an empty list to contain scraped data
first_names = []

# Parse to specific tag and get ResultSet
first_name = soup.find_all('span', attrs=['class','sidearm-roster-player-first-name'])

# Iterate through ResultSet, strip the text of '\n' and put in the empty list above
for name in first_name:
       first_names.append(name.text.replace('\n', ' ').strip())
    
# Print the new list to varify the contents    
print(first_names)


# ### Get Player Height

# In[ ]:


heights = []

player_height = soup.find_all('span', attrs=['class','sidearm-roster-player-height'])

for height in player_height:
       heights.append(height.text.replace('\n', '').strip())

print(heights)


# ### Get Player Weight and strip whitespace and "lbs"

# In[ ]:


weights = []

player_weight = soup.find_all('td', attrs=['class','rp_weight'])

for weight in player_weight:
       weights.append(weight.text.replace('\n', ' ').strip())

print(weights)


# ### Get Player Year

# In[ ]:


years = []

player_year = soup.find_all('td', attrs=['class','roster_class'])

for year in player_year:
       years.append(year.text.replace('\n', ' ').strip())
        
class_abbrv = [word.replace('Fr.', 'FR').replace('Sr.', 'SR').replace('Jr.', 'JR').replace('So.', 'SO') for word in years]
   
print(class_abbrv)


# ### Get Player Hometown and State

# In[ ]:


hometowns = []

player_hometown = soup.find_all('td', attrs=['class','hometownhighschool'])

for hometown in player_hometown:
    hometowns.append(hometown.text.replace('\n', ' ').strip())

print(hometowns)


# ### Get Player Position

# In[ ]:


positions = []
player_position = soup.find_all('td', attrs=['class','rp_position_short'])
for pos in player_position:
    positions.append(pos.text.replace('\n', ' ').strip())
    
print(positions)


# ### Create a DataFrame with pandas, combine lists you want and label the columns

# In[ ]:


df = pd.DataFrame(list(zip(jersey_numbers, last_names, first_names, positions, heights, weights, class_abbrv, hometowns)), 
               columns =['Jersey No.', 'Last','First', 'POS', 'Height', 'Weight', 'Year', 'Hometown'])

df


# ### Create new pandas DataFrames to split columns containing 2 elements into seperate columns and append to the orignal DataFrame

# In[ ]:


tmp_df = df["Hometown"].str.split(",", n=1, expand=True)
df["Town"]= tmp_df[0]
df["State"]= tmp_df[1]

tmp_df2 = df["State"].str.split(" /", expand=True)
df["State"] = tmp_df2[0]
df["Highschool"] = tmp_df2[1]

df


# ### Create a new DataFrame for exporting. Drop unnecessary columns. Rearrange the new DataFrame 

# In[ ]:


# Drop the 'Hometown' and 'Highschool' columns from the Dataframe
new_df = df.drop(["Hometown","Highschool"], axis=1)

# Rearrange Dataframe column order if necessary
new_df = new_df[['Jersey No.', 'First', 'Last', 'POS', 'Year', 'Height', 'Weight', 'Town', 'State']]

new_df


# # Export the DataFrame.
# ## Double check the export path and name before running

# In[ ]:


new_df.to_csv(r'D:\From_HOME\UNC_MLAX_Roster_Test.csv',na_rep='Unknown')

