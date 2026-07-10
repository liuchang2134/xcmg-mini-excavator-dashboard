# 原始数据目录

原始 Excel 统一保存在 `source-excel/`。既有小挖文件沿用以下命名：

`XCMG_<吨级>_mini_excavator_competitor_source.xlsx`

12 吨以上页面使用：

`XCMG_<吨级>_excavator_competitor_source.xlsx`

| 文件 | 对应看板 | 原始输入 |
| --- | --- | --- |
| `source-excel/XCMG_1-2t_mini_excavator_competitor_source.xlsx` | 1-2 吨级挖掘机 | `1-2.xlsx` |
| `source-excel/XCMG_2-3t_mini_excavator_competitor_source.xlsx` | 2-3 吨级挖掘机 | `2-3.xlsx` |
| `source-excel/XCMG_3.5t_mini_excavator_competitor_source.xlsx` | 3.5 吨级挖掘机 | 既有 3.5 吨数据表 |
| `source-excel/XCMG_4-5t_mini_excavator_competitor_source.xlsx` | 4-5 吨级挖掘机 | `4-5.xlsx` |
| `source-excel/XCMG_5-6t_mini_excavator_competitor_source.xlsx` | 5-6 吨级挖掘机 | `5-6.xlsx` |
| `source-excel/XCMG_7-8t_mini_excavator_competitor_source.xlsx` | 7-8 吨级挖掘机 | `7-8 无动臂偏摆.xlsx` |
| `source-excel/XCMG_8-10t_mini_excavator_competitor_source.xlsx` | 8-10 吨级挖掘机 | 修订版 `8-10 1.xlsx` |
| `source-excel/XCMG_12-14t_excavator_competitor_source.xlsx` | 12-14 吨级挖掘机 | `12-14.xlsx` |
| `source-excel/XCMG_14-16t_short_tail_excavator_competitor_source.xlsx` | 14-16 吨级短尾挖掘机 | `14-16短尾.xlsx` |

`source-register.csv` 用于登记每个数据集的市场版本、外部来源和核验状态。当前未填写的厂家资料不得自动推断；页面中的空白配置按“待核验”处理，不自动等同于“无配置”。
