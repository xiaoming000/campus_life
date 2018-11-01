facuty1 = int(input('请输入第一科的成绩：'))
facuty2 = int(input('请输入第二科的成绩：'))
facuty3 = int(input('请输入第三科的成绩：'))
max =facuty1
min = facuty1
avx = (facuty1 + facuty2 + facuty3) / 3
if facuty2 > max:
    max = facuty2
if facuty3 > max:
    max = facuty3

if facuty2 < max:
    min = facuty2
if facuty3 < max:
    min = facuty3

print("最大为：%s; 最小为：%s; 平均成绩为：%s" % (max, min, avx))
