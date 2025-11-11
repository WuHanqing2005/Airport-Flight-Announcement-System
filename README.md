# Airport Flight Announcement System / 机场航班广播系统

Airport Flight Announcement System — an offline GUI tool that composes and plays airport announcements by stitching high‑quality WAV voice packs.  
离线可用的机场广播系统——通过拼接高质量 WAV 语音包来合成并播放机场广播，并提供可视化图形界面。

---

## About the Author / 关于作者

- Author / 作者: Wu Hanqing (Daniel) / 吴瀚庆（Daniel）  
- Vision / 初衷: Make airport audio operations reliable, efficient, and easy for non‑technical staff / 让机场广播生成更稳定高效，便于非技术人员使用  
- Copyright / 版权: All rights reserved by Wu Hanqing / 版权所有 © 吴瀚庆  
- License Note / 许可声明: Unauthorized use or redistribution is prohibited; infringement will be pursued / 未经允许禁止使用或传播，侵权必究  
- Appreciation / 致谢: Your feedback drives improvement / 感谢您的反馈使项目不断进步

---

## Basic Information / 基本信息

| Item | English | 中文 |
| ---- | ------- | ---- |
| Software Name | Airport Flight Announcement System | 航班广播语音系统 |
| Version | 2025.10.22 | 2025.10.22 |
| Copyright Holder | Wu Hanqing | 吴瀚庆 |
| License Statement | Unauthorized use prohibited; infringement will be prosecuted | 未经允许禁止盗用，侵权必究 |

---

## Contact / 联系方式

- WeChat / 微信: Daniel_Qinghan  
- Phone / 手机: +86-195-2887-3640 ; +82-010-7435-5296  
- Email / 邮箱: wuhanqing2005@gmail.com  

Welcome to reach out for cooperation, feature requests, and voice pack customization. / 欢迎就合作、功能需求及语音包定制联系我。

---

## Table of Contents / 目录

1. Features / 功能特性  
2. System Requirements / 系统要求  
3. Installation / 安装部署  
4. Quick Start / 快速上手  
5. Data Model & Fields / 数据模型与字段说明  
6. GUI Overview & Operations / 界面总览与操作指南  
7. Broadcast Types & Examples / 广播类型与示例文本  
8. File & Folder Structure / 目录与文件结构  
9. Voice Pack Rules / 语音包规范  
10. Best Practices / 使用建议与注意事项  
11. Troubleshooting & FAQ / 故障排查与常见问题  
12. Backup & Data Safety / 备份与数据安全  
13. Roadmap / 开发路线图  
14. Contributing / 贡献方式  
15. License & Disclaimer / 许可与声明  
16. Changelog / 更新日志  
17. Appendix: Data Entry Tips / 附录：数据录入技巧  

---

## 1. Features / 功能特性

- Offline synthesis via stitching WAV units (no external TTS) / 通过拼接 WAV 单元离线合成（无需外部 TTS）  
- GUI built with tkinter (progress bar + error dialogs) / 基于 tkinter 的 GUI（含进度条 + 可视化报错）  
- Persistent Excel storage (data/data.xlsx) / Excel 文件持久化存储（data/data.xlsx）  
- Multi-language: CN + EN (+ optional JA / KO) / 多语言：中英（可选日语 / 韩语）  
- Flexible counters & shared flights (ranges with "-", multi-flight with space) / 灵活值机柜台（“-”表示范围），共享航班号用空格  
- Multiple broadcast types (Check-in, Arrival, Baggage, Delay variants) / 多类广播（值机、到达、行李、延误类型）  
- Right-click context menu for play/edit/delete (since 2025-10-01) / 右键菜单快捷播放/编辑/删除（2025-10-01 起）  
- Stop-all-processes button / “停止所有进程”按钮  
- Automatic stereo conversion for WAV / 自动转换语音包为双声道  
- Consistent output naming: FlightNumber-AnnouncementType.wav / 统一输出命名：航班号-广播类型.wav  

