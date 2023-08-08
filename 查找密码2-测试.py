from fnmatch import fnmatch
import psutil
import os
import subprocess

def run_cmd_and_get_output(cmd):
    try:
        result = subprocess.check_output(cmd, shell=True)
        return result
    except subprocess.CalledProcessError as e:
        # print(f"命令执行失败: {e}")
        return None

def find_all_code(basedir, pwd):
    target_path_list = list()
    code_pattern = pwd+'.*'
    processed_extension_list = [r'*.txt',r'*.doc',r'*.docx',code_pattern]

    for root, dirs, files in os.walk(basedir):
        for file in files:
            path = os.path.join(root,file)
            for extension in processed_extension_list:
                if fnmatch(path, extension):
                    if os.access(path,os.R_OK):
                        print("找到文件："+path)
                        if extension == code_pattern:
                            target_path_list.append(path)
                        elif extension == r'*.doc' or extension==r'*.docx':
                            cmd = r'findstr /s /i /n '+ pwd +' '+path
                            result = run_cmd_and_get_output()
                            if result != None:
                                target_path_list.append(path)

                        break
    for path in target_path_list:
        print("test:"+path)
        break
    return target_path_list

def get_disks():
    basedirs = list()
    for sdiskpart in psutil.disk_partitions():
        print(sdiskpart)
        basedirs.append(sdiskpart.device)
    return basedirs


if __name__ == '__main__':
    basedirs = get_disks()
    print(basedirs)
    pwd = input("请输入您要搜索的密码： ")
    target_path_list = list()
    for basedir in basedirs:
        target_path_list.extend(find_all_code(basedir, pwd))

    f_result = open("密码搜索结果.txt", "w", encoding="utf8")
    for target_path in target_path_list:
        f_result.write(target_path+"\n")
    f_result.close()
    os.system("pause")