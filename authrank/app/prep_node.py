import os
import zipfile
import tarfile

from app import extract_refs, hashish, get_arxiv_meta, sub_mapping
from py2neo import authenticate, Graph, Node, Relationship


def prep_node(graph, f3, in2,  meta_res):
    # Node creation
    ref_list = []
    refs = []
    text = ''
    available = False

    item_count = 1

    c_title = hashish.compress(meta_res['tit'])
    rp_node = graph.find_one("Paper", "id", hashish.get_hash(c_title))

    if rp_node:
        rp = rp_node
        rp['complete'] = "T"
        rp.push()
    else:
        rp = Node("Paper", name=c_title, id=hashish.get_hash(c_title),
                  title=meta_res['tit'], q_score=0.01, complete="T")
        graph.create(rp)

    for a in meta_res['aut']:
        try:
            a = a.decode('utf-8')
        except:
            a = a.decode('latin-1')

        author_node = graph.find_one("Author", "name", a)
        if author_node:
            aut = author_node
        else:
            aut = Node("Author", name=a)
            graph.create(aut)

        graph.create(Relationship(aut, "Published", rp))

    for c in meta_res['cat']:
        C = c.decode('utf-8')
        subject_name = sub_mapping.map_id_to_name(C)

        if not subject_name:
            continue

        category_node = graph.find_one("Category", "name", C)
        if category_node:
            cat = category_node
        else:
            cat = Node("Category", name=C, subject=subject_name)
            graph.create(cat)
        graph.create(Relationship(rp, "BelongsTo", cat))

    # Extract References
    in3 = in2 + '/' + f3

    os.mkdir(in3 + "full")

    try:
        tar = tarfile.open(in3)
        tar.extractall(in3 + "full")
        tar.close()
    except:
        try:
            with zipfile.ZipFile(in3, "r") as zeep:
                zeep.extractall(in3 + "full")
        except:
            return []

    '''
    if item_count == 1:
        with zipfile.ZipFile(in2+"/"+f3,"r") as zeep:
            os.makedirs(in3)
            zeep.extractall(in3)
'''
    for f4 in os.listdir(in3 + "full"):
        if f4.lower().endswith(".bbl"):
            available = True
            with open(in3 + 'full' + '/' + f4) as f:
                try:
                    text = text + '\n' + f.read()
                except:
                    pass
            break

    if not available:
        for f4 in os.listdir(in3 + "full"):
            if f4.lower().endswith(".tex"):
                available = True
                with open(in3 + 'full' + '/' + f4) as f:
                    try:
                        text = text + '\n' + f.read()
                    except:
                        pass

    # Create Reference Relationship
    if available:
        refs = extract_refs.lets_hit_it(text)


        ref_list.append(rp['q_score'])
        for ref in refs:
            comp_title = hashish.compress(ref)
            if not comp_title:
                continue

            h_title = hashish.get_hash(comp_title)
            paper_node = graph.find_one("Paper", "id", h_title)
            if paper_node:
                ppr = paper_node
            else:
                ppr = Node("Paper", name=comp_title, id=h_title,
                           title=ref.lstrip().rstrip(), q_score=0.01, complete="F")
                graph.create(ppr)

            if len(list(graph.match(start_node=rp, end_node=ppr, rel_type="Refers"))) == 0 and (rp != ppr):
                graph.create(Relationship(rp, "Refers", ppr))
                ref_list.append(ppr)

    return ref_list
