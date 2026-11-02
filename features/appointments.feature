Feature: Book a resident support appointment
  As a resident who needs council support
  I want to reserve an available appointment
  So that I know when my enquiry can be discussed

  Background:
    Given the service clock is "2026-11-02T09:00:00+00:00"
    And the council offers "2026-11-03T10:00:00+00:00"

  Scenario: Confirm an available future appointment
    When resident "R001" requests "2026-11-03T10:00:00+00:00"
    Then the result is "confirmed"
    And there are 1 stored bookings
    And the stored appointment belongs to "R001"
