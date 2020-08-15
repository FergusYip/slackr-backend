from flask import Blueprint, send_file, request

IMG_URL_ROUTE = Blueprint('img_url', __name__)


@IMG_URL_ROUTE.route('/imgurl/<imgsrc>', methods=['GET'])
def route_img_display(imgsrc):
    '''Flask route for /imgurl'''
    return send_file(f'../profile_images/{imgsrc}')


@IMG_URL_ROUTE.route('/imgurl/defaults/<imgsrc>', methods=['GET'])
def route_defaults_img_display(imgsrc):
    '''Flask route for /imgurl'''
    return send_file(f'../profile_images/defaults/{imgsrc}')
