from datetime import datetime
from behave import given, when, then
from booking import BookingService


@given('the service clock is "{now}"')
def set_clock(context, now):
    context.now = datetime.fromisoformat(now)


@given('the council offers "{slot}"')
def offer_slot(context, slot):
    context.service = BookingService(
        [datetime.fromisoformat(slot)], lambda: context.now
    )


@given('resident "{resident}" has booked "{slot}"')
def existing_booking(context, resident, slot):
    context.service.book(resident, slot)


@when('resident "{resident}" requests "{slot}"')
def request_booking(context, resident, slot):
    try:
        context.booking = context.service.book(resident, slot)
        context.result = "confirmed"
    except ValueError as error:
        context.result = str(error)


@then('the result is "{expected}"')
def check_result(context, expected):
    assert context.result == expected, (
        f"Expected {expected!r}, got {context.result!r}"
    )


@then('there are {count:d} stored bookings')
def check_count(context, count):
    assert len(context.service.bookings) == count


@then('the stored appointment belongs to "{resident}"')
def check_owner(context, resident):
    assert context.service.bookings[0].resident_id == resident
