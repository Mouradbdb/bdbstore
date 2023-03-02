from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

#verfication import
'''from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator,default_token_generator
from django.core.mail import EmailMessage
# Create your views here.'''

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password = make_password(password)
            username = email.split('@')[0]
            user = Account.objects.create(first_name=first_name,last_name=last_name,email=email,password=password,username = username)
            user.phone_number =phone_number
            user.is_active = True
            user.save()
            
            #user_activation
            
            '''current_site = get_current_site(request)
            mail_subject = 'plese activate your acc'
            message = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':PasswordResetTokenGenerator().make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            '''
            messages.success(request,'Registration successful')
            return redirect('register')



            
    else:
        form = RegistrationForm()
    context = {
        'form':form,
    }
    return render(request,'accounts/register.html',context)




def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password  = request.POST['password']
        user = auth.authenticate(email=email,password=password)
        if user != None :
            auth.login(request,user)
            return redirect('home')
        else:
            messages.error(request,'invalid login form')
            return redirect('login')
        
    return render(request,'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You Are Logged out')
    return redirect('login')
    
@login_required(login_url = 'login')

def dashboard(request):
    context = {

    }
    return render(request,'accounts/dashboard.html',context)

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        print(email)
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if Account.objects.filter(email=email).exists():
            if password == confirm_password :
                user = Account.objects.get(email=email)
                #password = make_password(password)
                user.set_password(password)
                user.save()
                messages.success(request,'password changed')
                return redirect('login')
            else:
                messages.error(request,'password do not match')
                return redirect('forgotpassword')

            
        else:
            messages.error(request,'Account does not exist ')
            return redirect('forgotpassword')
    else:
        return render(request,'accounts/forgotpassword.html')


'''def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password :
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            #password = make_password(password)
            user.set_password(password)
        else:
            messages.error(request,'password do not match')
            return redirect('resetpassword')
    return render(request,'accounts/resetpassword.html')'''