"""Small in-memory appointment service for the SWE6301 demonstration."""
from dataclasses import dataclass
from datetime import datetime
import re


@dataclass(frozen=True)
class Booking:
    reference: str
    resident_id: str
    slot: datetime


class BookingService:
    def __init__(self, available_slots, clock):
        self.available_slots = frozenset(available_slots)
        if any(s.tzinfo is None or s.utcoffset() is None
               for s in self.available_slots):
            raise ValueError("Offered slots must include a UTC offset")
        self.clock = clock
        self._bookings = {}

    @property
    def bookings(self):
        return tuple(self._bookings.values())

    def book(self, resident_id, slot_text):
        if not isinstance(resident_id, str) or not re.fullmatch(
            r"[A-Za-z0-9_-]{1,40}", resident_id
        ):
            raise ValueError("Enter a resident identifier of 1 to 40 letters, digits, _ or -")
        try:
            slot = datetime.fromisoformat(slot_text)
        except (ValueError, TypeError):
            raise ValueError(
                "Enter an ISO 8601 date and time with a UTC offset"
            ) from None
        if slot.tzinfo is None or slot.utcoffset() is None:
            raise ValueError("Enter an ISO 8601 date and time with a UTC offset")
        now = self.clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("Service clock must include a UTC offset")
        if slot <= now:
            raise ValueError("Choose an appointment in the future")
        if slot not in self.available_slots:
            raise ValueError("Choose an appointment offered by the council")
        if slot in self._bookings:
            raise ValueError("That appointment is already booked")
        booking = Booking(f"B{len(self._bookings) + 1:04d}", resident_id, slot)
        self._bookings[slot] = booking
        return booking
