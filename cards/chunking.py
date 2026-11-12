def chunk_text(text, size=500, overlap=50):
    """Splits the text into segments of `size` characters. Consecutive segments
    overlap by `overlap` characters. Returns a list of strings."""

    strings = []
    if overlap >= size:
        raise ValueError

    elif len(text) < size:
        strings.append(text)

        return strings

    frag = size - overlap

    for i in range(0, len(text), frag):
        strings.append(text[i : i + size])
        if i + size >= len(text):
            break

    return strings
