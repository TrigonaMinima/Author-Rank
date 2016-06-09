from flask import render_template, request, redirect, url_for
from werkzeug import secure_filename

from app import app

import os
import zipfile

from app import compare_rank, sys_update, get_top_authors, get_top_papers, sub_mapping, auth_profile, search_arxiv, auto_feed

def allowed_file(filename):
    return '.' in filename and  filename.rsplit('.', 1)[1] == 'zip'

@app.route('/index', methods=['GET'])
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/compare/<id>', methods = ['GET'])
def compare(id):
   rank = compare_rank.compare_rank(id.replace('+','/'))

   return render_template('compare.html', data=rank)


@app.route('/compare-authors', methods = ['GET', 'POST'])
def compare_authors():
   is_resp = False
   rank=[]

   if request.method == 'POST':
      is_resp = True
      rank = compare_rank.compare_rank(request.form['id'])


   return render_template('compare_authors.html', is_resp = is_resp, rank_list=rank)


@app.route('/update', methods=['GET', 'POST'])
def update():
    data = {}
    is_resp = False
    if request.method == 'POST':
        is_resp = True
        url = 'http://arxiv.org/list/cs/new?skip=0&show=2000'
        data = auto_feed.auto_feed(url)

    return render_template('update.html', data = data, is_resp = is_resp)


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

if __name__ == "__main__":
    a = datetime.datetime.now().hour
    if a == 0:
        print("HELLO")