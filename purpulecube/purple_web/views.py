from django.shortcuts import render, redirect
import pyodbc
from django import forms
from .forms import RegistrationForm,SignUpForm
from .db import insert_user,connect_to_db, save_form_data
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout #update_session_auth_hash
from .db import insert_user_signup,insert_user,connect_to_db
from .forms import RegistrationForm
from .models import NewTest1

def sign_up(request):
    if request.method == 'POST':
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            name = fm.cleaned_data['username']
            first_name=fm.cleaned_data['first_name']
            email = fm.cleaned_data['email']
            pwd = fm.cleaned_data['password1']
            
            
            conn = connect_to_db()
            if conn:
                insert_user_signup(conn, name,first_name, email, pwd)
                messages.info(request, 'Your Account Successfully Created..!!!')
            else:
                messages.error(request, 'Error connecting to the database.')

            fm.save()
    else:
        fm = SignUpForm()
    return render(request, 'signup.html', {'form': fm})


def login_form(request):
    if not request.user.is_authenticated:


        if request.method=='POST':
            fm = AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                upass=fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user:
                    login(request, user)
                    messages.success(request, 'Logged  in successfully')
                    return HttpResponseRedirect('/profile/')
        else:
            fm = AuthenticationForm()
        return render(request, 'loginform.html', {'form':fm})
    else:
        return HttpResponseRedirect('/profile/') 



def profile(request):
    
      
    if request.method == 'POST':
        form_data = {
            
            'Que1': request.POST.get('Que1'),
            'Que2': request.POST.get('Que2'),

            'Que3': request.POST.get('Que3'),
            'Que4': request.POST.get('Que4'),
            
            
            
        }
        save_form_data(form_data)

        return render(request, 'summary.html', {'data': form_data})

    

    if request.user.is_authenticated:
        return render(request, 'test.html', {'name': request.user})
    else:
        return HttpResponseRedirect('/login/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

 

class RegistrationForm(forms.Form):

    full_name = forms.CharField(label='Full Name', max_length=100)
    email = forms.EmailField(label='Email')
 

def placeholder_view(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            selected_name = form.cleaned_data['full_name']
            selected_email = form.cleaned_data['email']
            try:
                connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-7JF3UC3K\SQLEXPRESS;DATABASE=test;Trusted_Connection=yes;')
                cursor = connection.cursor()
                cursor.execute("SELECT full_name, email FROM test7 WHERE full_name = ? AND email = ?", (selected_name, selected_email))
                rows = cursor.fetchall()
                if not rows:
                    return render(request, 'record_not_found.html')
                formatted_strings = []
                for row in rows:
                    name = row[0]
                    email = row[1]
                    formatted_string = f"I'm {name} and {email} this is my contact mail id"
                    formatted_strings.append(formatted_string)

                cursor.close()
                connection.close()
                return render(request, 'err_template.html', {'formatted_strings': formatted_strings})
            except pyodbc.Error as e:
                error_message = str(e)
                return render(request, 'err_template.html', {'error_message': error_message})
    else:
        form = RegistrationForm()
    return render(request, 'export_data.html', {'form': form})
