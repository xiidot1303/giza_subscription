import openpyxl
from django.http import HttpResponse
from app.models import Payment


def export_payments_to_excel(request):
    # Create a new workbook and add a sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Платежи"

    # Get the model fields and use their verbose_name for the headers
    columns = ['Пользователь', 'Номер телефона', 'Источник', 'Тариф', 'Сумма',
               'Дата платежа']

    # Add headers to the first row
    ws.append(columns)

    # Use .values() to fetch only the required fields from the database
    payments = Payment.objects.all().values(
        'bot_user__name', 'bot_user__phone', 'bot_user__utm_source',
        'amount', 'subscription__plan__name', 'payment_date'
    )

    # Add the data for each payment (values are dictionaries)
    for payment in payments:
        row = [
            # Handle potential null bot_user
            payment['bot_user__name'],
            payment['bot_user__phone'],
            payment['bot_user__utm_source'],
            payment['subscription__plan__name'] if 'subscription__plan__name' in payment else 'Бонус',
            payment['amount'],
            payment['payment_date'],
        ]
        ws.append(row)

    # Set the HTTP response content type to Excel file format
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=payments.xlsx'

    # Save the workbook to the response object
    wb.save(response)

    return response
