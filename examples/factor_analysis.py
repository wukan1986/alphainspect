"""
单因子分析

1. 先根据因子值，对股票进行分层
2. 对分层后的股票，计算因子值的描述性统计
3. 对分层后的股票，计算对应收益的描述性统计
4. 对分层后的股票，计算IC，IC的描述性统计

"""
# %%
import os
import sys
from pathlib import Path

# 修改当前目录到上层目录，方便跨不同IDE中使用
pwd = str(Path(__file__).parents[1])
os.chdir(pwd)
sys.path.append(pwd)
# ===============
# %%
import matplotlib.pyplot as plt
import polars as pl

from alphainspect.reports import create_1x3_sheet, create_3x2_sheet
from alphainspect.plotting import create_describe1_sheet
from alphainspect.utils import with_factor_quantile, with_factor_top_k  # noqa

# %% 加载数据
df = pl.read_parquet('data/data.parquet')

factor = 'SMA_010'  # 考察因子
forward_returns = ['RETURN_CC_01', 'RETURN_OO_01', 'RETURN_OO_02', 'RETURN_OO_05']  # 同一因子，不同持有期对比

# %% 因子值分层
# df = with_factor_quantile(df, factor, quantiles=10, factor_quantile='_fq_1')
df = with_factor_top_k(df, factor, top_k=20, factor_quantile='_fq_1')

# %% 分组后因子值的描述性统计
create_describe1_sheet(df, [factor], factor_quantile='_fq_1')
# %% 对应收益的描述性统计
create_describe1_sheet(df, forward_returns, factor_quantile='_fq_1')

# %% IC统计
axvlines = ('2020-01-01', '2024-01-01',)

# 有多个，挑一个显示
for fwd_ret_1 in forward_returns[0:1]:
    fig, ic_dict, hist_dict, cum, avg, std = create_1x3_sheet(df, factor, fwd_ret_1, factor_quantile='_fq_1', axvlines=axvlines)

# %% 画比较全的图
create_3x2_sheet(df, factor, fwd_ret_1, factor_quantile='_fq_1', axvlines=axvlines)

# %%
plt.show()

# %%
