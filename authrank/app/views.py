from flask import render_template, request, redirect, url_for
from werkzeug import secure_filename

from app import app

import os
import zipfile

from app import compare_rank, sys_update, get_top_authors, get_top_papers, sub_mapping, auth_profile, search_arxiv

def allowed_file(filename):
    return '.' in filename and  filename.rsplit('.', 1)[1] == 'zip'

@app.route('/index', methods=['GET'])
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/compare/<id>', methods = ['GET'])
def compare(id):
   rank = compare_rank.compare_rank(id.replace('+','/'))
   print(rank)

   return render_template('compare.html', data=rank)


@app.route('/compare-authors', methods = ['GET', 'POST'])
def compare_authors():
   is_resp = False
   rank=[]

   if request.method == 'POST':
      is_resp = True
      rank = compare_rank.compare_rank(request.form['id'])


   return render_template('compare_authors.html', is_resp = is_resp, rank_list=rank)

@app.route('/feed', methods=['GET', 'POST'])
def feed():
    error_code = 0
    is_resp = False
    data = None

    if request.method == 'POST':
        is_resp = True
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            data = sys_update.graph_update(file.filename)
            if not data:
                    error_code = 2
            elif data['E'] == True:
                    error_code = 3

        else:
            error_code = 1


    return render_template('feed.html', is_resp=is_resp, error_code = error_code, data = data)


@app.route('/top-authors', methods=['GET', 'POST'])
def top_authors():
    error_code = 0
    is_resp = False
    data = []
    meta={}
    title =''
    if request.method == 'POST':
        is_resp = True
        cat = request.form['cat']
        lim = request.form['lim']
        meta['cat'] = cat
        meta['lim'] = lim
        title = sub_mapping.map_id_to_name(cat)
        if not cat:
            error_code = 1
        else:
            data = get_top_authors.get_top_authors(cat, lim)

    return render_template('top_authors.html', is_resp=is_resp, error_code = error_code, data = data, title = title, meta=meta)


@app.route('/top-papers', methods=['GET', 'POST'])
def top_papers():
    error_code = 0
    is_resp = False
    title =''
    data = []
    meta = {}
    if request.method == 'POST':
        is_resp = True
        cat = request.form['cat']
        lim = request.form['lim']
        meta['cat'] = cat
        meta['lim'] = lim
        title = sub_mapping.map_id_to_name(cat)
        if not cat:
            error_code = 1
        else:
            data = get_top_papers.get_top_papers(cat, lim)

    return render_template('top_papers.html', is_resp=is_resp, error_code = error_code, data = data, title = title, meta=meta)


@app.route('/author/<author_name>', methods=['GET', 'POST'])
def author_profile(author_name):
    data = auth_profile.author_profile(author_name.replace('+', ' '))
    return render_template('author_profile.html', data = data, name = author_name.replace('+', ' '))

@app.route('/search', methods=['GET','POST'])
def search():
    error_code = 0
    is_resp = False
    data = []
    meta={}
    title =''
    if request.method == 'POST':
        term = request.form['term'].replace(' ','+')
        if term:
            is_resp = True

        cat = request.form['cat']
        typ = request.form['type']
        meta['title'] = term
        meta['cat'] = cat
        meta['typ'] = typ

        data = search_arxiv.search_arxiv(term, typ, cat)

    return render_template('search.html', is_resp=is_resp, error_code = error_code, data = data, meta = meta)
