# -*- coding:utf-8 -*-
# 软件名称：Airport Flight Announcement System
# 版本号：2025.09.08
# 软件版权归属：吴瀚庆
# 未经允许，禁止盗用，侵权必究

# 有意请联系软件作者 吴瀚庆
# 微信：whq20050121
# 手机：19528873640
# 邮箱：m19528873640@outlook.com
# 欢迎提出宝贵意见，感谢支持！

# 新版本的pydub，不再包含pyaudioop包，但是可能会出现兼容性错误，此时请执行以下语句
# python -m pip install pydub audioop-lts

import os
import datetime
from datetime import datetime

import pandas as pd
from pydub import AudioSegment
import tkinter as tk
from tkinter import ttk
import threading
from tkinter import messagebox
import pygame
import threading


# 将一些必要的列表储存在这里，方便查找
language_type = ['CN_EN', 'CN_EN_JA', 'CN_EN_KO']                       # 供用户选择的语言类型下拉列表
announcement_type = ["Check_in", "Arrival", "Baggage_Claim", "Departure_Delay_Determined", "Departure_Delay_Undetermined", \
                     "Arrival_Delay_Determined", "Arrival_Delay_Undetermined"]            # 供用户选择的广播种类下列表


# 写错误日志的函数
def write_error_log(error_message):
    import datetime
    # 获取当前时间
    now = datetime.datetime.now()
    # 格式化时间为字符串
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # 构造日志信息
    log_message = f"[{timestamp}]\nERROR: {error_message}\n\n"
    
    # 定义日志文件名
    log_filename = f"error_log.txt"
    
    # 打开文件，写入日志信息
    with open(log_filename, "a") as file:
        file.write(log_message)


def update_progress(step, total, progress_bar, label, text):
    # 更新进度条的值
    progress_bar.configure(value=(step / total) * 100)
    # 更新标签的文本
    label.config(text=f"Importing voice packs:  ({step} / {total})\n{text}")

# 检验时间是否为"hh:mm"格式的函数，如果是，返回True，反之返回False
def is_valid_time(time_str):
    try:
        # 尝试按照"小时:分钟"的格式来解析时间字符串
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        # 如果解析失败，返回False
        return False



# 假设这是我们的二维数组数据，现在每行有12个元素
'''
data = [
    ['MU2546', 'SHE', 'CGO', 'XMN', 'HGH', 'B11-B18', '18', '2', '10:00', '10:00', '', 'CN-EN'],
    ['MU1278', 'SHE', '', 'PVG', 'HGH', 'C13-C18', '15', '8', '11:30', '11:30', '', 'CN-EN'],
    ['CA630', 'SHE', 'PVG', 'NRT', '', 'F01-F06-F08', '130', '6', '12:00', '12:15', '', 'CN-EN-JA'],
    ['CZ628', 'NRT', '', 'SHE', '', 'F11-F20', '20', '1', '12:00', '14:00', 'Air_Traffic_Control', 'CN-EN-JA']
]
'''

# 用来储存航班信息的xlsx文件
filename = os.path.join('data', 'data.xlsx')

# 从xlsx文件读取data
def read_xlsx(filename):
    try:
        df = pd.read_excel(filename, engine='openpyxl')
        # 将DataFrame中所有的NaN值替换为空字符串''
        df = df.fillna(value='')
        return df.values.tolist()
    except Exception as error_message:
        messagebox.showerror("Error", f"read_xlsx failed: {error_message}")
        write_error_log(error_message)
        return None

# data = read_xlsx(filename)    
# print(data)


# 将data写入xlsx文件
def write_xlsx(data, filename):
    try:
        # 创建一个空的DataFrame
        empty_df = pd.DataFrame()

        # 先将空的DataFrame写入Excel文件，以清空文件内容
        empty_df.to_excel(filename, index=False, engine='openpyxl', startrow=0)

        # 创建一个新的DataFrame来保存更新后的数据
        df = pd.DataFrame(data)

        # 将更新后的数据写入Excel文件，从第一行开始
        df.to_excel(filename, index=False, engine='openpyxl', startrow=0, header=True)
        # messagebox.showinfo("Success", "Data saved successfully.")
    except Exception as error_message:
        messagebox.showerror("Error", f"write_xlsx failed: {error_message}")
        write_error_log(error_message)



# 读取cityname_cn目录中的所有文件名
file_names_1 = os.listdir(os.path.join('material', 'cityname_cn'))
citynames = [name.rsplit('.', 1)[0] for name in file_names_1]
# print(citynames)        # citynames = ['SHE', 'PEK', 'PKX', 'SHA', 'PVG']

# 读取airlines_cn目录中的所有文件名
file_names_2 = os.listdir(os.path.join('material', 'airlines_cn'))
airlines = [name.rsplit('.', 1)[0] for name in file_names_2]
# print(airlines)     # airlines = ['CA', 'CZ', 'MU']

# 读取delay_reason_cn目录中的所有文件名
file_names_3 = os.listdir(os.path.join('material', 'delay_reason_cn'))
delay_reasons = [name.rsplit('.', 1)[0] for name in file_names_3]
# print(airlines)     # airlines = ['Air_Traffic_Control', 'Weather_Enroute']



def update_table(new_data):
    try:    
        global data  # 添加全局变量声明
        # 清除表格内容
        for i in reversed(table.get_children()):
            table.delete(i)

        # 重新插入数据
        for row in new_data:
            table.insert('', 'end', values=row)  # 确保row有足够的元素
    except Exception as error_message:
        messagebox.showerror("Error", f"update_table failed: {error_message}")
        write_error_log(error_message)

def clear_function():
    try:    
        global data  # 添加全局变量声明
        data = []  # 清空data列表
        update_table(data)  # 更新表格
        write_xlsx(data, filename)
    except Exception as error_message:
        messagebox.showerror("Error", f"clear_fuction failed: {error_message}")
        write_error_log(error_message)

def refresh_table():
    try:    
        global data  # 添加全局变量声明
        # 从xlsx文件中重新读取数据
        data = read_xlsx(filename)
       
        # 使用列表推导式创建新的二维数组，将登机口号码和行李提取处号码都转换为整数类型再转换成字符串类型并存储
        # 其中第 6 和第 7 列的元素转换为字符串类型，且如果是浮点数则先转换为整数
        new_data = [
            original_row[:5] + [
                str(int(original_row[5])) if isinstance(original_row[5], float) else original_row[5],
                str(int(original_row[6])) if isinstance(original_row[6], float) else original_row[6],
            ] + original_row[7:]
            for original_row in data
]

        # 更新表格
        update_table(new_data)
        messagebox.showinfo("Information", "Flight information read successfully!")
    except Exception as error_message:
        messagebox.showerror("Error", f"refresh_table failed: {error_message}")
        write_error_log(error_message)
        


# 将文件夹中所有子文件夹中的wav文件全部转换为双声道
def convert_to_stereo(input_folder):
    # 初始化Tkinter窗口
    root = tk.Tk()
    root.title("Converting audio files")
    root.geometry("500x120")

    # 创建进度条
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=20, padx=20, fill="both", expand=True)

    # 创建一个标签控件
    label = tk.Label(root, text="Converting audio files", font=("Times New Roman", 15))
    label.pack()

    # 获取 material 文件夹下的文件夹个数
    entries = os.listdir(input_folder)
    subfolders = [entry for entry in entries if os.path.isdir(os.path.join(input_folder, entry))]
    total_subfolders = len(subfolders)

    # 循环执行 int(len(subfolders)) 次，也就是要遍历 int(len(subfolders)) 个子文件夹
    i = 0

    # 遍历input_folder中的所有文件和子文件夹
    for current_root, dirs, files in os.walk(input_folder):  # 第一层循环，遍历子文件夹
        for filename in files:  # 第二层循环，遍历子文件夹中的语音包
            if filename.endswith(".wav"):
                try:
                    input_path = os.path.join(current_root, filename)
                    audio = AudioSegment.from_wav(input_path)
                    stereo_audio = audio.set_channels(2)
                    stereo_audio.export(input_path, format="wav")
                except Exception as error_message:
                    messagebox.showerror("Error", f"Failed to convert audio file: {filename}\nError message: {error_message}")
                    write_error_log(f"Failed to convert audio file: {filename}\nError message: {error_message}")
                    continue

        # 更新进度条和标签
        step = i
        total = total_subfolders
        update_progress(step, total, progress_bar, label, current_root)  # 使用current_root而不是root
        root.update()  # 刷新主窗口，以便更新进度条和标签
        i += 1  # 增加当前的步数

    # 在这里不需要调用root.mainloop()，因为程序会在所有文件处理完毕后退出
    # 如果需要保持窗口打开，确保在最后调用root.mainloop()，并且在此之前不要退出程序

    # 运行完毕，弹出提示窗口
    # messagebox.showinfo("Information", "Converting audio files to dual-channel successfully!")
    root.destroy()



