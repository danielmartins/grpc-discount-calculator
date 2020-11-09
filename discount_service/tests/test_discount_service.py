from discount_service.use_cases.discount import DiscountUseCase


def test_success_5_percent_discount_at_users_birthday(user_at_birthday, product_with_price_100):
    # When
    price_with_discount = DiscountUseCase().calculate(
        user=user_at_birthday,
        product=product_with_price_100
    )

    # Then
    assert price_with_discount == 95


def test_failure_no_discount_out_of_users_birthday_or_black_fridays(user_out_of_birthday, product_with_price_100):
    # When
    price_with_discount = DiscountUseCase().calculate(
        user=user_out_of_birthday,
        product=product_with_price_100
    )

    # Then
    assert price_with_discount == 100


def test_success_10_percent_discount_at_black_friday(freezer, user, product_with_price_100):
    # Given
    freezer.move_to("2020-11-25")

    # When
    price_with_discount = DiscountUseCase().calculate(user=user, product=product_with_price_100)

    # Then
    assert price_with_discount == 90


def test_success_10_percent_maximum_discount_at_black_fridays_and_users_birthday(
        freezer,
        user_with_birthday_at_black_fridays,
        product_with_price_100
):
    # Given
    freezer.move_to("2020-11-25")

    # When
    price_with_discount = DiscountUseCase().calculate(user=user_with_birthday_at_black_fridays,
                                                      product=product_with_price_100)

    # Then
    assert price_with_discount == 90
