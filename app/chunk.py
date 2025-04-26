from flask import Blueprint, render_template
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from .data_preparation import  customer_engagement

churn_bp = Blueprint('churn', __name__)

@churn_bp.route('/churn')
def churn():
    # Correlation Matrix
    correlation = customer_engagement[['disengaged', 'AGE_RANGE', 'INCOME_RANGE']].copy()
    correlation['AGE_RANGE'] = correlation['AGE_RANGE'].astype('category').cat.codes
    correlation['INCOME_RANGE'] = correlation['INCOME_RANGE'].astype('category').cat.codes
    corr_matrix = correlation.corr()

    plt.figure(figsize=(8, 4))
    sns.heatmap(corr_matrix, annot=True, cmap='BuPu', fmt='.2f', cbar=True, square=True, linewidths=0.5)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    heatmap_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

     # Spend Trend Plot
    spend_trend = customer_engagement.groupby(['YEAR', 'disengaged'])['total_spend'].sum().reset_index()
    spend_plot = px.line(
        spend_trend,
        x='YEAR',
        y='total_spend',
        color='disengaged',
        title='Total Spend by Disengagement Status',
        template='plotly_dark',
        markers=True
    ).to_html(full_html=False)

    # Frequency Trend Plot
    freq_trend = customer_engagement.groupby(['YEAR', 'disengaged'])['frequency_of_purchase'].sum().reset_index()
    freq_plot = px.line(
        freq_trend,
        x='YEAR',
        y='frequency_of_purchase',
        color='disengaged',
        title='Purchase Frequency by Disengagement Status',
        template='plotly_dark',
        markers=True
    ).to_html(full_html=False)


    return render_template('churn.html',
                           heatmap=heatmap_base64,
                           spend_plot=spend_plot,
                           freq_plot=freq_plot)