---

## 2. System Requirements / 系统要求

- OS: Windows 10/11 (recommended), macOS/Linux possible with proper environment / 操作系统：推荐 Windows 10/11，macOS/Linux 需保证依赖  
- Python: 3.8–3.12 supported / Python：支持 3.8–3.12  
- Dependencies: pandas, openpyxl, pydub, tkinter, standard libs / 依赖：pandas、openpyxl、pydub、tkinter、标准库  
- Audio: Stereo WAV (44.1kHz/48kHz recommended) / 音频：双声道 WAV（建议 44.1kHz/48kHz）  

---

## 3. Installation / 安装部署

Steps / 步骤:  
1. Clone or download the project / 克隆或下载项目  
2. Create virtual environment: `python -m venv .venv` & activate / 创建虚拟环境并激活  
3. Install dependencies: `pip install -r requirements.txt` / 安装依赖  
4. Ensure `data/`, `material/`, `output/` directories exist / 确认相关目录存在  
5. Run `main.py` or packaged executable / 运行 `main.py` 或打包可执行文件  

If using packaged EXE, Python setup is not required. / 若使用打包 EXE，无需安装 Python。

---

## 4. Quick Start / 快速上手

Workflow / 基本流程:  
1. Edit or add flight info / 编辑或添加航班信息  
2. Click “Save Info” to persist / 点击 “Save Info” 保存  
3. Choose broadcast type + language set / 选择广播类型与语言  
4. Generate or play; file appears in `output/` / 生成或播放；文件出现在 `output/`  

Right-click menu allows fast play/edit/delete. / 右键菜单可快速播放/编辑/删除。  
Default demo flights: MU2546, MU1278, CA630, CZ628 / 默认示例航班：MU2546、MU1278、CA630、CZ628。

---

## 5. Data Model & Fields / 数据模型与字段说明

Stored in `data/data.xlsx`. / 存储于 `data/data.xlsx`。

| Index | Field (EN) | 字段(中文) | Description / 说明 |
| ----- | ---------- | ---------- | ------------------ |
| 0 | Flight Number | 航班号 | e.g. CZ627 |
| 1 | Departure | 出发地 | 起飞机场/城市 |
| 2 | Stopover | 经停地 | 可为空 |
| 3 | Destination | 目的地 | 终到城市 |
| 4 | Divert | 备降机场 | 仅特殊情况 |
| 5 | Check-in Counter | 值机柜台 | 多柜台用“-” |
| 6 | Boarding Gate | 登机口号码 | 如 A12 |
| 7 | Baggage Claim | 行李转盘 | 转盘号 |
| 8 | Scheduled Arrival Time | 计划抵达时间 | 计划时间 |
| 9 | Estimated Arrival Time | 预计抵达时间 | 更新预测 |
| 10 | Delay Reason | 延误原因 | 语音包需匹配 |
| 11 | Language | 语言类型 | 中英 / 中英日 / 中英韩 |

Shared flights separated by space; counters use hyphen range. / 共享航班用空格分隔；柜台范围用连字符表示。

---

## 6. GUI Overview & Operations / 界面与操作指南

- Left Panel: Add Flight / Delete Flight / Play Announcement  
  左侧：添加航班 / 删除航班 / 播放广播  
- Right Panel: Clear / Read Info / Save Info  
  右侧：清除 / 读取信息 / 保存信息  
- Progress bar + error dialog feedback / 进度条 + 报错弹窗  
- Stop All Processes button / 停止所有进程按钮  
- Right-click (Play/Edit/Delete) / 右键（播放/编辑/删除）  
- Login screen + Exit button / 登录界面 + 退出按钮  

Tip: After editing, click “Save Info”; if gate/baggage looks wrong, click “Read Info”.  
提示：编辑后请“Save Info”；登机口或行李转盘异常时点“Read Info”。

---

