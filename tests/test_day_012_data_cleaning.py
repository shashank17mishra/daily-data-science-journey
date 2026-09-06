import pandas as pd
import numpy as np
from learning.pandas.day_012_data_cleaning import clean_customer_dataset

def test_clean_customer_dataset():
    raw_data = {
        "customer_id": [101, 102, 101, 103],
        "age": [25.0, np.nan, 25.0, 35.0],
        "email": ["ALICE@EXAMPLE.COM ", "Bob@Example.com", "alice@example.com", " Charlie@example.com "]
    }
    df = pd.DataFrame(raw_data)
    cleaned = clean_customer_dataset(df)

    assert len(cleaned) == 3
    assert list(cleaned["customer_id"]) == [101, 102, 103]
    assert cleaned.loc[cleaned["customer_id"] == 102, "age"].values[0] == 30.0
    assert cleaned.loc[cleaned["customer_id"] == 101, "email"].values[0] == "alice@example.com"
