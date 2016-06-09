# For papers where references are provided in comma-separated format
def get_refs(text):
    cont = True
    start = 0

    refs = []

    while cont:
        get_bib_item = text.find('\\bibitem', start)
        if get_bib_item == -1:
            cont = False
            break
        st = text.find("``", get_bib_item)
        if st == -1:
            cont = False
            break
        st = st + 2
        ed = text.find(",''", st)

        ref = text[st:ed]
        refs.append(ref)
        start = ed

    return refs
