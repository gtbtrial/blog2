import json
import urllib

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import login, logout  # as DjangoLogout
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView


from .forms import BlogNew
from .models import RegisterForm, Login, BlogEntries


def index(request):
    return render(request, "index.html")


class signup(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = 'signup.html'
    success_url = '/new-registration'
    success_message = "Signup successful"

    def dispatch(self, *args, **kwargs):
        return super(signup, self).dispatch(*args, **kwargs)


def mylogin(request):
    form = Login(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        user = form.cleaned_data.get("user")
        userobj = User.objects.get(username__iexact=username)
        login(request, userobj)
        request.session["uname"] = username
        request.session["userid"] = user
        return HttpResponseRedirect(reverse("userpanel"))
    else:
        return render(request, "login.html", {"form": form})


def mylogout(request):
    logout(request)
    # DjangoLogout(request)
    return HttpResponseRedirect(reverse("meralogin"))


@login_required(login_url="/user-login/")
def blogsuccess(request):
    return render(request, "blogsuccess.html")


def userpanel(request):
    if request.user.is_authenticated:
        if request.session.has_key("uname"):
            # obj = BlogEntries.objects.all()
            obj = BlogEntries.objects.filter(user=request.user)
            context = {"entries": obj}
            return render(request, "userpanel.html", context)


        else:
            return HttpResponseRedirect(reverse("meralogin"))
    else:
        return HttpResponseRedirect(reverse("meralogin"))


@login_required(login_url="/user-login/")
def newblog(request):
    if request.method == "POST":
        formobj = BlogNew(request.POST, request.FILES)
        if formobj.is_valid():
            data = formobj.save(commit=False)
            data.user = request.user
            data.save()
            return HttpResponseRedirect(reverse('blogsuccess'))
    else:
        formobj = BlogNew()
    return render(request, "newblog.html", {"myform": formobj})


@method_decorator(login_required, name='dispatch')
class updateblog(SuccessMessageMixin, UpdateView):
    model = BlogEntries
    template_name = 'updateblog.html'
    fields = ['title', 'blog_body']
    success_message = "Updation successful"

    def get_object(self, queryset=None):
        blogid = self.kwargs['pk']
        obj = BlogEntries.objects.get(id=blogid)

        return obj

    def get_success_url(self):
        return ('/update-blog/' + str(self.kwargs['pk']))


def fetchblog(request):
    # obj = BlogEntries.objects.all()
    obj = BlogEntries.objects.filter(user=request.user)
    context = {"entries": obj}
    return render(request, "blog_list.html", context)




def deleteblog(request, pk):
    BlogEntries.objects.filter(id=pk).delete()
    obj = BlogEntries.objects.filter(user=request.user)
    context = {"entries": obj}
    return render(request, "blog_list.html", context)

def contactus(request):
    if request.method == 'POST':
        data = request.POST
        name = data.get("name", "0")
        emailid = data.get("emailid", "0")
        phone = data.get("phone", "0")
        message = data.get("message", "0")
        fullmessage = "Name : " + name + "\nPhone : " + phone + "\nEmail id : " + emailid + "\nMessage : " + message

        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        ''' End reCAPTCHA validation '''

        if result['success']:
            send_mail(
                'Mail from website',
                fullmessage,
                emailid,
                ['gtbcomputers@gmail.com'],
                fail_silently=False,
            )
            context = {"message": "Your message has been received. We will contact us shortly"}
        else:
            context = {"message": "Please confirm that u are human"}
        return render(request, "contactus.html", context)
    else:
        return render(request, "contactus.html")

def changepass(request):
    if request.method == 'POST':
        data = request.POST
        myusername = request.session["uname"]
        oldpassword = data.get("oldpassword", "0")
        user = authenticate(request, username=myusername, password=oldpassword)
        if user is None:
            context = {"message2": "Wrong old password"}
        else:
            password1 = data.get("password1", "0")
            password2 = data.get("password2", "0")
            if password1 == password2:

                u = User.objects.get(username__iexact=myusername)
                u.set_password(password1)
                u.save()
                context = {"message1": "Password changed successfully. Please login again"}
            else:
                context = {"message2": "Password does not match"}
        return render(request, "changepassword.html", context)
    else:
        return render(request, "changepassword.html")

#
# class FetchBlog(ListView):
#     model = BlogEntries
#     template_name = 'blog_list.html'

def bad_request(request):
   context = {}
   return render(request, '404.html', context, status=400)


def permission_denied(request):
   context = {}
   return render(request, '404.html', context, status=403)


def page_not_found(request):
   context = {}
   return render(request, '404.html', context, status=404)


def server_error(request):
   context = {}
   return render(request, '404.html', context, status=500)
