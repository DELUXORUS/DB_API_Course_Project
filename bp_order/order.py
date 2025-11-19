import os
from flask import render_template, redirect, url_for, request, session
from . import bp
from database.sql_provider import SQLProvider
from database.DB_operations import select_with_headers, insert, update, insert_any
from .model_route import model_route, model_route_cache
from cache.wrapper import fetch_from_cache


provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@bp.route('/', methods=['GET'])
def order():
    if 'basket_items' not in session:
        session['basket_items'] = {}

    all_items_result_info = model_route_cache(provider, [], 'all_favors.sql', select_with_headers)
    all_items = all_items_result_info.result
    connected_favors_result_info = model_route(provider, session['user_id'], 'check_favors.sql', select_with_headers)
    connected_favors = connected_favors_result_info.result

    ids_to_remove = {d['id_favor'] for d in connected_favors}
    filtered_items = [d for d in all_items if d['id_favor'] not in ids_to_remove]
    connected_favors_transformed = transform_favor_dict(connected_favors)

    id_favors = [id_favor['id_favor'] for id_favor in all_items]
    session_dict_basket = session.get('basket_items', {})

    basket_items = {}
    if session_dict_basket:
        for id in id_favors:
            str_id = str(id)
            if session_dict_basket.get(str_id):
                basket_items[str_id] = session_dict_basket[str_id]

    # print("basket_items: ", basket_items)
    return render_template("basket_order.html", basket=basket_items, items=filtered_items, connected_favors=connected_favors_transformed)

@bp.route('/save_order', methods=['GET'])
def save_order():
    client_favor = []
    for id_favor in session['basket_items'].keys():
        user_id = session.get('user_id')
        client_favor.append((user_id, id_favor))

    model_route(provider, client_favor, 'add_client_favor.sql', insert_any)

    session['basket_items'] = {}
    return render_template("success_order.html")

@bp.route('/clear_basket', methods=['GET'])
def clear_basket():
    session['basket_items'] = {}
    return redirect(url_for('bp_order.order'))

@bp.route('/', methods=['POST'])
def add_basket():
    id_favor = request.form.get('id_favor')
    result_info = model_route(provider, [id_favor], 'get_favor.sql', select_with_headers)

    session_dict_basket = session.get('basket_items', {})
    favor_info = result_info.result[0]
    if session_dict_basket.get(id_favor) is None:
        session_dict_basket[id_favor] = favor_info
        session['basket_items'].update(session_dict_basket)

    return redirect(url_for('bp_order.order'))

@bp.route('/disconnect_favor', methods=['POST'])
def disconnect_favor():
    params = list(request.form.values())
    model_route(provider, params, 'disconnect_favor.sql', update)
    return redirect(url_for('bp_order.order'))

def transform_favor_dict(favors: dict) -> dict:
    new_dict = {}

    for item in favors:
        id_favor = str(item['id_favor'])
        value_dict = {k: v for k, v in item.items() if k != 'id_favor'}
        new_dict[id_favor] = value_dict

    return new_dict