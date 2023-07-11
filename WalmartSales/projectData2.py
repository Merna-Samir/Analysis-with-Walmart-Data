#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import pandas as pd
import seaborn as sns
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

walmart_data = pd.read_csv(r'walmart-sales-dataset-of-45stores.csv')
print(walmart_data.head())


# In[4]:


from datetime import datetime
walmart_data['Date']=pd.to_datetime(walmart_data['Date']);
walmart_data.dtypes


# In[5]:


#Making sure the data is clean
#Checking the possibility of data containing empty cells
print(walmart_data.dtypes)
cols = walmart_data.columns
walmart_data[cols].isnull().sum()


# In[6]:


#Checking the possibility of data containing duplicates
print(walmart_data.duplicated())


# In[7]:


# Print the shape of the data
print(walmart_data.shape)
print(walmart_data.info())
print(walmart_data.describe())


# In[8]:


#After ensuring data is correct, consistent and usable we can analyze it & visualize it savely


# In[9]:


#A. Which store has maximum sales?
#In order to find out the maximum sales, I will create a new variable called ‘total_sales’.
#Then group by stores and find the sum of the weekly sales of each store.
#This will give me the maximum sales. Store-20 has the maximum sales of $301,397,792.
total_sales = walmart_data.groupby('Store')['Weekly_Sales'].sum().round().sort_values(ascending=False)
pd.DataFrame(total_sales).head(1)


# In[10]:


#B. Which store has maximum standard deviation i.e., the sales vary a lot.
#To find out the maximum standard deviation, create a new variable and then group it by stores and find the standard deviation.
#Store-14 has a maximum standard deviation = $317,569.949.
walmart_data_std=walmart_data.groupby('Store')['Weekly_Sales'].std().round(3).sort_values(ascending=False)
pd.DataFrame(walmart_data_std).head(1)


# In[11]:


#C. Some holidays have a negative impact on sales.
#Find out holidays that have higher sales than the mean sales in the non-holiday season for all stores together.
#We have 4 Holiday Events,
#(1) Super Bowl: 12-Feb-10, 11-Feb-11, 10-Feb-12, 8-Feb-13,
#(2) Labour Day: 10-Sep-10, 9-Sep-11, 7-Sep-12, 6-Sep-13,
#(3) Thanksgiving: 26-Nov-10, 25-Nov-11, 23-Nov-12, 29-Nov-13,
#(4) Christmas: 31-Dec-10, 30-Dec-11, 28-Dec-12, 27-Dec-13.
#Now calculate the holiday event sales of each of the events and then find the non-holiday sales.
#I found that Thanksgiving has the highest sales ($1,471,273.43) than non-holiday sales ($1,041,256.38).
super_bowl=['12-2-2010','11-2-2011','10-2-2012']
labour_day=['10-9-2010','9-9-2011','7-9-2012']
thanksgiving=['26-11-2010','25-11-2011','23-11-2012']
christmas=['31-12-2010','30-12-2011','28-12-2012']
super_bowl_sales=walmart_data.loc[walmart_data.Date.isin(super_bowl)]['Weekly_Sales'].mean()
labour_day_sales=walmart_data.loc[walmart_data.Date.isin(labour_day)]['Weekly_Sales'].mean()
thanksgiving_sales=walmart_data.loc[walmart_data.Date.isin(thanksgiving)]['Weekly_Sales'].mean()
christmas_sales=walmart_data.loc[walmart_data.Date.isin(christmas)]['Weekly_Sales'].mean()
super_bowl_sales,labour_day_sales,thanksgiving_sales,christmas_sales


# In[12]:


non_holiday_sales= walmart_data[(walmart_data['Holiday_Flag']==0)]['Weekly_Sales'].mean()
non_holiday_sales


# In[13]:


conclusion=pd.DataFrame([{'Super Bowl Sales':super_bowl_sales,
 'Labour Day Sales':labour_day_sales,
'Thanksgiving Sales':thanksgiving_sales,
'Christmas Sales':christmas_sales,
'Non Holiday Sales':non_holiday_sales}]).T
conclusion


# In[14]:


df = pd.DataFrame(walmart_data)
df['Day'] = pd.DatetimeIndex(df['Date']).day
df['Month'] = pd.DatetimeIndex(df['Date']).month
df['Year'] = pd.DatetimeIndex(df['Date']).year
season ={12:'winter', 1:'winter' , 2:'winter',
         3:'Spring' , 4:'Spring' , 5:'Spring',
         6:'Summer' , 7:'Summer' , 8:'Summer',
         9:'Autumn' , 10:'Autumn', 11:'Autumn' 
        }

df


# In[15]:


df['season']= (df['Month']).map(season)
df


# # c) visualize quantitive variables distributions

# ## Line Hist

# In[16]:


#use subplot because help easy comparisons between plots.
#used line histograms are used to observe the distribution of each numerical column in this data
fig,axis=plt.subplots(nrows=2,ncols=3,figsize=(10,10))
ax =sns.distplot(df['Weekly_Sales'],kde=True ,ax = axis[0,0],color='purple')
ax =sns.distplot(df['Holiday_Flag'],kde=True ,ax = axis[0,1],color='purple')
ax =sns.distplot(df['Temperature'],kde=True ,ax = axis[0,2],color='purple')
ax =sns.distplot(df['Fuel_Price'],kde=True ,ax = axis[1,0],color='purple')
ax =sns.distplot(df['CPI'],kde=True ,ax = axis[1,1],color='purple')
ax =sns.distplot(df['Unemployment'],kde=True ,ax = axis[1,2],color='purple')


