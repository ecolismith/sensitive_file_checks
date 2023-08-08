import tkinter as tk
import os
import re
from pandas import read_excel
from fnmatch import fnmatch
from psutil import disk_partitions
import xlrd

title = "网络安全自我检查工具"
main_text = "请选择您需要使用的功能"
custom_font = ("黑体", 16)
button1_name = "检查口令强度"
button2_name = "检索敏感表格文件"
button3_name = "检索数据格式文件"
button4_name = "查找可能存有密码的文件"

def on_button_click(button_number):
    if button_number==1:
        test_pwd()
    elif button_number==2:
        search_xls()
    else:
        label.config(text=f"Button {button_number} Clicked!")




def center_window(window, width_percent, height_percent):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = int(screen_width * width_percent)
    window_height = int(screen_height * height_percent)
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

def create_button1(i):
    button = tk.Button(root, text=button1_name, command=lambda i=i: on_button_click(i))
    return button

def create_button2(i):
    button = tk.Button(root, text=button2_name, command=lambda i=i: on_button_click(i))
    return button

def create_button3(i):
    button = tk.Button(root, text=button3_name, command=lambda i=i: on_button_click(i))
    return button

def create_button4(i):
    button = tk.Button(root, text=button4_name, command=lambda i=i: on_button_click(i))
    return button

pat_char = re.compile(r"[a-zA-Z]")
pat_digit = re.compile(r"\d+")
pat_spec = re.compile(r"[!@#$%^&*()<>?/\|{}~]")
common_list = ["123","abc","110","Sjj","pass","qwer","asdf","zxcv"]

def test(var):
    if len(var) < 8:
        print("密码长度至少应该为8位")
        return False

    if var.find(' ')!=-1:
        print("密码中间不能有空格")
        return False

    if not pat_digit.search(var):
        print("密码应该包含数字,字母和特殊字符,该密码缺少数字")
        return False

    for common in common_list:
        if common in var:
            print("密码中不应该有"+common+"这么简单的序列")
            return False

    if not pat_char.search(var):
        print("密码应该包含数字,字母和特殊字符,该密码缺少字母")
        return False
    if not pat_spec.search(var):
        print("密码应该包含数字,字母和特殊字符,该密码缺少特殊字符")
        return False
    print("恭喜您，密码强度足够")

    return True

def test_pwd():
    var = "test"
    print("口令至少应该有8位，包含数字，字母和特殊符号,中间不能有空格")
    while(var != "exit"):
        print("请输入您的口令来判断是否为弱口令，输入exit退出")
        var = input()
        var = var.strip()
        if var == "exit":
            break
        test(var)
    print("已经退出口令强度判断程序")
    os.system("pause")

def read_excel_headers(exl_path):
    print("检查文件:"+exl_path)
    try:
        df = read_excel(exl_path)
        headers = df.columns.tolist()
    except ValueError as e:
        print(e)
        return None
    except xlrd.biffh.XLRDError as e:
        return None
    return headers

def read_sensitive(sensitive_path):
    f = open(sensitive_path,"r",encoding="utf8")
    sensitive_list = list()
    f.seek(0,2)
    eof = f.tell()
    f.seek(0,0)
    while f.tell() < eof:
        word = f.readline().rstrip()
        if word != "" or " ":
            sensitive_list.append(word)
    f.close()
    return sensitive_list

def examine_header(exl_path,headers,sensitive_list,f_result):
    for header in headers:
        header = str(header)
        for s_word in sensitive_list:
            if s_word in header:
                report = "文件目录："+exl_path+"  的表头\""+header+"\"含有敏感元素\""+s_word+"\"\n"
                f_result.write(report)
                print(report)
                return

def go_through_excels(excel_path_list,sensitive_list,f_result):
    for exl_path in excel_path_list:
        try:
            headers = read_excel_headers(exl_path)
            if headers != None:
                examine_header(exl_path,headers,sensitive_list,f_result)
        except Exception as e:
            print(e)


def find_all_xls(basedir):
    excel_path_list = list()
    for root, dirs, files in os.walk(basedir):
        for file in files:
            path = os.path.join(root,file)
            if fnmatch(path, "*.xls") or fnmatch(path, "*.xlsx"):
                if os.access(path,os.R_OK):
                    print("找到文件："+path)
                    excel_path_list.append(path)
    return excel_path_list

def get_disks():
    basedirs = list()
    for sdiskpart in disk_partitions():
        print(sdiskpart)
        basedirs.append(sdiskpart.device)
    return basedirs
def search_xls():
    basedirs = get_disks()
    print(basedirs)
    try:
        f_result = open("敏感xls表格检查结果.txt", "w", encoding="utf8")
        for basedir in basedirs:
            excel_path_list = find_all_xls(basedir)
            sensitive_list = read_sensitive("sensitive words.properties")
            go_through_excels(excel_path_list, sensitive_list,f_result)
        f_result.close()
        os.system("pause")
    except Exception as e:
        print(e)
        os.system("pause")



if __name__ == '__main__':

    root = tk.Tk()
    root.title(title)

    center_window(root, 0.2, 0.2)  # Set window size to 20% of screen width and height

    label = tk.Label(root, text=main_text, font=custom_font)
    label.pack()


    button1 = create_button1(1)
    button1.pack(fill=tk.BOTH, expand=True)

    button2 = create_button2(2)
    button2.pack(fill=tk.BOTH, expand=True)

    button3 = create_button3(3)
    button3.pack(fill=tk.BOTH, expand=True)

    button4 = create_button4(4)
    button4.pack(fill=tk.BOTH, expand=True)

    root.mainloop()