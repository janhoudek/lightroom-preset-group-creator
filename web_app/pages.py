from flask import Blueprint, render_template, request, make_response, send_file

import os
import shutil

from web_app.main import create_directory, edit_xmp_cluster, process_folder, remove_file

bp = Blueprint('pages', __name__)

@bp.route('/')
def home():
    return render_template('pages/home.html')

@bp.route('/creator', methods=['GET', 'POST'])
def creator():
    return render_template('pages/creator.html')

@bp.route('/success_upload', methods=['POST'])
def success_upload():
    if request.method == 'POST':
        new_value = request.form.get('new_value')

        f = request.files['file'] 
        f.save(f.filename)

        processed_file = process_folder(f.filename, new_value)

        return send_file(processed_file, as_attachment=True, download_name=f.filename)

    return render_template('pages/success_upload.html', name = f.filename)  

@bp.route('/about')
def about():
    return render_template('pages/about.html')