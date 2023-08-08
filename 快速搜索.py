import os
from pandas import read_excel
from fnmatch import fnmatch
from psutil import disk_partitions
import xlrd

#该代码的功能是查询系统内所有敏感的excel信息
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
    search_xls()


