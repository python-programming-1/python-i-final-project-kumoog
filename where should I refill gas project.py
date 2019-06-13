#!/usr/bin/env python
# coding: utf-8

# In[34]:


import pandas as pd
from glob import glob

glob('c:/data/oil/지역*.xls')


# In[62]:


sf = glob('c:/data/oil/지역*.xls')
sf


# In[36]:


tmp_raw = []
for file_name in sf:
    tmp = pd.read_excel(file_name, header=2)
    tmp_raw.append(tmp)
station_raw =pd.concat(tmp_raw)


# In[38]:


station_raw.head()


# In[39]:


stations = pd.DataFrame({'oil_store':station_raw['상호'],
                       '주소':station_raw['주소'],
                        '가격':station_raw['휘발유'],
                        '셀프':station_raw['셀프여부'],
                        '상표':station_raw['상표']
                       })
stations.head()


# In[40]:


stations['구'] = [eachAddress.split()[1] for eachAddress in stations['주소']]
stations.head()


# In[41]:


stations['구'].unique()


# In[43]:


stations = stations[stations['가격'] != '-']
stations.head()


# In[44]:


stations['가격'] =  [float(value) for value in stations['가격']]


# In[45]:


stations.reset_index(inplace=True)
del stations['index']


# In[46]:


stations.info()


# In[47]:


import json
import folium
import googlemaps
import warnings
warnings.simplefilter(action = "ignore", category = FutureWarning)


# In[48]:


stations.sort_values(by='가격', ascending=False).head(10)


# In[49]:


import numpy as np
gu_data = pd.pivot_table(stations, index= ['구'], values=["가격"], aggfunc=np.mean)
gu_data = gu_data.sort_values(by='가격', ascending=False)
gu_data


# In[50]:


brand_data = pd.pivot_table(stations, index= ['상표'], values=["가격"], aggfunc=np.mean)
brand_data = brand_data.sort_values(by='가격', ascending=False)
brand_data


# In[52]:


import json

geo_path = 'c:/data/oil/seoul.json'
geo_str = json.load(open(geo_path, encoding='utf-8'))

map = folium.Map(location=[37.5502, 126.982], zoom_start=10.5, 
                 tiles='Stamen Toner')

map.choropleth(geo_data = geo_str,
               data = gu_data,
               columns=[gu_data.index, '가격'],
               fill_color='PuRd', 
               key_on='feature.id')
map


# In[63]:


top100 = stations.sort_values(by='가격', ascending=False).head(100)
top100


# In[64]:


bottom100 = stations.sort_values(by='가격', ascending=True).head(100)
bottom100


# In[65]:


gmap_key = "AIzaSyBQUB65_qWJYy6YuIuZpTb3ysRbae9V2NQ"
gmaps = googlemaps.Client(key=gmap_key)


# In[73]:


from tqdm import tqdm_notebook
lat =[]
lng =[]

for n in tqdm_notebook(top100.index):
    try:
        tmp_add = str(top100['주소'][n]).split('(')[0]
        tmp_map = gmaps.geocode(tmp_add)
        
        tmp_loc = tmp_map[0].get('geometry')
        lat.append(tmp_loc['location']['lat'])
        lng.append(tmp_loc['location']['lng'])
        
    except:
        lat.append(np.nan)
        lng.append(np.nan)
  

top100['lat'] = lat
top100['lng'] = lng
top100


# In[67]:


lat =[]
lng =[]

for n in tqdm_notebook(bottom100.index):
    try:
        tmp_add = str(bottom100['주소'][n]).split('(')[0]
        tmp_map = gmaps.geocode(tmp_add)
        
        tmp_loc = tmp_map[0].get('geometry')
        lat.append(tmp_loc['location']['lat'])
        lng.append(tmp_loc['location']['lng'])
        
    except:
        lat.append(np.nan)
        lng.append(np.nan)
       
bottom100['lat'] = lat
bottom100['lng'] = lng
bottom100


# In[75]:


map = folium.Map(location=[37.5202, 126.975], zoom_start=10.5)

map.choropleth(geo_data = geo_str,
               data = gu_data,
               columns=[gu_data.index, '가격'],
               fill_color='PuRd', 
               key_on='feature.id')

for n in top100.index:
    if pd.notnull(top100['lat'][n], ):
        folium.Marker([top100['lat'][n], top100['lng'][n]],color='#3186cc', fill_color='#3186cc').add_to(map)
    

        
map


# In[60]:


map = folium.Map(location=[37.5202, 126.975], zoom_start=10.5)
map.choropleth(geo_data = geo_str,
               data = gu_data,
               columns=[gu_data.index, '가격'],
               fill_color='PuRd', 
               key_on='feature.id')

for n in bottom100.index:
    if pd.notnull(bottom100['lat'][n]): 
        folium.Marker([bottom100['lat'][n], 
        bottom100['lng'][n]]).add_to(map)
map


# In[ ]:




