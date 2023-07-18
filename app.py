from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import json

app = Flask(__name__, template_folder="templates")

df = pd.read_csv('raw_data.csv')

@app.route('/', methods=['GET', 'POST'])
def dashboard():

    if request.method == 'POST':
        selected_segment = request.form.get('segment')
        selected_price_plan = request.form.get('price_plan')
        selected_discounted_mf = request.form.get('discounted_mf')
        selected_admin_center = request.form.get('admin_center')

        filtered_df = df.copy()

        if selected_segment and selected_segment != 'All':
            filtered_df = filtered_df[filtered_df['SEGMENT_NAME'] == selected_segment]

        if selected_price_plan and selected_price_plan != 'All':
            filtered_df = filtered_df[filtered_df['PRICE_PLAN_DESC'] == selected_price_plan]

        if selected_discounted_mf and selected_discounted_mf != 'All':
            filtered_df = filtered_df[filtered_df['DISCOUNTED_MF_W_VAT'] == float(selected_discounted_mf)]
        
        if selected_admin_center and selected_admin_center != 'All':
            filtered_df = filtered_df[filtered_df['ADMIN_CENTER'] == selected_admin_center]

        fig1 = px.bar(filtered_df, x='ACCOUNT_START_DATE', y='CNT_SUB', title="FWA Activations")
        fig2 = px.pie(filtered_df, names='PRICE_PLAN_DESC', title='FWA Activations')

    else:
        fig1 = px.bar(df, x='ACCOUNT_START_DATE', y='CNT_SUB', title="FWA Activations")
        fig2 = px.pie(df, names='PRICE_PLAN_DESC', title='FWA Activations')

    fig2.update_layout(legend_title_text='Price plans:')

    segment_options = ['All'] + df['SEGMENT_NAME'].unique().tolist()
    price_plan_options = ['All'] + df['PRICE_PLAN_DESC'].unique().tolist()
    discounted_mf_options = ['All'] + df['DISCOUNTED_MF_W_VAT'].astype(str).unique().tolist()
    admin_center_options = ['All'] + df['ADMIN_CENTER'].unique().tolist()

    return render_template('index.html', fig1=fig1.to_html(full_html=False), fig2=fig2.to_html(full_html=False), segment_options=segment_options, price_plan_options=price_plan_options, discounted_mf_options=discounted_mf_options, admin_center_options=admin_center_options)

@app.route('/get_price_plans', methods=['POST'])
def get_price_plans():
    segment = request.form.get('segment')

    df = pd.read_csv('raw_data.csv')
    
    if segment and segment != 'All':
        df = df[df['SEGMENT_NAME'] == segment]

    price_plan_options = ['All'] + df['PRICE_PLAN_DESC'].unique().tolist()

    return json.dumps(price_plan_options)

@app.route('/get_discounted_mf', methods=['POST'])
def get_discounted_mf():
    segment = request.form.get('segment')
    price_plan = request.form.get('price_plan')

    df = pd.read_csv('raw_data.csv')
    
    if segment and segment != 'All':
        df = df[df['SEGMENT_NAME'] == segment]
   
    if price_plan and price_plan != 'All':
        df = df[df['PRICE_PLAN_DESC'] == price_plan]

    discounted_mf_options = ['All'] + df['DISCOUNTED_MF_W_VAT'].unique().tolist()

    return json.dumps(discounted_mf_options)

@app.route('/get_admin_centers', methods=['POST'])
def get_admin_centers():
    segment = request.form.get('segment')
    price_plan = request.form.get('price_plan')
    discounted_mf = request.form.get('discounted_mf')

    df = pd.read_csv('raw_data.csv')
    
    if segment and segment != 'All':
        df = df[df['SEGMENT_NAME'] == segment]
    
    if price_plan and price_plan != 'All':
        df = df[df['PRICE_PLAN_DESC'] == price_plan]
    
    if discounted_mf and discounted_mf != 'All':
        df = df[df['DISCOUNTED_MF_W_VAT'] == discounted_mf]

    admin_center_options = ['All'] + df['ADMIN_CENTER'].unique().tolist()

    return json.dumps(admin_center_options)

if __name__ == '__main__':
    app.run(debug=True)