## 7. Broadcast Types & Examples / 广播类型与示例

Types / 类型:  
1. Check-in / 值机广播  
2. Arrival / 到达广播  
3. Baggage Claim / 行李提取广播  
4. Departure Delay Determined / 出发延误已定  
5. Departure Delay Undetermined / 出发延误未定  
6. Arrival Delay Determined / 到达延误已定  
7. Arrival Delay Undetermined / 到达延误未定  

Example (Check-in) / 示例（值机广播）:  
- CN: 乘坐 中国南方航空公司 CZ627 次航班，从 沈阳 前往 东京 的旅客请注意。您乘坐的航班现在开始办理乘机手续，请前往 F01 至 F06 号柜台办理，谢谢！  
- EN: May I have your attention please! We are now ready for check-in for China Southern Airlines Flight CZ627 from Shenyang to Tokyo Narita at check-in counter number F01 to F06. Thank you!  
- JA (optional / 可选): ご案内申し上げます...（略）  

Example (Arrival) / 示例（到达广播）:  
- CN: 迎接旅客的各位请注意，从 东京 飞来的 中国南方航空公司 CZ627 次航班，已经到达本站，请您在到达大厅等候接待，谢谢！  
- EN: May I have your attention please. China Southern Airlines Flight CZ627 with service from Tokyo Narita has arrived. Thank you!  

Example (Baggage Claim) / 示例（行李提取）:  
- CN: 乘坐 上海航空公司 FM9499 次航班，从 郑州 到达本站的旅客请注意。请前往 8 号行李转盘提取您的行李，谢谢！  
- EN: May I have your attention please. Arriving passengers on Shanghai Airlines Flight FM9499 from Zhengzhou. Your baggage will be available at baggage claim 8. Thank you.  

Templates validated; city voice pack presence auto-checked. / 模板已验证；城市语音包有自动存在性检测。

---

## 8. File & Folder Structure / 目录与文件结构

Below is the current repository layout (Poetry-managed Python project).  
以下为当前仓库结构（使用 Poetry 进行包管理）。

```
Airport-Flight-Announcement-System/
├── pyproject.toml                  # Poetry project config: metadata, dependencies
│                                   # Poetry 项目配置：元数据与依赖声明
├── poetry.lock                     # Locked exact dependency versions
│                                   # 锁定依赖版本（保证可复现）
├── README.md                       # Project documentation / 项目说明文档
├── .gitignore                      # Git ignore rules / Git 忽略规则
├── application.log                 # Application runtime log (may rotate)
│                                   # 运行日志（可能滚动）
├── src/                            # Source code root (per Poetry's src layout)
│   └── airport_flight_announcement_system/   # Main package (modules here)
│       ├── __init__.py             # Package initializer / 包初始化
│       └── ...                     # Other Python modules / 其它核心模块
├── data/                           # Primary flight data storage (Excel, etc.)
│                                   # 主要航班数据（如 data.xlsx）
├── data_copy/                      # Manual or automated backups of data/
│                                   # data/ 目录的备份
├── material/                       # Voice pack resources (WAV units)
│   ├── airlines_cn/                # Airline names (CN) / 航空公司中文
│   ├── alnum_cn/                   # Alphanumeric units (CN) / 数字字母中文
│   ├── cityname_cn/                # City names (CN) / 城市名称中文
│   ├── template_cn/                # Chinese sentence templates / 中文模板
│   ├── template_en/                # English sentence templates / 英文模板
│   ├── template_ja/                # Japanese sentence templates / 日文模板
│   └── delay_reason_cn/            # Delay reason units (CN) / 延误原因
├── static/                         # Static frontend assets (CSS/JS/img)
│                                   # 前端静态资源（CSS/JS/图片）
├── templates/                      # HTML / GUI template files
│                                   # HTML/界面模板文件
├── tests/                          # Automated tests (unit/integration)
│                                   # 自动化测试（单元/集成）
└── output/                         # Generated announcement WAV files (not committed)
                                    # 运行时生成的广播音频目录（通常不入库）
```

