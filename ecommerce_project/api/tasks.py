from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order  # Assuming you have an Order model

@shared_task
def send_order_confirmation_email(order_id):
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Order Confirmation - #{order.id}'
        to_email = order.customer.email
        message = render_to_string('emails/order_confirmation.html', {
            'order': order,
        })
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False,
        )
    except Order.DoesNotExist as e:
        raise ValueError(f"Order ID {order_id} not found") from e

