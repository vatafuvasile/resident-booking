import unittest
from datetime import datetime
from booking import BookingService

NOW = datetime.fromisoformat("2026-11-02T09:00:00+00:00")
SLOT = "2026-11-03T10:00:00+00:00"


class BookingTests(unittest.TestCase):
    def setUp(self):
        self.service = BookingService([datetime.fromisoformat(SLOT)], lambda: NOW)

    def rejected(self, resident, slot, message):
        before = self.service.bookings
        with self.assertRaisesRegex(ValueError, message):
            self.service.book(resident, slot)
        self.assertEqual(before, self.service.bookings)

    def test_success_stores_matching_details(self):
        booking = self.service.book("R001", SLOT)
        self.assertEqual("B0001", booking.reference)
        self.assertEqual("R001", booking.resident_id)
        self.assertEqual(datetime.fromisoformat(SLOT), booking.slot)
        self.assertEqual((booking,), self.service.bookings)

    def test_blank_identifier(self):
        self.rejected("", SLOT, "resident identifier")

    def test_non_string_identifier(self):
        self.rejected(None, SLOT, "resident identifier")

    def test_identifier_length_boundary(self):
        self.service.book("R" * 40, SLOT)
        self.rejected("R" * 41, SLOT, "resident identifier")

    def test_identifier_with_control_character(self):
        self.rejected("R001\n", SLOT, "resident identifier")

    def test_malformed_date(self):
        self.rejected("R001", "not-a-date", "ISO 8601")

    def test_non_string_date(self):
        self.rejected("R001", None, "ISO 8601")

    def test_missing_offset(self):
        self.rejected("R001", "2026-11-03T10:00:00", "UTC offset")

    def test_exact_now_is_rejected(self):
        self.rejected("R001", NOW.isoformat(), "future")

    def test_past_date(self):
        self.rejected("R001", "2026-11-01T09:00:00+00:00", "future")

    def test_unoffered_slot(self):
        self.rejected("R001", "2026-11-03T12:00:00+00:00", "offered")

    def test_duplicate_preserves_original(self):
        original = self.service.book("R001", SLOT)
        self.rejected("R002", SLOT, "already booked")
        self.assertEqual((original,), self.service.bookings)

    def test_equivalent_offsets_cannot_double_book(self):
        self.service.book("R001", SLOT)
        self.rejected("R002", "2026-11-03T11:00:00+01:00", "already booked")

    def test_state_is_isolated_between_instances(self):
        other = BookingService([datetime.fromisoformat(SLOT)], lambda: NOW)
        self.service.book("R001", SLOT)
        self.assertEqual((), other.bookings)

    def test_naive_configured_slot_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "UTC offset"):
            BookingService([datetime(2026, 11, 3, 10)], lambda: NOW)

    def test_naive_service_clock_is_rejected(self):
        self.service.clock = lambda: datetime(2026, 11, 2, 9)
        self.rejected("R001", SLOT, "Service clock")


if __name__ == "__main__":
    unittest.main()
