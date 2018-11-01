def print_str1():
    print('########')
    print('#      #')
    print('#      #')
    print('########')


def print_str2():
    print('  *  ')
    print(' *** ')
    print('*****')


def print_area(r):
    pi = 3.14
    s = pi*r**2
    c = 2*r*pi
    print("这个圆的周长为 %s 厘米！" % c)
    print("这个圆的面积为 %s 平方厘米！" % s)


def print_transform(num):
    a, b = num // 16, num % 16
    print("你输入的为 %s 斤 %s 两" % (a, b))


if __name__ == '__main__':
    print_str1()
    print_str2()
    print_area(3)
    print_transform(216)