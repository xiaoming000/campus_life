from django.shortcuts import render, redirect, reverse, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.http import JsonResponse, Http404
from .forms import EditProForm, EditUserForm
from .models import User, Profile, Follow, Message
from django.contrib.auth import authenticate, login, logout
from django.views import View, generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages


def index(request):
    context = {
        'htitle': '校园生活-首页'
    }
    return render(request, 'users/index.html', context)


class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class EditBaseView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'users/edit_base.html'
    context_object_name = 'user_it'

    def get(self, request, *args, **kwargs):
        response = super(EditBaseView, self).get(request, *args, **kwargs)
        user_it = super(EditBaseView, self).get_object(queryset=None)
        # redirect(reverse('users:edit', kwargs={'pk': user_it.id}))
        # redirect('edit/' + kwargs['pk'] + '/')
        # return  HttpResponse(kwargs['pk'])
        return response

    def get_context_data(self, **kwargs):
        context = super(EditBaseView, self).get_context_data(**kwargs)
        user_it = super(EditBaseView, self).get_object(queryset=None)
        context.update({
            'user_it': user_it,
        })
        return context


def edit_nav(request):
    if request.session['user_it']:
        user_it = request.session['user_it']
    else:
        raise Http404
    return render(request, 'users/_edit_nav.html', {'user_it': user_it})


class InfoView(LoginRequiredMixin, View):

    def get(self, request, pk):
        user = request.user
        user_it = get_object_or_404(User, pk=pk)
        # user_pro = get_object_or_404(Profile, pk=pk)
        user_pro = Profile.objects.filter(pk=pk)
        request.session['user_it'] = pk
        follower = Follow.objects.filter(follower=pk)

        identity = 0
        if user_it == user:
            identity = 1
        context = {
            'identity': identity,
            'user_it': user_it,
            'user_pro': user_pro,
            'follower': follower,
        }
        return render(request, 'users/info.html', context=context)


class EditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user_it = get_object_or_404(User, pk=pk)
        user_info = get_object_or_404(Profile, pk=pk)
        context = {
            'user_it': user_it,
            'user_info': user_info,
        }
        return render(request, 'users/edit.html', context=context)

    def post(self, request, pk):
        user_it = get_object_or_404(User, pk=pk)
        user_info = get_object_or_404(Profile, pk=pk)

        user_form = EditUserForm(request.POST, instance=user_it)
        pro_form = EditProForm(request.POST, instance=user_info)
        if user_form.is_valid() and pro_form.is_valid():
            try:
                user_form.save()
                pro_form.save()
            except:
                raise Http404("保存失败！")
            messages.success(request, '修改成功！')
            return redirect('/info/' + pk + '/')
        else:
            context = {
                'user_form': user_form,
                'pro_form': pro_form
            }
            return render(request, 'users/edit.html', context=context)


class EditActivateView(LoginRequiredMixin, View):

    def get(self, request, user_pk):
        user_it = get_object_or_404(User, pk=user_pk)
        user_pro = get_object_or_404(Profile, pk=user_pk)
        context = {
            'user_it': user_it,
            'user_pro': user_pro
        }
        return render(request, 'users/activate.html', context=context)

    def post(self, request, user_pk):
        user_pro = get_object_or_404(Profile, pk=user_pk)
        name_show = request.POST.get('name_show', '')
        email_show = request.POST.get('email_show', '')
        follow_show = request.POST.get('follow_show', '')
        collects_show = request.POST.get('collects_show', '')
        name_show = 1 if name_show else 0
        email_show = 1 if email_show else 0
        follow_show = 1 if follow_show else 0
        collects_show = 1 if collects_show else 0
        try:
            user_pro.name_show = name_show
            user_pro.email_show = email_show
            user_pro.follow_show = follow_show
            user_pro.collects_show = collects_show
            user_pro.save()
            messages.success(request, '隐私设置修改成功！')
        except:
            raise Http404
        return redirect('/info/' + user_pk + '/')


class EditUserDel(LoginRequiredMixin, View):
    def get(self, request, user_pk):
        user_it = get_object_or_404(User, pk=user_pk)
        user_pro = get_object_or_404(Profile, pk=user_pk)
        context = {
            'user_it': user_it,
            'user_pro': user_pro
        }
        return render(request, 'users/Edit_user_del.html', context=context)

    def post(self, request, user_pk):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user_del = authenticate(request, username=username, password=password)
        # return HttpResponse(user.id)
        if user_del == request.user or request.use.is_staff:
            try:
                user_del.is_active = 0
                user_del.save()
                messages.success(request, '隐私设置修改成功！')
            except:
                raise Http404
        else:
            raise Http404
        return redirect('/info/' + user_pk + '/')


class MessageView(LoginRequiredMixin, generic.ListView):
    model = Message
    template_name = 'users/message.html'
    context_object_name = 'message'

    def get_queryset(self):
        return super(MessageView, self).get_queryset().filter(is_delete=0)


class MessageNoReadView(MessageView):

    def get_queryset(self):
        return super(MessageNoReadView, self).get_queryset().filter(is_delete=0, is_read=0)


class MessageReadView(MessageView):

    def get_queryset(self):
        return super(MessageReadView, self).get_queryset().filter(is_delete=0, is_read=1)