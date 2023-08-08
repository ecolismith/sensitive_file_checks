from fnmatch import fnmatch
import psutil
import os

def find_all_extensions(basedir, extension_list):
    target_path_list = list()
    processed_extension_list = list()
    for extension in extension_list:
        extension = "*."+extension
        processed_extension_list.append(extension)
    for root, dirs, files in os.walk(basedir):
        for file in files:
            path = os.path.join(root,file)
            for extension in processed_extension_list:
                if fnmatch(path, extension):
                    if os.access(path,os.R_OK):
                        print("找到文件："+path)
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

def get_extension_list(path):
    f = open(path,"r",encoding="utf8")
    extension_list = list()
    f.seek(0,2)
    eof = f.tell()
    f.seek(0,0)
    while f.tell() < eof:
        extension_list.append(f.readline().rstrip())
    f.close()
    return extension_list


if __name__ == '__main__':
    basedirs = get_disks()
    print(basedirs)
    extension_path = "extensions.properties"
    extension_list = get_extension_list(extension_path)
    target_path_list = list()
    for basedir in basedirs:
        target_path_list.extend(find_all_extensions(basedir, extension_list))
    f_result = open("数据文件搜索结果.txt", "w", encoding="utf8")
    for target_path in target_path_list:
        f_result.write(target_path+"\n")
    f_result.close()
    os.system("pause")
