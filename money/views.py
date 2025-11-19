from django.shortcuts import get_object_or_404, render,redirect
from .models import *
import json
# Create your views here.

Uid='h@gmail.com'
def Dashboard(request):
    global Uid
    if Uid == '':
        return redirect("../")
    
    UserData = User.objects.filter(Email=Uid).values()[0]
    history = Transection_History.objects.filter(uid=Uid).select_related('transection_Type', 'Category').order_by('-Date')[:3]
    income_temp=Transection_History.objects.filter(uid=Uid,transection_Type=2).select_related('transection_Type', 'Category').order_by('-Date').values()
    Expense_temp=Transection_History.objects.filter(uid=Uid,transection_Type=1).select_related('transection_Type', 'Category').order_by('-Date').values()
    Transport_temp = Transection_History.objects.filter(uid=Uid,transection_Type=1,Category=2).select_related('transection_Type', 'Category').order_by('-Date').values()
    Food_temp = Transection_History.objects.filter(uid=Uid,transection_Type=1,Category=1).select_related('transection_Type', 'Category').order_by('-Date').values()
    Entertainmant_temp = Transection_History.objects.filter(uid=Uid,transection_Type=1,Category=4).select_related('transection_Type', 'Category').order_by('-Date').values()
    Other_temp = Transection_History.objects.filter(uid=Uid,transection_Type=1,Category=6).select_related('transection_Type', 'Category').order_by('-Date').values()
    
    income = sum(item['Amount'] for item in income_temp)
    Expense = sum(item['Amount'] for item in Expense_temp)
    Transport_total = sum(item['Amount'] for item in Transport_temp)
    Other_total = sum(item['Amount'] for item in Other_temp)
    Food_total = sum(item['Amount'] for item in Food_temp)
    Entertainmant_total = sum(item['Amount'] for item in Entertainmant_temp)
    if Expense !=0:
        Transport_pr = round((Transport_total / Expense) * 100, 2)
        Food_pr = round((Food_total / Expense) * 100, 2)
        Entertainmant_pr = round((Entertainmant_total / Expense) * 100, 2)
        Other_pr = round((Other_total / Expense) * 100, 2)
        Expense_Categories=[
        {
            'category': "Entertainment",
            'amount': Entertainmant_total,
            'percentage': Entertainmant_pr,
            'colorClass': "bg-green-500"
        },
        {
            'category': "Food & Dining",
            'amount': Food_total,
            'percentage': Food_pr,
            'colorClass': "bg-red-500"
        },
        {
            'category': "Transportation",
            'amount': Transport_total,
            'percentage': Transport_pr,
            'colorClass': "bg-blue-500"
        },
        {
            'category': "Other",
            'amount': Other_total,
            'percentage': Other_pr,
            'colorClass': "bg-purple-500"
        },
    ]    
    else:
        Transport_pr = 0
        Food_pr = 0
        Entertainmant_pr = 0
        Other_pr =0
        Expense_Categories=[]    
    
    
    data ={
        'user' : UserData,
        'history' : history,
        'income':income,
        'Expense':Expense,
        'Expense_Categories':Expense_Categories,
    }
    
    return render(request,"dashboard.html",data)

def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        UserData = User.objects.filter(Email = email).values()
        if len(UserData) >0:
            if UserData[0]['Password'] == password:
                global Uid
                Uid = UserData[0]['Email']
                return redirect("../Dashboard/")
    return render(request,"login.html")

def signup(request):
    
    if request.method=='POST':
        uname = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpass = request.POST.get("cpassword")
        if password == cpass:
            User.objects.create(Username=uname,Email=email,Password=password)
            return redirect('../')
    return render(request,"signup.html")

def analysis(request):
    global Uid
    if Uid == '':
        return redirect("../")
    UserData = User.objects.filter(Email=Uid).values()[0]
    historydata = Transection_History.objects.filter(uid=Uid).select_related('transection_Type', 'Category').order_by('-Date')
    temp=[]
    for i in historydata:
        temp.append({
            'id': i.id,
            'date': i.Date,
            'description': i.Description,
            'category': i.Category,
            'type' : i.transection_Type,
            'amount': i.Amount,        
        })
    demo=[{'id': 26, 'date': '2025-12-01', 'description': 'salary', 'category': 'Income', 'type': 'Credited', 'amount': 10000.0}, {'id': 30, 'date': '2025-11-22', 'description': 'Cloths', 'category':'Other', 'type': 'Debited', 'amount': 2000.0}, {'id': 31, 'date': '2025-11-22', 'description': 'Fast Food', 'category':'Food', 'type': 'Debited', 'amount': 500.0}, {'id': 29, 'date': '2025-11-20', 'description': 'Papa ', 'category': 'Income', 'type': 'Credited', 'amount': 5000.0}, {'id': 28, 'date': '2025-11-18', 'description': 'Pizza', 'category':'Food', 'type': 'Debited', 'amount': 750.0}, {'id': 33, 'date': '2025-11-15', 'description': 'Desal', 'category':'Transportation', 'type': 'Debited', 'amount': 500.0}, {'id': 32, 'date': '2025-11-08', 'description': 'petrol', 'category':'Transportation', 'type': 'Debited', 'amount': 500.0}, {'id': 27, 'date': '2025-11-02', 'description': 'Movie', 'category':'Entertainment', 'type': 'Debited', 'amount': 800.0}, {'id': 25, 'date': '2025-11-01', 'description': 'salary', 'category': 'Income', 'type': 'Credited', 'amount': 10000.0}]
    print(demo)
    data = {
        'user' : UserData,
        'historydata' : historydata,
    }
    return render(request,"analysis.html",data)

def transactions(request):
    global Uid
    if Uid == '':
        return redirect("../")
    UserData = User.objects.filter(Email=Uid).values()[0]
    # This is the fix
    historydata = Transection_History.objects.filter(uid=Uid).select_related('transection_Type', 'Category').order_by('-Date')
    if request.method=='POST':
        # -------------add------------------
        if request.POST.get("Operation") == 'Add Transaction':
            date = request.POST.get("date")
            description = request.POST.get("Description")
            category = request.POST.get("Category")
            type = request.POST.get("type")
            amount = request.POST.get("amount")
            if type == 'Debited':
                bal = User.objects.get(Email = Uid)
                bal.Balance = bal.Balance - float(amount)
                bal.save()
            else : 
                bal = User.objects.get(Email = Uid)
                bal.Balance = bal.Balance + float(amount)
                bal.save()
            category = Transection_Category.objects.get(Category=category)
            type = Transection_Type.objects.get(transection_Type = type)
            Transection_History.objects.create(uid=Uid,Date=date,Description=description,transection_Type=type,Category=category,Amount=amount)
        # -------------update-----------------
        elif request.POST.get("Operation") == 'Delete Transaction':
            t_id = request.POST.get("transaction-id")
            type = request.POST.get("type")
            amount = request.POST.get("amount")
            if type == 'Debited':
                bal = User.objects.get(Email = Uid)
                bal.Balance = bal.Balance + float(amount)
                bal.save()
            else : 
                bal = User.objects.get(Email = Uid)
                bal.Balance = bal.Balance - float(amount)
                bal.save()
            data = get_object_or_404(Transection_History, id=t_id)
            data.delete()
            
        
    data = {
        'user' : UserData,
        'historydata' : historydata,
    }
    return render(request, "transactions.html",data)