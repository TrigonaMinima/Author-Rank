

def get_refs(text):
    cont = True
    start = 0

    while cont:
        get_bib_item = text.find('\\bibitem',start)
        if get_bib_item == -1:
            cont = False
            break
        st = text.find("\\newblock", get_bib_item) + 9
        ed = text.find("\\newblock", st)
        print ' '.join(text[st:ed].replace('\\em','').replace('{','').replace('}','').replace('.','').strip().split())
        start = ed


