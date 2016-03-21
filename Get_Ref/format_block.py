import time

def get_refs(text, num_blocks):
    cont = True
    start = 0

    while cont:
        get_bib_item = text.find('\\bibitem',start)
        if get_bib_item == -1:
            cont = False
            break
        st = text.find("\\newblock", get_bib_item)
        if st == -1:
            cont = False
            break
        st = st + 9

        mid = text.find("\\newblock", st)


        if num_blocks > 2:
            st = mid + 9
            ed = text.find("\\newblock", st)
        else:
            ed = mid


        #print "BLOCKS",num_blocks, st, mid, ed

        print ' '.join(text[st:ed].replace('\\em','').replace('{','').replace('}','').replace('.','').replace('\BBOQ','').replace('\BBCQ','').replace('\Bem','').strip().split())

        print "----------"
        start = ed


