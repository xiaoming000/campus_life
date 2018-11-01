def str_center(str1, str2, str3, num):
    print('+' + '-' * (num-2) + '+')
    print('|' + str1.center(num-2) + '|')
    print('|' + str2.center(num - 2) + '|')
    print('|' + str3.center(num - 2) + '|')
    print('+' + '-' * (num-2) + '+')


if __name__ == '__main__':
    str_center('hello world', 'today is Monday', 'my name is XX', 30)
