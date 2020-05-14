#!/usr/bin/env python
# coding: utf-8

# # Web Scraper for Baseball Stats - WMT websites
# 
# ### Import Beautiful Soup Library and Parser

# In[1]:


from bs4 import BeautifulSoup

from lxml import html

import unicodedata

import requests
import re

import pandas as pd 

from pandas import Series, DataFrame


# ### Read in URL, parse the data and check that it's reading the type properly

# In[13]:


url = 'https://www.liberty.edu/wwwadmin/globals/templates/1912/docs/stats/baseteamcume31120.htm'

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

type(soup)


# 
# 
# ### Parse Data from the 'td' tags into a variabe

# In[15]:


all_stats = soup.find_all('td')

all_stats


# In[16]:


# Checking that 'all_stats' is a Result Set
type(all_stats)


# ### Get the text from inside all of the 'td' tags

# In[17]:


# Initialize an empty list that will house the text from inside the 'td' tags
stats=[]

# Loop through the 'all_stats', get the text, remove '\n' and append the text into the 'stats' list
for stat in all_stats:
    stats.append(stat.text.replace('\n', ' ').strip())

# Remove 'Overall Statistics' from the beginning of the list so the stats can eventually be broken up evenly
stats.pop(0)

# Verify 'stats' contains text
print(stats)


# In[18]:


# verify that 'stats' is a list
type(stats)


# In[19]:


# Remove both instances of the dash dividing line and put the stats into a new list
clean_stats = [ elem for elem in stats if elem != '----------']

print(clean_stats)


# ### Split stats list into a sublist containing player offensive stats only

# In[21]:


# Initialize a new list
# Iterate through the length of 'clean_stats' and place text into new lists of 24 items inside the 'chunks' list
# There are 24 columns for each baseball player including their name
chunks = [clean_stats[x:x+24] for x in range(0, len(clean_stats), 24)]

# Get the first list in chunks and put in into a new list for use as DataFrame column headers
offense_header = chunks[0]

# Slice out the lists for the players with ofensive stats and place into another list for use in a DataFrame
offensive_stats = chunks[1:17]

# Check that 'chunks' contains lists of text
#print(chunks)

# Check the 'offense header' list contains the correct text
#print(offense_header)

# Check that 'offensive stats' contains lists for each player needed. Adjust the range above if you're missing someone
print(offensive_stats)


# In[22]:


# Double checking that 'offensive_stats' is a list
type(offensive_stats)


# In[32]:


# Double checking that 'offensive_stats' is a list
type(offense_header)


# ### Find index of 'ERA' in order to know what index number to use to start spliting up the pitching stats

# In[23]:


# Get the index value of 'era'. Subtract 1 from the index value to find the start of the Pitching Stats table
clean_stats.index('era')


# ### Split stats list into a sublist containing player defensive stats only

# In[26]:


# Initialize a new list
# Iterate through the length of 'clean_stats' starting at index number before 'era'  place text into new lists
# The new lists should contain 23 items  are 23 baseball pitching stats 
pchunks = [clean_stats[x:x+23] for x in range(457, len(clean_stats), 23)]

pitching_header = pchunks[0]

pitching_stats = pchunks[1:14]

#print(pitching_header)

#print(pchunks)

print(pitching_stats)


#  

# ## Create a DataFrame with the columns

# In[27]:


df = pd.DataFrame(offensive_stats, columns=offense_header)

df


# ### Create new DataFrames to split columns containing 2 stats into 2 columns with 1 stat each

# In[28]:


tmp_df = df["gp-gs"].str.split("-", n=1, expand=True)
df["gp"]= tmp_df[0]
df["gs"]= tmp_df[1]

tmp_df2 = df["sb-att"].str.split("-", expand=True)
df["sb"] = tmp_df2[0]
df["att"] = tmp_df2[1]


df


# ### Delete any unneeded columns and rearrange the column order in a new DataFrame for exporting

# In[34]:


# Drop the columns from the Dataframe
new_df = df.drop(["gp-gs","sb-att", "a", "e", "fld%", "po", "tb","slg%","avg","ob%"], axis=1)

# Rearrange Dataframe column order
new_df = new_df[['Player','gp', 'gs', 'ab', 'r', 'h', '2b', '3b', 'hr', 'rbi','bb','hbp','so', 'gdp', 'sf', 'sh','sb','att']]

# Display new Dataframe
new_df


# # Export out the new DataFrame as a csv file
# ## Don't forget to double check the path and name

# In[30]:


new_df.to_csv('D:\From_HOME\Liberty_Baseball_Stats.csv',na_rep='Unknown')

