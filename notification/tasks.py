from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import EmailLog

User = get_user_model()


@shared_task(bind=True)
def send_order_confirmation_email(self, order_id, user_id):
    """
    Send order confirmation email to buyer
    """
    try:
        user = User.objects.get(id=user_id)
        user_email = user.email
        user_name = user.get_full_name() or user.username
    except User.DoesNotExist:
        return f'User not found with ID: {user_id}'
    
    subject = 'Order Confirmation - Thank You for Your Purchase!'
    message = f'''
    Hi {user_name},

    Thank you for your order! Your order has been confirmed.

    Order ID: {order_id}

    We will notify you once your order is processed and shipped.

    Best regards,
    Multi-Vendor Team
    '''
    
    try:
        email_log = EmailLog.objects.create(
            user=user,
            subject=subject,
            message=message,
            status='pending'
        )
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        
        email_log.status = 'sent'
        email_log.sent_at = timezone.now()
        email_log.save()
        
        return f'Email sent successfully to {user_email}'
        
    except Exception as e:
        if 'email_log' in locals():
            email_log.status = 'failed'
            email_log.save()
        return f'Failed to send email: {str(e)}'


@shared_task(bind=True)
def send_payment_success_email(self, order_id, user_id, amount):
    """
    Send payment success notification to buyer
    """
    try:
        user = User.objects.get(id=user_id)
        user_email = user.email
        user_name = user.get_full_name() or user.username
    except User.DoesNotExist:
        return f'User not found with ID: {user_id}'
    
    subject = 'Payment Successful - Order Confirmed'
    message = f'''
    Hi {user_name},

    Great news! Your payment of ${amount} has been successfully processed.

    Order ID: {order_id}
    Amount: ${amount}

    Your order is now confirmed and will be processed shortly.

    Best regards,
    Multi-Vendor Team
    '''
    
    try:
        email_log = EmailLog.objects.create(
            user=user,
            subject=subject,
            message=message,
            status='pending'
        )
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        
        email_log.status = 'sent'
        email_log.sent_at = timezone.now()
        email_log.save()
        
        return f'Payment confirmation email sent to {user_email}'
        
    except Exception as e:
        if 'email_log' in locals():
            email_log.status = 'failed'
            email_log.save()
        return f'Failed to send email: {str(e)}'


@shared_task(bind=True)
def send_vendor_order_notification(self, vendor_user_id, order_id, order_items):
    """
    Send new order notification to vendor
    """
    try:
        vendor_user = User.objects.get(id=vendor_user_id)
        vendor_email = vendor_user.email
        vendor_name = vendor_user.get_full_name() or vendor_user.username
    except User.DoesNotExist:
        return f'Vendor user not found with ID: {vendor_user_id}'
    
    subject = 'New Order Received - Action Required'
    message = f'''
    Hi {vendor_name},

    You have received a new order!

    Order ID: {order_id}
    Items: {order_items}

    Please log in to your vendor dashboard to process this order.

    Best regards,
    Multi-Vendor Team
    '''
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[vendor_email],
            fail_silently=False,
        )
        
        return f'Vendor notification sent to {vendor_email}'
        
    except Exception as e:
        return f'Failed to send vendor email: {str(e)}'


@shared_task(bind=True)
def send_order_shipped_email(self, user_id, order_id, tracking_number):
    """
    Send order shipped notification to buyer
    """
    try:
        user = User.objects.get(id=user_id)
        user_email = user.email
        user_name = user.get_full_name() or user.username
    except User.DoesNotExist:
        return f'User not found with ID: {user_id}'
    
    subject = 'Your Order Has Been Shipped!'
    message = f'''
    Hi {user_name},

    Your order has been shipped!

    Order ID: {order_id}
    Tracking Number: {tracking_number}

    You can track your order using the tracking number above.

    Best regards,
    Multi-Vendor Team
    '''
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        
        return f'Shipment notification sent to {user_email}'
        
    except Exception as e:
        return f'Failed to send email: {str(e)}'