"""
Analyzing COVID Spread
This focuses on modelling the spread of COVID-19 using data from Center for Systems Science and Engineering (CSSE) at Johns Hopkins University. 
"""

"""
Loading Data
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (10,3) # make figures larger

# Load the most recent data directly from GitHub 
base_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/" # loading from Internet
infected_dataset_url = base_url + "time_series_covid19_confirmed_global.csv"
recovered_dataset_url = base_url + "time_series_covid19_recovered_global.csv"
deaths_dataset_url = base_url + "time_series_covid19_deaths_global.csv"
countries_dataset_url = base_url + "../UID_ISO_FIPS_LookUp_Table.csv"

# Load the data for infected individuals, number of recovered, and number of deaths
infected = pd.read_csv(infected_dataset_url)
recovered = pd.read_csv(recovered_dataset_url)
deaths = pd.read_csv(deaths_dataset_url)

# See how the data looks like
infected.head()
recovered.head()
deaths.head()

# Closer look at the Province/State column
infected['Province/State'].value_counts()

# Closer look the data from China
infected[infected['Country/Region']=='China']

"""
Pre-processing the Data
"""
# Group all the data by country
infected = infected.groupby('Country/Region').sum()
recovered = recovered.groupby('Country/Region').sum()
deaths = deaths.groupby('Country/Region').sum()

infected.head()

# The DataFrames are now indexed by Country/Region and can now access the data for a specific country 
infected.loc['US'][2:].plot()
recovered.loc['US'][2:].plot()
plt.show()

infected.drop(columns=['Lat','Long'],inplace=True)
recovered.drop(columns=['Lat','Long'],inplace=True)
deaths.drop(columns=['Lat','Long'],inplace=True)

"""
Investigating the Data
"""
# Creating a frame that contains the data on infections indexed by date
def mkframe(country):
    df = pd.DataFrame({ 'infected' : infected.loc[country] ,
                        'recovered' : recovered.loc[country],
                        'deaths' : deaths.loc[country]})
    df.index = pd.to_datetime(df.index)
    return df

df = mkframe('US')
df

df.plot()
plt.show()

# Computing the number of new infections each day to see the speed at which pandemic progresses
df['ninfected'] = df['infected'].diff()
df['ninfected'].plot()
plt.show()

# Closer look at a specific month
df[(df.index.year==2020) & (df.index.month==7)]['ninfected'].plot()
plt.show()

# It looks like there are weekly fluctuations in data. To be able to see the trends it makes sense to smooth out the curve by computing running average
df['ninfav'] = df['ninfected'].rolling(window=7).mean()
df['ninfav'].plot()
plt.show()

# In order to be able to compare several countries, we might want to take the country's population into account, and compare the percentage of infected individuals with respect to country's population.
countries = pd.read_csv(countries_dataset_url)
countries

countries[(countries['Country_Region']=='US') & countries['Province_State'].isna()]

pop = countries[(countries['Country_Region']=='US') & countries['Province_State'].isna()]['Population'].iloc[0]
df['pinfected'] = df['infected']*100 / pop
df['pinfected'].plot(figsize=(10,3))
plt.show()

"""
Computing R_t
"""
# Looking at basic reproduction number R_0 to see how infectious the disease is by indicating the number of people that an infected person would further infect
# To compute R_t using this data take a rolling window of 8 ninfected values
df['Rt'] = df['ninfected'].rolling(8).apply(lambda x: x[4:].sum()/x[:4].sum())
df['Rt'].plot()
plt.show()

# To make the graph nicer fill values using replace and fillna function
ax = df[df.index<"2020-05-01"]['Rt'].replace(np.inf,np.nan).fillna(method='pad').plot(figsize=(10,3))
ax.set_ylim([0,6])
ax.axhline(1,linestyle='--',color='red')
plt.show()

# Looking at the daily difference in new cases to see clearly when pandemic is increasing or declining
df['ninfected'].diff().plot()
plt.show()

# Since there are data fluctuations caused by reporting it makes sense to smooth the curve by running rolling average to get the overall picture and focus on the first months of the pandemic
ax=df[df.index<"2020-06-01"]['ninfected'].diff().rolling(7).mean().plot()
ax.axhline(0,linestyle='-.',color='red')
plt.show()
