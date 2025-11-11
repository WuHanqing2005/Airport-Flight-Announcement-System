# Airport-Flight-Announcement-System
# 机场广播系统

Airport Flight Announcement System — an offline, GUI-based tool to compose and play airport announcements by stitching high‑quality WAV voice packs.  
离线可用的机场广播系统——通过拼接高质量 WAV 语音包合成并播放机场广播，提供可视化图形界面。

---

## About the Author
## 关于作者

- Author: Wu Hanqing (Daniel) — Original creator and maintainer  
- 作者：吴瀚庆（Daniel）— 本项目原创作者与维护者

- Vision: Make airport audio operations reliable, efficient, and friendly for non‑technical staff  
- 初衷：让机场广播生成更稳定高效，便于非技术人员上手使用

- Copyright: All rights reserved by Wu Hanqing  
- 版权：版权所有 © 吴瀚庆

- License note: Unauthorized use or redistribution is strictly prohibited; infringement will be pursued  
- 许可声明：未经允许，禁止盗用或传播，侵权必究

- Thanks: Your feedback keeps this project improving.  
- 致谢：感谢您提出宝贵意见，您的反馈让项目持续变好。

---

## Basic Information
## 基本信息

- Software Name: Airport Flight Announcement System  
- 软件名称：航班广播语音系统

- Version: 2025.10.22  
- 版本号：2025.10.22

- Copyright Holder: Wu Hanqing  
- 版权归属：吴瀚庆

- License Statement: Unauthorized use is prohibited; infringement will be prosecuted  
- 许可声明：未经允许，禁止盗用，侵权必究

---

## Contact
## 联系方式

- WeChat: Daniel_Qinghan  
- 微信：Daniel_Qinghan

- Phone: +86-195-2887-3640; +82-010-5861-5296  
- 手机：+86-195-2887-3640；+82-010-5861-5296

- Email: wuhanqing2005@gmail.com  
- 邮箱：wuhanqing2005@gmail.com

Welcome to reach out for cooperation, feature requests, and voice pack customization.  
欢迎就合作、功能需求及语音包定制联系我。

---

## Table of Contents
## 目录

1. Features  
2. System Requirements  
3. Installation  
4. Quick Start  
5. Data Model and Fields  
6. GUI Overview and Operations  
7. Broadcast Types and Examples  
8. File and Folder Structure  
9. Voice Pack Rules and Updates  
10. Best Practices and Notes  
11. Troubleshooting and FAQ  
12. Backup and Data Safety  
13. Roadmap  
14. Contributing  
15. License and Disclaimer  
16. Changelog (reserved at the end)

1. 功能特性  
2. 系统要求  
3. 安装部署  
4. 快速上手  
5. 数据模型与字段说明  
6. 界面总览与操作指南  
7. 广播类型与文本示例  
8. 目录与文件结构  
9. 语音包规范与更新  
10. 使用建议与注意事项  
11. 故障排查与常见问题  
12. 备份与数据安全  
13. 开发路线图  
14. 贡献方式  
15. 许可与声明  
16. 更新日志（文末预留）

---

## 1) Features
## 1) 功能特性

- Offline synthesis by stitching WAV voice units; no external TTS dependency  
- 通过拼接 WAV 语音单元离线合成，无需外网 TTS 依赖

- Clean GUI built with tkinter; supports progress bar and error dialogs  
- 基于 tkinter 的图形界面，含进度条与可视化报错窗口

- Persistent storage in Excel (data/data.xlsx); easy audit and editing  
- Excel 文件（data/data.xlsx）持久化存储，便于审计与编辑

- Multi-language announcements: Chinese + English (+ optional Japanese/Korean)  
- 多语言广播：中英组合（可选加入日语/韩语）

- Flexible counters and shared flights: F01-F06, multiple counters via “-”, shared numbers via space  
- 灵活值机柜台与共享航班：F01-F06；多个柜台用“-”；多个航班号用空格

- Multiple broadcast types: Check-in, Arrival, Baggage Claim, and various Delay templates  
- 多类广播：值机、到达、行李提取及多种延误模板

- Right-click context menu for quick play/edit/delete (since 2025-10-01)  
- 右键菜单快捷播放/编辑/删除（自 2025-10-01 起）

- Stop-all-processes button, detailed logging, and automatic stereo conversion for WAV  
- “停止所有进程”按钮、详细错误日志、自动将语音包转换为双声道

- Output WAV saved with consistent naming: FlightNumber-AnnouncementType.wav  
- 统一命名规则输出：航班号-广播类型.wav

