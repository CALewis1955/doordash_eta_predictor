if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import pickle
import mlflow
import os
import joblib
from datetime import datetime
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error



AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_DEFAULT_REGION =os.environ['AWS_DEFAULT_REGION']

@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    df = data

    numerical = ['max_item_price', 'min_item_price', 'subtotal', 'total_items', 'num_distinct_items', 'max_item_price', 'min_item_price', 'total_onshift_dashers', 'total_busy_dashers', 'total_outstanding_orders']

    categorical = ['market_id', 'store_id', 'store_primary_category', 'order_protocol']

    """## Validation Framework"""


    df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)
    df_train, df_val = train_test_split(df_full_train, test_size=0.25, random_state=1)

    len(df_train), len(df_val), len(df_test)

    df_train = df_train.reset_index(drop=True)
    df_val = df_val.reset_index(drop=True)
    df_test = df_test.reset_index(drop=True)

    y_train = df_train.actual_duration.values
    y_val = df_val.actual_duration.values
    y_test = df_test.actual_duration.values

    train_dict = df_train[categorical + numerical].to_dict(orient='records')
    val_dict = df_val[categorical + numerical].to_dict(orient='records')


    pipeline = make_pipeline(
        DictVectorizer(),
        LinearRegression()
    )
      
    now = datetime.now()
    
    mlflow.set_tracking_uri(uri="http://ec2-34-233-122-168.compute-1.amazonaws.com:5000")
    mlflow.end_run()
    mlflow.set_experiment(f'LR-{now}')
    mlflow.set_tag("model", "linear regression")
    mlflow.autolog()
      
    pipeline.fit(train_dict, y_train)
    y_pred = pipeline.predict(val_dict)

    rmse = mean_squared_error(y_pred, y_val, squared=False)
    print(f'This is the rmse:  {rmse}')
    mlflow.sklearn.log_model(pipeline, artifact_path="model")

    joblib.dump(pipeline, './mage_data/pipeline.pkl')
    print("Pipeline saved successfully.")
    
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

