from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth, messages
from .models import User
from .forms import SignupForm, ProfileForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import PasswordChangeForm




# class ProfileView(LoginRequiredMixin, TemplateView): # login_required
#     template_name = 'accounts/profile.html'

# profile = ProfileView.as_view()


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "프로필을 수정/저장했습니다.")
            return redirect('profile_edit')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile_form.html',{'form': form,})

# 비밀번호 변경
@login_required
def password_edit(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        # 키워드인자명을 함께 써줘도 가능
        # password_change_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_change_form.is_valid():
            password_change_form.save()
            return redirect('postlist')
    else:
        password_change_form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password_form.html',{
        						'password_change_form':password_change_form
    										})


# # 회원 가입
def signup(request):
#     # signup 으로 POST 요청이 왔을 때, 새로운 유저를 만드는 절차를 밟는다.
    if request.method == 'POST':
        form = SignupForm(request.POST)
        print(request.GET.get('city'))
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "회원가입을 환영합니다.")
            next_url = request.GET.get('next', 'postlist')
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, "accounts/signup_form.html",{'form':form,})

# 로그인
login = LoginView.as_view(template_name="accounts/login_form.html")

# 로그 아웃
def logout(request):
    # logout으로 POST 요청이 들어왔을 때, 로그아웃 절차를 밟는다.
    if request.method == 'POST':
        messages.success(request, '로그아웃되었습니다.')
        auth.logout(request)
        return redirect('/')

    # logout으로 GET 요청이 들어왔을 때, 로그인 화면을 띄워준다.
    return render(request, 'accounts/login_form.html')


# 회원 탈퇴
@login_required
def delete(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('/')
    return render(request, 'accounts/delete_form.html')

def developer(request):
    return render(request,'accounts/developer.html')