---

## 2) System Requirements
## 2) 系统要求

- OS: Windows 10/11 recommended (primary target), macOS/Linux possible with compatible environment  
- 操作系统：推荐 Windows 10/11（主要目标），macOS/Linux 需保证依赖环境兼容

- Python: 3.8–3.12 (project adjusted for interpreter compatibility)  
- Python：3.8–3.12（已考虑解释器兼容性）

- Dependencies: pandas, openpyxl, pydub (or equivalent), tkinter (bundled), standard library  
- 依赖：pandas、openpyxl、pydub（或同类）、tkinter（随 Python 提供）、标准库

- Audio: WAV voice packs must be stereo, 44.1kHz/48kHz recommended  
- 音频：WAV 语音包需为双声道，建议 44.1kHz/48kHz 采样率

---

## 3) Installation
## 3) 安装部署

- Recommended: Use a virtual environment, then install dependencies  
- 推荐：使用虚拟环境，随后安装依赖

- Steps  
- 步骤  
  1) Clone or download the project  
  1) 克隆或下载本项目  
  2) Create venv: python -m venv .venv && activate  
  2) 创建虚拟环境：python -m venv .venv 并激活  
  3) Install deps: pip install -r requirements.txt (if provided)  
  3) 安装依赖：pip install -r requirements.txt（如提供）  
  4) Ensure data/, material/, output/ exist and contain required files  
  4) 确认 data/、material/、output/ 目录存在且资源齐全

- If you run packaged executable, no Python setup is required  
- 如使用打包可执行程序，无需单独安装 Python

---

## 4) Quick Start
## 4) 快速上手

- Launch the app: run main.py or the packaged EXE  
- 启动程序：运行 main.py 或双击打包的 EXE

- Default flights are preloaded for demo: MU2546, MU1278, CA630, CZ628  
- 默认包含示例航班：MU2546、MU1278、CA630、CZ628

- Basic workflow  
- 基本流程  
  1) Add or edit flight info in the table or via input fields  
  1) 在表格或输入区添加/编辑航班信息  
  2) Save Info to persist into data/data.xlsx  
  2) 点击 Save Info 保存至 data/data.xlsx  
  3) Select a broadcast type and language combination  
  3) 选择广播类型与语言组合  
  4) Play or generate; output WAV appears in output/  
  4) 播放或生成；输出 WAV 文件保存在 output/

- Use right-click menu to play/edit/delete quickly (since 2025-10-01)  
- 可通过右键菜单快速播放/编辑/删除（自 2025-10-01 起）

---

## 5) Data Model and Fields
## 5) 数据模型与字段说明

All flight information is stored in data/data.xlsx.  
所有航班数据存储于 data/data.xlsx。

Field index and meaning:  
字段索引与含义：

| Index (索引) | Field (字段) | Description (说明) |
| --- | --- | --- |
| 0 | Flight Number | 航班号 |
| 1 | Departure | 出发地 |
| 2 | Stopover | 经停地 |
| 3 | Destination | 目的地 |
| 4 | Divert | 备降机场 |
| 5 | Check-in Counter | 值机柜台（多柜台用“-”） |
| 6 | Boarding Gate | 登机口号码 |
| 7 | Baggage Claim | 行李提取处（转盘号） |
| 8 | Scheduled Arrival Time | 计划抵达时间 |
| 9 | Estimated Arrival Time | 预计抵达时间 |
| 10 | Delay Reason | 延误原因 |
| 11 | Language | 语言类型（中英/中英日/中英韩） |

Notes: Shared flight numbers separated by spaces; counters like “F01-F06”.  
备注：共享航班号用空格分隔；多个值机柜台如“F01-F06”。

---

## 6) GUI Overview and Operations
## 6) 界面总览与操作指南

- Left action area: Add Flight, Delete Flight, Play Announcement  
- 左侧功能区：添加航班、删除航班、播放广播

- Right action area: Clear, Read Info, Save Info  
- 右侧功能区：清除、读取信息、保存信息

- Status feedback: Progress bar; error dialogs with details  
- 状态反馈：进度条；详细错误提示窗口

- Stop All Processes button to halt running tasks safely  
- “停止所有进程”按钮可安全终止当前任务

- Right-click menu (since 2025-10-01): Play / Edit / Delete  
- 右键菜单（2025-10-01 起）：播放 / 修改 / 删除

- Login screen polish and Exit button; workspace UI optimized  
- 登录界面美化与退出按钮；工作区界面优化

