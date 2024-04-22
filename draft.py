import pandas as pd
import streamlit as st
import datetime as dt

# Import data
file_path = "data_storage\philosophers.csv"
data = pd.read_csv(file_path)
data['date'] = pd.to_datetime(data['date'])
data['date'] = pd.to_datetime(data['date']).dt.date

# STREAMLIT WEB APP

# Title of the app
st.title('PHILOSOPHER POPULARITY')

# Description of the app
st.write('Explore the historical popularity of Socrates, Plato, and Aristotle using Google Trends data.'
        'This app visualizes how interest in these key philosophers has changed over time in the United States. ')

# Selection of time period
min_date = dt.date(2024, 1, 18)
max_date = dt.date(2024, 4, 18)
date_from = st.date_input("From", min_value=min_date, max_value=max_date, value=min_date)
date_to = st.date_input("To", min_value=min_date, max_value=max_date, value=max_date)
if date_to < date_from:
    st.error("The end date cannot be before the start date.")
else:
    st.success(f"Philosophers Popularity from {date_from} to {date_to}.")
period_select = data[(data['date'] >= date_from) & (data['date'] <= date_to)]

# Create a line chart
st.line_chart(period_select, x='date', y=['Plato', 'Aristotle', 'Socrates'])

# Most popular philosopher
total_interest = period_select.drop('date', axis=1).sum()
winner = total_interest.idxmax()
# Web
st.subheader(f'The most popular philosopher of the period was: {winner}')
image_path = f"data_storage/{winner}.jpg"
st.image(image_path, width=300)
st.bar_chart(total_interest)

# Analysis by day of the week
period_select['date'] = pd.to_datetime(period_select['date'])
period_select['day_week'] = period_select['date'].dt.day_name()
result = period_select.drop('date', axis=1).groupby('day_week').sum()
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
result['day_week'] = pd.Categorical(result.index, categories=days_order, ordered=True)
result = result.set_index('day_week')
sorted_result = result.sort_index()

# Web
st.subheader(f"The best day of the week for him was: {sorted_result['Plato'].idxmax()}")
st.bar_chart(sorted_result['Plato'])

# General data analysis
period_select['date'] = pd.to_datetime(period_select['date']).dt.date
general_analysis = {}
for col in period_select.columns[1:4]:  # Skip the 'Date' column
    max_idx = period_select[col].idxmax()
    max_date = period_select.loc[max_idx, 'date']
    max_interest = period_select.loc[max_idx, col]
    min_idx = period_select[col].idxmin()
    min_date = period_select.loc[min_idx, 'date']
    min_interest = period_select.loc[min_idx, col]
    sum_interest = period_select[col].sum()
    general_analysis[col] = (max_date, max_interest, min_date, min_interest, sum_interest)

ranking = pd.DataFrame(list(general_analysis.items()), columns=['Philosopher', 'Data'])
ranking[['Best Day', 'Interest', 'Worst Day', 'Worst Interest', 'Total Interest']] = pd.DataFrame(ranking['Data'].tolist(), index=ranking.index)
ranking.drop('Data', axis=1, inplace=True)

st.write(ranking)