---

## 9. Voice Pack Rules / 语音包规范

- Format: WAV only / 仅支持 WAV  
- Channels: Stereo required (auto-conversion supported) / 必须双声道（支持自动转换）  
- Do not arbitrarily rename/remove / 禁止随意重命名或删除  
- Contact author for new units / 新语音请联系作者合成  
- Categories: airline / alnum / city / template / delay / 分类含：航空公司、数字字母、城市、模板、延误原因  

---

## 10. Best Practices / 使用建议

- Do not modify internal folders unless instructed / 未经指示勿改内部目录  
- Black console may appear during synthesis (30–60s) / 合成时可能出现黑色控制台（30–60 秒）  
- Output naming: FlightNumber-AnnouncementType.wav / 输出命名：航班号-广播类型.wav  
- Refresh with “Read Info” if display anomaly / 显示异常用“Read Info”刷新  
- Use standardized flight number format (e.g. MU1278) / 使用规范航班号格式（如 MU1278）  

---

## 11. Troubleshooting & FAQ / 故障排查与常见问题

| Issue / 问题 | Cause / 可能原因 | Solution / 解决方案 |
| ------------ | ---------------- | ------------------- |
| WinError 2 | Missing file / 文件缺失 | Check voice pack paths / 检查语音包路径 |
| Non-stereo WAV | Source mono / 源文件单声道 | Auto-convert; re-provide HQ source / 自动转换或重新提供文件 |
| Excel cannot save | File locked / 文件占用 | Close Excel then retry / 关闭占用后重试 |
| City name not spoken | Missing voice unit / 语音单元缺失 | Add pack via author / 联系作者补充 |
| Shared flight not parsed | Format error / 格式错误 | Use space separation / 用空格分隔 |
| Counter range wrong | Hyphen misuse / 连字符误用 | Use F01-F06 format / 使用 F01-F06 |

---

## 12. Backup & Data Safety / 备份与安全

- Regularly copy `data/data.xlsx` to `data_copy/` / 定期复制 data.xlsx 到 data_copy/  
- Version control for `output/` if auditing required / 可对 output/ 做版本管理  
- Preserve error logs for diagnostics / 保存错误日志用于诊断  

---

## 13. Roadmap / 开发路线图

- More multilingual packs / 扩展多语言包  
- Custom template editor / 模板编辑器  
- Batch generation & scheduling / 批量与定时广播  
- Richer metadata (aircraft, stand, changes) / 更多元数据（机型、机位、变更）  
- Automatic updater / 自动更新机制  

---

## 14. Contributing / 贡献方式

- Contact author for feature requests / 功能需求请联系作者  
- Discuss before submitting patches / 修改前需沟通  
- Provide reproducible steps & logs / 提供复现步骤与日志  

---

## 15. License & Disclaimer / 许可与声明

- All rights reserved / 版权所有  
- No unauthorized redistribution / 禁止未授权传播  
- Infringement pursued legally / 侵权必究  
- Provided “as is”; use at own risk / 按“现状”提供；风险自负  

---

## 16. Update Log / 更新日志

### 2024.04.02
`Project initiated; switched from Google TTS to WAV stitching; first tkinter GUI`
`项目启动；由谷歌 TTS 改为 WAV 拼接；首版 tkinter GUI`

### 2024.04.04
`Bug fixes`
`修复若干问题`

### 2024.04.05
`Counter range logic improved; visual error dialogs added`
`值机柜台范围逻辑改进；新增可视化报错`

### 2024.04.06
`English check-in opening sentences; input validation; voice refinement via reecho.ai`
`英文句型前两句；输入校验；使用 reecho.ai 优化语音`
### 2024.04.07
`Completed English templates; city pack existence check; Japanese check-in templates`
`完善英文模板；检测城市语音包；新增日语值机句型`

