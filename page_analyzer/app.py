import os
import validators
from flask import (Flask, render_template, url_for, request,
                   flash, redirect, get_flashed_messages, abort)
from dotenv import load_dotenv
from urllib.parse import urlparse
from .models import get_all_urls, get_url_by_name, insert_url, get_url_by_id

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

if not app.config['SECRET_KEY']:
    raise RuntimeError("SECRET_KEY not set in .env file!")


@app.route('/', methods=['GET', 'POST'])
def index():
    url_input = request.form.get('url', '')

    if request.method == 'POST':
        if not validators.url(url_input):
            flash('Некорректный URL', 'danger')
            messages = get_flashed_messages(with_categories=True)
            return render_template(
                'index.html',
                url_input=url_input,
                messages=messages
                ), 422

        if len(url_input) > 255:
            flash('URL превышает 255 символов', 'danger')
            messages = get_flashed_messages(with_categories=True)
            return render_template(
                'index.html',
                url_input=url_input,
                messages=messages
                ), 422

        parsed_url = urlparse(url_input)
        normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}".lower()

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
                    'index.html',
                    url_input=url_input,
                    messages=messages
                    ), 500

    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html',
        url_input=url_input,
        messages=messages
    )


@app.route('/urls')
def list_urls():
    all_urls = get_all_urls()
    return render_template('urls_index.html', urls=all_urls)


@app.route('/urls/<int:id>')
def show_url(id):
    url_data = get_url_by_id(id)
    if url_data is None:
        abort(404, description="Страница не найдена")
    return render_template('urls_show.html', url=url_data)
