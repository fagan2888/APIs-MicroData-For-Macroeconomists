# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 15:16:16 2016

@author: mwaugh
"""
#%%

# This is an example of code that uses the API feature of the BEA. It defines
# a function that automatizes a bunch of stuff, the walks through several examples.
# The first example is GDP (from Spencer), the second example pulls the reginal
# data per capita income and population at the county level. This provides the
# the FIPS code which can then be merged with various other data sets...

# The guide: http://www.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf
# The place to find varible definitions:
    # http://www.bea.gov/API/bea_web_service_api_user_guide.htm

#%%

import pandas as pd
import requests

#%%

# So this is nice, Spencer wrote a funciton to work with this...

def bea_request(method, **kwargs):

    BEA_ID = "6BF79D8C-8042-4196-88DC-0E0C55B0C3B6"

# root url for bea API
    API_URL = "https://bea.gov/api/data"
    
# start constructing params dict
    params = dict(UserID=BEA_ID, method=method)
    
# bring in any additional keyword arguments to the dict
    params.update(kwargs)
        
# Make request
    r = requests.get(API_URL, params=params)
# This is going to give some "request type"
    return r
    
# **kwargs in that function. What this does is at the time the function is called,
# all extra parameters set by name are added to a dict called kwargs. The ** means
# that there can be many (A gap in my understanding)???

#%%
# Spencers example...
#gdp_data = bea_request("GetData", DataSetName="NIPA",
#                      TableId=6,
#                      Frequency="Q",
#                      Year=list(range(1990, 2017)))
## OK so what is going on here, it uses the method "Get Data", and then ceates
## a dictionary with the relavent informaiton....and then gdp_data is poped out.
## The key issue is that gdp_data is (what kind of type???) but more than jsut 
## a list. 
#
#gdp = pd.DataFrame(gdp_data.json()["BEAAPI"]["Results"]["Data"])
## Now this sets it up so that "BEAAPI" points it in the right place, results,
## and data. Actually, I have no idea what this is doing... This is just the structure,
## not sure why it is this way, but the first and secdon one are what they are..
## the later one is that there fare more fields like
#
## what happens here... gdp_data.json()["BEAAPI"]["Results"]["Notes"]
#
#print("The shape of gdp is", gdp.shape)
#gdp.head()

#%%

reg_data = bea_request("GetData", DataSetName="RegionalData",
                      KeyCode="PCPI_CI",
                      GeoFIPS = "County",
                      Year=list([2015]))

# This pulls the reginonal data, here per capita income (PCPI_CI) at the county
# level then the year. Note that the year can accept multiple entries...

reg_income = pd.DataFrame(reg_data.json()["BEAAPI"]["Results"]["Data"])

# Pull the data out for the json structure...and pop into a dataframe...

reg_income.DataValue = reg_income.DataValue.astype(float)

reg_income["State"]=reg_income.GeoFips.str.endswith("000")

# Now the data includes both state aggregates and the country level, want to drop
# the state aggregates, so take the fips codes that are state level

reg_income = reg_income.drop(reg_income[reg_income.State == True].index)

# Then drop them...

print("\n Average (across counties) of Income PC", reg_income.DataValue.mean())

# Then this is just s simple average across counties, about 40,000 per capita income
# which is in the ball park of what I would expect. 

#%%

# Same exact deal for the population at the county level

reg_data = bea_request("GetData", DataSetName="RegionalData",
                      KeyCode="POP_CI",
                      GeoFIPS = "County",
                      Year=list([2015]))

reg_pop = pd.DataFrame(reg_data.json()["BEAAPI"]["Results"]["Data"])

reg_pop.DataValue = reg_pop.DataValue.astype(float)

reg_pop["State"]=reg_pop.GeoFips.str.endswith("000")

reg_pop = reg_pop.drop(reg_pop[reg_pop.State == True].index)

print("\n Populaiton of US (BEA)", reg_pop.DataValue.sum())

# The 2014 is pretty close to the Census estimate off by 1mill on ~300mill base








