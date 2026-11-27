import requests

from django.conf import settings


class ZarinpalError(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code


TIMEOUT = (5, 20)


def get_payment_amount(payment):
    """
    Convert payment amount from Toman to Rial.
    """

    try:
        amount = int(payment.amount)
    except (TypeError, ValueError):
        raise ZarinpalError("مبلغ پرداخت نامعتبر است.")

    if amount <= 0:
        raise ZarinpalError("مبلغ پرداخت باید بیشتر از صفر باشد.")

    amount *= 10

    if amount < 1000:
        raise ZarinpalError("حداقل مبلغ پرداخت ۱۰۰ تومان است.")

    return amount


def get_merchant_id():
    """
    Get and validate merchant ID from Django settings.
    """

    merchant_id = getattr(settings, "ZARINPAL_MERCHANT_ID", None)

    if not merchant_id or merchant_id == "YOUR_MERCHANT_ID":
        raise ZarinpalError("تنظیمات درگاه پرداخت کامل نیست.")

    return merchant_id


def send_request(url, payload):
    """
    Send HTTP request to Zarinpal and validate its response.
    """

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=TIMEOUT,
        )

    except requests.Timeout as error:
        raise ZarinpalError("زمان ارتباط با درگاه پرداخت به پایان رسید.") from error

    except requests.RequestException as error:
        raise ZarinpalError("ارتباط با درگاه پرداخت برقرار نشد.") from error

    try:
        result = response.json()

    except ValueError as error:
        raise ZarinpalError("پاسخ دریافتی از درگاه معتبر نیست.") from error

    if not isinstance(result, dict):
        raise ZarinpalError("ساختار پاسخ درگاه نامعتبر است.")

    if not response.ok:
        errors = result.get("errors", {})
        message = "درخواست پرداخت ناموفق بود."
        code = None

        if isinstance(errors, dict):
            message = errors.get("message", message)
            code = errors.get("code")

        raise ZarinpalError(message, code=code)

    return result


def get_api_error(result):
    """
    Extract error information from Zarinpal response.
    """

    errors = result.get("errors", {})

    if isinstance(errors, dict):
        message = errors.get("message", "عملیات پرداخت ناموفق بود.")
        code = errors.get("code")

    else:
        message = "عملیات پرداخت ناموفق بود."
        code = None

    return ZarinpalError(message, code=code)


def create_payment_request(payment, callback_url):
    """
    Create a new payment request and return its authority.
    """

    amount = get_payment_amount(payment)

    payload = {
        "merchant_id": get_merchant_id(),
        "amount": amount,
        "callback_url": callback_url,
        "description": f"پرداخت سفارش شماره {payment.order_id}",
    }

    result = send_request(
        settings.ZARINPAL_REQUEST_URL,
        payload,
    )

    data = result.get("data", {})

    if not isinstance(data, dict) or data.get("code") != 100:
        raise get_api_error(result)

    authority = data.get("authority")

    if not isinstance(authority, str) or not authority.strip():
        raise ZarinpalError("شناسه پرداخت از زرین‌پال دریافت نشد.")

    return authority


def verify_payment(payment, authority=None):
    """
    Verify an existing payment using its stored authority.
    """

    stored_authority = payment.authority

    if not stored_authority:
        raise ZarinpalError("شناسه پرداخت در سیستم ثبت نشده است.")

    if authority is not None and authority != stored_authority:
        raise ZarinpalError("شناسه پرداخت معتبر نیست.")

    amount = get_payment_amount(payment)

    payload = {
        "merchant_id": get_merchant_id(),
        "amount": amount,
        "authority": stored_authority,
    }

    result = send_request(
        settings.ZARINPAL_VERIFY_URL,
        payload,
    )

    data = result.get("data", {})

    if not isinstance(data, dict):
        raise ZarinpalError("پاسخ تأیید پرداخت نامعتبر است.")

    code = data.get("code")

    if code not in (100, 101):
        raise get_api_error(result)

    ref_id = data.get("ref_id")

    if ref_id is None:
        raise ZarinpalError("کد پیگیری از زرین‌پال دریافت نشد.")

    return str(ref_id)
