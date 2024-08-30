from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .forms import *
from django.contrib.auth import logout, login
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import UpdateView, CreateView, DeleteView, ListView
from django.contrib.auth.models import User

# Create your views here.


# =================================================================
def signup(request):
    context = {}
    form = SignUpForm()
    context["form"] = form
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("home")
    return render(request, "accounts/signup.html", context)


# class CustomLoginView(LoginView):
#     # template_name = "accounts/login.html"
#     # redirect_authenticated_user = True
#     # success_url = reverse_lazy("home")
#     def get(self, request):
#         login(request)
#         return redirect("home")  # Redirect to the home page or any other page

#     def post(self, request):
#         login(request)
#         return redirect("home")


# class CustomLoginView(View):
#     def post(self, request, *args, **kwargs):
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         # التحقق من صحة بيانات تسجيل الدخول
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             # تسجيل دخول المستخدم
#             login(request, user)
#             return redirect("home")  # توجيه إلى الصفحة الرئيسية بعد تسجيل الدخول
#         else:
#             # عرض رسالة خطأ إذا كانت بيانات الاعتماد غير صحيحة
#             return render(
#                 request, "accounts/login.html", {"error": "Invalid credentials"}
#             )


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = AuthenticationForm


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("signup")  # Redirect to the signup page or any other page

    def post(self, request):
        logout(request)
        return redirect("signup")


class UserUpdateView(UpdateView):
    model = User
    fields = ("first_name", "last_name", "email")
    template_name = "accounts/my_account.html"
    success_url = reverse_lazy("my_account_done")

    def get_object(self):
        return self.request.user


def user_update_view_done(request):
    context = {}
    context["user"] = request.user
    return render(request, "accounts/my_account_done.html", context)
