"""Routes for tools"""
import json
import os
from flask import Blueprint, flash, redirect, request, session, Response # last one use for overriding and passing NAVIGATION to all templates
from markupsafe import escape
from helpers.common import render_template, loadJSONFromFile, saveJSONToFile, getNewId
from helpers.shopping import shopping_file, sales_tax
from helpers.settings import system_settings

shopping = Blueprint('shopping', __name__)

# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.
@shopping.route('/shopping', methods=['GET','POST'])
def index():
    """"Shopping page"""

    myshopping = loadJSONFromFile(shopping_file)
    update = False
    
    if request.method == 'POST':
        if not request.form.get('update_id'):
            item_id = getNewId(myshopping)
        else:
            item_id = int(request.form.get('update_id'))
        item = request.form.get('item-name')
        location = request.form.get('item-location')
        price = float(request.form.get('item-price'))
        priority = request.form.get('item-priority')
        purchased = int(request.form.get('item-purchased'))
        taxable = int(request.form.get('item-taxable'))
        item_dict = {
                        "id": item_id,
                        "name": item,
                        "price": price,
                        "location": location,
                        "priority": priority,
                        "taxable": taxable,
                        "purchased": purchased
                    }
        if not request.form.get('update_id'):
            myshopping.append(item_dict)
        else:
            for i in range(len(myshopping)):
                if myshopping[i]['id'] == int(request.form.get('update_id')):
                    myshopping[i] = item_dict
                    break

        if saveJSONToFile(shopping_file, myshopping):
            flash(f'Successfully updated shopping','success')
        else:
            flash(f'Failed to update shopping list','error')

    else:
        
        if request.args.get('update'):
            for i in range(len(myshopping)):
                if myshopping[i]['id'] == int(request.args.get('update')):
                    update = myshopping[i]
                    break

    location_info = {}
    for i in range(len(myshopping)):
        location = myshopping[i]['location']
        price = myshopping[i]['price'] if myshopping[i]['price'] != "" else "?"

        if price != "?":
            price = float(price)
            price_with_tax = float(price) * sales_tax + float(price)
        else:
            price_with_tax = "?"
        if location not in location_info.keys():
            location_info[location] = {'num_items': 1, 'subtotal': price, 'total': price_with_tax}
        else:
            location_info[location]['num_items'] += 1
            if price != "?" and location_info[location]['subtotal'] != "?":
                location_info[location]['subtotal'] += price
            else:
                location_info[location]['subtotal'] = "?"

            if price_with_tax != "?" and location_info[location]['total'] != "?":
                price_with_tax = float(price_with_tax)
                location_info[location]['total'] += price_with_tax
            else:
                location_info[location]['total'] = "?"


    return render_template('shopping/index.html', sidebar=True, tables=True, system_settings=system_settings, update=update, location_info=location_info, myshopping=loadJSONFromFile(shopping_file))

@shopping.route("/shopping/delete/<int:id>", methods=["GET", "POST"])
def delete_item(id):
    """Delete given item"""

    deleted = False
    myshopping = loadJSONFromFile(shopping_file)
    for i in range(len(myshopping)):
        if myshopping[i]['id'] == id:
            del myshopping[i]
            saveJSONToFile(shopping_file, myshopping)
            deleted = True
            break

    if deleted:
        flash('Successfully deleted item', 'success')
    else:
        flash('Failed to delete item', 'error')

    return redirect(f"/shopping")