import pandas as pd
import pytest


@pytest.fixture(scope="session")
def data_frame() -> pd.DataFrame:
    return pd.DataFrame(
        data=[
            ["A", "a", "x", 1],
            ["A", "b", "x", 1],
            ["A", "c", "x", 1],
            ["B", "a", "x", 1],
            ["B", "b", "x", 1],
            ["B", "c", "x", 1],
            ["A", "a", "y", 1],
        ],
        columns=["col_1", "col_2", "col_3", "col_4"],
    )
