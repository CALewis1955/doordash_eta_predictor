if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from influxdb import InfluxDBClient
import json
from datetime import datetime



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
    filepath = f'./mage_data/evidently_report_{datetime.now().strftime("%m-%d-%Y")}.py'
    
    client = InfluxDBClient(url='localhost:8086', username='user', password='password')
    client.switch_database('evidently_metrics')
    # Load your Evidently report
    with open(filepath, 'r') as f_in:
        evidently_report = json.load(f_in) 
    # Prepare InfluxDB data
    influx_data = [
        {
            "measurement": "model_metrics",
            "tags": {
                "model": "your_model_name",
            },
            "fields": evidently_report  # Ensure report_data is a flat dictionary
        }
    ]
    # Write data to InfluxDB
    client.write_points(influx_data)
    return data

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'