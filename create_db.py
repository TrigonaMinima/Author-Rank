import os,sys
import zipfile

import extract_refs, hashish, get_arxiv_meta
from py2neo import authenticate, Graph, Node, Relationship

graph = Graph("http://localhost:7474/db/data")

seed="/media/beingcooper/New Volume/xyz"


for f1 in os.listdir(seed):
    in1 = seed+str("/" + f1)

    for f2 in os.listdir(in1):
        refs = []
        text = ''
        available = False
        in2 = in1 + str("/" + f2)
        item_count = len(os.listdir(in2))
        try:
            f3 = os.listdir(in2)[0]
        except:
            continue

        # Metadata extraction using Arxiv API

        di = get_arxiv_meta.call_api(f3)

        # Node creation

        c_title = hashish.compress(di['tit'])
        rp_node = graph.find_one("Paper", "id", hashish.get_hash(c_title))
        if rp_node:
            rp = rp_node
        else:
            rp = Node("Paper", name = c_title, id = hashish.get_hash(c_title))
            graph.create(rp)

        for a in di['aut']:
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


        for c in di['cat']:
            category_node = graph.find_one("Category", "name", c.decode('utf-8'))
            if category_node:
                cat = category_node
            else:
                cat = Node("Category", name=c.decode('utf-8'))
                graph.create(cat)
            graph.create(Relationship(rp, "BelongsTo", cat))


        # Extract References

        in3 = (in2 + str("/" + f3)).replace(".zip","")

        if item_count == 1:
            with zipfile.ZipFile(in2+"/"+f3,"r") as zeep:
                os.makedirs(in3)
                zeep.extractall(in3)

        for f4 in os.listdir(in3):
                if f4.lower().endswith(".bbl"):
                    available = True
                    with open(in3+ '/' +f4) as f:
                        try:
                            text = text + '\n' + f.read()
                        except:
                            pass
                    break

        if not available:
            for f4 in os.listdir(in3):
                if f4.lower().endswith(".tex"):
                    available = True
                    with open(in3+ '/' +f4) as f:
                        try:
                            text = text + '\n' + f.read()
                        except:
                            pass
        # Create Reference Relationship

        if available:
            refs = extract_refs.lets_hit_it(text)

            for ref in refs:
                comp_title = hashish.compress(ref)

                if not comp_title:
                    continue

                h_title = hashish.get_hash(comp_title)
                paper_node = graph.find_one("Paper", "id", h_title)
                if paper_node:
                    ppr = paper_node
                else:
                    ppr = Node("Paper", name=comp_title, id=h_title)
                    graph.create(ppr)

                if len(list(graph.match(start_node=rp, end_node=ppr, rel_type="Refers"))) == 0 and (rp != ppr):
                    graph.create(Relationship(rp, "Refers", ppr))





