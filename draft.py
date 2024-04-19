import pandas as pd
import streamlit as st
import datetime as dt

file_path = 'philosophers.csv'
data = pd.read_csv(file_path)
data['date'] = pd.to_datetime(data['date']).dt.date

# Title of the app
st.title('PHILOSOPHER POPULARITY')

# Selector de fecha de inicio
min_date = dt.date(2024, 1, 18)
max_date = dt.date(2024, 4, 18)
date_from = st.date_input("From", min_value=min_date, max_value=max_date, value=min_date)
# Selector de fecha de fin
date_to = st.date_input("To", min_value=min_date, max_value=max_date, value=max_date)

if date_to < date_from:
    st.error("The end date cannot be before the start date.")
else:
    st.success(f"Philosophers Popularity from {date_from} to {date_to}.")

period_select = data[(data['date'] >= date_from) & (data['date'] <= date_to)]

# Create a chart
st.line_chart(period_select, x='date', y=['Plato', 'Aristotle', 'Socrates'])

max_dates_scores = {}
for col in period_select.columns[1:]:  # Skip the 'Date' column
    max_idx = period_select[col].idxmax()
    max_date = period_select.loc[max_idx, 'date']
    max_score = period_select.loc[max_idx, col]
    max_dates_scores[col] = (max_date, max_score)

sidebar = st.sidebar.selectbox('Philosophers',('Socratres', 'Plato', 'Aristotle'))

print(max_dates_scores)

# Convertir el diccionario a DataFrame
ranking = pd.DataFrame(list(max_dates_scores.items()), columns=['Philosopher', 'Data'])
ranking[['Date', 'Score']] = pd.DataFrame(ranking['Data'].tolist(), index=ranking.index)
ranking.drop('Data', axis=1, inplace=True)

max_score = ranking['Score'].idxmax()
winner = ranking.loc[max_score]

st.title(f'The most popular philosopher for this period was: {winner["Philosopher"]}')

print(ranking)
st.write(ranking)

print(ranking.shape)
