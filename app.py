from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px

app = Flask(__name__, template_folder="templates")

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    df = pd.read_csv('raw_data.csv')

    dropdown_options = df['year'].unique()

    if request.method == 'POST':
        selected_value = request.form.get('dropdown')

        if selected_value and selected_value != 'All':
            df = df[df['year'].astype(str) == selected_value]


    fig = px.bar(df, x = 'ACCOUNT_START_DATE', y = 'CNT_SUB')

    return render_template('index.html', plot=fig.to_html(full_html=False), dropdown_options=dropdown_options)

if __name__ == '__main__':
    app.run(debug=True)