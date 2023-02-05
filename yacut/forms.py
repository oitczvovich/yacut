from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Оригинальная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    URL(require_tld=True, message='Не корректный URL')]
    )
    custom_id = URLField(
        'Короткая ссылка',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать')
