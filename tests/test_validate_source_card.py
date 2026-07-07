import unittest

from scripts.validate_source_card import ValidationError, validate_card


def valid_card():
    return {
        "card_id": "sc-test-1",
        "title": "Synthetic card",
        "source_type": "report",
        "source_locator": "Synthetic Report A",
        "captured_at": "2026-07-06",
        "as_of_date": "2026-07-06",
        "claim_summary": "A synthetic report contains a sample claim.",
        "evidence_notes": ["The report includes a sample table."],
        "confidence": "medium",
        "limitations": ["Synthetic only."],
        "rights_notes": ["No rights conclusion implied."],
        "review_status": "reviewed",
        "tags": ["synthetic"],
    }


class ValidateSourceCardTests(unittest.TestCase):
    def test_valid_reviewed_card_passes(self):
        self.assertEqual(validate_card(valid_card()), [])

    def test_reviewed_card_requires_evidence_notes(self):
        card = valid_card()
        card["evidence_notes"] = []
        with self.assertRaisesRegex(ValidationError, "reviewed cards"):
            validate_card(card)

    def test_do_not_publish_warns_but_passes(self):
        card = valid_card()
        card["review_status"] = "do_not_publish"
        self.assertEqual(
            validate_card(card),
            ["WARNING: review_status is do_not_publish; do not publish this card."],
        )

    def test_source_locator_is_text_only(self):
        card = valid_card()
        card["source_locator"] = "https://example.invalid/should-not-be-fetched"
        self.assertEqual(validate_card(card), [])

    def test_array_fields_must_contain_strings(self):
        card = valid_card()
        card["tags"] = ["synthetic", 3]
        with self.assertRaisesRegex(ValidationError, r"tags\[1\]"):
            validate_card(card)


if __name__ == "__main__":
    unittest.main()