def button1_function():
    try:
        '''# 获取主窗口位置和大小
        root_x = root.winfo_x()
        root_y = root.winfo_y()
        root_width = root.winfo_width()
        root_height = root.winfo_height()

        # 计算弹出窗口在主窗口居中的位置
        top_x = root_x + root_width // 2 - 100
        top_y = root_y + root_height // 2 - 100

        # 创建一个新的Toplevel窗口用于输入
        top = tk.Toplevel(root)
        top.title("Input Data")
        top.geometry(f"300x100+{top_x}+{top_y}")'''
        
        # 获取屏幕中心点的坐标
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 500
        window_height = 600
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2) - 100

        # 创建一个新的Toplevel窗口用于输入
        top = tk.Toplevel(root)
        top.title("Input Data")
        top.geometry(f"{window_width}x{window_height}+{x}+{y}")    # 在指定位置（屏幕居中位置）显示窗口

        # 创建12个标签和输入框
        labels = ["Flight Number", "Departure", "Stopover", "Destination", "Divert", "Check-in Counter", "Boarding Gate", "Baggage Claim", "Scheduled Arrival Time (hh:mm)", "Estimated Arrival Time (hh:mm)", "Delay Reason", "Language Type"]
        entries = []  # 用于存储Entry控件对象
        for i, label in enumerate(labels):
            tk.Label(top, text=label).grid(row=i, column=0)

            label_widget = tk.Label(top, text=label)
            label_widget.grid(row=i, column=0, padx=50, pady=10)  # 设置padx和pady值增加间距
            top.geometry(f"{window_width}x{window_height}+{x}+{y + 50}")    # 在指定位置（屏幕居中位置）显示窗口

            if label in ['Departure', 'Stopover', 'Destination', "Divert"]:  # 如果是下拉列表需要创建下拉列表
                entry = ttk.Combobox(top, values=citynames)  # 创建城市名下拉列表
            elif label in ['Language Type']:
                entry = ttk.Combobox(top, values=language_type)
            elif label in ['Delay Reason']:
                entry = ttk.Combobox(top, values=delay_reasons)
            else:
                entry = tk.Entry(top)  # 创建文本输入框

            entry.grid(row=i, column=1)
            entries.append(entry)

        # 创建一个提交按钮
        submit_button = tk.Button(top, text="Submit", command=lambda: button1_submit(top, entries, data))
        submit_button.grid(row=12, column=0, columnspan=9)

        top.transient(root)     # 设置为临时窗口，当主窗口关闭时，这个窗口也会关闭
        top.grab_set()          # 阻止用户在其他窗口输入，直到这个窗口关闭
    except Exception as error_message:
        messagebox.showerror("Error", f"button1_function failed:\n{error_message}")
        write_error_log(error_message)


def button1_submit(top, entries, data):
    try:
        # 获取输入的数据
        new_row = [entry.get() for entry in entries]
        # "Flight Number", "Departure", "Stopover", "Destination", "Divert", "Check-in Counter", "Boarding Gate", "Baggage Claim", "Scheduled Arrival Time (hh:mm)", "Estimated Arrival Time (hh:mm)", "Delay Reason", "Language Type"
        new_flight_number = new_row[0]  # new_flight_number = 'CZ627 JL5022'
        # 立即给new_flight_numbers赋值
        new_flight_numbers = new_flight_number.split(sep=' ')  # flight_numbers = ['CZ627', 'JL5022']
        
        # 声明空列表 new_airlines = ['CZ', 'JL']
        new_airlines = []
        for flight_number in new_flight_numbers:
            new_airlines.append(str(flight_number[:2]))
        
        data = read_xlsx(filename)
        flight_numbers = [row[0] for row in data]  # 列表中已有的所有航班号的列表
        new_departure = new_row[1]
        new_stopover = new_row[2]
        new_destination = new_row[3]
        new_divert = new_row[4]
        new_checkin = new_row[5]
        new_boarding_gate = new_row[6]
        new_baggage_claim = new_row[7]
        new_scheduled_arrival_time = new_row[8]
        new_estimated_arrival_time = new_row[9]
        new_delay_reason = new_row[10]
        new_language_type = new_row[11]

        

        # 检查新航班号是否与已有航班号重复
        for i in new_flight_numbers:
            if i in flight_numbers:
                # 弹出窗口报错
                messagebox.showinfo("Error", f"The flight number {i} already exists in the list.")
                return
        
        # 检查输入的新航班号是否为纯大写字母与数字与空格组合
        for i in new_flight_number:
            if i not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ':
                # 弹出窗口报错
                messagebox.showinfo("Error", "Please check your input flight numbers.\nIt must consist of capital letters and numbers and splitted by space.")
                return

        # 检查新航空公司是否存在对应航空公司的中文语音包
        for new_airline in new_airlines:
            if new_airline not in airlines:
                messagebox.showinfo("Error", f"Please check your input flight number.\nIt has no matching airlines for: {new_airline}")
                return

        # 检查出发地、到达地是否存在于对应中文城市语音包
        if new_departure not in citynames:
            messagebox.showinfo("Error", f"Please check your input Departure.\nIt has no matching citynames for: {new_departure}")
            return
        if new_destination not in citynames:
            messagebox.showinfo("Error", f"Please check your input Destination.\nIt has no matching citynames for: {new_destination}")
            return

        # 若输入了经停地，检查经停地是否存在于对应中文城市语音包
        if new_stopover != '' and new_stopover not in citynames:
            messagebox.showinfo("Error", f"Please check your input Stopover.\nIt has no matching citynames for: {new_stopover}")
            return

        # 若输入了备降地，检查经停地是否存在于对应中文城市语音包
        if new_divert != '' and new_divert not in citynames:
            messagebox.showinfo("Error", f"Please check your input Stopover.\nIt has no matching citynames for: {new_divert}")
            return

        # 若输入了登机口号码，则检查是否为纯大写字母与数字组合
        if new_boarding_gate != '':
            for i in new_boarding_gate:
                if i not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789':
                    # 弹出窗口报错
                    messagebox.showinfo("Error", "Please check your input Boarding Gate.\nIt must be consist of capital letters and numbers.")
                    return

        # 若输入了行李提取处号码，则检查是否为纯大写字母与数字组合
        if new_baggage_claim != '':
            for i in new_baggage_claim:
                if i not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789':
                    # 弹出窗口报错
                    messagebox.showinfo("Error", "Please check your input Boarding Gate.\nIt must be consist of capital letters and numbers.")
                    return

        # 检查输入的新值机柜台是否为纯大写字母与数字组合 并且只被-分隔
        for i in new_checkin:
            if i not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-':
                # 弹出窗口报错
                messagebox.showinfo("Error", "Please check your input Check-in counter number.\nIt must consist of capital letters and numbers and just splited with '-'.")
                return
        
        # 若输入了计划抵达时间，检查是否为"hh:mm"格式的字符串
        if new_scheduled_arrival_time != '' and is_valid_time(new_scheduled_arrival_time) == False:
            # 弹出窗口报错
            messagebox.showinfo("Error", "Please check your input Scheduled Arrival Time.\nIt must be format: \"hh:mm\"")
            return

        # 若输入了预计抵达时间，检查是否为"hh:mm"格式的字符串
        if new_estimated_arrival_time != '' and is_valid_time(new_estimated_arrival_time) == False:
            # 弹出窗口报错
            messagebox.showinfo("Error", "Please check your input Estimated Arrival Time.\nIt must be format: \"hh:mm\"")
            return
        

        # 检查空值
        if new_flight_number == '':
            messagebox.showwarning("Warning", "Flight number cannot be empty.")
            return
        elif new_departure == '':
            messagebox.showwarning("Warning", "Departure cannot be empty.")
            return
        elif new_destination == '':
            messagebox.showwarning("Warning", "Destination cannot be empty.")
            return
        elif new_checkin == '':
            messagebox.showwarning("Warning", "Check-in counter cannot be empty.")
            return
        elif new_language_type =='':
            messagebox.showwarning("Warning", "Language type cannot be empty.")
            return
        else:
            # 将输入的数据添加到data数组中
            data.append(new_row)
            
            # 更新表格
            update_table(data)
            
            # 将修改后的数据写入Excel文件
            write_xlsx(data, filename)

            # 关闭输入窗口
            top.destroy()
    except Exception as error_message:
        # 如果发生异常，捕获异常信息并显示错误消息框
        messagebox.showerror("Error", 'button1_submit failed:\n' + str(error_message))
        write_error_log(error_message)
        return

