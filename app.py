from flask import Flask, request, render_template, jsonify
from auth import Authefication, Login
from db import Data
import json
import logging

app = Flask(__name__, template_folder='static/templates')
base = Data()
auth = Authefication()

@app.route('/api/authentication', methods=['POST'])
def authentication():

    try:
        match request.method:

            case 'POST':
                data = json.loads(request.data.decode())

                create = auth.auth(**data)

                match create:
                    case 'insert_restik':
                        return app.response_class(response=json.dumps({
                        'status': 500,
                        'from': 'server',
                        'msg' : 'RESTAURANT CREATION ERROR',
                    }))

                    case 'insert_auth':
                        return app.response_class(response=json.dumps({
                        'status': 500,
                        'from': 'server',
                        'msg' : 'AUTHENTICATION CREATION ERROR',
                    }))

                    case 'USER ALREADY REGISTERED':
                        return app.response_class(response=json.dumps({
                        'status': 400,
                        'from': 'user exists',
                        'msg' : 'Користувач з данним ім\'ям вже існує',
                    }))

                    case 'USER EMAIL ALREADY REGISTERED':
                        return app.response_class(response=json.dumps({
                        'status': 400,
                        'from': 'email exists',
                        'msg' : 'Користувач з данною поштою вже існує',
                    }))

                    case 'Неправильний формат електроної пошти, пошта не має містити . в початку та кінці, може містити тільки один символ @ та не має містити : ; < > -':
                        return app.response_class(response=json.dumps({
                        'status': 400,
                        'from': 'email',
                        'msg' : create,
                    }))

                    case 'Пароль повинен складатись з 8 симовлів, мати тільки букви латинського алфавіту, цифри та хоча б один спеціальний символ _ або . без пробілів':
                        return app.response_class(response=json.dumps({
                        'status': 400,
                        'from': 'password',
                        'msg' : create,
                    }))

                    case "Ім'я користувача повинно складатись з 8 символів та містити тільки букви латинського алфавіту, цифри та _ підкреслення":
                        return app.response_class(response=json.dumps({
                        'status': 400,
                        'from': 'name',
                        'msg' : create,
                    }))

                    case _:
                        return app.response_class(response=json.dumps({
                            'status': 200,
                            'msg' : 'Authentication succesful',
                            'hash_key' : create
                        }))

            case _:
                return app.response_class(response=json.dumps({
                    'status': 405,
                    'msg' : 'METHOD NOT ALLOWED',
                }))
    except:
        return app.response_class(response=json.dumps({
                    'status': 502,
                    'msg' : 'BAD GATEAWAY',
                }))


log = Login()
@app.route('/api/login', methods=['POST'])
def login():

    try:


        match request.method:

            case 'POST':

                data = json.loads(request.data.decode())

                match data['method']:

                    case 'loginUser':
                        user = log.loginUser(data['key'])
                        if user:
                            return app.response_class(response=json.dumps({
                                'status': 200,
                                'data' : user,
                            }))

                        else:
                            return app.response_class(response=json.dumps({
                                'status': 400,
                                'data' : 'USER NOT EXISTS',
                            }))

                    case 'authUser':
                        authuser = log.authUser(data['password'], data['email'])
                        match authuser:
                            case 'Користувача з данною поштою не існує':
                                return app.response_class(response=json.dumps({
                                    'status': 400,
                                    'msg' : authuser,
                                }))
                            case 'Неправильний пароль. Перевірте правильність вводу':
                                return app.response_class(response=json.dumps({
                                    'status': 400,
                                    'msg' : authuser,
                                }))
                            case _:
                                return app.response_class(response=json.dumps({
                                    'status': 200,
                                    'data' : authuser,
                                }))

            case _:
                return app.response_class(response=json.dumps({
                    'status': 405,
                    'msg' : 'METHOD NOT ALLOWED',
                }))


    except:
        return app.response_class(response=json.dumps({
                    'status': 502,
                    'msg' : 'BAD GATEAWAY',
                }))

@app.route('/admin_panel/<restaurant>')
def admin(restaurant):
    try:
        restaurant_data = base.get_restaurant_data(restaurant)
        if restaurant_data:
            return jsonify(restaurant_data)
        else:
            return jsonify({'error': 'Ресторан не найден'})
    except Exception as e:
        return jsonify({'error': f'Ошибка при получении данных о ресторане: {str(e)}'})


@app.route('/admin_panel/<restaurant>/settings', methods=['GET', 'POST'])
def settings(restaurant):
    if request.method == 'GET':
        # Получение существующих данных из базы данных
        old_data = base.get_user_data(restaurant)
        # return jsonify(restaurant=restaurant, old_data=old_data)
        return render_template('test.html', restaurant=restaurant, old_data=old_data)

    elif request.method == 'POST':
        try:
            # Обработка данных, отправленных формой в формате JSON
            data = request.get_json()

            # Обработка изображения (если оно включено)
            logo = None
            if 'logo' in data:
                logo = data.pop('logo')

            # отправка на сохранения данных
            base.update_user_data(
                restaurant,
                data.get('email'),
                data.get('password'),
                data.get('address'),
                data.get('new_restaurant_name'),
                data.get('start_day'),
                data.get('end_day'),
                data.get('start_time'),
                data.get('end_time'),
                logo
            )

            # Возврат данных в формате JSON
            return jsonify({'message': 'Changes saved successfully'})
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            return jsonify({'message': f'Error: {str(e)}'}), 500


@app.route('/admin_panel/<restaurant>/tables', methods=['GET', 'DELETE'])
def tables(restaurant):
    if request.method == 'GET':
        table_data = base.get_table_data(restaurant)
        return jsonify({'tables': table_data})

    elif request.method == 'DELETE':
        try:
            # ID стола из параметра запроса
            table_id_to_delete = int(request.args.get('id'))
            # удаления стола из базы данных
            deleted_successfully = base.delete_table(restaurant, table_id_to_delete)

            if deleted_successfully:
                return jsonify({'message': 'Table deleted successfully'})
            else:
                return jsonify({'message': 'Error deleting table'}), 500

        except Exception as e:
            logging.error(f"Error: {str(e)}")
            return jsonify({'message': f'Error: {str(e)}'}), 500

# @app.route('/admin_panel/<restaurant>/tables/add', methods='PUT')
# def table_add(restaurant):
#     if request.method == 'PUT':
#
@app.route('/admin_panel/<restaurant>/menu', methods=['GET'])
def menu(restaurant):
    if request.method == 'GET':
        menu_data = base.get_menu_data(restaurant)
        return jsonify({'menu': menu_data})


if __name__ == "__main__":
    app.run(debug=True, host=('0.0.0.0'), port=8000)

