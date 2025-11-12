# Airport Flight Announcement System / 机场航班广播系统

<p align="center">
  <a href="https://github.com/WuHanqing2005/Airport-Flight-Announcement-System">
    <img src="https://github.com/WuHanqing2005/Airport-Flight-Announcement-System//docs/screenshot.png" alt="System Screenshot / 系统截图" width="850">
  </a>
</p>
<p align="center">
    <img src="https://img.shields.io/badge/For-Windows%2010/11-blue.svg" alt="For Windows 10/11">
    <img src="https://img.shields.io/badge/Status-Ready%20to%20Use-brightgreen.svg" alt="Ready to Use">
    <img src="https://img.shields.io/badge/License-Proprietary-red.svg" alt="License">
</p>

An offline-first, GUI-driven tool that composes and plays high-quality, multi-lingual airport announcements by stitching pre-recorded WAV voice packs.  
一款离线可用的、带图形界面的机场广播系统。它通过拼接高质量的 WAV 语音包来合成并播放多语言的、专业级的机场广播。

---

## About the Author / 关于作者

- **Author / 作者**: Wu Hanqing (Daniel) / 吴瀚庆（Daniel）  
- **Vision / 初衷**: To make airport audio operations reliable, efficient, and easy for non-technical staff. / 让机场广播的生成与播报更稳定、高效，便于非技术人员使用。
- **Copyright / 版权**: Copyright © Wu Hanqing. All Rights Reserved. / 版权所有 © 吴瀚庆。
- **License Note / 许可声明**: Unauthorized use or redistribution for any purpose is strictly prohibited. Infringement will be pursued. / 未经授权，严禁出于任何目的使用或传播本软件。侵权必究。

---

## Contact / 联系方式

- **WeChat / 微信**: `Daniel_Qinghan`  
- **Phone / 手机**: `+86-195-2887-3640` (CN) / `+82-010-7435-5296` (KR)  
- **Email / 邮箱**: `wuhanqing2005@gmail.com`  

Welcome to reach out for cooperation, feature requests, and voice pack customization. / 欢迎就项目合作、功能需求及语音包定制事宜与我联系。

---

## Table of Contents / 目录

