from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.db import transaction
from django.http import HttpResponseBadRequest

from order.models import Order, PaymentStatus
from .models import Payment
from .services import (
    create_payment_request,
    verify_payment,
    ZarinpalError,
)


class StartPaymentView(LoginRequiredMixin, View):

    def post(self, request, order_id):

        # 1. دریافت سفارش متعلق به کاربر فعلی
        order = get_object_or_404(Order, id=order_id, user=request.user)

        # 2. جلوگیری از پرداخت مجدد سفارش
        if order.is_paid == PaymentStatus.PAID:
            messages.info(request, "این سفارش قبلاً پرداخت شده است.")
            return redirect("orders:detail", id=order.id)

        # 3. ایجاد رکورد پرداخت
        payment = Payment.objects.create(order=order, amount=order.total_price)

        # 4. ساخت آدرس بازگشت از درگاه
        callback_url = request.build_absolute_uri(reverse("payments:verify"))

        try:
            # 5. ارسال درخواست به زرین‌پال
            authority = create_payment_request(
                payment=payment, callback_url=callback_url
            )

            # 6. ذخیره شناسه پرداخت
            payment.authority = authority
            payment.save(update_fields=["authority", "updated_at"])

        except ZarinpalError as error:

            payment.status = Payment.Status.FAILED
            payment.save(update_fields=["status", "updated_at"])

            messages.error(request, str(error))

            return redirect("orders:detail", id=order.id)

        # 7. انتقال کاربر به درگاه
        payment_url = f"{settings.ZARINPAL_STARTPAY_URL}{authority}"

        return redirect(payment_url)


class VerifyPaymentView(View):

    def get(self, request):

        # 1. دریافت اطلاعات برگشتی از زرین‌پال
        authority = request.GET.get("Authority")
        callback_status = request.GET.get("Status")

        if not authority:
            return HttpResponseBadRequest("شناسه پرداخت نامعتبر است.")

        order_id = None

        try:

            # 2. جلوگیری از پردازش هم‌زمان یک پرداخت
            with transaction.atomic():

                payment = get_object_or_404(
                    Payment.objects.select_for_update().select_related("order"),
                    authority=authority,
                )

                order_id = payment.order_id

                # 3. جلوگیری از تأیید تکراری
                if payment.status == Payment.Status.SUCCESS:

                    ref_id = payment.ref_id

                # 4. بررسی وضعیت پرداخت
                elif payment.status != Payment.Status.PENDING:

                    messages.error(
                        request, "این پرداخت قبلاً پردازش شده یا معتبر نیست."
                    )

                    return redirect("orders:detail", id=order_id)

                # 5. بررسی وضعیت برگشتی از درگاه
                elif callback_status != "OK":

                    payment.status = Payment.Status.FAILED
                    payment.save(update_fields=["status", "updated_at"])

                    messages.error(request, "پرداخت توسط کاربر لغو شد یا ناموفق بود.")

                    return redirect("orders:detail", id=order_id)

                else:

                    # 6. تأیید پرداخت از سمت سرور
                    ref_id = verify_payment(payment=payment, authority=authority)

                    # 7. ثبت پرداخت موفق
                    payment.status = Payment.Status.SUCCESS
                    payment.ref_id = ref_id
                    payment.save(update_fields=["status", "ref_id", "updated_at"])

                    # 8. تغییر وضعیت سفارش
                    order = Order.objects.select_for_update().get(pk=payment.order_id)

                    order.is_paid = PaymentStatus.PAID
                    order.save(update_fields=["is_paid"])

        except ZarinpalError as error:

            # در خطای ارتباطی، پرداخت را ناموفق نکن.
            # ممکن است زرین‌پال پرداخت را انجام داده باشد.
            messages.error(request, str(error))

            if order_id is not None:
                return redirect("orders:detail", id=order_id)

            raise

        # 9. نمایش نتیجه پرداخت
        messages.success(request, f"پرداخت با موفقیت انجام شد. کد پیگیری: {ref_id}")

        return redirect("orders:detail", id=order_id)
