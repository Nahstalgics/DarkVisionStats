import pytest
import pandas as pd
@pytest.fixture
def sample_dataframe():
    data = {
        "depth": [1, 2, 3, 4, 5],
        "wall_location": ["A", "B", "C", "D", "E"]
    }
    df = pd.DataFrame(data)
    print(df)
    return df

def test_kde():
    from statistics import Statistics
    df = pd.DataFrame({
        "depth": [1, 2, 3, 4, 5]
    })
    stats = Statistics(df)
    kde = stats.create_kde()
    print(kde)
    assert kde is not None

test_kde()