Tips: After editing, click Save Info; if gate or baggage carousel looks wrong, click Read Info to refresh.  
提示：编辑后请保存；登机口或行李转盘显示异常时，点击 Read Info 重新读取。

---

## 7) Broadcast Types and Examples
## 7) 广播类型与文本示例

Supported types include (examples below):  
支持的广播类型（部分示例如下）：

- 1. Check-in  
- 1. 值机广播（Check_in）

- 2. Arrival  
- 2. 到达广播（Arrival）

- 3. Baggage Claim  
- 3. 行李提取广播（Baggage_Claim）

- 4. Departure Delay Determined  
- 4. 出发延误已定（Departure_Delay_Determined）

- 5. Departure Delay Undetermined  
- 5. 出发延误未定（Departure_Delay_Undetermined）

- 6. Arrival Delay Determined  
- 6. 到达延误已定（Arrival_Delay_Determined）

- 7. Arrival Delay Undetermined  
- 7. 到达延误未定（Arrival_Delay_Undetermined）

Example 1 — Check-in  
示例 1 — 值机广播（Check_in）

- Chinese:  
乘坐 中国南方航空公司 CZ627 次航班，从 沈阳 前往 东京 的旅客请注意。您乘坐的航班现在开始办理乘机手续，请前往 F01 至 F06 号柜台办理，谢谢！
- 中文：

- English:  
May I have your attention please! We are now ready for check-in for, China Southern Airlines, Flight CZ627, From Shenyang to Tokyo Narita, at check-in counter number F01 to F06. Thank you!
- 英文：

- Japanese (if enabled):  
ご案内申し上げます，ただいまから チェックイン(Check-in) を開始いたします。中国南方航空627便，審陽 発 東京成田 ゆきにご搭乗の客様は，チェックイン カウンター (Check-in Counter) 番号 F01 から F06，までお進みください。
- 日语（如开启）：

Example 2 — Arrival  
示例 2 — 到达广播（Arrival）

- Chinese:  
迎接旅客的各位请注意，从 东京 飞来的 中国南方航空公司 CZ627 次航班，已经到达本站，请您在到达大厅等候接待，谢谢！
- 中文：

- English:  
May I have your attention please. China Southern Airlines, Flight CZ627 with service from Tokyo Narita has arrived. Thank you!
- 英文：

Example 3 — Baggage Claim  
示例 3 — 行李提取广播（Baggage_Claim）

- Chinese:  
乘坐 上海航空公司 FM9499 次航班，从 郑州 到达本站的旅客请注意。请前往 8 号行李转盘提取您的行李，谢谢！
- 中文：

- English:  
May I have your attention please. Arriving passengers on Shanghai Airlines. Flight FM9499 with service from Zhengzhou. Your baggage will be available at baggage claim 8, thank you.
- 英文：

Notes: English and Japanese sentence templates are validated; city voice pack presence is checked.  
说明：英文、日文句型已完善；城市语音包存在性有检测。

---

## 8) File and Folder Structure
## 8) 目录与文件结构

Project root/  
项目根目录/

- data/ — flight data storage  
- data/ — 航班数据存储  
  - data.xlsx — main flight information file  
  - data.xlsx — 航班信息文件

- data_copy/ — data backup  
- data_copy/ — 数据备份

- material/ — voice pack resources  
- material/ — 语音包资源  
  - airlines_cn/ — airline names (CN)  
  - airlines_cn/ — 航空公司中文语音包  
  - alnum_cn/ — alphanumeric (CN)  
  - alnum_cn/ — 数字字母中文语音包  
  - cityname_cn/ — city names (CN)  
  - cityname_cn/ — 城市名称中文语音包  
  - template_cn/ — sentence templates (CN)  
  - template_cn/ — 中文模板语音  
  - template_en/ — sentence templates (EN)  
  - template_en/ — 英文模板语音  
  - template_ja/ — sentence templates (JA)  
  - template_ja/ — 日文模板语音  
  - delay_reason_cn/ — delay reasons (CN)  
  - delay_reason_cn/ — 延误原因语音包

- output/ — generated announcements (WAV)  
- output/ — 输出目录（生成的广播 WAV 文件）

---

## 9) Voice Pack Rules and Updates
## 9) 语音包规范与更新

- Only WAV format is supported; stereo required  
- 仅支持 WAV 格式；必须为双声道

- The app auto-converts to stereo if needed  
- 程序可自动转换为双声道（如需）

- Keep file names consistent; do not rename/remove folders arbitrarily  
- 保持文件命名规范；切勿随意改名或删除目录

