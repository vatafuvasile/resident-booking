"""Small in-memory appointment service for the SWE6301 demonstration."""
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Booking:
    reference: str
    resident_id: str
    slot: datetime


class BookingService:
    def __init__(self, available_slots, clock):
        self.available_slots = frozenset(available_slots)
        self.clock = clock
        self._bookings = {}

    @property
    def bookings(self):
        return tuple(self._bookings.values())

    def book(self, resident_id, slot_text):
        raise NotImplementedError("Booking behaviour not implemented yet")
