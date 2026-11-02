"""Run three illustrative requests using a deliberately fixed demo clock."""
from datetime import datetime
from booking import BookingService

slot = "2026-11-03T10:00:00+00:00"
service = BookingService(
    [datetime.fromisoformat(slot)],
    lambda: datetime.fromisoformat("2026-11-02T09:00:00+00:00"),
)
print("Demonstration clock: 2 November 2026 at 09:00 UTC")
for resident, requested in [("R001", slot), ("R002", slot), ("R003", "invalid")]:
    try:
        result = service.book(resident, requested)
        print(f"{resident}: confirmed {result.reference} at {result.slot.isoformat()}")
    except ValueError as error:
        print(f"{resident}: {error}")
print(f"Stored bookings: {len(service.bookings)}")
