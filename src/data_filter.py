import pandas as pd
import re

def filter_by_financial_products(df, product_column='Product'):
    """
    Filter complaints data by specific financial products:
    - Credit Card
    - Personal Loan
    - Buy Now Pay Later (BNPL)
    - Savings Account
    - Money Transfer
    
    Args:
        df (pd.DataFrame): The complaints dataframe
        product_column (str): Name of the column containing product information
    
    Returns:
        pd.DataFrame: Filtered dataframe containing only the specified products
    """
    
    # Define the target products and their variations
    target_products = {
        'credit_card': [
            'credit card', 'creditcard', 'credit-card', 'credit_cards',
            'visa', 'mastercard', 'amex', 'american express'
        ],
        'personal_loan': [
            'personal loan', 'personalloan', 'personal-loan', 'personal_loan',
            'unsecured loan', 'consumer loan'
        ],
        'bnpl': [
            'buy now pay later', 'bnpl', 'buy-now-pay-later', 'buy_now_pay_later',
            'afterpay', 'klarna', 'affirm', 'zip pay', 'quadpay'
        ],
        'savings_account': [
            'savings account', 'savingsaccount', 'savings-account', 'savings_account',
            'savings', 'high yield savings', 'money market'
        ],
        'money_transfer': [
            'money transfer', 'moneytransfer', 'money-transfer', 'money_transfer',
            'wire transfer', 'wiretransfer', 'international transfer',
            'remittance', 'western union', 'moneygram'
        ]
    }
    
    # Create a combined pattern for all target products
    all_patterns = []
    for product_type, patterns in target_products.items():
        all_patterns.extend(patterns)
    
    # Create regex pattern (case insensitive)
    pattern = '|'.join(map(re.escape, all_patterns))
    
    # Filter the dataframe
    if product_column in df.columns:
        # Convert to string and make case insensitive
        product_series = df[product_column].astype(str).str.lower()
        
        # Apply the filter
        mask = product_series.str.contains(pattern, case=False, na=False)
        filtered_df = df[mask].copy()
        
        # Add a column to identify which product category each complaint belongs to
        filtered_df['product_category'] = 'other'
        
        for product_type, patterns in target_products.items():
            product_pattern = '|'.join(map(re.escape, patterns))
            product_mask = product_series.str.contains(product_pattern, case=False, na=False)
            filtered_df.loc[product_mask, 'product_category'] = product_type
        
        print(f"Original dataset size: {len(df)}")
        print(f"Filtered dataset size: {len(filtered_df)}")
        print(f"Records filtered out: {len(df) - len(filtered_df)}")
        
        # Show distribution of product categories
        print("\nProduct category distribution:")
        print(filtered_df['product_category'].value_counts())
        
        return filtered_df
    else:
        print(f"Column '{product_column}' not found in the dataset.")
        print(f"Available columns: {df.columns.tolist()}")
        return df

def get_product_statistics(df, product_column='Product'):
    """
    Get statistics for the specified financial products
    
    Args:
        df (pd.DataFrame): The complaints dataframe
        product_column (str): Name of the column containing product information
    
    Returns:
        dict: Statistics for each product category
    """
    
    filtered_df = filter_by_financial_products(df, product_column)
    
    if len(filtered_df) == 0:
        return {}
    
    # Get statistics by product category
    stats = {}
    
    for category in filtered_df['product_category'].unique():
        if category != 'other':
            category_data = filtered_df[filtered_df['product_category'] == category]
            stats[category] = {
                'count': len(category_data),
                'percentage': (len(category_data) / len(df)) * 100
            }
    
    return stats 