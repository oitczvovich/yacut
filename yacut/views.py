from flask import flash, redirect, render_template, request

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .utils import check_symbols, check_unique_short_url, get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """
    Обработка оригинальной ссылки и проверка есть ли вариант сокращенной.
    Создание короткой ссылки или использования ссылки пользователя.
    """
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data

        if check_unique_short_url(custom_id) is not None:
            flash(f'Имя {custom_id} уже занято!')
            return render_template('create_link.html', form=form)

        if custom_id and not check_symbols(custom_id):
            flash('Допустимые символы: A-z, 0-9')
            return render_template('create_link.html', form=form)

        if not custom_id:
            custom_id = get_unique_short_id()

        new_link = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(new_link)
        db.session.commit()
        flash(f'Ваша новая ссылка готова: '
              f'<a href="{request.base_url}{custom_id}">'
              f'{request.base_url}{custom_id}</a>')
    return render_template('create_link.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def yacut_redirect(short):
    """
    Редирект на оригинальную ссылку.
    """
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original)
