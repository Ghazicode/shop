from decimal import Decimal

from products.models import Product, ProductStatus


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get("cart", {})

    def save(self):
        # فقط تعداد محصول در Session ذخیره می‌شود
        self.session["cart"] = {
            str(product_id): {
                "quantity": item["quantity"],
            }
            for product_id, item in self.cart.items()
        }
        self.session.modified = True

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)

        if not product.is_available:
            return False

        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
            }

        if update_quantity:
            new_quantity = quantity
        else:
            new_quantity = self.cart[product_id]["quantity"] + quantity

        if new_quantity <= 0:
            self.remove(product)
            return True

        if new_quantity > product.stock:
            return False

        self.cart[product_id]["quantity"] = new_quantity

        self.save()

        return True

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session.pop("cart", None)
        self.session.modified = True
        self.cart = {}

    def __iter__(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(
            id__in=product_ids,
            status=ProductStatus.ACTIVE,
        )

        for product in products:
            item = self.cart[str(product.id)]

            quantity = item["quantity"]

            # قیمت‌ها همیشه از دیتابیس خوانده می‌شوند
            current_price = Decimal(str(product.final_price))
            original_price = Decimal(str(product.price))

            yield {
                "product": product,
                "quantity": quantity,
                "price": current_price,
                "original_price": original_price,
                "total_price": current_price * quantity,
                "discount_price": (original_price - current_price) * quantity,
            }

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_subtotal_price(self):
        return sum(
            (item["original_price"] * item["quantity"] for item in self),
            Decimal("0"),
        )

    def get_discount_total(self):
        return self.get_subtotal_price() - self.get_total_price()

    def get_total_price(self):
        return sum(
            (item["total_price"] for item in self),
            Decimal("0"),
        )

    def get_final_price(self):
        return self.get_total_price()