def button2_function():
    try:
        # 获取主窗口位置和大小
        root_x = root.winfo_x()
        root_y = root.winfo_y()
        root_width = root.winfo_width()
        root_height = root.winfo_height()

        # 计算弹出窗口位置
        top_x = root_x + root_width // 2 - 150
        top_y = root_y + root_height // 2 - 50

        # 创建一个新的Toplevel窗口用于输入
        top = tk.Toplevel(root)
        top.title("Delete Data")
        top.geometry("300x100+{}+{}".format(top_x, top_y))

        # 创建一个标签和一个下拉列表
        tk.Label(top, text="Name to Delete:").grid(row=0, column=0)
        data = read_xlsx(filename)
        flight_options = [row[0] for row in data]
        flight_to_delete = tk.StringVar(top)    # 创建一个变量用于存储选中的航班号
        flight_drop_down = ttk.Combobox(top, textvariable=flight_to_delete, values=flight_options, state="readonly")
        flight_drop_down.grid(row=0, column=1)

        # 创建一个提交按钮
        submit_button = tk.Button(top, text="Delete", command=lambda: button2_submit(top, flight_to_delete, data))
        submit_button.grid(row=1, column=0, columnspan=2)

        top.transient(root)  # 设置为临时窗口
        top.grab_set()  # 阻止用户在其他窗口输入
    except Exception as error_message:
        messagebox.showerror("Error", f"button2_function failed: {error_message}")
        write_error_log(error_message)

def button2_submit(top, name_to_delete_entry, global_data):
    try:
        # 获取要删除的名字
        name_to_delete = name_to_delete_entry.get()

        # 检查名字是否为空
        if name_to_delete:
            # 遍历global_data数组，找到并删除匹配的名字
            for i, row in enumerate(global_data):
                if row[0] == name_to_delete:
                    # 直接从原始列表中删除匹配的行
                    global_data.pop(i)
                    break  # 找到后退出循环

            # 更新表格
            update_table(global_data)

            # 将修改后的数据写入Excel文件
            write_xlsx(global_data, filename)

            # 关闭输入窗口
            top.destroy()
        else:
            messagebox.showwarning("Warning", "Flight number cannot be empty.")
    except Exception as error_messagee:
        # 如果发生异常，捕获异常信息并显示错误消息框
        messagebox.showerror("Error", 'button2_submit failed:\n' + str(error_message))
        write_error_log(error_message)
        return

def button3_function():
    try:
        # 获取主窗口位置和大小
        root_x = root.winfo_x()
        root_y = root.winfo_y()
        root_width = root.winfo_width()
        root_height = root.winfo_height()

        # 计算弹出窗口位置
        top_x = root_x + root_width // 2 - 200
        top_y = root_y + root_height // 2 - 100

        # 创建一个新的Toplevel窗口用于输入，并设置位置
        top = tk.Toplevel(root)
        top.title("Search Data")
        top.geometry("400x200+{}+{}".format(top_x, top_y))

        # 创建一个标签和一个下拉列表供用户选择广播种类
        tk.Label(top, text="Flight to Search:").grid(row=0, column=0)
        data = read_xlsx(filename)  # 从xlsx文件中读取航班数据data
        flight_options = [row[0] for row in data]       # 这是一个列表，包含表格中已有的所有航班信息的航班号
        flight_to_search = tk.StringVar(top)            # 创建一个变量用于存储选中的航班号
        search_drop_down = ttk.Combobox(top, textvariable=flight_to_search, values=flight_options, state="readonly", width=30)
        search_drop_down.grid(row=0, column=1)

        # 增加垂直距离
        tk.Label(top, text="").grid(row=1, columnspan=2, pady=40)  # 在两个下拉列表之间插入一个空行并增加距离

        # 创建一个下拉列表供用户选择广播种类
        tk.Label(top, text="Announcement Type:").grid(row=1, column=0)
        announcement_options = announcement_type      # 供用户选择播放航班广播的种类
        announcement_var = tk.StringVar(top)
        announcement_drop_down = ttk.Combobox(top, textvariable=announcement_var, values=announcement_options, state="readonly", width=30)
        announcement_drop_down.grid(row=1, column=1)

        # 创建一个提交按钮
        submit_button = tk.Button(top, text="Play", command=lambda: search_data(top, flight_to_search, announcement_var, data))
        submit_button.grid(row=2, column=0, columnspan=2)

        top.transient(root)  # 设置为临时窗口
        top.grab_set()  # 阻止用户在其他窗口输入
    except Exception as error_message:
        messagebox.showerror("Error", f"button3_function failed:\n{error_message}")
        write_error_log(error_message)

def button4_function():
    try:
        # 获取output目录中的所有文件名（不包含扩展名）
        output_list_temp = os.listdir(os.path.join('output'))
        output_list = [name.rsplit('.', 1)[0] for name in output_list_temp if name.endswith('.wav')]

        # 获取主窗口位置和大小
        root_x = root.winfo_x()
        root_y = root.winfo_y()
        root_width = root.winfo_width()
        root_height = root.winfo_height()

        # 计算弹出窗口位置
        top_x = root_x + root_width // 2 - 150
        top_y = root_y + root_height // 2 - 50

        # 创建一个新的Toplevel窗口用于选择文件
        top = tk.Toplevel(root)
        top.title("Play Existing Announcement")
        top.geometry("300x100+{}+{}".format(top_x, top_y))
        

        # 创建一个标签和一个下拉列表
        tk.Label(top, text="Flight to Play:").grid(row=0, column=0)
        flight_to_play = tk.StringVar(top)  # 创建一个变量用于存储选中的航班号
        flight_drop_down = ttk.Combobox(top, textvariable=flight_to_play, values=output_list, state="readonly")
        flight_drop_down.grid(row=0, column=1)

        # 增加垂直距离
        tk.Label(top, text="").grid(row=1, columnspan=2, pady=20)  # 在两个下拉列表之间插入一个空行并增加距离

        # 创建一个提交按钮
        submit_button = tk.Button(top, text="Play", command=lambda: button4_submit(top, flight_to_play))
        submit_button.grid(row=1, column=0, columnspan=2)

        top.transient(root)  # 设置为临时窗口
        top.grab_set()  # 阻止用户在其他窗口输入
    except Exception as error_message:
        messagebox.showerror("Error", f"button4_function failed:\n{error_message}")
        write_error_log(error_message)


