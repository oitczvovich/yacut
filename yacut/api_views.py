from http import HTTPStatus
from re import match

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import check_symbols, check_unique_short_url, get_unique_short_id

REQUEST_EMPTY = 'Отсутствует тело запроса'
URL_REQUIRED_FIELD = '\"url\" является обязательным полем!'
CHECK_URL = r'^[a-z]+://[^\/\?:]+(:[0-9]+)?(\/.*?)?(\?.*)?$'
ERROR_URL = 'Указан недопустимый URL'
ERROR_SHORT_URL = 'Указано недопустимое имя для короткой ссылки'
ID_NOT_FREE = 'Имя "{}" уже занято.'
NOT_FOUND_ID = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """
    Обработка запроса POST.
    Проверка поступивших данных. Создание и сохранение ссылок в БД.
    """
    arg = request.get_data()
    if not arg:
        return jsonify({'message': REQUEST_EMPTY}), HTTPStatus.BAD_REQUEST
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(REQUEST_EMPTY)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_REQUIRED_FIELD)
    if not match(CHECK_URL, data['url']):
        raise InvalidAPIUsage(ERROR_URL)
    if not data.get('custom_id'):
        data['custom_id'] = get_unique_short_id()
    custom_id = data['custom_id']
    if len(custom_id) > 16 or not check_symbols(custom_id):
        raise InvalidAPIUsage(ERROR_SHORT_URL)
    if check_unique_short_url(custom_id):
        raise InvalidAPIUsage(ID_NOT_FREE.format(data["custom_id"]))

    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original(short):
    """
    Редирект на сайт по короткой ссылке.
    """
    redirect = URLMap.query.filter_by(short=str(short)).first()
    if not redirect:
        raise InvalidAPIUsage(NOT_FOUND_ID, HTTPStatus.NOT_FOUND)
    return jsonify({'url': redirect.original})