### 2024.04.08
`Added Boarding Gate & Baggage Claim; manual city input; Shanghai district packs (CN/EN/JA)`
`新增登机口与行李转盘；手动城市输入；上海各区中英日语音库`

### 2024.04.10
`Logic & comments improved; example flights updated`
`优化逻辑与注释；更新示例航班`

### 2024.04.11
`Removed unused code; generate text transcript with audio`
`删除无用代码；生成文本与音频`

### 2024.04.17
`Framework for broadcast type selection`
`广播类型选择框架`

### 2024.04.26
`Added language combinations (CN-EN / CN-EN-JA / CN-EN-KO); stronger checks; path & naming adjusted; added MU1278`
`增加语言组合；增强检查；修改输出路径与命名；新增 MU1278`

### 2024.04.27
`Migrated to Visual Studio; persistent Excel storage`
`迁移至 Visual Studio；Excel 持久化`

### 2024.04.28
`Added try…except per function; improved error hints; portable paths; “Stop All Processes” button`
`函数加 try…except；优化报错；路径跨平台；新增“停止所有进程”`

### 2024.04.29
`Login UI beautified; arrival with stopover improved; error logs; progress bar`
`美化登录；完善经停到达；错误日志；进度条`

### 2024.04.30
`Shared flights supported (space-separated); English arrival added`
`支持共享航班；补全到达英文部分`

### 2024.05.01
`Switched interface to English; voice file renaming to EN`
`界面改为英文；语音文件英文化`

### 2024.05.02
`Python interpreter compatibility adjustments`
`调整解释器兼容性`

### 2024.05.05
`Fixed WinError 2; all packs stereo; improved `refresh_table()` `
`修复 WinError2；全部语音包双声道；完善 `refresh_table()` `

### 2024.05.06
`Auto stereo conversion feature`
`自动双声道转换功能`

### 2024.05.20
`Added more voice resources`
`新增语音资源`

### 2024.06.14
`Added Exit on login; UI improved`
`登录界面新增退出；界面美化`

### 2024.10.27
`Fixed saving; re-synthesized some packs with GPT-SoVITS`
`修复保存问题；用 GPT-SoVITS 重合成部分语音`

### 2024.11.11
`Added Divert / Scheduled / Estimated / Delay Reason fields; 12-column UI; debugging state`
`新增备降/计划/预计/延误原因字段；界面 12 列；调试中`

### 2025.10.01
`Added right-click context menu; Save Info success toast`
`新增右键菜单；保存成功提示`

### 2025.11.11
`Converted project to a hybrid Python + Web architecture (desktop logic + browser UI); adopted Poetry for dependency & environment management; reorganized code into src/ package layout; integrated templates/static for web front-end; updated README (file structure + install section) for Poetry workflow; prepared groundwork for future test suite.`
`项目升级为 Python + Web 混合架构（桌面逻辑 + 浏览器界面）；采用 Poetry 管理依赖与环境；重构代码为 src/ 包布局；整合 templates/static 目录用于 Web 前端；更新 README（目录结构与安装部分）以适配 Poetry 工作流；为后续测试框架预留结构。`


---

## 17. Appendix: Data Entry Tips / 附录：数据录入技巧

- Flight Number: Uppercase letters + digits (e.g. CZ627) / 航班号：大写字母+数字（如 CZ627）  
- Counters: Use range F01-F06 or list segments / 柜台：使用范围如 F01-F06  
- Shared Flights: Separate by spaces (CZ627 KL1234) / 共享航班：用空格分隔（如 CZ627 KL1234）  
- Delay Reason: Use standardized vocabulary / 延误原因：使用标准词汇（与语音包一致）  
- Language: Select supported combination (CN-EN / CN-EN-JA / CN-EN-KO) / 语言类型：按需选择支持组合  

---

Thank you for using Airport Flight Announcement System! / 感谢使用航班广播语音系统！