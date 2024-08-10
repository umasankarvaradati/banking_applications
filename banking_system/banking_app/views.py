# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Customer, Transaction, User
from .forms import CustomerForm
from django.contrib.auth.hashers import make_password, check_password
import random
import string


from django.http import HttpResponse

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Transaction
from decimal import Decimal


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']

        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and User.is_admin:
            login(request, user)
            return redirect('admin_dashboard')
    return render(request, 'admin_login.html')

@login_required
def admin_dashboard(request):
    customers = Customer.objects.all()
    return render(request, 'admin_dashboard.html', {'customers': customers})

@login_required
def add_customer(request):
    
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.account_no = generate_account_no() 
            customer.password = generate_temporary_password()
            customer.save()
            redirect('customer_detail_popup.html')
            return redirect('admin_dashboard')
    else:
        form = CustomerForm()
    return render(request, 'add_customer.html', {'form': form})

@login_required
def edit_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer.is_active==True
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'edit_customer.html', {'form': form})

@login_required
def delete_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    customer.delete()
    return redirect('admin_dashboard')

def generate_account_no():
   
    return ''.join(random.choices(string.digits, k=12))

def generate_temporary_password():
   
   return ''.join(random.choices(string.ascii_letters + string.digits, k=8))



def customer_login(request):
    if request.method == 'POST':
        account_no = request.POST['account_no']
        password = request.POST['password']
        
        try:
             customer = Customer.objects.get(account_no=account_no)
             if customer.is_active == True:
                if check_password(password, customer.password):
                    request.session['customer_id'] = customer.id
                    return redirect('customer_dashboard')
                 
        except Customer.DoesNotExist:
                pass
    return render(request, 'customer_login.html')

def customer_setup(request):
    if request.method == 'POST':
        account_no = request.POST['account_no']
        temp_password = request.POST['temp_password']
        new_password = request.POST['new_password']
        try:
            customer = Customer.objects.get(account_no=account_no)
            if customer.password == temp_password:
                customer.password = make_password(new_password)
                customer.save()
                return redirect('customer_login')
        except Customer.DoesNotExist:
            pass
    return render(request, 'customer_setup.html')

def customer_logout(request):
    if 'customer_id' in request.session:
        del request.session['customer_id']
    return redirect('customer_login')

def customer_dashboard(request):
    customer_id = request.session.get('customer_id')
    customer = Customer.objects.get(id=customer_id)
    return render(request, 'customer_dashboard.html', {'customer': customer})

def view_transactions(request):
    customer_id = request.session.get('customer_id')
    transactions = Transaction.objects.filter(customer_id=customer_id).order_by('-transaction_date')
    return render(request, 'view_transactions.html', {'transactions': transactions})

def deposit(request):
    customer_id = request.session.get('customer_id')
    customer = Customer.objects.get(id=customer_id)
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])
        customer.initial_balance += amount  
        customer.save() 
        
        Transaction.objects.create(
            customer=customer,
            transaction_type='Deposit',
            amount=amount
        )
        return redirect('customer_dashboard')
    return render(request, 'deposit.html', {'customer': customer})

def withdraw(request):
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])
        customer_id = request.session.get('customer_id')
        customer = Customer.objects.get(id=customer_id)
        if customer.initial_balance >= amount:
            customer.initial_balance -= amount
            customer.save()
        
            Transaction.objects.create(customer=customer, transaction_type='Withdraw', amount=amount)
        return redirect('customer_dashboard')
    return render(request, 'withdraw.html')

def close_account(request):
    customer_id = request.session.get('customer_id')
    customer = Customer.objects.get(id=customer_id)
    if customer.initial_balance == 0:
        customer.is_active = False
        customer.save()
        return redirect('customer_logout')
    return redirect('customer_dashboard')
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


def download_transactions_pdf(request):
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transactions.pdf"'

 
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter


    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "Transaction History")

  
    customer_id = request.session.get('customer_id')
    customer = Customer.objects.get(id=customer_id)
   


   
    transactions = Transaction.objects.filter(customer=customer).order_by('transaction_date')[:10]

    
    y = height - 100
    p.setFont("Helvetica", 12)

   
    p.drawString(50, y, "Transaction Type")
    p.drawString(200, y, "Amount")
    p.drawString(350, y, "transaction_date")
    y -= 20

    
    for transaction in transactions:
        p.drawString(50, y, transaction.transaction_type)
        p.drawString(200, y, f"${transaction.amount:.2f}")
        p.drawString(350, y, transaction.transaction_date.strftime("%Y-%m-%d %H:%M:%S"))
        y -= 20

        
        if y < 50:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 12)

   
    p.showPage()
    p.save()
    return response

