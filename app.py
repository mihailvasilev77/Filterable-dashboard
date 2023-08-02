from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import json

# Create a Flask app and specify the template folder
app = Flask(__name__, template_folder="templates")

# Define a route for the dashboard page (homepage)
@app.route('/', methods=['GET', 'POST'])
def dashboard():
    # Get the matched route from the request
    matched_rule = request.url_rule

    # If no route matches the current request, return an error message
    if not matched_rule:
        return "No route matched the current request."

    # Get the data path based on the matched route
    data_path = get_data_path(matched_rule.rule)
    
    # Read the data from the CSV file into a DataFrame
    df = pd.read_csv(data_path)

    # Check if the request method is POST (form submitted, user input)
    if request.method == 'POST':
        # Get the selected values from the dropdown menus
        selected_segment = request.form.get('segment')
        selected_price_plan = request.form.get('price_plan')
        selected_discounted_mf = request.form.get('discounted_mf')
        selected_admin_center = request.form.get('admin_center')

        # Filter the DataFrame based on the selected values
        filtered_df = get_filtered_df(data_path, selected_segment, selected_price_plan, selected_discounted_mf, selected_admin_center, "SEGMENT_NAME", "PRICE_PLAN_DESC", "DISCOUNTED_MF_W_VAT", "ADMIN_CENTER")

        # Get the x-axis type, start date, and end date for the plot, this is used to format the x axis
        xaxis, start_date, end_date = get_axis(filtered_df, "ACCOUNT_START_DATE")

        # Create two plots using Plotly Express library
        fig1 = px.bar(filtered_df, x='ACCOUNT_START_DATE', y='CNT_SUB', title="FWA Activations", labels={"ACCOUNT_START_DATE": "Account start date","CNT_SUB": "Count"})
        fig2 = px.pie(filtered_df, names='PRICE_PLAN_DESC', title='FWA Activations')

    else:
        # If it's a GET request (page load without form submission), use the whole unfiltered DataFrame for the plots
        xaxis, start_date, end_date = get_axis(df, "ACCOUNT_START_DATE")

        fig1 = px.bar(df, x='ACCOUNT_START_DATE', y='CNT_SUB', title="FWA Activations", labels={"ACCOUNT_START_DATE": "Account start date","CNT_SUB": "Count"})
        fig2 = px.pie(df, names='PRICE_PLAN_DESC', title='FWA Activations')

    # Customize the plots (x-axis, date range, tick format, etc.)
    fig1.update_xaxes(type=xaxis, range=[start_date, end_date], dtick="M1", tickformat="%b\n%Y", tickangle=0, automargin=True, tickfont=dict(size=9))
    fig2.update_layout(legend_title_text='Price plans:')

    # Create lists of options for dropdown filters
    segment_options = ['All'] + sorted(df['SEGMENT_NAME'].unique().tolist())
    price_plan_options = ['All'] + sorted(df['PRICE_PLAN_DESC'].unique().tolist())
    discounted_mf_options = ['All'] + sorted(df['DISCOUNTED_MF_W_VAT'].unique().tolist())
    admin_center_options = ['All'] + sorted(df['ADMIN_CENTER'].unique().tolist())
    date_options = ['All'] + sorted(df['year'].unique().tolist())

    # Render the template 'index.html' with the plots and filter options
    return render_template('index.html', fig1=fig1.to_html(full_html=False), fig2=fig2.to_html(full_html=False), segment_options=segment_options, price_plan_options=price_plan_options, discounted_mf_options=discounted_mf_options, admin_center_options=admin_center_options, date_options=date_options)

# The functions deact(), install() are analogical to index()
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
    date_options = ['All'] + sorted(df['YEAR_ID'].unique().tolist())

    return render_template('install.html', fig1=fig1.to_html(full_html=False), fig2=fig2.to_html(full_html=False), segment_options=segment_options, price_plan_options=price_plan_options, discounted_mf_options=discounted_mf_options, admin_center_options=admin_center_options, date_options=date_options)

