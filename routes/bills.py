"""Routes for tools"""
import json
import os
from flask import Blueprint, flash, request, session, Response # last one use for overriding and passing NAVIGATION to all templates
from markupsafe import escape
from helpers.common import redirect, render_template, loadJSONFromFile, saveJSONToFile, getNewId
from helpers.bills import bill_file, bill_info_file, getBillInfo, getBillHistory

bills = Blueprint('bills', __name__)

# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.
@bills.route('/bills', methods=['GET','POST'])
def index():
    """"default landing page"""

    update = False
    mybills = loadJSONFromFile(bill_file)

    upcoming_bills = { 'due_dates': {} }
    unpaid_bills = [b for b in mybills if b['paid'] == 0]
    for bill in unpaid_bills:
        amount = float(bill['past_due']) if bill['amount'] == "" else float(bill['amount'])
        paid_by = bill['paid_by']
        due_date = bill['due_date']
        if due_date not in upcoming_bills['due_dates']:
            upcoming_bills['due_dates'][due_date] = { paid_by: amount }
        else:
            # check if paid_by is already present, add to total else add initial entry
            if paid_by not in upcoming_bills['due_dates'][due_date].keys():
                upcoming_bills['due_dates'][due_date][paid_by] = amount
            else:
                upcoming_bills['due_dates'][due_date][paid_by] += amount

    if request.method == 'POST':

        if request.form.get('update_id'):
            bill_id = int(request.form.get('update_id'))
        else:
            bill_id = getNewId(mybills)

        bill_name = request.form.get('bill-name')
        bill_due  = request.form.get('bill-due')
        bill_amount  = request.form.get('bill-amount')
        bill_past_due  = request.form.get('bill-past-due')
        bill_paid_by = request.form.get('paid-by')
        bill_paid  = int(request.form.get('bill-paid'))

        paid_date  = request.form.get('bill-paid-date')

        json_obj = {
                        "id": bill_id,
                        "name": bill_name,
                        "paid_by": bill_paid_by,
                        "due_date": bill_due,
                        "amount": bill_amount,
                        "past_due": bill_past_due,
                        "paid": bill_paid,
                        "paid_date": paid_date
                    }
        if request.form.get('update_id'):
            for i in range(len(mybills)):
                if mybills[i]['id'] == bill_id:
                    mybills[i]['name'] = bill_name
                    mybills[i]['paid_by'] = bill_paid_by
                    mybills[i]['due_date'] = bill_due
                    mybills[i]['amount'] = bill_amount
                    mybills[i]['past_due'] = bill_past_due
                    mybills[i]['paid'] = bill_paid
                    mybills[i]['paid_date'] = paid_date
                    break
        else:
            mybills.append(json_obj)
        try:
            saveJSONToFile(bill_file, mybills)
            if request.form.get('update_id'):
                flash('Successfully updated bill','success')
            else:
                flash('Successfully added new bill','success')
        except:
            flash('Failed to update bill!', 'danger')
    elif request.method == 'GET':
        if request.args.get('update'):
            update_id = int(request.args.get('update'))
            for i in range(len(mybills)):
                if mybills[i]['id'] == update_id:
                    update = mybills[i]

    return render_template('bills/index.html', sidebar=True, tables=True, bills=loadJSONFromFile(bill_file), update=update, upcoming_bills=upcoming_bills)

@bills.route('/bills/delete/<int:bill_id>', methods=['GET','POST'])
def delete_bill(bill_id):
    """"delete given bill"""

    deleted = False
    mybills = loadJSONFromFile(bill_file)
    for i in range(len(mybills)):
        if mybills[i]['id'] == bill_id:
            del mybills[i]
            saveJSONToFile(bill_file, mybills)
            deleted = True
            break

    if deleted:
        flash('Successfully deleted bill', 'success')
    else:
        flash('Failed to delete bill', 'error')

    return redirect(f'/bills')

@bills.route('/bills/paid/<int:bill_id>', methods=['GET','POST'])
def paid_bill(bill_id):
    """"Mark given bill as paid"""

    paid = False
    mybills = loadJSONFromFile(bill_file)
    for i in range(len(mybills)):
        if mybills[i]['id'] == bill_id:
            mybills[i]['paid'] = 1
            saveJSONToFile(bill_file, mybills)
            paid = True
            break

    if paid:
        flash('Successfully marked bill as paid', 'success')
    else:
        flash('Failed to mark bill as paid', 'error')

    return redirect(f'/bills')

@bills.route('/bills/unpaid/<int:bill_id>', methods=['GET','POST'])
def unpaid_bill(bill_id):
    """"Mark given bill as unpaid"""

    unpaid = False
    mybills = loadJSONFromFile(bill_file)
    for i in range(len(mybills)):
        if mybills[i]['id'] == bill_id:
            mybills[i]['paid'] = 0
            saveJSONToFile(bill_file, mybills)
            unpaid = True
            break

    if unpaid:
        flash('Successfully marked bill as unpaid', 'success')
    else:
        flash('Failed to mark bill as unpaid', 'error')

    return redirect(f'/bills')

@bills.route('/bills/info/<bill_name>', methods=['GET','POST'])
def info(bill_name):
    """"Information and payment history"""

    bill_history = []
    mybills = loadJSONFromFile(bill_file)
    for i in range(len(mybills)):
        if mybills[i]['name'] == bill_name:
            bill = mybills[i]

    mybills_info = loadJSONFromFile(bill_info_file)
    bill_info = getBillInfo(bill_name)

    if request.method == 'POST':
        login_method = request.form.get('login_method')
        username = request.form.get('username')
        password = request.form.get('password')
        phone = request.form.get('phone')
        entry = {"name": bill_name, "login_method": login_method, "username": username, "password": password, "phone": phone}
        if not bill_info:
            # Add
            mybills_info.append(entry)
        else:
            # Update
            for i in range(len(mybills_info)):
                if mybills_info[i]['name'] == bill_name:
                    mybills_info[i] = entry
        saveJSONToFile(bill_info_file, mybills_info)

    bill_info = getBillInfo(bill_name)
    get_bill_history = getBillHistory(bill_name)
    for h in get_bill_history:
        if h['paid'] == 1:
            bill_history.append(h)

    return render_template('bills/info.html', sidebar=True, tables=True, bill=bill, bill_info=bill_info, bill_history=bill_history)