def play_audio(flight_number):
    try:
        # 确保只初始化一次pygame，避免在多个线程中重复初始化
        pygame.init()
        pygame.mixer.init()

        # 根据航班号构造音频文件的路径
        audio_path = f"output/{flight_number}.wav"

        # 加载并开始播放音频
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()

        # 等待音频播放完成
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # 播放完成后退出pygame
        pygame.quit()
    except Exception as error_message:
        messagebox.showerror("Error", f"Failed to play audio: {error_message}")
        write_error_log(error_message)

def button4_submit(top, flight_to_play):
    try:
        # 获取要播放的航班号
        flight_number = flight_to_play.get()

        # 如果输入为空，则提示用户
        if not flight_number:
            messagebox.showwarning("Warning", "Please select a flight announcement to play.")
            return

        # 创建一个新线程来播放音频
        audio_thread = threading.Thread(target=play_audio, args=(flight_number,))
        audio_thread.start()

        # 关闭弹出窗口
        top.destroy()
    except Exception as error_message:
        messagebox.showerror("Error", f"button4_submit failed: {error_message}")
        write_error_log(error_message)


# 创建一个函数来停止所有音频
def stop_all_audio():
    import time
    import pygame
    try:
        # 确保只初始化一次pygame，避免在多个线程中重复初始化
        pygame.init()
        pygame.mixer.init()
        
        # 检查是否有音频正在播放
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        
        # 可选：延迟一点时间，确保音频已停止
        time.sleep(0.5)
        
    except pygame.error:
        # 如果发生错误（例如mixer尚未初始化），则忽略它
        pass
    finally:
        # 播放完成后退出pygame
        pygame.quit()