@app.route('/rep', methods=['GET', 'POST'])
def report():
    matched_rule = request.url_rule

    if not matched_rule:
        return "No route matched the current request."

    # Load three different dataframes
    data_path = get_data_path(matched_rule.rule)
    df = pd.read_csv(data_path)

    data_path1 = get_data_path("/rep_act")
    df1 = pd.read_csv(data_path)

    data_path2 = get_data_path("/rep_deact")
    df2 = pd.read_csv(data_path)

    if request.method == 'POST':
        selected_segment = request.form.get('segment')
        selected_price_plan = request.form.get('price_plan')
        selected_discounted_mf = request.form.get('discounted_mf')
        selected_admin_center = request.form.get('admin_center')

        # Create the different filtered dataframes based on the same filters
        filtered_df = get_filtered_df(data_path, selected_segment, selected_price_plan, selected_discounted_mf, selected_admin_center, "SEGMENT_NAME", "PRICE_PLAN_DESC", "DISCOUNTED_MF_W_VAT", "ADMIN_CENTER")
        filtered_df1 = get_filtered_df(data_path1, selected_segment, selected_price_plan, selected_discounted_mf, selected_admin_center, "SEGMENT_NAME", "PRICE_PLAN_DESC", "DISCOUNTED_MF_W_VAT", "ADMIN_CENTER")
        filtered_df2 = get_filtered_df(data_path2, selected_segment, selected_price_plan, selected_discounted_mf, selected_admin_center, "SEGMENT_NAME", "PRICE_PLAN_DESC", "DISCOUNTED_MF_W_VAT", "ADMIN_CENTER")
        
        # Variables that save the counts of the dataframes
        df_count, act_count, deact_count, count_4g, count_5g = return_counts(filtered_df,filtered_df1,filtered_df2)

        fig1 = px.pie(filtered_df, names='PRICE_PLAN', title='FWA services')
    else:
        # Variables that save the counts of the dataframes
        df_count, act_count, deact_count, count_4g, count_5g = return_counts(df,df1,df2)

        fig1 = px.pie(df, names='PRICE_PLAN', title='FWA services')

    fig1.update_layout(legend_title_text='Price plans:')

    price_plan_options = ['All'] + sorted(df['PRICE_PLAN'].unique().tolist())
    admin_center_options =['All'] + sorted(df['ADMIN_CENTER'].unique().tolist())

    return render_template('report.html', fig1=fig1.to_html(full_html=False),df_count=df_count, count_4g=count_4g, count_5g=count_5g, act_count=act_count, deact_count=deact_count, price_plan_options=price_plan_options, admin_center_options=admin_center_options)

# Helper function to filter the DataFrame based on selected filters
def get_filtered_df(data_path, selected_segment, selected_price_plan, selected_discounted_mf, selected_admin_center, first_field, second_field, third_field, forth_field):
    df = pd.read_csv(data_path)
    filtered_df = df.copy()

    # Apply filters based on selected values for each column
    if selected_segment and selected_segment != 'All':
        # "filtered_df[first_field] == selected_segment" returns a boolean value (True or False)
        # based on whether the selected field is in the dataframe or not,
        # then the dataframe is filtered with the rows that returned True
        filtered_df = filtered_df[filtered_df[first_field] == selected_segment]

    if selected_price_plan and selected_price_plan != 'All':
        filtered_df = filtered_df[filtered_df[second_field] == selected_price_plan]

    if selected_discounted_mf and selected_discounted_mf != 'All':
        filtered_df = filtered_df[filtered_df[third_field].astype(str) == selected_discounted_mf]
    
    if selected_admin_center and selected_admin_center != 'All':
        filtered_df = filtered_df[filtered_df[forth_field] == selected_admin_center]

    return filtered_df

# Helper function to return counts for different types of activations/deactivations
def return_counts(df, df1, df2):
    df_count = len(df)
    act_count = len(df1)
    deact_count = len(df2)
    count_4g = len(df[df['PRICE_PLAN'] == '4G'])
    count_5g = len(df[df['PRICE_PLAN'] == '5G'])

    return df_count, act_count, deact_count, count_4g, count_5g

