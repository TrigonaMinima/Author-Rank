import os, time
import format_block
import format_comma

def lets_hit_it(text):
    first_bib = text.find("\\bibitem")+ 9
    next_bib = text.find("\\bibitem", first_bib)
    bib_text = text[first_bib:next_bib]

    num_blocks = bib_text.count("\\newblock")
    if num_blocks == 0:
        format_comma.get_refs(text)
    elif num_blocks > 1:
        format_block.get_refs(text)
