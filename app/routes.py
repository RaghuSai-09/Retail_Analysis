from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import pandas as pd
import plotly.express as px
import json
from plotly.offline import plot
from . import mongo
from .data_preparation import final_df, customer_engagement, basket_df
import os
main = Blueprint('main', __name__)


UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'csv', 'json'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

USERS = {'admin': 'admin123'}


@main.route('/menu')
def menu():
    return render_template('menu.html')

@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if USERS.get(request.form['username']) == request.form['password']:
            session['user'] = request.form['username']
            return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@main.route('/dashboard')
def dashboard():
    final_df['CHILDREN'] = final_df['CHILDREN'].replace({'Y': 1, 'N': 0})

    hh_size_plot = px.bar(
        final_df.groupby('HH_SIZE')['SPEND'].sum().reset_index(),
        x='HH_SIZE',
        y='SPEND',
        title='Total Spend by Household Size',
        template='plotly_dark',
        color='SPEND',  
        height=1000    
    ).update_layout(
        yaxis_tickformat=',',
        margin=dict(l=60, r=60, t=60, b=60),
        bargap=0.5,
        title_x=0.5
    ).to_html(full_html=False)


    children_plot = px.bar(
        final_df.groupby('CHILDREN')['SPEND'].sum().reset_index(),
        x='CHILDREN', y='SPEND',
        title='Total Spend by Children Present',
        template='plotly_dark',
        color='SPEND',  
        height=700      
    ).update_layout(
        yaxis_tickformat=',',
        margin=dict(l=60, r=60, t=60, b=60),
        bargap=0.5,
        title_x=0.5
    ).to_html(full_html=False)
    

    location_plot = px.bar(
        final_df.groupby('STORE_R')['SPEND'].sum().reset_index(),
        x='STORE_R', y='SPEND',
        title='Avg Spend by Store Region',
        template='plotly_dark',
        height=500      
    ).update_layout(
        yaxis_tickformat=',',
        margin=dict(l=60, r=60, t=60, b=60),
        bargap=0.5,
        title_x=0.5
    ).to_html(full_html=False)
    

    year_plot = px.line(
        final_df.groupby('YEAR')['SPEND'].sum().reset_index(),
        x='YEAR', y='SPEND',
        title='Yearly Household Spending',
        template='plotly_dark',
        markers=True
    ).to_html(full_html=False)

    dept_plot = px.line(
        final_df.groupby(['YEAR', 'DEPARTMENT'])['SPEND'].sum().reset_index(),
        x='YEAR', y='SPEND', color='DEPARTMENT',
        title='Spend by Department Over Years',
        template='plotly_dark'
    ).to_html(full_html=False)

    top_items_df = (
    final_df.groupby('PRODUCT_NUM')['SPEND']
    .sum()
    .nlargest(7)
    .reset_index()
    )

   
    top_items_df['PRODUCT_NUM'] = top_items_df['PRODUCT_NUM'].astype(str)

    top_items_plot = px.bar(
        top_items_df,
        x='PRODUCT_NUM',
        y='SPEND',
        title='Top 7 Articles by Spend',
        template='plotly_dark',
        color_discrete_sequence=['deepskyblue']  # Optional custom color
    )

   
    top_items_plot.update_traces(width=0.6)
    top_items_plot.update_layout(
        xaxis_title='Product Number',
        yaxis_title='Total Spend',
        bargap=0.2,  # Reduce bar spacing
        height=400
    )

    top_items_plot = top_items_plot.to_html(full_html=False)

    brand_plot = px.pie(
        final_df, names='BRAND_TY',
        title='Brand Share by Type',
        template='plotly_dark'
    ).to_html(full_html=False)

    units_plot = px.line(
        final_df.groupby(['YEAR', 'DEPARTMENT'])['UNITS'].sum().reset_index(),
        x='YEAR', y='UNITS', color='DEPARTMENT',
        title='Units Sold by Product Category Over Time',
        template='plotly_dark'
    ).to_html(full_html=False)

    return render_template('dashboard.html',
                           hh_size_plot=hh_size_plot,
                           children_plot=children_plot,
                           location_plot=location_plot,
                           year_plot=year_plot,
                           dept_plot=dept_plot,
                           top_items_plot=top_items_plot,
                           brand_plot=brand_plot,
                           units_plot=units_plot)

@main.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        dataset_type = request.form.get('dataset_type')

        if not file or file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(request.url)

        if dataset_type not in ['households', 'products', 'transactions']:
            flash('Invalid dataset type selected.', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            extension = file.filename.rsplit('.', 1)[1].lower()
            target_filename = f"uploaded_{dataset_type}.{extension}"
            file_path = os.path.join(UPLOAD_FOLDER, target_filename)

            try:
                if extension == 'csv':
                    df = pd.read_csv(file)
                    df.to_csv(file_path, index=False)
                elif extension == 'json':
                    data = json.load(file)
                    df = pd.DataFrame(data)
                    df.to_csv(file_path, index=False)
                else:
                    flash('Unsupported file type.', 'danger')
                    return redirect(request.url)

                flash(f'Successfully uploaded and refreshed {dataset_type} dataset! ✅', 'success')
                return redirect(url_for('main.upload'))  # 🔥 Stay on Upload page

            except Exception as e:
                print("Upload error:", e)
                flash('An error occurred while processing the file.', 'danger')
                return redirect(request.url)

        else:
            flash('Invalid file type. Please upload a CSV or JSON.', 'danger')

    return render_template('upload.html')
   

@main.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    sort_by = "BASKET_NUM"
    hshd_query = ""

    valid_sort_fields = ["BASKET_NUM", "PRODUCT_NUM", "COMMODITY", "DEPARTMENT", "PURCHASE_", "HSHD_NUM"]

    if request.method == 'POST':
        hshd_query = request.form.get('hshd_num', '').strip()
        sort_by = request.form.get('sort_by', 'BASKET_NUM')

        if sort_by not in valid_sort_fields:
            sort_by = "BASKET_NUM"

        filtered = final_df[final_df['HSHD_NUM'].astype(str).str.contains(hshd_query, na=False)]

        try:
            results = filtered.sort_values(by=sort_by, ascending=True).to_dict(orient='records')
        except Exception as e:
            print("Sort failed:", e)
            results = filtered.to_dict(orient='records')

    return render_template('search.html', results=results, sort_by=sort_by, hshd_query=hshd_query)
