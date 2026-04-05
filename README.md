# BillPro Invoicing System

A premium Django-based billing and delivery challan system with PDF generation and WhatsApp sharing capabilities.

## Features
- **User Accounts**: Secure registration and login.
- **Dashboard**: Track all your bills and challans in one place.
- **GST Billing**: Automatic GST calculations based on custom rates.
- **PDF Generation**: Download professional invoices and challans instantly.
- **WhatsApp Integration**: Share bill details directly to WhatsApp.
- **Premium UI**: Glassmorphism aesthetic and responsive design.

## Quick Start

1. **Activate Virtual Environment** (if not already):
   ```bash
   source .venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Run Application**:
   ```bash
   python manage.py runserver
   ```

5. **Access**:
   Open `http://127.0.0.1:8000` in your browser.

## Project Structure
- `bill_project/`: Django project configuration.
- `core/`: Main app logic for billing, challans, and accounts.
- `templates/`: Premium HTML layouts and styling.
- `media/`: Storage for generated PDFs (optional, current version generates them on-the-fly).
