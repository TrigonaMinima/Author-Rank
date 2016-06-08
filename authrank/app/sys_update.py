from py2neo import authenticate, Graph, Node, Relationship
import queue

from app import prep_node, get_arxiv_meta, hashish, sub_mapping
from .config import graph_url, upload_folder

graph = Graph(graph_url)

get_ref_query = """
MATCH (p:Paper)-[:Refers]->(r:Paper)
WHERE p.name = {name}
RETURN r
"""


def update_graph_algo(q, c):
    while not q.empty():
        N = q.get()

        nd = N[0]
        o_sc = N[1]
        n_sc = N[2]

        Ref_N = graph.cypher.execute(get_ref_query, name=nd['name'])
        for n in range(0, len(Ref_N)):
            node = Ref_N[n][0]
            old_qs = node['q_score']
            node['q_score'] = node['q_score'] + n_sc - o_sc
            node.push()
            c += 1

            q.put((node, old_qs, node['q_score']))
    return c


def graph_update(fl_name):
    disp_data = {}
    update_queue = queue.Queue()

    meta_res = get_arxiv_meta.call_api(fl_name)

    try:
        c_title = hashish.compress(meta_res['tit'])
    except:
        return None

    ref_list = []

    updated_node_count = 0
    rp_node = graph.find_one("Paper", "id", hashish.get_hash(c_title))

    if not rp_node or rp_node['complete'] == "F":
        filename = fl_name

        path = upload_folder
        updated_node_count += 1
        ref_list = prep_node.prep_node(graph, filename, path, meta_res)
        if len(ref_list) > 0:
            disp_data['tit'] = meta_res['tit']
            disp_data['aut'] = meta_res['aut']
            disp_data['cat'] = []
            for category in meta_res['cat']:
                subject_name = sub_mapping.map_id_to_name(
                    category.decode('utf-8').strip())
            if subject_name:
                disp_data['cat'].append(subject_name)

    try:
        add_score = ref_list[0]
    except:
        pass

    for i in range(1, len(ref_list)):
        ref_node = ref_list[i]
        ref_node_score = ref_node['q_score']

        ref_node['q_score'] = ref_node['q_score'] + add_score
        ref_node.push()
        update_queue.put((ref_list[i], ref_node_score, ref_node['q_score']))
        updated_node_count += 1

    if updated_node_count:
        updated_node_count = update_graph_algo(
            update_queue, updated_node_count)

    #disp_data['C'] =  updated_node_count
    return disp_data
