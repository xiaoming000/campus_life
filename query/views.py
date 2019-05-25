import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .spider import QuerySpider
from django.conf import settings
from .models import Course, QueryUsers
from users.models import User
from django.contrib.auth.hashers import make_password, check_password


@login_required()
def course_login(request):
    if request.method == 'POST':
        number = request.POST.get('number', '')
        password = request.POST.get('password', '')
        encrypt_password = make_password(password)
        check_code = request.POST.get('check_code', '')
        remember = request.POST.get('remember', '')
        # 如果记住密码 则存储账户密码
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        now = datetime.datetime.now()
        if remember:
            QueryUsers.objects.filter(user=user).delete()
            QueryUsers.objects.create(number=number, password=encrypt_password, user=user, last_login_time=now)
        else:
            # 修改登入时间
            QueryUsers.objects.filter(user=user).update(last_login_time=now)
        value = request.session['course_value']
        cookies = request.session['course_cookies']
        qs = QuerySpider()
        qs.login(number, password, check_code, value, cookies)
        info = qs.get_course()
        # 数据存储
        # 将已有的记录删除
        Course.objects.filter(user=user, xnd=info['xnd'], xqd=info['xqd']).delete()
        # 增加数据
        Course.objects.create(user=user, xnd=info['xnd'], xqd=info['xqd'], number=info['number'], name=info['name'], faculty=info['faculty'], major=info['major'], a_class=info['a_class'], course_table=info['course_table'])
        return redirect('/query/courses')
    else:
        # 保存文件必须输入完整路径
        user_id = request.user.id
        static_url = settings.STATICFILES_DIRS[0] + "\code\\" + str(user_id) + ".jpg"
        qs = QuerySpider()
        res = qs.get_img(static_url)
        request.session['course_cookies'] = res[0]
        request.session['course_value'] = res[1]
        context = {
            'id': str(user_id),
        }
        return render(request, 'query/course_login.html', context=context)


@login_required()
def grade_login(request):
    if request.method == 'POST':
        number = request.POST.get('number', '')
        password = request.POST.get('password', '')
        year = request.POST.get('year', '')
        term = request.POST.get('term', '')
        encrypt_password = make_password(password)
        check_code = request.POST.get('check_code', '')
        remember = request.POST.get('remember', '')
        # 如果记住密码 则存储账户密码
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        now = datetime.datetime.now()
        if remember:
            QueryUsers.objects.filter(user=user).delete()
            QueryUsers.objects.create(number=number, password=encrypt_password, user=user, last_login_time=now)
        else:
            # 修改登入时间
            QueryUsers.objects.filter(user=user).update(last_login_time=now)
        value = request.session['course_value']
        cookies = request.session['course_cookies']
        qs = QuerySpider()
        qs.login(number, password, check_code, value, cookies)
        info = qs.get_grade(year, term)
        for grade in info['grades']:
            del grade[0:3]
            del grade[2:3]
            del grade[6:8]
            del grade[5:6]
            del grade[-3:]
        return render(request, 'query/grade.html', context=info)
    else:
        # 保存文件必须输入完整路径
        user_id = request.user.id
        static_url = settings.STATICFILES_DIRS[0] + "\code\\" + str(user_id) + ".jpg"
        qs = QuerySpider()
        print(static_url)
        res = qs.get_img(static_url)
        request.session['course_cookies'] = res[0]
        request.session['course_value'] = res[1]
        context = {
            'id': str(user_id),
        }
        return render(request, 'query/grade_login.html', context=context)


# 成绩展示
@login_required()
def courses(request):
    user = request.user
    course_info = Course.objects.filter(user=user).order_by('-xnd', 'xqd')   # user=user,
    if course_info:
        context = {
            'xnd': course_info[0].xnd,
            'xqd': course_info[0].xqd,
            'number': course_info[0].number,
            'name': course_info[0].name,
            'faculty': course_info[0].faculty,
            'major': course_info[0].major,
            'a_class': course_info[0].a_class,
            'course_table': course_info[0].course_table
        }
        return render(request, 'query/course.html', context=context)
    else:
        return redirect('/query/course_login')


