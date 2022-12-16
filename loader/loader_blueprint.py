from flask import Blueprint, render_template, request, current_app
from functions import save_upload_picture, PostsHandler
import logging

load_photo_blueprint = Blueprint('load_photo_blueprint', __name__, template_folder='..templates')
logging.basicConfig(filename='basic.log', level=logging.INFO)


@load_photo_blueprint.route('/post')
def add_new_post():
    return render_template('post_form.html')


@load_photo_blueprint.route('/post', methods=['POST'])
def add_new_post_from_user():
    picture = request.files.get('picture')
    content = request.form.get('content')

    if not picture or not content:
        return 'Данные не получены'

    picture_path = save_upload_picture(picture)

    if not picture_path:
        logging.info(f'Файл: {picture.filename} - не изображение')
        return 'Файл - не изображение'

    posts_handler = PostsHandler(current_app.config['POST_PATH'])
    new_post = {'pic': picture_path, 'content': content}
    error = posts_handler.add_post(new_post)
    if error:
        logging.error(f"Ошибка загрузки поста {error}")
        return 'Ошибка загрузки'

    return render_template('post_uploaded.html', picture_path=picture_path, content=content)
