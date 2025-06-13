from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import account
import re

class user:
    @staticmethod
    def get_user(request):
        return request.session.get('user_email', '')

class home_operation:
    
    @staticmethod
    def valid(email):
        email_condition = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.search(email_condition, email) is not None


    def get_login(self,request):
        return render(request, 'login/index_login.html')

    def index_sign_in(self,request):
        return render(request, 'login/index_sign_in.html')

    def validate(self,request):
        try:
            email = str(request.POST['email'])
            password = str(request.POST['password'])
            a = list(account.objects.filter(email=email, password=password))
            if a:
                request.session['user_email'] = email
                return redirect('home')
            else:
                return render(request, 'login/index_login.html')
        except Exception as e:
            return render(request, 'login/index_login.html')

    def create(self,request):
        try:
            name = str(request.POST['name'])
            email = str(request.POST['email'])
            password = str(request.POST['password'])

            if name == '':
                return render(request, 'login/index_sign_in_2.html', {'msg': 'Enter a Valid Name'})

            if email == 'email@example.com' or not self.valid(email):
                return render(request, 'login/index_sign_in_2.html', {'msg': 'Enter a Valid Email'})

            if account.objects.filter(email=email, password=password).exists():
                return render(request, 'login/index_sign_in_2.html', {'msg': 'The email is already in use!'})

            request.session['user_email'] = email
            acc = account(name=name.upper(), email=email, password=password)
            acc.save()
            return redirect('home')
        except Exception as e:
            return render(request, 'login/index_sign_in_2.html', {'msg': 'An error occurred: ' + str(e)})

    
    
    