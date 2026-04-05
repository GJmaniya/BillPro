from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Bill, Challan
from .forms import UserRegistrationForm, BillForm, ChallanForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
import io
import os
from django.conf import settings
from decimal import Decimal

# For PDF generation
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/index.html')

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Account created! You can now login.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    bills = Bill.objects.filter(user=request.user).order_by('-created_at')
    challans = Challan.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/dashboard.html', {'bills': bills, 'challans': challans})

@login_required
def create_bill(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.user = request.user
            bill.save()
            messages.success(request, "Bill created successfully!")
            return redirect('dashboard')
    else:
        form = BillForm()
    return render(request, 'core/create_bill.html', {'form': form})

@login_required
def create_challan(request):
    if request.method == 'POST':
        form = ChallanForm(request.POST)
        if form.is_valid():
            challan = form.save(commit=False)
            challan.user = request.user
            challan.save()
            messages.success(request, "Challan created successfully!")
            return redirect('dashboard')
    else:
        form = ChallanForm()
    return render(request, 'core/create_challan.html', {'form': form})

@login_required
def download_bill(request, id):
    bill = get_object_or_404(Bill, id=id, user=request.user)
    if not HAS_REPORTLAB:
        return HttpResponse("PDF generation library 'reportlab' is not installed. Please run: pip install reportlab", status=501)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width/2, height - 50, "INVOICE / BILL")

    # Seller Info
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 100, f"Seller: {request.user.username.title()}")
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 120, f"Email: {request.user.email}")
    p.line(50, height - 130, width - 50, height - 130)

    # Client Info
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 160, f"Billed To:")
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 180, f"Name: {bill.client_name}")
    p.drawString(50, height - 200, f"Address: {bill.client_address}")
    p.drawString(50, height - 220, f"Phone: {bill.client_phone or 'N/A'}")

    # Bill Info
    p.drawString(400, height - 180, f"Invoice No: INV-{bill.id}")
    p.drawString(400, height - 200, f"Date: {bill.billing_date}")
    p.drawString(400, height - 220, f"Project: {bill.project_name}")

    # Table Header
    p.line(50, height - 250, width - 50, height - 250)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(55, height - 270, "Description")
    p.drawString(400, height - 270, "Amount")
    p.line(50, height - 280, width - 50, height - 280)

    # Table Body
    p.setFont("Helvetica", 12)
    p.drawString(55, height - 300, f"Project Services: {bill.project_name}")
    p.drawRightString(width - 60, height - 300, f"Rs.{bill.price:.2f}")

    # Totals
    gst_amount = (bill.price * bill.gst_rate) / Decimal('100.00')
    p.line(350, height - 350, width - 50, height - 350)
    p.drawString(355, height - 370, "Subtotal:")
    p.drawRightString(width-60, height - 370, f"Rs.{bill.price:.2f}")
    p.drawString(355, height - 390, f"GST ({bill.gst_rate}%):")
    p.drawRightString(width-60, height - 390, f"Rs.{gst_amount:.2f}")
    p.setFont("Helvetica-Bold", 14)
    p.drawString(355, height - 420, "Total:")
    p.drawRightString(width-60, height - 420, f"Rs.{bill.total_amount:.2f}")

    # Footer
    p.setFont("Helvetica-Oblique", 10)
    p.drawCentredString(width/2, 50, "Thank you for your business!")

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'Bill_{bill.id}.pdf')

@login_required
def download_challan(request, id):
    challan = get_object_or_404(Challan, id=id, user=request.user)
    if not HAS_REPORTLAB:
        return HttpResponse("PDF generation library 'reportlab' is not installed.", status=501)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width/2, height - 50, "DELIVERY CHALLAN")

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 100, f"From: {request.user.username.title()}")
    p.line(50, height - 110, width - 50, height - 110)

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 140, f"Deliver To:")
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 160, f"Name: {challan.client_name}")
    p.drawString(50, height - 180, f"Address: {challan.client_address}")

    p.drawString(400, height - 160, f"Challan No: CH-{challan.id}")
    p.drawString(400, height - 180, f"Date: {challan.delivery_date}")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 230, "Delivery Details / Description:")
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 250, challan.description or "No description provided.")

    p.drawCentredString(width/2, 50, "Authorized Signatory")

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'Challan_{challan.id}.pdf')

@login_required
def whatsapp_share(request, id):
    bill = get_object_or_404(Bill, id=id, user=request.user)
    # Since we can't easily upload first and then send PDF to whatsapp from server side without Twilio,
    # we'll use a direct whatsapp web share link with a prefilled message.
    # The message will notify the client and maybe provide a public link if hosted.
    phone = str(bill.client_phone or "").replace('+', '').replace('-', '').replace(' ', '')
    text = f"Hello {bill.client_name}, your bill for project {bill.project_name} is ready. Total Amount: Rs.{bill.total_amount}. We have shared the PDF with you."
    whatsapp_url = f"https://wa.me/{phone}?text={text.replace(' ', '%20')}"
    return redirect(whatsapp_url)
