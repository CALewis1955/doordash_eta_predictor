if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import random
import datetime

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
    df = data.copy(deep=True)
    # Function to vary numerical data by a random percentage up to 3%
    dollar_values = ['max_item_price', 'min_item_price', 'subtotal', 'max_item_price', 'min_item_price']
    integer_values = ['total_items', 'num_distinct_items','total_onshift_dashers', 'total_busy_dashers', 'total_outstanding_orders']
    
    def fake_dollar_data(value):
        percentage = random.uniform(-0.10, 0.10)  # Random percentage between -3% and 3%
        return round((value * (1 + percentage)), 2)
    
    def fake_integer_data(value):
        number = random.randint(0,4)
        return value + number
    
    """
    def fake_datetimes(value):
        time =pd.to_datetime(value)
        time = (time.hour * 3600 + time.minute * 60 + time.second) / 10**9
        number = random.randint(0, 10**6)
        return time + number
    """
    
    # Apply the function to each numerical column in the dataframe
    for column in df[dollar_values]:
        df[column] = df[column].apply(fake_dollar_data)
    for column in df[integer_values]:
        df[column] = df[column].apply(fake_integer_data)
    """    
    df['created_at'] = pd.to_datetime(df['created_at']).astype(int) / 10**9
    df['actual_delivery_time'] = df['actual_delivery_time'].apply(fake_datetimes)
    """
    filename = f'./mage_data/fake_data_{datetime.datetime.now().strftime("%m-%d-%Y")}.csv'  
    df.to_csv(filename, index=False)   
    return data, df

    
    

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
