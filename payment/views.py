import stripe
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from order.models import Order
from vendor.models import VendorProfile
from .models import Payment, Payout
from .permissions import IsBuyer, IsVendor

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentAPIView(APIView):
 #   permission_classes = [IsAuthenticated,IsBuyer]
    def post(self, request):
        user = request.user
        order_id = request.data.get("order_id")
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)
        if order.user != user:
            return Response({"error": "Not your order"}, status=403)
        if order.payment_status == "success":
            return Response({"error": "Already paid"}, status=400)
        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                "payment_method": "stripe",
                "amount": order.total_amount,
                "status": "pending"
            })
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(order.total_amount * 100),
                currency="usd",
                metadata={
                    "order_id": str(order.id),
                    "user_id": str(user.id)
                })
            payment.transaction_id = intent.id
            payment.save()
            return Response({
                "client_secret": intent.client_secret
            })
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        


class StripeWebhookAPIView(APIView):
    # authentication_classes = []
    # permission_classes = []
    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
        try:
            event = stripe.Webhook.construct_event(payload,sig_header,settings.STRIPE_WEBHOOK_SECRET)
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)
        if event["type"] == "payment_intent.succeeded":
            intent = event["data"]["object"]
            transaction_id = intent["id"]
            order_id = intent["metadata"].get("order_id")
            try:
                payment = Payment.objects.get(transaction_id=transaction_id)
                if payment.status == "success":
                    return HttpResponse(status=200)
                order = Order.objects.get(id=order_id)
                with transaction.atomic():
                    payment.status = "success"
                    payment.paid_at = timezone.now()
                    payment.save()
                    order.payment_status = "success"
                    order.status = "paid"
                    order.save()
            except Exception:
                pass
        elif event["type"] == "payment_intent.payment_failed":
            intent = event["data"]["object"]
            transaction_id = intent["id"]
            try:
                payment = Payment.objects.get(transaction_id=transaction_id)
                payment.status = "failed"
                payment.save()
            except Payment.DoesNotExist:
                pass
        return HttpResponse(status=200)        