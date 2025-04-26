import pandas as pd
import numpy as np
from pathlib import Path


DATA_DIR = Path("data")

households_df = pd.read_csv(DATA_DIR / "households.csv")
products_df = pd.read_csv(DATA_DIR / "products.csv")
transactions_df = pd.read_csv(DATA_DIR / "transactions.csv")

households_df.replace(r'^(null|\s+)$', np.nan, regex=True, inplace=True)
for col in households_df.select_dtypes(include='object'):
    households_df[col].fillna(households_df[col].mode()[0], inplace=True)

households_df.columns = households_df.columns.str.replace(r'\s+', '', regex=True)
products_df.columns = products_df.columns.str.replace(r'\s+', '', regex=True)
transactions_df.columns = transactions_df.columns.str.replace(r'\s+', '', regex=True)

households_transactions = pd.merge(transactions_df, households_df, how='inner', on='HSHD_NUM', validate='many_to_one')
final_df = pd.merge(households_transactions, products_df, how='inner', on='PRODUCT_NUM', validate='many_to_one')

final_df['SPEND'] = pd.to_numeric(final_df['SPEND'], errors='coerce').fillna(0)
final_df['UNITS'] = pd.to_numeric(final_df['UNITS'], errors='coerce').fillna(0)

final_df['PURCHASE_DATE'] = pd.to_datetime(final_df['PURCHASE_'], errors='coerce')
final_df['YEAR'] = final_df['PURCHASE_DATE'].dt.year


customer_engagement = final_df.groupby(['HSHD_NUM', 'YEAR']).agg(
    total_spend=('SPEND', 'sum'),
    frequency_of_purchase=('BASKET_NUM', 'nunique'),
    recency_of_purchase=('PURCHASE_DATE', lambda x: (x.max() - x.min()).days)
).reset_index()

customer_engagement['spend_diff'] = customer_engagement.groupby('HSHD_NUM')['total_spend'].diff()
customer_engagement['frequency_diff'] = customer_engagement.groupby('HSHD_NUM')['frequency_of_purchase'].diff()
customer_engagement['disengaged'] = np.where(
    (customer_engagement['spend_diff'] < -0.2) |
    (customer_engagement['frequency_diff'] < -0.2), 1, 0
)

demographics = final_df[['HSHD_NUM', 'AGE_RANGE', 'INCOME_RANGE']].drop_duplicates()
customer_engagement = customer_engagement.merge(demographics, on='HSHD_NUM', how='left')


basket_df = final_df.groupby('BASKET_NUM')['PRODUCT_NUM'].apply(list).reset_index()


__all__ = ["final_df", "customer_engagement", "basket_df"]
