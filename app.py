from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import json
import plotly.graph_objects as go

app = Flask(__name__, template_folder="templates")

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    matched_rule = request.url_rule

    if not matched_rule:
        return "No route matched the current request."

    data_path = get_data_path(matched_rule.rule)
    df = pd.read_csv(data_path)

    if request.method == 'POST':
        selected_segment = request.form.get('segment')
        selected_price_plan = request.form.get('price_plan')
        selected_discounted_mf = request.form.get('discounted_mf')
        selected_admin_center = request.form.get('admin_center')

        filtered_df = get_filtered_df(data_path, selected_segment, selected_price_plan, selected_discounted_mf, selected_admin_center, "SEGMENT_NAME", "PRICE_PLAN_DESC", "DISCOUNTED_MF_W_VAT", "ADMIN_CENTER")

        xaxis, start_date, end_date = get_axis(filtered_df, "ACCOUNT_START_DATE")

        fig1 = px.bar(filtered_df, x='ACCOUNT_START_DATE', y='CNT_SUB', title="FWA Activations", labels={"ACCOUNT_START_DATE": "Account start date","CNT_SUB": "Count"})
        fig2 = px.pie(filtered_df, names='PRICE_PLAN_DESC', title='FWA Activations')

    else:
        xaxis, start_date, end_date = get_axis(df, "ACCOUNT_START_DATE")

        fig1 = px.bar(df, x='ACCOUNT_START_DATE', y='CNT_SUB', title="FWA Activations", labels={"ACCOUNT_START_DATE": "Account start date","CNT_SUB": "Count"})
        fig2 = px.pie(df, names='PRICE_PLAN_DESC', title='FWA Activations')

    fig1.update_xaxes(type=xaxis, range=[start_date, end_date], dtick="M1", tickformat="%b\n%Y", tickangle = 0, automargin=True, tickfont=dict(size=9))

    fig2.update_layout(legend_title_text='Price plans:')

    segment_options = ['All'] + sorted(df['SEGMENT_NAME'].unique().tolist())
    price_plan_options = ['All'] + sorted(df['PRICE_PLAN_DESC'].unique().tolist())
    discounted_mf_options = ['All'] + sorted(df['DISCOUNTED_MF_W_VAT'].unique().tolist())
    admin_center_options =['All'] + sorted(df['ADMIN_CENTER'].unique().tolist())

    return render_template('index.html', fig1=fig1.to_html(full_html=False), fig2=fig2.to_html(full_html=False), segment_options=segment_options, price_plan_options=price_plan_options, discounted_mf_options=discounted_mf_options, admin_center_options=admin_center_options)

@app.route('/deact', methods=['GET', 'POST'])
def deact():
    matched_rule = request.url_rule

    if not matched_rule:
        return "No route matched the current request."

    data_path = get_data_path(matched_rule.rule)
    df = pd.read_csv(data_path)

    if request.method == 'POST':
        selected_segment = request.form.get('segment')
        selected_price_plan = request.form.get('price_plan')
        selected_discounted_mf = request.form.get('discounted_mf')
        selected_admin_center = request.form.get('admin_center')

        filtered_df = filtered_df = get_filtered_df(data_path, selected_segment, selected_price_plan, selected_discounted_mf, selected_admin_center, "SEGMENT_NAME", "PRICE_PLAN_DESC", "DISCOUNTED_MF_W_VAT", "ADMIN_CENTER")

        xaxis, start_date, end_date = get_axis(filtered_df, "ACCOUNT_END_DATE")

        fig1 = px.bar(filtered_df, x='ACCOUNT_END_DATE', y='CNT_SUB', title="FWA Deactivations", labels={"ACCOUNT_END_DATE": "Account end date","CNT_SUB": "Count"})
        fig2 = px.pie(filtered_df, names='PRICE_PLAN_DESC', title='FWA Deactivations')

    else:
        xaxis, start_date, end_date = get_axis(df, "ACCOUNT_END_DATE")

        fig1 = px.bar(df, x='ACCOUNT_END_DATE', y='CNT_SUB', title="FWA Deactivations", labels={"ACCOUNT_END_DATE": "Account end date","CNT_SUB": "Count"})
        fig2 = px.pie(df, names='PRICE_PLAN_DESC', title='FWA Deactivations')

    fig1.update_xaxes(type=xaxis, range=[start_date, end_date], dtick="M1", tickformat="%b\n%Y", tickangle = 0, automargin=True, tickfont=dict(size=9))
    fig2.update_layout(legend_title_text='Price plans:')

    segment_options = ['All'] + sorted(df['SEGMENT_NAME'].unique().tolist())
    price_plan_options = ['All'] + sorted(df['PRICE_PLAN_DESC'].unique().tolist())
    discounted_mf_options = ['All'] + sorted(df['DISCOUNTED_MF_W_VAT'].unique().tolist())
    admin_center_options =['All'] + sorted(df['ADMIN_CENTER'].unique().tolist())

    return render_template('deact.html', fig1=fig1.to_html(full_html=False), fig2=fig2.to_html(full_html=False), segment_options=segment_options, price_plan_options=price_plan_options, discounted_mf_options=discounted_mf_options, admin_center_options=admin_center_options)

