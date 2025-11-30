import glob
import os
from flask import render_template, abort
from markupsafe import Markup
from app import app

# Configuration for the pages directory
PAGES_DIR = 'pages'

def get_pages_catalog():
    """
    Scans the PAGES_DIR, parses filenames formatted as '000x_slug.html',
    and returns a list of dictionaries sorted by the numeric prefix.

    Returns:
        list: [{'slug': 'page1', 'filename': '0001_page1.html'}, ...]
    """
    if not os.path.exists(PAGES_DIR):
        return []

    catalog = []

    # for filename in glob.glob(os.path.join(PAGES_DIR, '\d+_\w+.html')):
    for filepath in glob.glob(os.path.join(PAGES_DIR, '*.html')):
        # Split into ["0001", "somename.html"]
        filename = os.path.basename(filepath)
        [number_part, slug_part] = filename.replace(".html", "").split('_', 1)

        catalog.append({
            'order': int(number_part),
            'slug': slug_part,
            'filename': filename
        })

    # Sort the list by the 'order' key
    catalog.sort(key=lambda x: x['order'])

    return catalog


@app.route('/')
def index():
    # We might want the list of pages on the index too
    catalog = get_pages_catalog()
    pages_list = [item['slug'] for item in catalog]

    return render_template('index.html', pages=pages_list)


@app.route('/<slug>')
def dynamic_page(slug):
    # 1. Get the sorted catalog of files
    catalog = get_pages_catalog()

    if slug not in [item['slug'] for item in catalog]:
        abort(404)

    # 2. Extract the list of slug strings for the template (e.g. navigation)
    pages_list = [item['slug'] for item in catalog]

    # 3. Find the specific file for the requested slug
    # We search the catalog for a matching slug
    target_page = next((item for item in catalog if item['slug'] == slug), None)


    # 5. Read the content
    filepath = os.path.join(PAGES_DIR, target_page['filename'])
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 6. Render template
    # We pass 'pages' (the list of strings) and the content
    return render_template(
        'page.html',
        content=Markup(content),
        title=slug,
        pages=pages_list
    )