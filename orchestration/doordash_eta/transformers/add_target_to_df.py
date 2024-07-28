if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

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
    
    """
    Returns a dataframe with the duration of the delivery in minutes
    """
    df = data
    # our target is actual duration
    # the created_at and actual_delivery_time are dates;  let's convert them
    df['created_at'] = pd.to_datetime(df['created_at']).astype(int) / 10**9
    df['actual_delivery_time'] = pd.to_datetime(df['actual_delivery_time']).astype(int) / 10**9
    df['actual_duration'] = (df['actual_delivery_time'] - df['created_at']) / 60
    return df
    
    


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
