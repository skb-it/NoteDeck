from cards.chunking import chunk_text


def test_chunks_overlap_by_given_number_of_characters():
    assert chunk_text("abcdefghij", size=4, overlap=1) == ["abcd", "defg", "ghij"]


def test_respects_size_and_overlap_other_than_one():
    assert chunk_text("abcdefghij", size=5, overlap=2) == ["abcde", "defgh", "ghij"]


def test_does_not_add_empty_chunk_at_the_end():
    assert chunk_text("abcdefghi", size=4, overlap=1) == ["abcd", "defg", "ghi"]
