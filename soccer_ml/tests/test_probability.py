from soccer_betway.model.probability import no_vig_probabilities
from soccer_betway.providers.demo import demo_quotes


def test_no_vig_sums_to_one_per_book():
    quotes = demo_quotes()
    result = no_vig_probabilities(quotes)
    book_count = len({q.bookmaker for q in quotes})
    for index in range(book_count):
        total = sum(result[q.selection_key][index] for q in quotes[:3])
        assert total == pytest.approx(1.0)

import pytest
