from datetime import datetime
import json
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendees_bc.settings")
django.setup()


from attendees.models import AccountVO


def update_account(ch, method, properties, body):
    content = json.loads(body)
    first_name = content["first_name"]
    last_name = content["last_name"]
    email = content["email"]
    is_active = content["is_active"]
    updated_string = content["updated"]
    updated = datetime.fromisoformat(updated_string)

    if is_active:
        print("making stuff", email)
        account, _ = AccountVO.objects.update_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "updated": updated
            }
        )

    else:
        try:
            account = AccountVO.objects.get(email=email)
            account.delete()
            print(f"Account {email} deleted")
        except AccountVO.DoesNotExist:
            print(f"Account {email} not found")


while True:
    try:
        connection_params = pika.ConnectionParameters(host='rabbitmq')
        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()

        channel.exchange_declare(exchange='account_info', exchange_type='fanout')
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange='account_info', queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=update_account, auto_ack=True)

        print("Waiting for account info messages...")
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError:
        print("Could not connect to RabbitMQ. Retrying in 2 seconds...")
        time.sleep(2)
