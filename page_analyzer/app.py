import os
from flask import (Flask, render_template, url_for, request,
                   flash, redirect, get_flashed_messages, abort)
from dotenv import load_dotenv
import requests
from .validators import validate_url
from .parser import parse_seo_data
from .url_normalyz import normalize_url
from .models import (get_all_urls, get_url_by_name, insert_url,
                     get_url_by_id, insert_url_check, get_url_checks)

INDEX = "index.html"

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

if not app.config['SECRET_KEY']:
    raise RuntimeError("SECRET_KEY not set in .env file!")


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template(INDEX, url_input='', messages=messages)


@app.route('/urls', methods=['POST'])
def add_url():
    url_input = request.form.get('url', '')
    error = validate_url(url_input)
    if error:
        flash(error, 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            INDEX, url_input=url_input, messages=messages
        ), 422

    normalized_url = normalize_url(url_input)
    existing_url = get_url_by_name(normalized_url)
    if existing_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for('show_url', id=existing_url[0]))
    else:
        new_url = insert_url(normalized_url)
        if new_url:
            flash('Страница успешно добавлена', 'success')
            return redirect(url_for('show_url', id=new_url[0]))
        else:
            flash('Произошла ошибка при добавлении URL', 'danger')
            messages = get_flashed_messages(with_categories=True)
            return render_template(
                INDEX, url_input=url_input, messages=messages
            ), 500


@app.route('/urls')
def list_urls():
    all_urls = get_all_urls()
    messages = get_flashed_messages(with_categories=True)
    return render_template('urls_index.html', urls=all_urls, messages=messages)


@app.route('/urls/<int:id>')
def show_url(id):
    url_data = get_url_by_id(id)
    if url_data is None:
        abort(404, description="Страница не найдена")
    checks_data = get_url_checks(id)
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'urls_show.html',
        url=url_data,
        checks=checks_data,
        messages=messages
    )


@app.route('/urls/<int:id>/checks', methods=['POST'])
def add_url_check(id):
    url_item = get_url_by_id(id)
    if url_item is None:
        flash('Невозможно добавить проверку: URL не найден.', 'danger')
        return redirect(url_for('list_urls'))

    url_name = url_item[1]
    try:
        response = requests.get(url_name, timeout=10)
        response.raise_for_status()
        status_code = response.status_code
        seo_data = parse_seo_data(response.text)
        insert_url_check(
            id,
            status_code,
            seo_data['h1'],
            seo_data['title'],
            seo_data['description']
        )
        flash('Страница успешно проверена', 'success')
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при проверке URL {url_name}: {e}")
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('show_url', id=id))
