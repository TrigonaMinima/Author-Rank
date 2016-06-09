# For papers where references are provided in the form of blocks
def get_refs(text, num_blocks):
    cont = True
    start = 0

    refs = []

    while cont:
        get_bib_item = text.find('\\bibitem', start)
        if get_bib_item == -1:
            cont = False
            break
        st = text.find("\\newblock", get_bib_item)
        if st == -1:
            cont = False
            break
        st = st + 9

        mid = text.find("\\newblock", st)
        if mid == -1:
            cont = False
            break

        if num_blocks > 2:
            st = mid + 9
            ed = text.find("\\newblock", st)
        else:
            ed = mid

        ref = text[st:ed]
        refs.append(ref)
        start = ed

    return refs
