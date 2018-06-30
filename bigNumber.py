#_*_ coding:utf8 _*_
# 此处可 import 模块

"""
@param string line 为单行测试数据
@return string 处理后的结果
"""
def solution(line):
    # 缩进请使用 4 个空格，遵循 PEP8 规范
    # 返回处理后的结果
    data = line.strip().split("-")
    a = data[0]
    b = data[1]
    print a
    print b
    al = len(a)-1
    bl = len(b)-1
    re = 0
    while bl >= 0:
        at = a[al] - '0'
        bt = b[bl] - '0'
        if at - bt - re >= 0:
            re = 0
        	a[al] = at - bt - re + '0'
       	else:
            re = 1
            a[al] = at + 10 - bt - re + '0'
        al -= 1
        bl -= 1
    a[al] -= re
    return a

if __name__ == '__main__':
    print solution("13124314314321343124321421-423143214")