# ## Boxplot 

# In[17]:


#The box chart is used to show the range of the distribution, its central value, and its variability.
#display the out layer
fig,axis=plt.subplots(nrows=2,ncols=3, figsize=(10,10))
ax=df.boxplot('Weekly_Sales',ax=axis[0,0])
ax=df.boxplot('CPI',ax=axis[0,1])
ax=df.boxplot('Temperature',ax=axis[0,2])
ax=df.boxplot('Fuel_Price',ax=axis[1,0])
ax=df.boxplot('Unemployment',ax=axis[1,1])
ax=df.boxplot('Store',ax=axis[1,2])
plt.show()


# # d) Provide a monthly and semester view of sales in units and give insights.

# ## pie chart

# In[20]:


# used groupby to display the mean "Weekly_Sales" for "season" and "Month"
# used pie identify proportions of the different components
season = df.groupby("season")['Weekly_Sales'].mean().to_frame().reset_index()
month = df.groupby("Month")['Weekly_Sales'].mean().to_frame().reset_index()
plt.figure(figsize = (15,10))
plt.subplot(1,2,1)
plt.pie (season['Weekly_Sales'],labels =season['season'] ,autopct='%1.1f%%')
plt.title("Season")
plt.subplot(1,2,2)
plt.pie (month['Weekly_Sales'],labels =month["Month"] ,autopct='%1.1f%%')
plt.title("Month")
plt.show()


# 	The insights of question “d” is from the visualization between weekly sales , Month and visualization between weekly sales , Season we realize that month 12 and season winter has heightest mean of weekly sales
# 
# so we can increase holiday flags in this month to increase the weekly sales and do the same factors that help this month to has heightest mean of weekly sales to the stores that has low weekly sales

# ## Scatter

# In[21]:


#scatter used to identify relationships between two variables
# used where the dependent variable can have multiple values for a value of the independent variable.
fig, axes = plt.subplots(2,2, figsize=(10,8))
sns.scatterplot( y="Weekly_Sales",x="Fuel_Price",data=df, color= 'orange',  ax=axes[0,0])
sns.scatterplot( y="Weekly_Sales",x= "CPI",data=df,color = 'black', ax=axes[0, 1])
sns.scatterplot( y="Weekly_Sales",x= "Unemployment",data=df, color='green', ax=axes[1, 0])
sns.scatterplot( y="Weekly_Sales",x= "Temperature",data=df,   ax=axes[1, 1])
plt.show()


# the insights of question e is from the scatter visualization between Fuel_Price,Weekly_Sales we realize that when the intensity of fuel price increase the weekly sales go down and when the intensity of fuel price decrease the weekly sales increase so we know the the relation between weekly sales and fuel price is reverse
# 
# from the scatter visualization between Unemployment ,Weekly_Sales we realize that when the intensity of Unemployment increase the weekly sales go down and when the intensity of Unemployment decrease the weekly sales increase so we know the the relation between weekly sales and Unemployment is reverse
# 
# from this two relations we know that fuel price and unemployment impact negative on weekly salses so the stores that have high Unemployment and high fuel price have low weekly sales and we show that using barplots between store,Unemployment and store,fuel price
# 

# ## barplot

# In[22]:


new_data = df.groupby("Store")['Weekly_Sales'].sum().to_frame().reset_index()
new_data1 = df.groupby("Store")['Unemployment'].sum().to_frame().reset_index()
new_data2 = df.groupby("Store")['Fuel_Price'].sum().to_frame().reset_index()
plt.figure(figsize = (10,10))
plt.subplot(3,1,1)
sns.barplot( y="Weekly_Sales",x="Store",data=new_data )
plt.subplot(3,1,2)
sns.barplot( y='Unemployment',x= "Store",data=new_data1 )
plt.subplot(3,1,3)
sns.barplot( y='Fuel_Price',x= "Store",data=new_data2 , color = 'black')
plt.show() 


# form this chart we realize that store 20 has the maximum weekly sales
# 
# from this bar plot we realize that store 12,28,38 has maximum frequency of Unemployment
# 
# from this bar plot we realize that store 10,12,28,33,38,42 has maximum frequency of fuel price
# 

# We know from those people who have a store with a few weekly sales, like 12,28,38, that they have high unemployment and high fuel prices

# ## Grouped Column chart

# In[23]:


# We use this to compare weekly sales in each store during 3 years
Negative_Impact = pd.pivot_table(df,index="Store",columns="Year",values="Weekly_Sales",aggfunc=np.mean)
Negative_Impact.columns = [2010,2011,2012]
Negative_Impact.plot(kind="bar",figsize=(16,5),rot=360,width=0.9,colormap='viridis_r')
plt.show()


# from this relation we realize that the store number 14 in 2010 was the highest mean of sales , the store number 4 in 2011 & 2012 was the highest mean of sales

# In[24]:


# We use this to compare weekly sales in each store during 4 season
Negative_Impact2 = pd.pivot_table(df,index="Store",columns="season",values="Weekly_Sales",aggfunc=np.sum)
Negative_Impact2.columns = ["Winter",'Spring','Summer','Autumn']
Negative_Impact2.plot(kind="bar",figsize=(16,5),rot=360,width=0.9,colormap="turbo")
plt.show()


# from this relation we realize that the store number 20 in winter , spring ,Autumn was the highest sum of sales, the store number 4 and 20 in summer that total sales are approximating
# 

# In[ ]:





# In[ ]:





# In[ ]:




