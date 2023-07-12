from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px

app = Flask(__name__, template_folder="templates")

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        selected_columns = request.form.getlist('columns')

        df = pd.read_csv('raw_data.csv')

        fig = px.bar(df, x = 'ACCOUNT_START_DATE', y = 'CNT_SUB')

        return render_template('index.html', plot=fig.to_html(full_html=False), columns=df.columns)

    return render_template('index.html', columns=[])

if __name__ == '__main__':
    app.run(debug=True)