def search_data(top, flight_var, announcement_var, data):
    def play_announcement():
        import pygame
        pygame.mixer.init()
        if pygame.mixer.music.get_busy():
            messagebox.showwarning("Warning", "Please wait for the current process to end!")
            return
        try:
            combined = AudioSegment.empty()  # 初始化combined变量

            # 获取要搜索的名字
            search_name = flight_var.get()

            # 检查用户输入了航班号
            if search_name == '':
                messagebox.showwarning("Warning", "Please choose a flight number to search.")
                return

            # 通过用户输入的航班号，找到对应的航班行信息
            for row in data:
                if row[0] == search_name:  # 假设名字是唯一的
                    # print("Matched Row:", row)  # 打印匹配的行
                    # row = ['MU2546', 'SHE', 'CGO', 'XMN', 'HGH', 'B11-B18', '18', '2', '10:00', '12:00', 'Air_Traffic_Control', 'CN-EN']
                    flight_name = str(row[0])           # flight = 'CZ627 JL5022'
                    flights = str(row[0]).split(sep=' ')     # flights = ['CZ627', 'JL5022']
                    # airline = flight[:2]
                    departure = str(row[1])
                    stopover = str(row[2])
                    destination = str(row[3])
                    divert = str(row[4])
                    counter = str(row[5])
                    boarding_gate = str(row[6])
                    baggage_claim = str(row[7])
                    
                    scheduled_arrival_time = str(row[8])
                    if scheduled_arrival_time != '':
                        [scheduled_arrival_hour, scheduled_arrival_minute] = scheduled_arrival_time.split(sep = ':')
                    else:
                        [scheduled_arrival_hour, scheduled_arrival_minute] = ['', '']

                    estimated_arrival_time = str(row[9])
                    if estimated_arrival_time != '':
                        [estimated_arrival_hour, estimated_arrival_minute] = estimated_arrival_time.split(sep = ':')
                    else:
                        [estimated_arrival_hour, estimated_arrival_minute] = ['', '']

                    delay_reason = str(row[10])
                    language_type = str(row[11])

                    announcement_type = announcement_var.get()

                    # 调试输出信息
                    if 1 == 0:  # 改为1即输出以下调试信息
                        print(f"flight_name: \t{flight_name}")
                        print(f"flights: \t{flights}")
                        print(f"departure: \t{departure}")
                        print(f"stopover: \t{stopover}")
                        print(f"destination: \t{destination}")
                        print(f"divert: \t{divert}")
                        print(f"counter: \t{counter}")
                        print(f"boarding_gate: \t{boarding_gate}")
                        print(f"baggage_claim: \t{baggage_claim}")
                        print(f"scheduled_arrival_time: \t{scheduled_arrival_time}")
                        print(f"scheduled_arrival_hour: \t{scheduled_arrival_hour}")
                        print(f"scheduled_arrival_minute: \t{scheduled_arrival_minute}")
                        print(f"estimated_arrival_time: \t{estimated_arrival_time}")
                        print(f"estimated_arrival_hour: \t{estimated_arrival_hour}")
                        print(f"estimated_arrival_minute: \t{estimated_arrival_minute}")
                        print(f"delay_reason: \t{delay_reason}")
                        print(f"language_type: \t{language_type}")
                        print(f"announcement_type: \t{announcement_type}")


                    

            # 对应航班信息获取完毕，停留0.5秒后，关闭输入窗口
            import time
            time.sleep(0.5)
            # 关闭输入窗口
            top.destroy()
            
            # 初始化name列表，用于存储需要合成的wav文件名称
            name = []

            # 以下是值机广播部分
            if announcement_type == "Check_in":    # 调用 check-in 广播的合成函数
                # 中文广播部分
                if stopover == '':  # 如果没有经停站
                    name = [os.path.join('material', 'mix', '756.wav'), os.path.join('material', 'template_cn', '1.wav')]   # 756提示音 乘坐
                    
                    # 对于共享航班
                    for flight in flights:  # flight = 'CZ627' 然后 flight = 'JL5022'
                        name.append(os.path.join('material', 'airlines_cn', str(flight[:2]) + '.wav'))  # 中国南方航空公司
                        for i in flight:    # i = 'C' 然后 i ='Z' 然后 i = '6' ...
                            name.append(os.path.join('material', 'alnum_cn', str(i) + '.wav'))          # C-Z-6-2-7
                            
                    name.append(os.path.join('material', 'template_cn', '2.wav'))                       # 次航班，从
                    name.append(os.path.join('material', 'cityname_cn', str(departure) + '.wav'))       # 沈阳
                    name.append(os.path.join('material', 'template_cn', '4.wav'))                       # 前往
                    name.append(os.path.join('material', 'cityname_cn', str(destination) + '.wav'))     # 东京
                    name.append(os.path.join('material', 'template_cn', '5.wav'))                       # 的旅客请注意，您乘坐的航班现在开始办理乘机手续，请前往
                    for i in counter:                                                                   # counter = F01-F06
                        if i not in '-':
                            name.append(os.path.join('material', 'alnum_cn', str(i) + '.wav'))          # F 0 1 至 F 0 6
                        else:
                            name.append(os.path.join('material', 'template_cn', '6.wav'))               # 至
                    name.append(os.path.join('material', 'template_cn', '7.wav'))                       # 号柜台办理，谢谢
                else:  # 如果有经停站
                    name = [os.path.join('material', 'mix', '756.wav'), os.path.join('material', 'template_cn', '1.wav')]   # 756提示音 乘坐
                    
                    # 对于共享航班
                    for flight in flights:  # flight = 'CZ627' 然后 flight = 'JL5022'
                        name.append(os.path.join('material', 'airlines_cn', str(flight[:2]) + '.wav'))  # 中国南方航空公司
                        for i in flight:    # i = 'C' 然后 i ='Z' 然后 i = '6' ...
                            name.append(os.path.join('material', 'alnum_cn', str(i) + '.wav'))          # C-Z-6-2-7
                    
                    name.append(os.path.join('material', 'template_cn', '2.wav'))                       # 次航班，从
                    name.append(os.path.join('material', 'cityname_cn', str(departure) + '.wav'))       # 沈阳
                    name.append(os.path.join('material', 'template_cn', '3.wav'))                       # 经由
                    name.append(os.path.join('material', 'cityname_cn', str(stopover) + '.wav'))        # 上海浦东
                    name.append(os.path.join('material', 'template_cn', '4.wav'))                       # 前往
                    name.append(os.path.join('material', 'cityname_cn', str(destination) + '.wav'))     # 东京
                    name.append(os.path.join('material', 'template_cn', '5.wav'))                       # 的旅客请注意，您乘坐的航班现在开始办理乘机手续，请前往
                    for i in counter:                                                                   # counter = F01-F06
                        if i not in '-':
                            name.append(os.path.join('material', 'alnum_cn', str(i) + '.wav'))          # F 0 1 至 F 0 6
                        else:
                            name.append(os.path.join('material', 'template_cn', '6.wav'))               # 至
                    name.append(os.path.join('material', 'template_cn', '7.wav'))                       # 号柜台办理，谢谢

                # 英文广播部分
                if stopover == '':  # 如果没有经停站
                    name.append(os.path.join('material', 'template_en', '1.wav'))                       # May I have your attention please
                    name.append(os.path.join('material', 'template_en', '2.wav'))                       # We are now ready for check-in for
                    
                    # 对于共享航班
                    for flight in flights:  # flight = 'CZ627' 然后 flight = 'JL5022'
                        name.append(os.path.join('material', 'airlines_en', str(flight[:2]) + '.wav'))  # China Southern Airlines
                        name.append(os.path.join('material', 'template_en', '3.wav'))                   # Flight
                        for i in flight:    # i = 'C' 然后 i ='Z' 然后 i = '6' ...
                            name.append(os.path.join('material', 'alnum_en', str(i) + '.wav'))          # C-Z-6-2-7

                    name.append(os.path.join('material', 'template_en', '4.wav'))                       # From
                    name.append(os.path.join('material', 'cityname_en', str(departure) + '.wav'))       # Shenyang
                    name.append(os.path.join('material', 'template_en', '5.wav'))                       # To
                    name.append(os.path.join('material', 'cityname_en', str(destination) + '.wav'))     # Tokyo Narita
                    name.append(os.path.join('material', 'template_en', '7.wav'))                       # At check-in counter number
                    for i in counter:                                                                   # counter = F01-F06
                        if i not in '-':
                            name.append(os.path.join('material', 'alnum_en', str(i) + '.wav'))          # F 0 1 to F 0 6
                        else:
                            name.append(os.path.join('material', 'template_en', '5.wav'))
                    name.append(os.path.join('material', 'template_en', '8.wav'))                       # Thank you

                elif stopover != '':    # 如果有经停站
                    name.append(os.path.join('material', 'template_en', '1.wav'))                       # May I have your attention please
                    name.append(os.path.join('material', 'template_en', '2.wav'))                       # We are now ready for check-in for
                    
                    # 对于共享航班
                    for flight in flights:  # flight = 'CZ627' 然后 flight = 'JL5022'
                        name.append(os.path.join('material', 'airlines_en', str(flight[:2]) + '.wav'))  # China Southern Airlines
                        name.append(os.path.join('material', 'template_en', '3.wav'))                   # Flight
                        for i in flight:    # i = 'C' 然后 i ='Z' 然后 i = '6' ...
                            name.append(os.path.join('material', 'alnum_en', str(i) + '.wav'))          # C-Z-6-2-7
                            
                    name.append(os.path.join('material', 'template_en', '4.wav'))                       # From
                    name.append(os.path.join('material', 'cityname_en', str(departure) + '.wav'))       # Shenyang
                    name.append(os.path.join('material', 'template_en', '5.wav'))                       # To
                    name.append(os.path.join('material', 'cityname_en', str(stopover) + '.wav'))        # Tokyo Narita
                    name.append(os.path.join('material', 'template_en', '6.wav'))                       # With continuing service to
                    name.append(os.path.join('material', 'cityname_en', str(destination) + '.wav'))     # Tokyo Narita
                    name.append(os.path.join('material', 'template_en', '7.wav'))                       # At check-in counter number
                    for i in counter:                                                                   # counter = F01-F06
                        if i not in '-':
                            name.append(os.path.join('material', 'alnum_en', str(i) + '.wav'))          # F 0 1 to F 0 6
                        else:
                            name.append(os.path.join('material', 'template_en', '5.wav'))               # to
                    name.append(os.path.join('material', 'template_en', '8.wav'))                       # Thank you

                # 日文广播部分
                if language_type == 'CN_EN_JA':
                    if stopover == '':  # 如果没有经停站
                        name.append(os.path.join('material', 'template_ja', '1.wav'))                   # ご案内申し上げます
                        name.append(os.path.join('material', 'template_ja', '2.wav'))                   # ただいまから チェックイン(Check-in) を開始いたします
                                                
                        # 对于共享航班
                        for flight in flights:  # flight = 'CZ627' 然后 flight = 'JL5022'
                            name.append(os.path.join('material', 'airlines_ja', str(flight[:2]) + '.wav'))  # 中国南方航空
                            for i in flight:    # i = 'C' 然后 i ='Z' 然后 i = '6' ...
                                if i.isnumeric():
                                    name.append(os.path.join('material', 'alnum_ja', str(i) + '.wav'))      # 6-2-7
                            name.append(os.path.join('material', 'template_ja', '3.wav'))                   # 便
                        
                        name.append(os.path.join('material', 'cityname_ja', str(departure) + '.wav'))   # 審陽
                        name.append(os.path.join('material', 'template_ja', '4.wav'))                   # 発
                        name.append(os.path.join('material', 'cityname_ja', str(destination) + '.wav')) # 東京成田
                        name.append(os.path.join('material', 'template_ja', '6.wav'))                   # ゆきにご搭乗の客様は
                        name.append(os.path.join('material', 'template_ja', '7.wav'))                   # チェックイン カウンター (Check-in Counter) 番号
                        for i in counter:                                                               # counter = F01-F06
                            if i not in '-':
                                name.append(os.path.join('material', 'alnum_ja', str(i) + '.wav'))      # F 0 1 から F 0 6
                            else:
                                name.append(os.path.join('material', 'template_ja', '9.wav'))           # から
                        name.append(os.path.join('material', 'template_ja', '8.wav'))                   # までお進みください

                    elif stopover != '':    # 如果有经停站
                        name.append(os.path.join('material', 'template_ja', '1.wav'))                   # ご案内申し上げます
                        name.append(os.path.join('material', 'template_ja', '2.wav'))                   # ただいまから チェックイン(Check-in) を開始いたします
                        
                        # 对于共享航班
                        for flight in flights:  # flight = 'CZ627' 然后 flight = 'JL5022'
                            name.append(os.path.join('material', 'airlines_ja', str(flight[:2]) + '.wav'))  # 中国南方航空
                            for i in flight:    # i = 'C' 然后 i ='Z' 然后 i = '6' ...
                                if i.isnumeric():
                                    name.append(os.path.join('material', 'alnum_ja', str(i) + '.wav'))      # 6-2-7
                            name.append(os.path.join('material', 'template_ja', '3.wav'))                   # 便

                        name.append(os.path.join('material', 'cityname_ja', str(departure) + '.wav'))   # 審陽
                        name.append(os.path.join('material', 'template_ja', '4.wav'))                   # 発
                        name.append(os.path.join('material', 'cityname_ja', str(stopover) + '.wav'))    # 香港
                        name.append(os.path.join('material', 'template_ja', '5.wav'))                   # 経由
                        name.append(os.path.join('material', 'cityname_ja', str(destination) + '.wav')) # 東京成田
                        name.append(os.path.join('material', 'template_ja', '6.wav'))                   # ゆきにご搭乗の客様は
                        name.append(os.path.join('material', 'template_ja', '7.wav'))                   # チェックイン カウンター (Check-in Counter) 番号
                        for i in counter:                                                               # counter = F01-F06
                            if i not in '-':
                                name.append(os.path.join('material', 'alnum_ja', str(i) + '.wav'))      # F 0 1 から F 0 6
                            else:
                                name.append(os.path.join('material', 'template_ja', '9.wav'))           # から
                        name.append(os.path.join('material', 'template_ja', '8.wav'))                   # までお進みください

                    else:
                        messagebox.showinfo("Warning", "Please confirm audio file exists.")

            # 以下是到达广播部分
            elif announcement_type == "Arrival":   # 调用 Arrival 广播的合成函数
                # 中文广播部分
                if stopover == '':      # 如果没有经停站
                    name = [os.path.join('material', 'mix', '756.wav'), os.path.join('material', 'template_cn', '8.wav'), os.path.join('material', 'template_cn', '9.wav'),
                            os.path.join('material', 'cityname_cn', str(departure) + '.wav'), os.path.join('material', 'template_cn', '10.wav')]
                                                                                                # 迎接旅客的各位请注意，从 东京 飞来的

                    # 对于共享航班
                    for flight in flights:  # flight = 'CZ627' 然后 flight = 'JL5022'
                        name.append(os.path.join('material', 'airlines_cn', str(flight[:2]) + '.wav'))  # 中国南方航空公司
                        for i in flight:    # i = 'C' 然后 i ='Z' 然后 i = '6' ...
                            name.append(os.path.join('material', 'alnum_cn', str(i) + '.wav'))  # C-Z-6-2-7
                    
                    name.append(os.path.join('material', 'template_cn', '11.wav'))              # 次航班，已经到达本站，请您在到达大厅等候接待，谢谢
                elif stopover != '':    # 如果有经停站
                    name = [os.path.join('material', 'mix', '756.wav'), os.path.join('material', 'template_cn', '8.wav'), os.path.join('material', 'template_cn', '9.wav'),
                            os.path.join('material', 'cityname_cn', str(departure) + '.wav'), os.path.join('material', 'template_cn', '3.wav'), 
                            os.path.join('material', 'cityname_cn', str(stopover) + '.wav'), os.path.join('material', 'template_cn', '10.wav')]
                                                                                                # 迎接旅客的各位请注意，从 东京 经由 上海 飞来的
                    # 对于共享航班
                    for flight in flights:  # flight = 'CZ627' 然后 flight = 'JL5022'
                        name.append(os.path.join('material', 'airlines_cn', str(flight[:2]) + '.wav'))  # 中国南方航空公司
                        for i in flight:    # i = 'C' 然后 i ='Z' 然后 i = '6' ...
                            name.append(os.path.join('material', 'alnum_cn', str(i) + '.wav'))  # C-Z-6-2-7
                    
                    name.append(os.path.join('material', 'template_cn', '11.wav'))              # 次航班，已经到达本站，请您在到达大厅等候接待，谢谢
                
                # 英文广播部分
                if stopover == '':      # 如果没有经停站
                    name.append(os.path.join('material', 'template_en', '1.wav'))               # May I have your attention please.

                    # 对于共享航班
                    for flight in flights:  # flight = 'CZ627' 然后 flight = 'JL5022'
                        name.append(os.path.join('material', 'airlines_en', str(flight[:2]) + '.wav'))  # China Southern Airlines
                        name.append(os.path.join('material', 'template_en', '3.wav'))                   # Flight
                        for i in flight:    # i = 'C' 然后 i ='Z' 然后 i = '6' ...
                            name.append(os.path.join('material', 'alnum_en', str(i) + '.wav'))          # C-Z-6-2-7
                        
                    name.append(os.path.join('material', 'template_en', '9.wav'))                       # with service from
                    name.append(os.path.join('material', 'cityname_en', str(departure) + '.wav'))       # Tokyo Narita
                    name.append(os.path.join('material', 'template_en', '10.wav'))                      # has arrived
                    name.append(os.path.join('material', 'template_en', '8.wav'))                       # thank you

                elif stopover != '':    # 如果有经停站
                    name.append(os.path.join('material', 'template_en', '1.wav'))               # May I have your attention please.

                    # 对于共享航班
                    for flight in flights:  # flight = 'CZ627' 然后 flight = 'JL5022'
                        name.append(os.path.join('material', 'airlines_en', str(flight[:2]) + '.wav'))  # China Southern Airlines
                        name.append(os.path.join('material', 'template_en', '3.wav'))                   # Flight
                        for i in flight:    # i = 'C' 然后 i ='Z' 然后 i = '6' ...
                            name.append(os.path.join('material', 'alnum_en', str(i) + '.wav'))          # C-Z-6-2-7
                        
                    name.append(os.path.join('material', 'template_en', '9.wav'))                       # with service from
                    name.append(os.path.join('material', 'cityname_en', str(departure) + '.wav'))       # Shenyang
                    name.append(os.path.join('material', 'template_en', '11.wav'))                      # and
                    name.append(os.path.join('material', 'cityname_en', str(stopover) + '.wav'))        # Shanghai Pudong
                    name.append(os.path.join('material', 'template_en', '10.wav'))                      # has arrived
                    name.append(os.path.join('material', 'template_en', '8.wav'))                       # thank you

            # 以下是行李提取广播部分
            elif announcement_type == "Baggage_Claim":   # 调用 Baggage-Claim 广播的合成函数
                # 中文广播部分
                if stopover == '':      # 如果没有经停站
                    name = [os.path.join('material', 'mix', '756.wav'), os.path.join('material', 'template_cn', '1.wav')]
                                                                                                        # 乘坐
                    # 对于共享航班
                    for flight in flights:  # flight = 'CZ627' 然后 flight = 'JL5022'
                        name.append(os.path.join('material', 'airlines_cn', str(flight[:2]) + '.wav'))  # 中国南方航空公司
                        for i in flight:    # i = 'C' 然后 i ='Z' 然后 i = '6' ...
                            name.append(os.path.join('material', 'alnum_cn', str(i) + '.wav'))          # C-Z-6-2-7
 
                    name.append(os.path.join('material', 'template_cn', '2.wav'))                       # 次航班，从
                    name.append(os.path.join('material', 'cityname_cn', str(departure) + '.wav'))       # 沈阳
                    name.append(os.path.join('material', 'template_cn', '12.wav'))                      # 到达本站的旅客请注意，请前往
                    for i in baggage_claim:
                        name.append(os.path.join('material', 'alnum_cn', str(i) + '.wav'))              # B-2-8
                    name.append(os.path.join('material', 'template_cn', '13.wav'))                      # 号行李转盘提取您的行李，谢谢！
                    
                elif stopover != '':    # 如果有经停站
                    name = [os.path.join('material', 'mix', '756.wav'), os.path.join('material', 'template_cn', '1.wav')]
                                                                                                        # 乘坐
                    # 对于共享航班
                    for flight in flights:  # flight = 'CZ627' 然后 flight = 'JL5022'
                        name.append(os.path.join('material', 'airlines_cn', str(flight[:2]) + '.wav'))  # 中国南方航空公司
                        for i in flight:    # i = 'C' 然后 i ='Z' 然后 i = '6' ...
                            name.append(os.path.join('material', 'alnum_cn', str(i) + '.wav'))          # C-Z-6-2-7
                            
                    name.append(os.path.join('material', 'template_cn', '2.wav'))                       # 次航班，从
                    name.append(os.path.join('material', 'cityname_cn', str(departure) + '.wav'))       # 沈阳
                    name.append(os.path.join('material', 'template_cn', '3.wav'))                       # 经由
                    name.append(os.path.join('material', 'cityname_cn', str(stopover) + '.wav'))        # 上海浦东
                    name.append(os.path.join('material', 'template_cn', '12.wav'))                      # 到达本站的旅客请注意，请前往
                    for i in baggage_claim:
                        name.append(os.path.join('material', 'alnum_cn', str(i) + '.wav'))              # B-2-8
                    name.append(os.path.join('material', 'template_cn', '13.wav'))                      # 号行李转盘提取您的行李，谢谢！
                # 英文广播部分
                if stopover == '':      # 如果没有经停站
                    name.append(os.path.join('material', 'template_en', '1.wav'))                       # May I have your attention please.
                    name.append(os.path.join('material', 'template_en', '12.wav'))                      # Arriving passengers on
                    
                    # 对于共享航班
                    for flight in flights:  # flight = 'CZ627' 然后 flight = 'JL5022'
                        name.append(os.path.join('material', 'airlines_en', str(flight[:2]) + '.wav'))  # China Southern Airlines
                        name.append(os.path.join('material', 'template_en', '3.wav'))                   # Flight
                        for i in flight:    # i = 'C' 然后 i ='Z' 然后 i = '6' ...
                            name.append(os.path.join('material', 'alnum_en', str(i) + '.wav'))          # C-Z-6-2-7
                    
                    name.append(os.path.join('material', 'template_en', '9.wav'))                       # with service from
                    name.append(os.path.join('material', 'cityname_en', str(departure) + '.wav'))       # Shenyang
                    name.append(os.path.join('material', 'template_en', '13.wav'))                      # Your baggage will be available at baggage claim
                    for i in baggage_claim:
                        name.append(os.path.join('material', 'alnum_en', str(i) + '.wav'))              # B-2-8
                    name.append(os.path.join('material', 'template_en', '8.wav'))                       # Thank you
                elif stopover != '':    # 如果有经停站
                    name.append(os.path.join('material', 'template_en', '1.wav'))                       # May I have your attention please.
                    name.append(os.path.join('material', 'template_en', '12.wav'))                      # Arriving passengers on
                    
                    # 对于共享航班
                    for flight in flights:  # flight = 'CZ627' 然后 flight = 'JL5022'
                        name.append(os.path.join('material', 'airlines_en', str(flight[:2]) + '.wav'))  # China Southern Airlines
                        name.append(os.path.join('material', 'template_en', '3.wav'))                   # Flight
                        for i in flight:    # i = 'C' 然后 i ='Z' 然后 i = '6' ...
                            name.append(os.path.join('material', 'alnum_en', str(i) + '.wav'))          # C-Z-6-2-7
                    
                    name.append(os.path.join('material', 'template_en', '9.wav'))                       # with service from
                    name.append(os.path.join('material', 'cityname_en', str(departure) + '.wav'))       # Shenyang
                    name.append(os.path.join('material', 'template_en', '11.wav'))                      # And
                    name.append(os.path.join('material', 'cityname_en', str(stopover) + '.wav'))        # Shanghai Pudong
                    name.append(os.path.join('material', 'template_en', '13.wav'))                      # Your baggage will be available at baggage claim
                    for i in baggage_claim:
                        name.append(os.path.join('material', 'alnum_en', str(i) + '.wav'))              # B-2-8
                    name.append(os.path.join('material', 'template_en', '8.wav'))                       # Thank you
            
            # 以下是出发延误已定广播部分
            elif announcement_type == "Departure_Delay_Determined":   # 调用 Baggage-Claim 广播的合成函数        
                print('Departure_Delay_Determined')
            
            # 以下是出发延误未定广播部分
            elif announcement_type == "Departure_Delay_Undetermined":   # 调用 Baggage-Claim 广播的合成函数        
                print('Departure_Delay_Undetermined')
                
            # 以下是到达延误已定广播部分
            elif announcement_type == "Arrival_Delay_Determined":   # 调用 Baggage-Claim 广播的合成函数        
                print('Arrival_Delay_Determined')
                
            # 以下是到达延误未定广播部分
            elif announcement_type == "Arrival_Delay_Undetermined":   # 调用 Baggage-Claim 广播的合成函数        
                print('Arrival_Delay_Undetermined')
                    
            else:
                messagebox.showwarning("Warning", "Please choose an announcement type.")
                return


            # 检查name列表中所有需要的语音片段的路径是否正确，以及对应语音包是否都存在，如果不存在，则报错缺失的所有语音包文件路径
            missing_filename = []
            for wav_file in name:
                if os.path.exists(wav_file) == False:
                    missing_filename.append(wav_file)
            if missing_filename != []:
                # for missing_file in missing_filename:
                messagebox.showwarning("Warning", "Missing wav files!\nNo matching wav files for\n" + str(missing_filename))
                write_error_log("Missing wav files!\nNo matching wav files for\n" + str(missing_filename))
                return
            

            # name检索完毕，开始生成音频
            import pygame
            # 初始化pygame的子系统
            pygame.init()
            pygame.event.get()  # 清空事件队列


            # 引入进度条窗口
            root = tk.Tk()
            root.title("Importing voice packs")
            root.geometry("500x120")

            # 创建进度条
            progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
            progress_bar.pack(pady=20, padx=20, fill="both", expand=True)

            # 创建一个标签控件
            label = tk.Label(root, text="Importing voice packs", font=("Times New Roman", 15))
            label.pack()

            # 循环执行 len(name) 次，也就是要合成 len(name) 个语音片段
            i = 0
            for wav_file in name:
                i += 1
                try:
                    # 读取每个音频文件
                    sound = AudioSegment.from_wav(wav_file)
                    # 将音频文件添加到合并片段中
                    combined += sound
                except Exception as error_message:
                    messagebox.showerror("Error", f"Failed to load audio file: {wav_file}\nError message: {error_message}")
                    write_error_log(f"Failed to load audio file: {wav_file}\nError message: {error_message}")
                    continue

                update_progress(i, len(name), progress_bar, label, name[i - 1])  # 更新进度条和标签
                root.update()  # 刷新主窗口，以便更新进度条和标签

            # 循环完成后，稍作延时，然后销毁窗口
            import time
            time.sleep(0.5)
            root.destroy()
            
            # 将合并的片段导出为wav文件
            combined.export(os.path.join('output', str(flight_name) + '_' + str(announcement_type) + '.wav'), format="wav")

            time.sleep(0.5)

            pygame.mixer.init()
            pygame.mixer.music.load(os.path.join('output', str(flight_name) + '_' + str(announcement_type) + '.wav'))
            pygame.mixer.music.play()
            time.sleep(0.5)
            # pygame.mixer.music.get_busy() 判断是否正在播放音乐，返回1为正在播放
            while pygame.mixer.music.get_busy():
                time.sleep(1)
            # time.sleep(50)
            pygame.mixer.music.stop()
            pygame.quit()

        except pygame.error:
        # 如果发生错误（例如mixer尚未初始化），则忽略它
            pass
        
        except Exception as error_message:
            # 如果发生异常，捕获异常信息并显示错误消息框
            messagebox.showerror("Error", 'An error occurred during combining wav audio.\n' + str(error_message))
            write_error_log(error_message)
            return

        # 关闭输入窗口
        top.destroy()
    try:
        # 创建并启动播放音频的线程
        audio_thread = threading.Thread(target=play_announcement)
        audio_thread.start()
    except Exception as error_message:
        # 如果发生异常，捕获异常信息并显示错误消息框
        messagebox.showerror("Error", 'An error occurred when playing combined audio.\n' + str(error_message))
        write_error_log(error_message)
        return



