import os
from psutil import disk_partitions
import subprocess

def run_cmd_and_get_output(cmd):
    try:
        result = subprocess.check_output(cmd, shell=True)
        return result
    except subprocess.CalledProcessError as e:
        # print(f"命令执行失败: {e}")
        return None


def get_disks():
    basedirs = list()
    for sdiskpart in disk_partitions():
        basedirs.append(sdiskpart.device)
    if basedirs[0] == basedirs[1]:
        basedirs.pop(0)
    print(basedirs)
    return basedirs

def output2list(output,disk):
    output = str(output)
    tmp = output.split(disk)
    result = list()
    for path in tmp:
        if path != '':
            path = disk+path
            path = path.replace(r'\\','/')
            result.append(path)
    return result

def divide_result(stra):
    idx = stra.find(".txt")

    path = stra[0:idx + 4]
    b = stra[idx + 4:-1]
    idx = b.find(':', 2)
    code = b[idx + 1:-1]
    line_num = b[1:idx]
    result = "文件地址："+path +"\t所在行:"+line_num+"\t密码内容："+code
    return result

if __name__ == '__main__':
    target = input("请输入您想要查找的密码: ")
    disks = get_disks()
    result_list = list()
    # disks = [r'D:\\', r'E:\\', r'F:\\']
    for disk in disks:
        cmd = r'findstr /s /i /n '+ target +' '+disk+'*.txt'
        print("执行命令："+cmd)
        print("正在搜索："+ disk[0:1]+"盘")
        print("搜索磁盘的时间较长，可能需要几分钟，请您耐心等待")
        output = run_cmd_and_get_output(cmd)
        print("test: ",output)
        if output != None and output != "":
            result_list.extend(output2list(output,disk))
    try:
        f = open("疑似含有密码的文本文件.txt",'w',encoding='utf8')
        for path in result_list:
            result = divide_result(path)
            f.write(result+"\n")
        f.close()
        print("搜索完成，可能存放密码的文本文档具体信息保存于：疑似含有密码的文本文件.txt")
        os.system("pause")

    except Exception as e:
        print(e)
