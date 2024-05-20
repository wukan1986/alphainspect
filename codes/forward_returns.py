# this code is auto generated by the expr_codegen
# https://github.com/wukan1986/expr_codegen
# 此段代码由 expr_codegen 自动生成，欢迎提交 issue 或 pull request

import numpy as np  # noqa
import pandas as pd  # noqa
import polars as pl  # noqa
import polars.selectors as cs  # noqa
from loguru import logger  # noqa

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
    r"OPEN",
    r"CLOSE",
    r"_OC_01_0_",
    r"_CC_01_1_",
    r"_CO_01_2_",
    r"_OO_01_3_",
    r"_OO_02_4_",
    r"_OO_05_5_",
    r"_OO_10_6_",
)
(
    OPEN,
    CLOSE,
    _OC_01_0_,
    _CC_01_1_,
    _CO_01_2_,
    _OO_01_3_,
    _OO_02_4_,
    _OO_05_5_,
    _OO_10_6_,
) = (pl.col(i) for i in _)

_ = (
    r"_x_0",
    r"_x_1",
    r"_x_3",
    r"RETURN_CC_01",
    r"_x_2",
    r"RETURN_CO_01",
    r"RETURN_OC_01",
    r"RETURN_OO_01",
    r"RETURN_OO_02",
    r"RETURN_OO_05",
    r"RETURN_OO_10",
)
(
    _x_0,
    _x_1,
    _x_3,
    RETURN_CC_01,
    _x_2,
    RETURN_CO_01,
    RETURN_OC_01,
    RETURN_OO_01,
    RETURN_OO_02,
    RETURN_OO_05,
    RETURN_OO_10,
) = (pl.col(i) for i in _)

_DATE_ = "date"
_ASSET_ = "asset"

CS_SW_L1 = pl.col(r"^sw_l1_\d+$")


def func_0_ts__asset(df: pl.DataFrame) -> pl.DataFrame:
    df = df.sort(by=[_DATE_])
    # ========================================
    df = df.with_columns(
        _x_0=ts_delay(CLOSE, -1),
        _x_1=ts_delay(OPEN, -1),
    )
    return df


def func_0_cl(df: pl.DataFrame) -> pl.DataFrame:
    # ========================================
    df = df.with_columns(
        _x_3=1 / CLOSE,
    )
    # ========================================
    df = df.with_columns(
        RETURN_CC_01=_x_0 * _x_3 - 1,
        _x_2=1 / _x_1,
        RETURN_CO_01=_x_1 * _x_3 - 1,
    )
    # ========================================
    df = df.with_columns(
        RETURN_OC_01=_x_0 * _x_2 - 1,
    )
    return df


def func_1_ts__asset(df: pl.DataFrame) -> pl.DataFrame:
    df = df.sort(by=[_DATE_])
    # ========================================
    df = df.with_columns(
        _OO_01_3_=_x_2 * ts_delay(OPEN, -2),
        _OO_02_4_=_x_2 * ts_delay(OPEN, -3),
        _OO_05_5_=_x_2 * ts_delay(OPEN, -6),
        _OO_10_6_=_x_2 * ts_delay(OPEN, -11),
    )
    return df


def func_2_cl(df: pl.DataFrame) -> pl.DataFrame:
    # ========================================
    df = df.with_columns(
        RETURN_OO_01=_OO_01_3_ - 1,
        RETURN_OO_02=_OO_02_4_ ** 0.5 - 1,
        RETURN_OO_05=_OO_05_5_ ** 0.2 - 1,
        RETURN_OO_10=_OO_10_6_ ** 0.1 - 1,
    )
    return df


"""
#========================================func_0_ts__asset
_x_0 = ts_delay(CLOSE, -1)
_x_1 = ts_delay(OPEN, -1)
#========================================func_0_cl
_x_3 = 1/CLOSE
#========================================func_0_cl
RETURN_CC_01 = _x_0*_x_3 - 1
_x_2 = 1/_x_1
RETURN_CO_01 = _x_1*_x_3 - 1
#========================================func_0_cl
RETURN_OC_01 = _x_0*_x_2 - 1
#========================================func_1_ts__asset
_OO_01_3_ = _x_2*ts_delay(OPEN, -2)
_OO_02_4_ = _x_2*ts_delay(OPEN, -3)
_OO_05_5_ = _x_2*ts_delay(OPEN, -6)
_OO_10_6_ = _x_2*ts_delay(OPEN, -11)
#========================================func_2_cl
RETURN_OO_01 = _OO_01_3_ - 1
RETURN_OO_02 = _OO_02_4_**0.5 - 1
RETURN_OO_05 = _OO_05_5_**0.2 - 1
RETURN_OO_10 = _OO_10_6_**0.1 - 1
"""

"""
_OC_01_0_ = ts_delay(CLOSE, -1)/ts_delay(OPEN, -1)
_CC_01_1_ = ts_delay(CLOSE, -1)/CLOSE
_CO_01_2_ = ts_delay(OPEN, -1)/CLOSE
_OO_01_3_ = ts_delay(OPEN, -2)/ts_delay(OPEN, -1)
_OO_02_4_ = ts_delay(OPEN, -3)/ts_delay(OPEN, -1)
_OO_05_5_ = ts_delay(OPEN, -6)/ts_delay(OPEN, -1)
_OO_10_6_ = ts_delay(OPEN, -11)/ts_delay(OPEN, -1)
RETURN_OC_01 = _OC_01_0_ - 1
RETURN_CC_01 = _CC_01_1_ - 1
RETURN_CO_01 = _CO_01_2_ - 1
RETURN_OO_01 = _OO_01_3_ - 1
RETURN_OO_02 = _OO_02_4_**0.5 - 1
RETURN_OO_05 = _OO_05_5_**0.2 - 1
RETURN_OO_10 = _OO_10_6_**0.1 - 1
"""


def main(df: pl.DataFrame) -> pl.DataFrame:
    # logger.info("start...")

    df = df.sort(by=[_DATE_, _ASSET_])
    df = df.group_by(_ASSET_).map_groups(func_0_ts__asset)
    df = func_0_cl(df)
    df = df.group_by(_ASSET_).map_groups(func_1_ts__asset)
    df = func_2_cl(df)

    # drop intermediate columns
    # df = df.select(pl.exclude(r'^_x_\d+$'))
    df = df.select(~cs.starts_with("_"))

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