# Helper function to get the data path based on the route
def get_data_path(path):
    if path == '/':
        return 'data/act.csv'
    elif path == '/deact':
        return 'data/deact.csv'
    elif path == '/inst':
        return 'data/wfm.csv'
    elif path == '/rep':
        return 'data/weekly.csv'
    elif path == '/rep_act':
        return 'data/act_fwa.csv'
    elif path == '/rep_deact':
        return 'data/deact_fwa.csv'
    else:
        return jsonify(error="Invalid URL path")

# Helper function to determine the x-axis type and date range for plotting
def get_axis(df, field):
    start_date = pd.to_datetime(df[field]).min()
    end_date = pd.to_datetime(df[field]).max()

    # Calculate the difference in the months
    date_diff_months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month

    #If the difference is less than 3 months the x axis is sorted accordingly to its little data size
    xaxis = 'date'
    if date_diff_months < 3:
        xaxis = 'category'

    return xaxis, start_date, end_date

# Routes for dynamic dropdown menus (filter options)
# These routes return JSON data to populate the dropdown menus with relevant options based on selected filters.
# The functions are similar, with slight variations based on the selected filters.
@app.route('/get_price_plans', methods=['POST'])
def get_price_plans():
    # Get the 'segment' and 'current_path' values from the form data submitted via POST
    segment = request.form.get('segment')
    current_path = request.form.get('current_path')

    df = pd.read_csv(get_data_path(current_path))
    
     # Check if the current path is '/inst' or any other path
    if current_path == '/inst':
        # In '/inst' everything is the same only the name of the column is changed
        if segment and segment != 'All':
            df = df[df['WORK_ORDER_STATUS'] == segment]

        price_plan_options = ['All'] + df['WORK_ORDER_OPERATION'].unique().tolist()
    else:
        # Apply filtering on the DataFrame based on the 'segment' value
        if segment and segment != 'All':
            # Boolean indexing: Select rows where 'SEGMENT_NAME' column equals the 'segment' value
            df = df[df['SEGMENT_NAME'] == segment]
        
        # Get unique 'PRICE_PLAN_DESC' values in the filtered DataFrame
        # and create a list of options with 'All' as the first element
        price_plan_options = ['All'] + df['PRICE_PLAN_DESC'].unique().tolist()

    # Convert the list of price plan options to a JSON format and return it as a response
    return json.dumps(price_plan_options)

# The rest of the functions are the same as the one above with the only difference
# that with each filter it has to be gotten into account the previous filter 
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
            df = df[df['DISCOUNTED_MF_W_VAT'].astype(str) == discounted_mf]

        admin_center_options = ['All'] + df['ADMIN_CENTER'].unique().tolist()

    return json.dumps(admin_center_options)

@app.route('/get_date', methods=['POST'])
def get_date():
    segment = request.form.get('segment')
    price_plan = request.form.get('price_plan')
    discounted_mf = request.form.get('discounted_mf')
    admin_center = request.form.get('admin_center')
    current_path = request.form.get('current_path')

    df = pd.read_csv(get_data_path(current_path))

    if current_path == '/inst':
        if segment and segment != 'All':
            df = df[df['WORK_ORDER_STATUS'] == segment]
        
        if price_plan and price_plan != 'All':
            df = df[df['WORK_ORDER_OPERATION'] == price_plan]
        
        if discounted_mf and discounted_mf != 'All':
            df = df[df['ADDRESS_ADMIN_CENTER'] == discounted_mf]

        if admin_center and admin_center != 'All':
            df = df[df['TIME_TO_COMPLETE'] == admin_center]
        
        date_options = ['All'] + df['YEAR_ID'].unique().tolist()
    else:
        if segment and segment != 'All':
            df = df[df['SEGMENT_NAME'] == segment]
        
        if price_plan and price_plan != 'All':
            df = df[df['PRICE_PLAN_DESC'] == price_plan]
        
        if discounted_mf and discounted_mf != 'All':
            df = df[df['DISCOUNTED_MF_W_VAT'] == discounted_mf]
        
        if admin_center and admin_center != 'All':
            df = df[df['ADMIN_CENTER'] == admin_center]

        date_options = ['All'] + df['year'].unique().tolist()

    return json.dumps(date_options)

if __name__ == '__main__':
    app.run(debug=True)
