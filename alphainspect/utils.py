import numpy as np
import pandas as pd
import polars as pl
from polars import Series, Expr, Int16

from alphainspect._nb import _sub_portfolio_returns


def rank_ic(a: str, b: str) -> Expr:
    """RankIC"""
    return pl.corr(a, b, method='spearman', ddof=0, propagate_nans=False)


def auto_corr(a: str, period: int) -> Expr:
    """自相关"""
    return pl.corr(pl.col(a), pl.col(a).shift(period), method='spearman', ddof=0, propagate_nans=False)


def _qcut(x: Series, q: int) -> Series:
    # TODO 等待提供
    if x.null_count() == len(x):
        return x
    else:
        return pd.qcut(x, q, labels=False, duplicates='drop')


def cs_bucket(x: Expr, q: int = 10) -> Expr:
    """Convert float values into indexes for user-specified buckets. Bucket is useful for creating group values, which can be passed to group operators as input."""
    # TODO 等官方提供原生功能
    return x.map_batches(lambda x1: Series(_qcut(x1, q), nan_to_null=True, dtype=Int16))


def cumulative_returns(returns: np.ndarray, weights: np.ndarray,
                       period: int = 3, is_mean: bool = True,
                       benchmark: np.ndarray = None) -> np.ndarray:
    """累积收益

    精确计算收益是非常麻烦的事情，比如考虑手续费、滑点、涨跌停无法入场。考虑过多也会导致计算量巨大。
    这里只做估算，用于不同因子之间收益比较基本够用。更精确的计算请使用专用的回测引擎

    需求：因子每天更新，但策略是持仓3天
    1. 每3天取一次因子，并持有3天。即入场时间对净值影响很大。净值波动剧烈
    2. 资金分成3份，每天入场一份。每份隔3天做一次调仓，多份资金不共享。净值波动平滑

    本函数使用的第2种方法，例如：某支股票持仓信息如下
    [0,1,1,1,0,0]
    资金分成三份，每次持有三天，
    [0,0,0,1,1,1] # 第0、3、6...位，fill后两格
    [0,1,1,1,0,0] # 第1、4、7...位，fill后两格
    [0,0,1,1,1,0] # 第2、5、8...位，fill后两格

    之后就是weights*returns就是每期的收益率，横截面mean后就是这份资金每天的收益率。+1再cumprod就是这份资金的净值
    最后多份资金直接平均，就是总的净值

    weights*returns做了period轮
    cumprod计算了period次

    Parameters
    ----------
    returns: np.ndarray
        1期简单收益率。自动记在出场位置。
    weights: np.ndarray
        持仓权重。需要将信号移动到出场日期
    period: int
        持有期数。即资金拆成多少份
    is_mean:
        权重处理方式。
        - True 表示等权，weights的取值为-1,0,1
        - False 表示在外指定权重。weights的取值为-1~1,weights.abs().sum(axis=1)==1
    benchmark: 1d np.ndarray
        基准收益率

    Returns
    -------
    np.ndarray

    References
    ----------
    https://github.com/quantopian/alphalens/issues/187

    """
    # 修正数据中出现的nan
    returns = np.where(returns == returns, returns, 0.0)
    weights = np.where(weights == weights, weights, 0.0)
    # 一维修改成二维，代码统一
    if returns.ndim == 1:
        returns = returns.reshape(-1, 1)
    if weights.ndim == 1:
        weights = weights.reshape(-1, 1)

    # 形状
    m, n = weights.shape

    #  记录每份资金每期收益率
    out = _sub_portfolio_returns(m, n, weights, returns, period, is_mean)

    if benchmark is None:
        # 多份净值直接叠加后平均
        return (out + 1).cumprod(axis=0).mean(axis=1)
    else:
        # 有基准，计算超额收益
        return (out + 1).cumprod(axis=0).mean(axis=1) - (benchmark + 1).cumprod()