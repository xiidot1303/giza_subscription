# views.py
import openpyxl
from django.http import HttpResponse
from bot.models import Bot_user

def export_bot_users_to_excel(request):
    # Fetch relevant Bot_user fields
    bot_users = Bot_user.objects.all().values(
        'name', 'firstname', 'phone', 'date', 'utm_source', 'subscription__plan__name'
    )

    # Define the columns for the Excel file
    columns = [
        'Имя пользователя',
        'Никнейм',
        'Телефон',
        'Дата регистрации',
        'Источник',
        'Подписка'
    ]
    
    # Create a new workbook and add a sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Пользователи бота"

    # Add the headers to the first row
    ws.append(columns)

    # Add the data for each bot_user (values are dictionaries)
    for bot_user in bot_users:
        row = [
            bot_user['name'],
            bot_user['firstname'],
            bot_user['phone'],
            bot_user['date'],
            bot_user['utm_source'],
            bot_user['subscription__plan__name']
        ]
        ws.append(row)

    # Set the HTTP response content type to Excel file format
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=bot_users.xlsx'
    
    # Save the workbook to the response object
    wb.save(response)
    
    return response