1.  [**Quick Start Guide (For End-Users)** / **快速上手指南 (最终用户)**](#1-quick-start-guide-for-end-users--快速上手指南-最终用户)
    -   [1.1 Download & Unzip / 下载与解压](#11-download--unzip--下载与解压)
    -   [1.2 Launch the Application / 启动程序](#12-launch-the-application--启动程序)
    -   [1.3 Interface Overview / 界面概览](#13-interface-overview--界面概览)
2.  [**Core Operation Workflow** / **核心操作流程**](#2-core-operation-workflow--核心操作流程)
    -   [2.1 Adding a New Flight / 添加一个新航班](#21-adding-a-new-flight--添加一个新航班)
    -   [2.2 Generating & Playing Announcements / 生成并播放广播](#22-generating--playing-announcements--生成并播放广播)
    -   [2.3 Editing & Deleting Flights / 编辑与删除航班](#23-editing--deleting-flights--编辑与删除航班)
    -   [2.4 Saving & Refreshing Data / 保存与刷新数据](#24-saving--refreshing-data--保存与刷新数据)
3.  [**`release` Folder Explained** / **`release` 文件夹内容详解**](#3-release-folder-explained--release-文件夹内容详解)
4.  [**Frequently Asked Questions (FAQ)** / **常见问题与解决方案**](#4-frequently-asked-questions-faq--常见问题与解决方案)
5.  [**Broadcast Types & Data Fields** / **广播类型与数据字段说明**](#5-broadcast-types--data-fields--广播类型与数据字段说明)
6.  [**Changelog** / **更新日志**](#6-changelog--更新日志)
7.  [**License & Disclaimer** / **许可与声明**](#7-license--disclaimer--许可与声明)
8.  [**(For Developers) Local Development Setup** / **(开发者参考) 本地开发部署**](#8-for-developers-local-development-setup--开发者参考-本地开发部署)

---

## 1. Quick Start Guide (For End-Users) / 快速上手指南 (最终用户)

This guide is designed for operators who will be using the software directly. No programming knowledge is required.  
本指南为直接使用本软件的操作人员设计。无需任何编程知识。

### 1.1 Download & Unzip / 下载与解压

1.  Go to the project's [GitHub Releases page](https://github.com/WuHanqing2005/Airport-Flight-Announcement-System/releases).  
    访问本项目的 [GitHub Releases 页面](https://github.com/WuHanqing2005/Airport-Flight-Announcement-System/releases)。
2.  Find the latest version and download the `release.zip` file.  
    找到最新版本的 `release.zip` 文件并下载。
3.  After downloading, right-click `release.zip` and select "**Extract All...**".  
    下载完成后，右键点击 `release.zip` 文件，选择“**全部解压缩...**”。
4.  You will get a folder named `release`. This is your main application directory.  
    您将得到一个名为 `release` 的文件夹。这就是您的主程序目录。

### 1.2 Launch the Application / 启动程序

1.  Enter the extracted `release` folder.  
    进入解压后的 `release` 文件夹。
2.  Find and **double-click** the file named `start.bat`.  
    找到并**双击**名为 `start.bat` 的文件。
    > This is the startup script. Its icon might look like a window with gears.  
    > 这是一个启动脚本，图标可能是一个带有齿轮的窗口。
3.  A black command window will pop up first. **Do not close it.** After a few seconds, your default web browser will automatically open and display the main interface.  
    程序启动时，会先弹出一个黑色的命令窗口，请**不要关闭它**。几秒钟后，系统会自动打开您的默认浏览器，并显示软件主界面。

**Congratulations! The application is now running.**  
**恭喜！程序已成功运行。**

### 1.3 Interface Overview / 界面概览

- **Main Flight Table / 主航班列表**: The central area of the screen, displaying all flight information. / 屏幕中央的核心区域，显示所有航班信息。
- **Top Toolbar / 顶部工具栏**: Contains core action buttons like "Add Flight," "Delete Selected," and "New Announcement." / 包含“添加航班”、“删除选中”、“制作新广播”等核心功能按钮。
- **Right-side Toolbar / 右侧工具栏**: For data management, such as "Refresh from Disk" and "Save to Disk." / 用于管理数据，如“从磁盘刷新”和“保存到磁盘”。
- **Log Viewer / 底部日志区**: Shows real-time backend activity, helping you understand what the program is doing. / 实时显示程序后台的运行状态，帮助您了解当前正在发生什么。

## 2. Core Operation Workflow / 核心操作流程

### 2.1 Adding a New Flight / 添加一个新航班

1.  Click the **[Add Flight]** button on the top toolbar.  
    点击顶部工具栏的 **[Add Flight]** 按钮。
2.  In the pop-up window, fill in the flight details (flight number, destination, gate, etc.).  
    在弹出的窗口中，依次填写航班的详细信息（航班号、目的地、登机口等）。
    > **Tip**: For field-specific rules, refer to the [Data Fields Guide](#5-broadcast-types--data-fields--广播类型与数据字段说明).  
    > **提示**: 关于每个字段的填写规则，请参考 [数据字段说明](#5-broadcast-types--data-fields--广播类型与数据字段说明) 部分。
3.  Click **[Add]** when done. The new flight will immediately appear in the main table.  
    填写完毕后，点击 **[Add]** 按钮。新航班将立刻出现在主航班列表中。

### 2.2 Generating & Playing Announcements / 生成并播放广播

1.  In the main flight table, **click** to select the flight you want to announce.  
    在主航班列表中，**单击**选中您想播报的航班。
2.  Click the **[New Announcement]** button on the top toolbar.  
    点击顶部工具栏的 **[New Announcement]** 按钮。
3.  In the pop-up, select the **Broadcast Type** (e.g., Check-in, Arrival, Delay) from the dropdown menu.  
    在弹窗中，从下拉菜单里选择您想制作的**广播类型**（如：值机、到达、延误等）。
4.  Click **[Generate & Play]**.  
    点击 **[Generate & Play]** 按钮。
5.  The system will synthesize the audio (progress will be shown in the log viewer) and play it automatically upon completion. The generated audio file is saved in the `output` folder.  
    系统会开始合成音频（底部日志区会显示进度），完成后将自动播放。制作好的音频文件会保存在 `output` 文件夹内。

### 2.3 Editing & Deleting Flights / 编辑与删除航班

- **To Edit / 编辑**: **Right-click** on a flight in the table and select **[Edit]** from the context menu. / 在主航班列表上，**右键单击**您想修改的航班，在弹出的菜单中选择 **[Edit]**。
- **To Delete / 删除**:
    - **Single Delete / 单个删除**: Right-click a flight and select **[Delete]**. / 右键单击要删除的航班，选择 **[Delete]**。
    - **Bulk Delete / 批量删除**: Hold the `Ctrl` key and click multiple flights, then click the **[Delete Selected]** button on the top toolbar. / 按住 `Ctrl` 键并单击多个航班，然后点击顶部工具栏的 **[Delete Selected]** 按钮。

### 2.4 Saving & Refreshing Data / 保存与刷新数据

- **To Save / 保存**: After adding, editing, or deleting flights, always click **[Save to Disk]** on the right-side toolbar to permanently save all changes to the `data.xlsx` file. / 在您添加、编辑或删除了航班信息后，务必点击右侧的 **[Save to Disk]** 按钮，以将所有更改永久保存到 `data.xlsx` 文件中。
- **To Refresh / 刷新**: If you manually edited the `data.xlsx` file or the interface seems out of sync, click **[Refresh from Disk]** to reload the latest data from the file. / 如果您手动修改了 `data.xlsx` 文件，或者感觉界面显示不正确，可以点击 **[Refresh from Disk]** 按钮，从文件中重新加载最新的航班数据。

## 3. `release` Folder Explained / `release` 文件夹内容详解

Understanding the contents of the `release` folder will help you use the software better.  
了解 `release` 文件夹中各个部分的作用能帮助您更好地使用本软件。

- **`start.bat` (Application Starter / 启动程序)**
  > This is the **only file you need to double-click**. It's the shortcut to launch the entire application.  
  > **您唯一需要双击的文件**。它是启动整个软件的快捷方式。

- **`data` (Data Folder / 数据文件夹)**
  > Contains `data.xlsx`, your flight information database. You can open it with Excel to bulk edit or back up your data.  
  > 存放 `data.xlsx` 文件，这是您的航班信息数据库。您可以直接用 Excel 打开它来批量编辑或备份数据。

- **`output` (Audio Output Folder / 音频输出文件夹)**
  > All generated announcement audio files (`.wav`) are saved here. You can access this folder to find, play, or manage these files.  
  > 所有通过本软件生成的广播音频（`.wav` 文件）都会保存在这里。您可以随时进入此文件夹查找、播放或管理这些音频。

- **`material` (Voice Pack Library / 语音素材库)**
  > Contains all the raw voice clips used to build announcements (e.g., "Beijing," "Tokyo," "flight"). **Do not modify or delete any content in this folder**, as it will cause announcements to fail.  
  > 存放所有用于拼接广播的原始语音片段（如“北京”、“东京”、“航班”等）。**请勿修改或删除此文件夹内的任何内容**，否则会导致广播无法正常生成。

- **`src`, `python`, `ffmpeg.exe` (Core Engine / 软件核心引擎)**
  > These are the core programs and libraries that make the software run. **Please treat them as a "black box." Do not move, rename, or delete them.**  
  > 这些是保证软件正常运行的核心程序和依赖库。**请将它们视为“黑匣子”，完全不需要也请不要进行任何移动、重命名或删除操作。**

## 4. Frequently Asked Questions (FAQ) / 常见问题与解决方案

| Issue / 问题 | Possible Cause / 可能原因 | Solution / 解决方案 |
| :--- | :--- | :--- |
| **Application flashes and closes / 双击 `start.bat` 后，程序一闪而过** | Your system may be missing required runtimes, or an antivirus program may have quarantined files. / 您的系统可能缺少必要的运行库，或者文件被杀毒软件误删。 | 1. Try right-clicking `start.bat` and selecting "Run as administrator." / 尝试在 `start.bat` 上右键，选择“以管理员身份运行”。<br>2. Temporarily disable your antivirus, re-extract the zip file, and run again. / 暂时关闭杀毒软件后重新解压并运行。 |
| **Announcement fails, error `FileNotFoundError` / 广播无法生成，或提示 `FileNotFoundError`** | A voice clip is missing from `material`, or a city/airline name you entered has no corresponding voice pack. / `material` 语音素材库中的文件缺失，或您输入的地名/航司名没有对应的语音包。 | 1. Ensure the `material` folder is intact. / 确保 `material` 文件夹完整。<br>2. Check if the city/airline name is spelled correctly. / 检查您输入的城市/航司名称是否正确。<br>3. Contact the author for new voice packs. / 如需新增语音，请联系作者。 |
| **Audio is distorted or silent / 声音失真或没有声音** | The source audio format is incompatible (e.g., mono). / 音频素材格式不兼容（如单声道）。 | Click the **[Convert Audio]** button on the right-side toolbar. This will automatically convert all files in the `material` folder to the standard format. / 点击界面右侧的 **[Convert Audio]** 按钮。该功能会自动将 `material` 文件夹内所有音频转换为标准格式。 |
| **Cannot save data / 无法保存数据** | The `data/data.xlsx` file is open in another program (like Microsoft Excel). / `data/data.xlsx` 文件正被另一个程序（如 Microsoft Excel）打开。 | Close the file in the other program, then click **[Save to Disk]** again. / 请先关闭正在编辑 `data.xlsx` 的 Excel 程序，然后再点击 **[Save to Disk]**。 |

## 5. Broadcast Types & Data Fields / 广播类型与数据字段说明

**Supported Broadcast Types / 支持的广播类型**:
- `Check-in` / 值机广播
- `Arrival` / 到达广播
- `Baggage_Claim` / 行李提取
- `Departure_Delay_Determined` / 出发延误（时间已定）
- ...and more. See the full list in the "New Announcement" pop-up. / ...以及更多。请在“New Announcement”弹窗中查看完整列表。

**Data Fields Guide / 数据字段填写指南**:

| Field (EN) / 字段 (中文) | Description / 填写说明 | Example / 示例 |
| :--- | :--- | :--- |
| **Flight Number / 航班号** | For codeshares, separate with a **space**. / 共享航班请用**空格**隔开。 | `CZ627 MU1234` |
| **Check-in Counter / 值机柜台** | For ranges, use a **hyphen** `-`. / 连续柜台请用**连字符** `-`。 | `F01-F06` |
| **Time Fields / 时间字段** | Must use `HH:MM` 24-hour format. / 必须使用 `HH:MM` 格式的24小时制。 | `09:30` or `21:45` |
| **Language Type / 语言类型** | Uppercase language codes, separated by a **hyphen** `-`. / 大写语言代码，用**连字符** `-` 分隔。 | `CN-EN` or `CN-EN-JP` |

## 6. Changelog / 更新日志

- **2025.11.11**: **Major Architecture Upgrade**. 
Migrated project to a Python + Web architecture (Flask backend + Bootstrap 5 frontend) for a more robust, maintainable, and feature-rich platform. 
**重大架构升级**。项目迁移至 Python + Web 架构（Flask 后端 + Bootstrap 5 前端），为更健壮、可维护和功能丰富的平台奠定基础。

- **2025.10.01**: 
Added right-click context menu for table rows; added success toast notifications. 
新增表格右键菜单；增加成功操作的提示。

- **2024.11.11**: 
Added Divert, Scheduled/Estimated Time, and Delay Reason fields to the data model and UI. 
新增备降、计划/预计时间、延误原因字段。

- **2024.10.27**: 
Fixed saving; re-synthesized some packs with GPT-SoVITS. 
修复保存问题；用 GPT-SoVITS 重合成部分语音。

- **2024.06.14**: 
Added Exit on login; UI improved. 
登录界面新增退出；界面美化。

- **2024.05.20**: 
Added more voice resources. 
新增语音资源。

- **2024.05.06**: 
Implemented automatic stereo conversion for all source audio files. 
实现对所有源音频文件的自动双声道转换功能。

- **2024.05.05**: 
Fixed WinError 2; all packs stereo; improved `refresh_table()`. 
修复 WinError2；全部语音包双声道；完善 `refresh_table()`。

- **2024.05.02**: 
Python interpreter compatibility adjustments. 
调整解释器兼容性。

- **2024.05.01**: 
Switched interface to English; voice file renaming to EN. 
界面改为英文；语音文件英文化。

- **2024.04.30**: 
Shared flights supported (space-separated); English arrival added. 
支持共享航班；补全到达英文部分。

- **2024.04.29**: 
Introduced a real-time progress bar; beautified UI. 
为耗时任务引入实时进度条，并美化界面。

- **2024.04.28**: 
Implemented the "Stop All Processes" button; made all file paths portable. 
实现“停止所有进程”按钮；使所有文件路径可移植。

- **2024.04.27**: 
Migrated data storage to a persistent `data.xlsx` file. 
数据存储迁移至持久化的 `data.xlsx` 文件。

- **2024.04.26**: 
Added language combinations (CN-EN-JA...); stronger checks. 
增加语言组合；增强检查。

- **2024.04.17**: 
Framework for broadcast type selection. 
广播类型选择框架。

- **2024.04.11**: 
Removed unused code; generate text transcript with audio. 
删除无用代码；生成文本与音频。

- **2024.04.10**: 
Logic & comments improved; example flights updated. 
优化逻辑与注释；更新示例航班。

- **2024.04.08**: 
Added Boarding Gate & Baggage Claim; manual city input. 
新增登机口与行李转盘；手动城市输入。

- **2024.04.07**: 
Completed English templates; city pack existence check. 
完善英文模板；检测城市语音包。

- **2024.04.06**: 
English check-in sentences; input validation; voice refinement. 
英文句型；输入校验；优化语音。

- **2024.04.05**: 
Counter range logic improved; visual error dialogs added. 
值机柜台范围逻辑改进；新增可视化报错。

- **2024.04.04**: 
Bug fixes. 
修复若干问题。

- **2024.04.02**: 
Project initiated; switched from Google TTS to local WAV stitching. 
项目启动；核心概念由在线 TTS 转向本地 WAV 拼接。

- **2025.11.12**: 
**Major Architecture Upgrade**: Migrated the user interface from `tkinter` to a modern web-based architecture. The system now utilizes a Python (Flask) backend to serve a dynamic HTML frontend, offering a more flexible and user-friendly experience. Adopted `Poetry` for robust dependency and environment management. 
**重大架构升级**：用户界面从原生的 `tkinter` 迁移至现代化的 Web 架构。 系统现采用 Python (Flask) 作为后端，驱动动态 HTML 前端界面，提供更灵活、更友好的用户体验。 引入 `Poetry` 进行更稳健的依赖与环境管理。

## 7. License & Disclaimer / 许可与声明

- **Copyright © Wu Hanqing (Daniel Wu Hanqing). All Rights Reserved.** / **版权所有 © 吴瀚庆。保留所有权利。**
- This software is provided "as is," without warranty of any kind. Use at your own risk. / 本软件按“现状”提供，不包含任何形式的保证。使用风险由用户自行承担。
- Unauthorized reproduction, redistribution, or use of this software or its components for commercial purposes is strictly prohibited. / 严禁未经授权的复制、再分发，或将本软件及其任何组件用于商业目的。

---

## 8. (For Developers) Local Development Setup / (开发者参考) 本地开发部署

**This section is only for developers who wish to modify the source code. Regular users can ignore this.**  
**此部分仅面向希望修改源代码或进行二次开发的开发者。普通用户请忽略。**

1.  **Prerequisites / 环境准备**:
    - Clone the full repository: `git clone https://github.com/WuHanqing2005/Airport-Flight-Announcement-System.git`
    - Install [Python 3.11+](https://www.python.org/)
    - Install [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) and add it to your system's PATH.
2.  **Install Dependencies / 安装依赖**:
    ```bash
    # Navigate to the project directory
    cd Airport-Flight-Announcement-System
    # Create and activate a virtual environment
    python -m venv .venv
    .venv\Scripts\activate
    # Install dependencies
    pip install -r requirements.txt
    ```
3.  **Run the Application / 运行程序**:
    ```bash
    python src/airport_flight_announcement_system/main.py
    ```

---
Thank you for using the Airport Flight Announcement System! 
感谢您使用航班广播语音系统！