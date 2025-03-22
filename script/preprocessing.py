import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

def preprocess_data(raw_data):
    """
    Preprocess raw financial data for model training or inference.
    
    Args:
        raw_data (pd.DataFrame): Raw data with columns like 'amount', 'category', 'date'.
    
    Returns:
        pd.DataFrame: Preprocessed data ready for machine learning models.
    """
    # Handle missing values in numerical columns
    imputer = SimpleImputer(strategy='mean')
    raw_data['amount'] = imputer.fit_transform(raw_data[['amount']])
    
    # Feature engineering: Extract month from date
    raw_data['month'] = pd.to_datetime(raw_data['date']).dt.month
    
    # One-hot encode categorical variables (e.g., 'category')
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded_categories = encoder.fit_transform(raw_data[['category']])
    category_columns = encoder.get_feature_names_out(['category'])
    raw_data = raw_data.join(pd.DataFrame(encoded_categories, columns=category_columns))
    
    # Scale numerical features
    scaler = StandardScaler()
    raw_data[['amount', 'month']] = scaler.fit_transform(raw_data[['amount', 'month']])
    
    # Drop original columns that are no longer needed
    raw_data.drop(['category', 'date'], axis=1, inplace=True)
    
    return raw_data

if __name__ == "__main__":
    # Example usage for testing
    sample_data = pd.DataFrame({
        'amount': [100, 200, None],
        'category': ['Food', 'Transport', 'Food'],
        'date': ['2023-01-01', '2023-01-02', '2023-01-03']
    })
    processed_data = preprocess_data(sample_data)
    print("Preprocessed Data:")
    print(processed_data)