@app.route('/inst', methods=['GET', 'POST'])
def inst():
    matched_rule = request.url_rule

    if not matched_rule:
        return "No route matched the current request."

    data_path = get_data_path(matched_rule.rule)
    df = pd.read_csv(data_path)

    if request.method == 'POST':
        selected_segment = request.form.get('segment')
        selected_price_plan = request.form.get('price_plan')
        selected_discounted_mf = request.form.get('discounted_mf')
        selected_admin_center = request.form.get('admin_center')

        filtered_df = get_filtered_df(data_path, selected_segment, selected_price_plan, selected_discounted_mf, selected_admin_center, "WORK_ORDER_STATUS", "WORK_ORDER_OPERATION", "ADDRESS_ADMIN_CENTER", "TIME_TO_COMPLETE")

        fig1 = px.bar(filtered_df, x='WEEK_NO', y='ORDERS_NUM', title="WFM Installations", labels={"WEEK_NO": "week","ORDERS_NUM": "Count"})
        fig2 = px.pie(filtered_df, names='ADDRESS_ADMIN_CENTER', title='WFM Installations')

    else:
        fig1 = px.bar(df, x='WEEK_NO', y='ORDERS_NUM', title="WFM Installations", labels={"WEEK_NO": "week","ORDERS_NUM": "Count"})
        fig2 = px.pie(df, names='ADDRESS_ADMIN_CENTER', title='WFM Installations')

    fig2.update_layout(legend_title_text='Admin centers:')

    segment_options = ['All'] + sorted(df['WORK_ORDER_STATUS'].unique().tolist())
    price_plan_options = ['All'] + sorted(df['WORK_ORDER_OPERATION'].unique().tolist())
    discounted_mf_options = ['All'] + sorted(df['ADDRESS_ADMIN_CENTER'].unique().tolist())
    admin_center_options = ['All'] + sorted(df['TIME_TO_COMPLETE'].unique().tolist())

    return render_template('install.html', fig1=fig1.to_html(full_html=False), fig2=fig2.to_html(full_html=False), segment_options=segment_options, price_plan_options=price_plan_options, discounted_mf_options=discounted_mf_options, admin_center_options=admin_center_options)

def get_filtered_df(data_path, selected_segment, selected_price_plan, selected_discounted_mf, selected_admin_center, first_field, second_field, third_field, forth_field):
    df = pd.read_csv(data_path)
    filtered_df = df.copy()

    if selected_segment and selected_segment != 'All':
        filtered_df = filtered_df[filtered_df[first_field] == selected_segment]

    if selected_price_plan and selected_price_plan != 'All':
        filtered_df = filtered_df[filtered_df[second_field] == selected_price_plan]

    if selected_discounted_mf and selected_discounted_mf != 'All':
        filtered_df = filtered_df[filtered_df[third_field] == selected_discounted_mf]
    
    if selected_admin_center and selected_admin_center != 'All':
        filtered_df = filtered_df[filtered_df[forth_field] == selected_admin_center]

    return filtered_df

def get_data_path(path):
    if path == '/':
        return 'data/act.csv'
    elif path == '/deact':
        return 'data/deact.csv'
    elif path == '/inst':
        return 'data/wfm.csv'
    else:
        return jsonify(error="Invalid URL path")
    
def get_axis(df, field):
    start_date = pd.to_datetime(df[field]).min()
    end_date = pd.to_datetime(df[field]).max()

    date_diff_months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month

    xaxis = 'date'
    if date_diff_months < 3:
        xaxis = 'category'

    return xaxis, start_date, end_date

@app.route('/get_price_plans', methods=['POST'])
def get_price_plans():
    segment = request.form.get('segment')
    current_path = request.form.get('current_path')

    df = pd.read_csv(get_data_path(current_path))
    
    if current_path == '/inst':
        if segment and segment != 'All':
            df = df[df['WORK_ORDER_STATUS'] == segment]
        
        price_plan_options = ['All'] + df['WORK_ORDER_OPERATION'].unique().tolist()
    else:
        if segment and segment != 'All':
            df = df[df['SEGMENT_NAME'] == segment]
        
        price_plan_options = ['All'] + df['PRICE_PLAN_DESC'].unique().tolist()

    return json.dumps(price_plan_options)

@app.route('/get_discounted_mf', methods=['POST'])
def get_discounted_mf():
    segment = request.form.get('segment')
    price_plan = request.form.get('price_plan')
    current_path = request.form.get('current_path')

    df = pd.read_csv(get_data_path(current_path))

    if current_path == '/inst':
        if segment and segment != 'All':
            df = df[df['WORK_ORDER_STATUS'] == segment]
    
        if price_plan and price_plan != 'All':
            df = df[df['WORK_ORDER_OPERATION'] == price_plan]

        discounted_mf_options = ['All'] + df['ADDRESS_ADMIN_CENTER'].unique().tolist()
    else:
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
    current_path = request.form.get('current_path')

    df = pd.read_csv(get_data_path(current_path))

    if current_path == '/inst':
        if segment and segment != 'All':
            df = df[df['WORK_ORDER_STATUS'] == segment]
        
        if price_plan and price_plan != 'All':
            df = df[df['WORK_ORDER_OPERATION'] == price_plan]
        
        if discounted_mf and discounted_mf != 'All':
            df = df[df['ADDRESS_ADMIN_CENTER'] == discounted_mf]

        admin_center_options = ['All'] + df['TIME_TO_COMPLETE'].unique().tolist()
    else:
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