- For new voice units, contact the author for synthesis and placement guidance  
- 新语音单元请联系作者获取并指导放置路径

- Typical structure includes airlines, alnum, city names, templates, delay reasons  
- 常见分类包括航空公司、数字字母、城市名、句型模板、延误原因

---

## 10) Best Practices and Notes
## 10) 使用建议与注意事项

- Do not modify folders/files under the app directory unless instructed  
- 请勿擅自修改软件目录下的任何文件夹与文件

- Black console windows may pop up during synthesis; please wait 30–60s  
- 合成时可能弹出黑色窗口，请耐心等待 30–60 秒

- Output naming: FlightNumber-AnnouncementType.wav under output/  
- 输出命名：output/ 下“航班号-广播类型.wav”

- If gate/baggage numbers look off, click Read Info to refresh  
- 登机口/行李转盘显示异常时，请点击 Read Info

- Use English UI; voice packs gradually standardized to English filenames  
- 界面为英文；语音包文件名逐步统一为英文

---

## 11) Troubleshooting and FAQ
## 11) 故障排查与常见问题

- WinError 2 “The system cannot find the file specified”  
- WinError 2 “找不到指定文件”  
  - Ensure all required voice pack files exist and paths are correct  
  - 确认语音包齐全且路径正确  
  - Avoid non-ASCII or overly long paths for critical assets  
  - 关键资源路径避免特殊字符或过长  
  - Run with sufficient permissions  
  - 以足够权限运行程序

- WAV not stereo / inconsistent sample rate  
- WAV 非双声道 / 采样率不一致  
  - The app can convert to stereo; still standardize sources for best quality  
  - 程序可转双声道；源文件规范化更佳

- Excel file locked or cannot save  
- Excel 文件被占用或无法保存  
  - Close Excel viewer/editor; then click Save Info again  
  - 关闭占用程序后重试 Save Info

- City/airline name not announced  
- 城市/航空公司未播报  
  - Check corresponding voice unit presence  
  - 检查对应语音单元是否存在  
  - For missing items, contact author to add  
  - 缺失语音请联系作者补充

- Shared flights and counter formats  
- 共享航班与柜台格式  
  - Shared numbers separated by spaces; counters by “-”  
  - 共享航班用空格隔开；柜台用“-”

---

## 12) Backup and Data Safety
## 12) 备份与数据安全

- data_copy/ keeps backups; regularly copy data/data.xlsx here  
- data_copy/ 用于备份；建议定期复制 data/data.xlsx

- Version your output/ for traceability if needed  
- 可对 output/ 做版本管理，便于追溯

- Keep error logs for diagnostics when reporting issues  
- 保留错误日志以便问题诊断与反馈

---

## 13) Roadmap
## 13) 开发路线图

- Extended multilingual packs and locale formatting  
- 扩展多语言语音包与本地化格式

- Template editor for custom phrasing  
- 模板编辑器以支持自定义措辞

- Batch generation and scheduling  
- 批量生成与定时任务

- Richer metadata (e.g., aircraft type, stand, belt reassign)  
- 更丰富的元数据（机型、机位、转盘变更等）

- Packaging and auto-update channel for operators  
- 更完善的打包与更新分发机制

---

## 14) Contributing
## 14) 贡献方式

- For feedback and feature requests, contact the author  
- 反馈与需求请联系作者

- PRs may be accepted upon prior discussion (private repo/process)  
- 经沟通后可协助提交修改（私有流程为主）

- Please include reproducible steps, logs, and sample data  
- 请附上可复现步骤、日志与示例数据

---

## 15) License and Disclaimer
## 15) 许可与声明

- All rights reserved by Wu Hanqing  
- 版权所有 © 吴瀚庆

- Unauthorized use, redistribution, or commercial exploitation is prohibited  
- 未经允许禁止使用、传播或商业利用

- Infringements will be pursued according to law  
- 侵权必究

- The software is provided “as is”; use at your own risk  
- 本软件按“现状”提供；使用风险由使用者承担

---

## 16) Changelog (Historical and Reserved)
## 16) 更新日志（历史记录与预留）

Historical updates:  
历史更新：

- 2024.04.02  
  - Project initiated; deprecated Google TTS API approach  
  - 改用拼接 WAV 包合成；弃用谷歌 TTS  
  - Built tkinter GUI  
  - 初版 GUI 完成

- 2024.04.04  
  - Bug fixes  
  - 修复若干问题

- 2024.04.05  
  - Revised counter logic; support any range via “-”  
  - 修改值机柜台逻辑，支持“-”范围  
  - Visual error dialogs  
  - 可视化报错窗口

