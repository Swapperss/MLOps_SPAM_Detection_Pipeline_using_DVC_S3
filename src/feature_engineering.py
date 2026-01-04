import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import logging
import yaml
from myutils.common_functions import *


# Setting up logger
logger = get_logger("feature_engineering")


def apply_tfidf(train_data: pd.DataFrame, test_data: pd.DataFrame, max_features: int) -> tuple:
    """Apply TfIdf to the data."""
    try:
        vectorizer = TfidfVectorizer(max_features=max_features)

        # Fill NaN values with empty strings
        train_data['text'] = train_data['text'].fillna('')
        test_data['text'] = test_data['text'].fillna('')

        X_train = train_data['text'].values
        y_train = train_data['target'].values
        X_test = test_data['text'].values
        y_test = test_data['target'].values

        X_train_bow = vectorizer.fit_transform(X_train)
        X_test_bow = vectorizer.transform(X_test)

        train_df = pd.DataFrame(X_train_bow.toarray())
        train_df['label'] = y_train

        test_df = pd.DataFrame(X_test_bow.toarray())
        test_df['label'] = y_test

        logger.debug('tfidf applied and data transformed')
        return train_df, test_df
    except Exception as e:
        logger.error('Error during tfidf transformation: %s', e)
        raise

def save_data(df: pd.DataFrame, file_path: str) -> None:
    """Save the dataframe to a CSV file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)
        logger.debug('Data saved to %s', file_path)
    except Exception as e:
        logger.error('Unexpected error occurred while saving the data: %s', e)
        raise

def main():
    try:
        params = read_params_yaml(params_path='params.yaml')
        max_features = params['feature_engineering']['max_features']
        #max_features = 50

        train_data = load_data('./artifacts/data/interim/train_processed.csv')
        test_data = load_data('./artifacts/data/interim/test_processed.csv')

        train_df, test_df = apply_tfidf(train_data, test_data, max_features)

        save_data(train_df, os.path.join("./artifacts/data", "processed", "train_tfidf.csv"))
        save_data(test_df, os.path.join("./artifacts/data", "processed", "test_tfidf.csv"))
    except Exception as e:
        logger.error('Failed to complete the feature engineering process: %s', e)
        print(f"Error: {e}")

if __name__ == '__main__':
    main()