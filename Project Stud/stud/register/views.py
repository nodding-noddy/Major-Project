from django.shortcuts import render
from django import forms
from register.models import Admin,Student_data,Branch
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib import messages
from . import generator
from zipfile import ZipFile
import os
import qrcode
from django.core.exceptions import ObjectDoesNotExist
import shutil
# Create your views here.
email = None
class Login_form(forms.Form):
    email = forms.CharField(max_length = 30,
    widget=forms.EmailInput(
        attrs= {
            'class': 'form-control'
        }
    ))
    password = forms.CharField(widget = forms.PasswordInput(
        attrs ={
            'class':'form-control'
        }
    ))

class Create_account(forms.Form):
    first_name = forms.CharField(max_length = 20)
    
    last_name = forms.CharField(max_length = 20)

    email = forms.CharField(max_length = 35)

    password = forms.CharField(max_length = 20,min_length=8)

    password2 = forms.CharField(max_length = 20,min_length = 8)
    
def create_account(request):
    if request.method == 'POST':
        form = Create_account(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            try:
                Admin.objects.get(email = email)
                return HttpResponseRedirect(reverse('create_account'),{
                    messages.add_message(request,messages.ERROR,'An account with that email address already exists!'),
                })
            except ObjectDoesNotExist:
                password = form.cleaned_data['password']
                password2 = form.cleaned_data['password2']
                if password == password2:
                    branch = request.POST['b_data']
                    try:
                        branch = Branch.objects.get(branch_code = branch)
                        admin = Admin(first_name = first_name.capitalize(),last_name = last_name.capitalize(),email = email,password = password,branch = branch)
                        admin.save()
                        return HttpResponseRedirect(reverse('create_account'),{
                            messages.add_message(request,messages.SUCCESS,'Successfully Registered!')
                        })
                    except ObjectDoesNotExist:
                        return HttpResponseRedirect(reverse('create_account'),{
                            messages.add_message(request,messages.ERROR,'Please select your branch'),
                        })
                else:
                    return HttpResponseRedirect(reverse('create_account'),{
                            messages.add_message(request,messages.ERROR,'Both passwords should match'),
                                
                        })
        else:
            return HttpResponseRedirect(reverse('create_account'),{
                messages.add_message(request,messages.ERROR,'Password should atleast be 8 character long!'),

            })    
    else:
        return render(request,'create_ac.html',
        {
            'form':Create_account(),
            'branches':Branch.objects.raw("SELECT branch_code FROM branch_data EXCEPT SELECT branch_code FROM branch_data WHERE branch_code = 'UD'")
        })

def home(request):
    # email = None
    global email
    try:
        if request.method == 'POST':
            form = Login_form(request.POST)
            if form.is_valid():
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                acquired = Admin.objects.get(email = email)    
                if(acquired.email == email):
                    if(acquired.password == password):
                        if acquired.branch_id == 'CS':
                            students = Student_data.objects.filter(b_code = 'CS')
                            defaulters = Student_data.objects.raw("SELECT * FROM student_data WHERE attendance < 4 AND b_code_id = 'CS'")

                        elif acquired.branch_id == 'ME':
                            students = Student_data.objects.filter(b_code = 'ME')
                            defaulters = Student_data.objects.raw("SELECT * FROM student_data WHERE attendance < 4 AND b_code_id = 'ME'")

                        elif acquired.branch_id == 'CE':
                            students = Student_data.objects.filter(b_code = 'CE')
                            defaulters = Student_data.objects.raw("SELECT * FROM student_data WHERE attendance < 4 AND b_code_id = 'CE'")

                        elif acquired.branch_id == 'EC':
                            students = Student_data.objects.filter(b_code = 'EC')
                            defaulters = Student_data.objects.raw("SELECT * FROM student_data WHERE attendance < 4 AND b_code_id = 'EC'")

                        elif acquired.branch_id == 'EX':
                            students = Student_data.objects.filter(b_code = 'EX')
                            defaulters = Student_data.objects.raw("SELECT * FROM student_data WHERE attendance < 4 AND b_code_id = 'EX'")

                        elif acquired.branch_id == 'IT':
                            students = Student_data.objects.filter(b_code = 'IT')
                            defaulters = Student_data.objects.raw("SELECT * FROM student_data WHERE attendance < 4 AND b_code_id = 'IT'")
                        else:
                            students = 'No data registered for students with this branch'
                            defaulters = 'None'
                        # students = Student_data.objects.all()
                        # defaulters = Student_data.objects.filter(attendance__lt = 4)
                        return render(request,'logged_in.html',{
                            'name':acquired.first_name,
                            "students":students,
                            'defaulters': defaulters
                        })
                        # return HttpResponseRedirect('logged')
                    else:
                        return HttpResponseRedirect(reverse('home'),{
                            messages.add_message(request,messages.ERROR,'Incorrect password or username!'),
                            
                        })
                
            else:
                return render(request,"admin_home.html",{
                    "form": form,
                    
                })
            
        return render(request,"admin_home.html",{
            "form":Login_form()})
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('home'),{
                        messages.add_message(request,messages.ERROR,'User does not exist!'),
                            
                    })

# def logged(request):
#     students = Student_data.objects.all()
#     return render(request,'logged_in.html',{
#                 'name':acquired.first_name,
#                 "students":students
#                 })
    


def gen_single(request):
    if request.method == 'POST':
        roll = request.POST['roll_inp']
        
        if roll in stud:
            image = qrcode.make(roll)
            os.chdir("~/'Project Stud'/stud/register/static")
            image.save('%s.png'%roll,'PNG')
            return render(request,'success.html',{
                'roll':roll
            }) 
    return render(request,'failure.html')

def generate(request):
    # students = Student_data.roll_man.retrieve()
    global email
    admin_branch  = Admin.objects.get(email = email)
    # students = Student_data.objects.raw("SELECT roll_no FROM student_data WHERE b_code_id = '%s'"%admin_branch.branch_id)
    import psycopg2
    connection = psycopg2.connect(user = 'pracuser',password = 'luvmanjaro',
                                host = 'localhost', database = 'practice')
    cursor = connection.cursor()
    cursor.execute("SELECT roll_no FROM student_data WHERE b_code_id = %s",(admin_branch.branch_id,))
    students = cursor.fetchall()                                
    for student in students:
        generator.gen(student,admin_branch.branch_id)
    if admin_branch.branch_id == 'CS':
        directory = 'cs'
    
    if admin_branch.branch_id == 'ME':
        directory = 'me'
    
    if admin_branch.branch_id == 'CE':
        directory = 'ce'
    
    if admin_branch.branch_id == 'IT':
        directory = 'it'
    
    if admin_branch.branch_id == 'EX':
        directory = 'ex'
    
    if admin_branch.branch_id == 'EC':
        directory = 'ec'
    
    os.chdir(f"/home/shubh/Project Stud/stud/register/static/downloadable/{directory.lower()}")
    
    file_paths = []
    for root,directories,files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root,filename)
            file_paths.append(filepath)
    # os.chdir('D:\\Project Stud\\stud\\register\\static')
    # with ZipFile('qrcode.zip','w') as zip:
    #     # for file in file_paths:
    #     zip.write(directory)
    shutil.make_archive('qrcodes','zip', "../%s"%directory.lower())
    return render(request,'success.html',{
        'branch':directory
    }) 


def test(request):
    return render(request,'testing.html')