- 2024.04.06  
  - Added first two English check-in sentences  
  - 增加英文值机句型前两句  
  - Input validation (flight format, null checks)  
  - 增加输入校验  
  - Voice set refined via reecho.ai  
  - 用 reecho.ai 完善语音包

- 2024.04.07  
  - Completed English sentence packs  
  - 完善英文句型  
  - English city pack presence check  
  - 检测英文城市语音包存在性  
  - Added Japanese check-in templates  
  - 增加日语值机句型

- 2024.04.08  
  - Added “Boarding Gate” and “Baggage Claim” fields  
  - 新增“登机口”“行李提取”字段  
  - Manual city input  
  - 支持手动输入城市  
  - Added Shanghai districts CN/EN/JA libraries  
  - 增加上海各区中英日语音库

- 2024.04.10  
  - Improved logic and comments; updated example flights  
  - 完善判断逻辑与注释；修改示例航班

- 2024.04.11  
  - Removed unused code; generate text transcript with audio  
  - 删除无用代码；生成音频同时生成文本

- 2024.04.17  
  - Framework for broadcast type selection  
  - 增加广播类型选择框架

- 2024.04.26  
  - Language packs: CN+EN, CN+EN+JA, CN+EN+KO  
  - 增加语言种类选择（中英/中英日/中英韩）  
  - Strengthened input checks; adjusted output path and naming; added MU1278 demo  
  - 完善检查逻辑；调整输出路径与命名；新增 MU1278

- 2024.04.27  
  - Migrated to Visual Studio; data persisted in data.xlsx  
  - 迁移至 Visual Studio；持久化存储至 data.xlsx

- 2024.04.28  
  - try...except for each function; improved error prompts; os.path.join for portability; Stop All Processes button  
  - 各函数加 try...except；完善报错；路径用 os.path.join；新增“停止所有进程”

- 2024.04.29  
  - Polished login UI; improved arrival with stopover; error logs; progress bar  
  - 美化登录；完善经停到达；增加错误日志；进度条

- 2024.04.30  
  - Shared flights support (space-separated); arrival EN part added  
  - 支持共享航班（空格分隔）；补全到达英文

- 2024.05.01  
  - Switched to English UI; voice files renaming to EN  
  - 改为英文界面；语音文件名逐步英文化

- 2024.05.02  
  - Python interpreter compatibility adjustments  
  - 调整 Python 版本兼容性

- 2024.05.05  
  - Fixed WinError 2; made all packs stereo; refined refresh_table()  
  - 解决 WinError2；统一双声道；完善 refresh_table()

- 2024.05.06  
  - Auto stereo-conversion for voice packs  
  - 增加自动双声道转换

- 2024.05.20  
  - Added more voice resources  
  - 增加语音资源

- 2024.06.14  
  - Exit button on login; UI polish  
  - 登录界面增设退出；美化界面

- 2024.10.27  
  - Fixed saving flight info; re-synthesized some packs with GPT-SoVITS  
  - 修复保存问题；部分语音用 GPT-SoVITS 复刻

- 2024.11.11  
  - Added 4 fields: Divert, Scheduled/Estimated Arrival, Delay Reason; UI shows 12 columns; still in debugging (non-final)  
  - 新增 4 栏：备降、计划/预计抵达、延误原因；界面 12 列；调试中（非正式）

- 2025.10.01  
  - Added right-click context menu; Save Info success toast  
  - 新增右键菜单；Save Info 后提示窗口

Reserved space for future updates (append below with date and bullet points).  
后续更新请按日期在下方续写（追加要点）。

---

## Appendix: Data Entry Tips
## 附录：数据录入技巧

- Flight Number: uppercase letters + digits recommended (e.g., CZ627)  
- 航班号：建议大写字母+数字（如 CZ627）

- Counters: use ranges like F01-F06 or list segments as needed  
- 柜台：可用范围 F01-F06 或多段组合

- Shared Flights: separate with spaces, e.g., CZ627 KL1234  
- 共享航班：用空格分隔，如 CZ627 KL1234

- Delay Reason: populate with controlled vocabulary consistent with voice packs  
- 延误原因：尽量使用与语音包一致的标准词汇

- Language: choose from supported sets (CN-EN / CN-EN-JA / CN-EN-KO)  
- 语言类型：从支持的组合中选择（中英/中英日/中英韩）

---

Thank you for using Airport Flight Announcement System!  
感谢使用航班广播语音系统！