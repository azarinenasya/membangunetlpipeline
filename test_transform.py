import pytest
import pandas as pd
from utils.transform import transform_data

def test_transform_price_cleaning():
    mock_data = [
        {'product_name': 'Baju Keren', 'price': 'Rp 200.000', 'category': 'T-shirt'}
    ]
    df = transform_data(mock_data)
    assert df['price'][0] == 200000

def test_transform_empty_input():
    df = transform_data([])
    assert df.empty == True
