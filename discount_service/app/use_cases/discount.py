from datetime import datetime

from loguru import logger
from stories import story, arguments, Success, Result


class DiscountUseCase:

    @story
    @arguments("product", "user")
    def calculate(I):  # noqa
        I.initialize  # noqa
        I.calculate_birthday_discount  # noqa
        I.calculate_black_fridays_discount  # noqa
        I.seal_maximum_limit  # noqa
        I.apply  # noqa

    def initialize(self, ctx):  # noqa
        ctx.discounts = []
        ctx.today = datetime.now()
        ctx.birthday = ctx.user.date_of_birth.ToDatetime()
        logger.info(f"Init - {ctx.today} - {ctx.birthday}")
        return Success()

    def calculate_birthday_discount(self, ctx):  # noqa
        is_birthday = ctx.today.day == ctx.birthday.day and ctx.today.month == ctx.birthday.month
        if is_birthday:
            ctx.discounts.append(5)
        return Success()

    def calculate_black_fridays_discount(self, ctx):  # noqa
        is_black_friday = ctx.today.day == 25 and ctx.today.month == 11
        if is_black_friday:
            ctx.discounts.append(10)
        return Success()

    def seal_maximum_limit(self, ctx):  # noqa
        if sum(ctx.discounts) > 10:
            ctx.discounts.clear()
            ctx.discounts.append(10)
        return Success()

    def apply(self, ctx):  # noqa
        discount = (ctx.product.price_in_cents / 100) * sum(ctx.discounts)
        return Result(int(ctx.product.price_in_cents - discount))
