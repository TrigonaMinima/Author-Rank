import time

def get_refs(text):
    cont = True
    start = 0

    while cont:
        get_bib_item = text.find('\\bibitem',start)
        if get_bib_item == -1:
            cont = False
            break
        st = text.find("``", get_bib_item)
        if st == -1:
            cont = False
            break
        st = st + 2
        ed = text.find(",''", st)
        print ' '.join(text[st:ed].replace('{','').replace('}','').strip().split())

        print "----------"

        start = ed
