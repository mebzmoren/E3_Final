import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style and color palette
sns.set_style('whitegrid')
sns.set_palette('viridis')

# Set page title
st.set_page_config(page_title = 'London Bike-Share Usage Analysis', layout = 'wide')

# Add a title
st.title('London Bike-Share Usage Analysis')

# Load the dataset
csv_file = "LondonBikeJourneyAug2023.csv"
df = pd.read_csv(csv_file)

# Convert 'Start date' and 'End date' columns to datetime
df['Start date'] = pd.to_datetime(df['Start date'], format = '%m/%d/%Y %H:%M')
df['End date'] = pd.to_datetime(df['End date'], format = '%m/%d/%Y %H:%M')

# Calculate the total duration in minutes
df['Total duration (mins)'] = df['Total duration (ms)'] / 60000

# Sidebar filters
st.sidebar.subheader('Filters')
bike_model = st.sidebar.multiselect('Bike Model', df['Bike model'].unique())
start_station = st.sidebar.multiselect('Start Station', df['Start station'].unique())
end_station = st.sidebar.multiselect('End Station', df['End station'].unique())
start_date_range = st.sidebar.date_input('Start Date Range', [df['Start date'].min().date(), df['Start date'].max().date()], min_value=df['Start date'].min().date(), max_value=df['Start date'].max().date())

# Apply filters
filtered_df = df.copy()
if bike_model:
    filtered_df = filtered_df[filtered_df['Bike model'].isin(bike_model)]
if start_station and end_station:
    filtered_df = filtered_df[(filtered_df['Start station'].isin(start_station)) & (filtered_df['End station'].isin(end_station))]
    if filtered_df.empty:
        st.error("No trips found for the selected combination of start and end stations.")
        st.stop()
elif start_station:
    filtered_df = filtered_df[filtered_df['Start station'].isin(start_station)]
elif end_station:
    filtered_df = filtered_df[filtered_df['End station'].isin(end_station)]
filtered_df = filtered_df[(filtered_df['Start date'].dt.date >= start_date_range[0]) & (filtered_df['Start date'].dt.date <= start_date_range[1])]

# Top Row
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label = 'Total Trips', value = len(filtered_df))

with col2:
    st.metric(label = 'Average Trip Duration (mins)', value = round(filtered_df['Total duration (mins)'].mean(), 2))

with col3:
    st.metric(label = 'Total Bike Models', value = filtered_df['Bike model'].nunique())

st.markdown('---')

# Data Display
st.subheader('Filtered Data')
st.write(filtered_df.head(10))

st.markdown('---')

# Second Row
col1, col2 = st.columns(2)

with col1:
    st.subheader('Bike Usage Duration over Time')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='Start date', y='Total duration (mins)', data = filtered_df, ax=ax)
    plt.title('Bike Usage Duration over Time', fontsize=16)
    plt.xlabel('Start Date', fontsize = 14)
    plt.ylabel('Total Duration (mins)', fontsize = 14)
    plt.xticks(rotation = 45, fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.grid(True, linestyle = '--', alpha = 0.7)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader('Top 10 Start Stations')
    top_start_stations = filtered_df['Start station'].value_counts().head(10)
    fig, ax = plt.subplots(figsize = (10, 6))
    sns.barplot(x = top_start_stations.values, y = top_start_stations.index, ax = ax)
    plt.title('Top 10 Start Stations', fontsize = 16)
    plt.xlabel('Number of Trips', fontsize = 14)
    plt.ylabel('Start Station', fontsize = 14)
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.grid(True, linestyle = '--', alpha = 0.7)
    plt.tight_layout()
    st.pyplot(fig)

st.markdown('---')

# Third Row
col1, col2 = st.columns(2)

with col1:
    st.subheader('Bike Model Usage')
    fig, ax = plt.subplots(figsize = (10, 6))
    sns.countplot(y = 'Bike model', data = filtered_df, ax = ax)
    plt.xlabel('Count', fontweight = 'bold')
    plt.ylabel('Bike Model', fontweight = 'bold')
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader('Daily Bike Rental Demands')
    daily_trips = filtered_df.groupby(filtered_df['Start date'].dt.date).size().reset_index()
    daily_trips.columns = ['Date', 'Number of Trips']
    fig, ax = plt.subplots(figsize = (10, 6))
    sns.lineplot(x = 'Date', y = 'Number of Trips', data = daily_trips, ax = ax)
    plt.xlabel('Date', fontweight = 'bold')
    plt.ylabel('Number of Trips', fontweight = 'bold')
    plt.xticks(rotation = 45)
    plt.tight_layout()
    st.pyplot(fig)

st.markdown('---')

# Fourth Row
col1, col2 = st.columns(2)

with col1:
    st.subheader('Bike Rentals by Day of the Week')
    filtered_df['Start Day'] = pd.Categorical(filtered_df['Start date'].dt.day_name(), categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered = True)
    rentals_by_day = filtered_df['Start Day'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x = rentals_by_day.values, y = rentals_by_day.index, ax = ax, order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    plt.title('Bike Rentals by Day of the Week', fontsize = 16)
    plt.xlabel('Number of Trips', fontsize = 14)
    plt.ylabel('Day of the Week', fontsize = 14)
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.grid(True, linestyle = '--', alpha = 0.7)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader('Bike Rentals by Hour of the Day')
    filtered_df['Start Hour'] = filtered_df['Start date'].dt.hour
    filtered_df['Start Day'] = pd.Categorical(filtered_df['Start date'].dt.day_name(), categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered = True)
    rentals_by_hour = filtered_df.groupby(['Start Day', 'Start Hour']).size().unstack()
    rentals_by_hour = rentals_by_hour.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(rentals_by_hour, cmap = 'Purples', annot = True, fmt = 'd', cbar_kws = {'label': 'Number of Trips'})
    plt.title('Bike Rentals by Hour and Day of the Week', fontsize = 16)
    plt.xlabel('Hour of the Day', fontsize = 14)
    plt.ylabel('Day of the Week', fontsize = 14)
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12, rotation = 0)
    plt.tight_layout()
    st.pyplot(fig)