# 原始数据目录

原始 Excel 统一保存在 `source-excel/`，文件命名规则为：

`XCMG_<吨级>_mini_excavator_competitor_source.xlsx`

| 文件 | 对应看板 | 原始输入 |
| --- | --- | --- |
| `source-excel/XCMG_1-2t_mini_excavator_competitor_source.xlsx` | 1-2 吨级挖掘机 | 用户提供 `1-2.xlsx` |
| `source-excel/XCMG_2-3t_mini_excavator_competitor_source.xlsx` | 2-3 吨级挖掘机 | 用户提供 `2-3.xlsx` |
| `source-excel/XCMG_3.5t_mini_excavator_competitor_source.xlsx` | 3.5 吨级挖掘机 | 既有 3.5 吨数据表 |
| `source-excel/XCMG_4-5t_mini_excavator_competitor_source.xlsx` | 4-5 吨级挖掘机 | 用户提供 `4-5.xlsx` |
| `source-excel/XCMG_5-6t_mini_excavator_competitor_source.xlsx` | 5-6 吨级挖掘机 | 用户提供 `5-6.xlsx` |
| `source-excel/XCMG_7-8t_mini_excavator_competitor_source.xlsx` | 7-8 吨级挖掘机 | 用户提供 `7-8 无动臂偏摆.xlsx` |
| `source-excel/XCMG_8-10t_mini_excavator_competitor_source.xlsx` | 8-10 吨级挖掘机 | 用户提供 `8-10.xlsx` |

`source-register.csv` 用于登记每个数据集的市场版本、外部来源和核验状态。当前未填写的厂家资料不得自动推断；页面中的空白配置按“待核验”处理，不自动等同于“无配置”。
