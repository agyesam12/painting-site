import requests
from django.conf import settings
from paint.models import User

def send_sms(phone_number, message):
    payload = {
        'sender': settings.SMS_SENDER_ID,
        'message': message,
        'recipients': [phone_number]
    }

    headers = {
        'Content-Type': 'application/json',
        'api-key': settings.SMS_API_KEY
    }

    try:
        check_user = User.objects.filter(phone_number=phone_number).exists()
        if check_user:
            user = User.objects.get(phone_number=phone_number)
            if user.allow_sms:
                response = requests.post("https://sms.arkesel.com/api/v2/sms/send", json=payload, headers=headers)
                response.raise_for_status()
                return response.json()
    except requests.exceptions.RequestException as e:
        return None
