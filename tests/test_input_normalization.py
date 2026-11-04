import unittest

from bloom_levels import normalize_bloom_level
from question_text import strip_question_number


class BloomLevelTests(unittest.TestCase):
    def test_normalizes_dataset_and_classifier_labels(self):
        labels = [
            "Remembering",
            "Remember",
            "Understanding",
            "Understandinging",
            "Apply",
            "Applying",
            "Analyzing",
            "Analyze",
            "Evaluating",
            "Evaluate",
            "Creating",
            "Create",
            "Remembering ",
        ]

        normalized = {normalize_bloom_level(label) for label in labels}

        self.assertEqual(
            normalized,
            {"remember", "understand", "apply", "analyze", "evaluate", "create"},
        )


class QuestionTextTests(unittest.TestCase):
    def test_removes_question_numbers_without_truncating_question_text(self):
        self.assertEqual(strip_question_number("1. Explain the process"), "Explain the process")
        self.assertEqual(strip_question_number("Question 12: Describe it"), "Describe it")
        self.assertEqual(strip_question_number("Explain it"), "Explain it")


if __name__ == "__main__":
    unittest.main()
