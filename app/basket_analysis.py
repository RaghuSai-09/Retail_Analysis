from flask import Blueprint, render_template
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from collections import Counter
from .data_preparation import basket_df

basket_bp = Blueprint('basket', __name__)

@basket_bp.route('/basket')
def basket():
    limited_basket_df = basket_df.head(5000)

    all_products = [item for sublist in limited_basket_df['PRODUCT_NUM'] for item in sublist]
    top_products = [p for p, _ in Counter(all_products).most_common(500)]

    limited_basket_df['FILTERED_PRODUCTS'] = limited_basket_df['PRODUCT_NUM'].apply(
        lambda items: [p for p in items if p in top_products]
    )

    te = TransactionEncoder()
    te_data = te.fit(limited_basket_df['FILTERED_PRODUCTS']).transform(limited_basket_df['FILTERED_PRODUCTS'])
    encoded_df = pd.DataFrame(te_data, columns=te.columns_)

    frequent_itemsets = apriori(encoded_df, min_support=0.005, use_colnames=True)

    if not frequent_itemsets.empty:
        rules_df = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)
        rules = rules_df[['antecedents', 'consequents', 'support', 'confidence', 'lift']].to_dict(orient='records')
        itemsets = frequent_itemsets.head(50).to_dict(orient='records')
    else:
        rules = []
        itemsets = []

    return render_template('basket.html',
                           frequent_itemsets=itemsets,
                           rules=rules)