# 这里储存账号和密码
passwords = [['wuhanqing', 'whq200501210517'], ['ll1272161887', 'JKcz627jl5022'], ['', '']]
def on_ok_click():
    if [account_entry.get(), password_entry.get()] in passwords:
        # messagebox.showinfo("Welcome", "Welcome to Automatic Flight Check-in Announcement System")
        import time
        time.sleep(0.5)
        root.destroy()  # 关闭欢迎界面
        # 在这里继续运行后续程序
    else:
        messagebox.showerror("Error", "Incorrect account or password. Please try again.")


# 点击按钮关闭窗口
def on_close_click():
    # 直接退出程序
    exit()


if __name__ == '__main__':    
    # 创建登录界面
    try:
        root = tk.Tk()
        root.title("Welcome")
        # 绑定关闭事件处理函数
        root.protocol("WM_DELETE_WINDOW", on_close_click)

        # 获取屏幕中心点的坐标
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 1400
        window_height = 800
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        root.geometry(f"{window_width}x{window_height}+{x}+{y}")    # 在指定位置（屏幕居中位置）显示窗口
        
        if os.path.exists(os.path.join("material", "pictures", "background.png")):
            bg_image = tk.PhotoImage(file=os.path.join("material", "pictures", "background.png"))
            bg_image = bg_image.subsample(1)    # 背景图片缩小倍数
            bg_label = tk.Label(root, image=bg_image)
            bg_label.place(relwidth=1, relheight=1)
        else:
            messagebox.showerror("Error", "Loading background picture failed!")

        text = "Welcome to Automatic Flight Check-in Announcement System\n\nClick 'Login' to start"
        text_label = tk.Label(root, text=text, font=("Times New Roman", 25), bg='lightblue', fg='black')
        text_label.place(relx=0.5, rely=0.4, anchor='center')

        account_label = tk.Label(root, text="Account:", font=("Times New Roman", 18), bg='lightblue', fg='black')
        account_label.place(relx=0.35, rely=0.5, anchor='center')
        account_entry = tk.Entry(root)
        account_entry.place(relx=0.5, rely=0.5, anchor='center')

        password_label = tk.Label(root, text="Password:", font=("Times New Roman", 18), bg='lightblue', fg='black')
        password_label.place(relx=0.35, rely=0.55, anchor='center')
        password_entry = tk.Entry(root, show="*")
        password_entry.place(relx=0.5, rely=0.55, anchor='center')

        login_button = tk.Button(root, text="Login", command=on_ok_click)   # 登录按钮
        login_button.place(relx=0.47, rely=0.6, anchor='center')
        exit_button = tk.Button(root, text="Exit", command=on_close_click)  # 退出按钮
        exit_button.place(relx=0.53, rely=0.6, anchor='center')

        root.mainloop()
    except Exception as error_message:
        # 如果发生异常，捕获异常信息并显示错误消息框
        messagebox.showerror("Error", error_message)
        write_error_log(error_message)


    # 主程序运行前，先尝试从xlsx文件读取航班数据data，并且将material文件夹下所有wav音频文件转换为双声道
    try:
        # 从Excel文件加载数据
        data = read_xlsx(filename)  # 如果读取成功，更新data变量
        
        source_directory = "material"  # 包含子文件夹的源文件夹路径
        convert_to_stereo(source_directory)     # 将material文件夹下所有wav音频文件转换为双声道

        messagebox.showinfo("Welcome", "Flight information read successfully!\nConverting audio files to dual-channel successfully!")
    except Exception as error_message:
        # 如果发生异常，捕获异常信息并显示错误消息框
        messagebox.showerror("Error", 'An error occurred when converting audio files to dual-channel.\n' + str(error_message))
        write_error_log(error_message)



    # 运行主程序
    try:
        # 创建主窗口
        root = tk.Tk()
        # 设置窗口大小为1500x800像素
        window_width = 1500
        window_height = 800
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")    # 设置窗口大小位置
        root.resizable(width=True, height=True)
        root.title("Automatic Flight Announcement System   Copyright belongs to @WuHanqing")


        # 创建一个Frame用于放置表格
        table_frame = tk.Frame(root)
        table_frame.pack(pady=10, expand=True, fill='both')

        # 创建表格，现在有12列
        table = ttk.Treeview(table_frame, columns=("Flight Number", "Departure", "Stopover", "Destination", "Divert", "Check-in Counter", "Boarding Gate", "Baggage Claim", "Scheduled Arrival Time", "Estimated Arrival Time", "Delay Reason", "Language Type"), show="headings")
        table.heading("Flight Number", text="Flight Number", anchor='center')
        table.heading("Departure", text="Departure", anchor='center')
        table.heading("Stopover", text="Stopover", anchor='center')
        table.heading("Destination", text="Destination", anchor='center')
        table.heading("Divert", text="Divert", anchor='center')
        table.heading("Check-in Counter", text="Check-in Counter", anchor='center')
        table.heading("Boarding Gate", text="Boarding Gate", anchor='center')
        table.heading("Baggage Claim", text="Baggage Claim", anchor='center')
        table.heading("Scheduled Arrival Time", text="Scheduled Arrival Time", anchor='center')
        table.heading("Estimated Arrival Time", text="Estimated Arrival Time", anchor='center')
        table.heading("Delay Reason", text="Delay Reason", anchor='center')
        table.heading("Language Type", text="Language Type", anchor='center')
        table.pack(fill='both', expand=True)

        # 设置每一列的宽度
        table.column("Flight Number", width=200)
        table.column("Departure", width=100)
        table.column("Stopover", width=100)
        table.column("Destination", width=100)
        table.column("Divert", width=100)
        table.column("Check-in Counter", width=100)
        table.column("Boarding Gate", width=100)
        table.column("Baggage Claim", width=100)
        table.column("Scheduled Arrival Time", width=120)
        table.column("Estimated Arrival Time", width=120)
        table.column("Delay Reason", width=150)
        table.column("Language Type", width=100)

        # 设置表格所在的Frame可以随着窗口变化而变化
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # 创建工作栏
        toolbar = tk.Frame(root, bg='lightblue')
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # 设置工作栏所在的Frame可以随着窗口变化而变化
        toolbar.grid_rowconfigure(0, weight=1)
        toolbar.grid_columnconfigure(0, weight=1)

        # 默认填充表格
        update_table(data)

        # 创建工作栏_1
        toolbar_1 = tk.Frame(root, bg='lightblue')
        toolbar_1.pack(side=tk.TOP, fill=tk.X)
        
        # 创建工作栏_2
        toolbar_2 = tk.Frame(root, bg='lightpink')
        toolbar_2.pack(side=tk.TOP, fill=tk.X)

        # 创建按钮并绑定函数

        # 创建添加航班按钮，绑定函数button1_fuction
        button1 = tk.Button(toolbar_1, text="Add flight", command=button1_function)
        button1.pack(side=tk.LEFT, padx=5, pady=6)
        
        # 创建删除航班按钮，绑定函数button2_fuction
        button2 = tk.Button(toolbar_1, text="Delete flight", command=button2_function)
        button2.pack(side=tk.LEFT, padx=5, pady=5)

        # 创建播放新航班广播按钮，绑定函数button3_fuction
        button3 = tk.Button(toolbar_1, text="Play new announcement", command=button3_function)
        button3.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 创建播放已有航班广播按钮，绑定函数button4_fuction
        button3 = tk.Button(toolbar_1, text="Play old announcement", command=button4_function)
        button3.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 创建停止音频按钮
        stop_button = tk.Button(toolbar_1, text="Stop All Process", command=stop_all_audio)
        stop_button.pack(side=tk.LEFT, padx=5, pady=5)

        # 创建保存信息按钮，将data作为参数传递给write_xlsx函数
        save_button = tk.Button(toolbar_2, text="Save Info", command=write_xlsx(data, filename))
        save_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # 创建刷新按钮，单击刷新按钮时调用refresh_table函数
        refresh_button = tk.Button(toolbar_2, text="Read Info", command=refresh_table)
        refresh_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # 创建清除按钮，不需要传递参数给clear_function
        clear_button = tk.Button(toolbar_2, text="Clear", command=clear_function)
        clear_button.pack(side=tk.RIGHT, padx=5, pady=5)


        # 运行主循环
        root.mainloop()
    except Exception as error_message:
        # 如果发生异常，捕获异常信息并显示错误消息框
        messagebox.showerror("Error", 'An error occurred when creating main window.\n' + str(error_message))
        write_error_log(error_message)