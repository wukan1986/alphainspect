# this code is auto generated by the expr_codegen
# https://github.com/wukan1986/expr_codegen
# 此段代码由 expr_codegen 自动生成，欢迎提交 issue 或 pull request
import re

import numpy as np  # noqa
import pandas as pd  # noqa
import polars as pl  # noqa
import polars.selectors as cs  # noqa
# from loguru import logger  # noqa

# ===================================
# 导入优先级，例如：ts_RSI在ta与talib中都出现了，优先使用ta
# 运行时，后导入覆盖前导入，但IDE智能提示是显示先导入的
_ = 0  # 只要之前出现了语句，之后的import位置不参与调整
# from polars_ta.prefix.talib import *  # noqa
from polars_ta.prefix.tdx import *  # noqa
from polars_ta.prefix.ta import *  # noqa
from polars_ta.prefix.wq import *  # noqa
from polars_ta.prefix.cdl import *  # noqa

# ===================================

_ = (
    "OPEN",
    "CLOSE",
)
(
    OPEN,
    CLOSE,
) = (pl.col(i) for i in _)

_ = (
    "_x_0",
    "RETURN_CC_1",
    "RETURN_OO_1",
    "RETURN_OO_2",
    "RETURN_OO_5",
)
(
    _x_0,
    RETURN_CC_1,
    RETURN_OO_1,
    RETURN_OO_2,
    RETURN_OO_5,
) = (pl.col(i) for i in _)

_DATE_ = "date"
_ASSET_ = "asset"


def func_0_ts__asset(df: pl.DataFrame) -> pl.DataFrame:
    df = df.sort(by=[_DATE_])
    # ========================================
    df = df.with_columns(
        _x_0=1 / ts_delay(OPEN, -1),
        RETURN_CC_1=(-CLOSE + ts_delay(CLOSE, -1)) / CLOSE,
    )
    # ========================================
    df = df.with_columns(
        RETURN_OO_1=_x_0 * ts_delay(OPEN, -2) - 1,
        RETURN_OO_2=_x_0 * ts_delay(OPEN, -3) - 1,
        RETURN_OO_5=_x_0 * ts_delay(OPEN, -6) - 1,
    )
    return df


"""
#========================================func_0_ts__asset
_x_0 = 1/ts_delay(OPEN, -1)
RETURN_CC_1 = (-CLOSE + ts_delay(CLOSE, -1))/CLOSE
#========================================func_0_ts__asset
RETURN_OO_1 = _x_0*ts_delay(OPEN, -2) - 1
RETURN_OO_2 = _x_0*ts_delay(OPEN, -3) - 1
RETURN_OO_5 = _x_0*ts_delay(OPEN, -6) - 1
"""

"""
RETURN_OO_1 = ts_delay(OPEN, -2)/ts_delay(OPEN, -1) - 1
RETURN_OO_2 = ts_delay(OPEN, -3)/ts_delay(OPEN, -1) - 1
RETURN_OO_5 = ts_delay(OPEN, -6)/ts_delay(OPEN, -1) - 1
RETURN_CC_1 = -1 + ts_delay(CLOSE, -1)/CLOSE
"""


def main(df: pl.DataFrame):
    # logger.info("start...")

    df = df.sort(by=[_DATE_, _ASSET_])
    df = df.group_by(by=[_ASSET_]).map_groups(func_0_ts__asset)

    # drop intermediate columns
    df = df.drop(columns=list(filter(lambda x: re.search(r"^_x_\d+", x), df.columns)))

    # shrink
    df = df.select(cs.all().shrink_dtype())
    df = df.shrink_to_fit()

    # logger.info('done')

    # save
    # df.write_parquet('output.parquet', compression='zstd')

    return df


if __name__ in ("__main__", "builtins"):
    # TODO: 数据加载或外部传入
    df_output = main(df_input)