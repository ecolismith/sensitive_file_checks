import re
import os

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

if __name__ == '__main__':
    test_pwd()








