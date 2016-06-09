import os
from app import format_block,  format_comma


# Finding the right reference format
def lets_hit_it(text):
    if not text:
        return []

    refs = []

    first_bib = text.find("\\bibitem") + 9
    next_bib = text.find("\\bibitem", first_bib)
    bib_text = text[first_bib:next_bib]

    num_blocks = bib_text.count("\\newblock")

    if num_blocks == 0:
        refs = format_comma.get_refs(text)
    elif num_blocks > 1:
        refs = format_block.get_refs(text, num_blocks)

    return refs
