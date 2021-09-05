from itertools import chain
import pandas as pd
import asyncio
import io
from decimal import Decimal
from functools import partial
from itertools import chain
from typing import List, Union, Any

import pandas as pd


def get_conditional_data(items: list, dot_path: str, values: Union[list, str, int]) -> Union[dict, None]:
    if not isinstance(values, list):
        values = [values]
    for item in items:
        item_value = get_field(dot_path, item)
        if item_value in values:
            return item
    return None


def get_field(dot_path: str, record: Any) -> Any:
    field, *fields = dot_path.split(".")
    dp = ".".join(fields)
    if not field:
        if record is None:
            return ""
        return record
    if isinstance(record, dict):
        val = record.get(field)
        return get_field(dp, val)
    elif isinstance(record, list):
        if len(record):
            val = record[0].get(field)
            return get_field(dp, val)
        return [get_field(dp, val) for val in record]
    else:
        if record is None:
            return ""
        return record



def explode_lists(data: list, field: str) -> list:
    return list(chain(*[explode_list(d, field) for d in data]))


def explode_list(data: dict, field: str) -> list:
    data_list = []
    field_list = data[field]
    top_level_data = {key: value for key, value in data.items() if key != field}
    for row in field_list:
        d = {}
        d.update(top_level_data)
        d.update({f"{field}.{key}": value for key, value in row.items()})
        data_list.append(d)
    return data_list


def explode_df(df: pd.DataFrame, col: str) -> pd.DataFrame:
    dfe = df.explode(col)
    return df.drop(columns=[col]).merge(
        dfe[col].apply(pd.Series).add_prefix(f"{col}."),
        left_index=True, right_index=True)
