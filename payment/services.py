from os import getenv
import stripe


def stripe_payment_create(amount, product_title):
    my_stripe = stripe_init()

    response_product_create = product_create(my_stripe, product_title)

    response_price_create = price_create(my_stripe, amount, product_title)

    response_session_create = checkout_session_create(my_stripe, response_price_create['id'])

    return response_session_create


def checkout_session_create(my_stripe, price_id):
    response = my_stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )

    return response


def price_create(my_stripe, amount, product_title):
    response = my_stripe.Price.create(
        currency="usd",
        unit_amount=amount,
        product_data={"name": product_title},
    )

    return response


def product_create(my_stripe, product_title):
    response = my_stripe.Product.create(name=product_title)

    return response


def stripe_init():
    stripe.api_key = getenv('STRIPE_KEY')

    return stripe
