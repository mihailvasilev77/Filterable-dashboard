from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import json

app = Flask(__name__, template_folder="templates")

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    df = pd.read_csv('raw_data.csv')


    column_options = df.columns.tolist()

    if request.method == 'POST':
        selected_column = request.form.get('column')  # Get the selected column from the dropdown
        selected_value = request.form.get('value')  # Get the value entered by the user

        if selected_column and selected_value:
            df = df[df[selected_column].astype(str) == selected_value]


    fig = px.bar(df, x = 'ACCOUNT_START_DATE', y = 'CNT_SUB')

    unique_values = {column: df[column].unique().tolist() for column in column_options}
    unique_values_json = json.dumps(unique_values)

    return render_template('index.html', plot=fig.to_html(full_html=False), column_options=column_options, unique_values=unique_values_json)

if __name__ == '__main__':
    app.run(debug=True)