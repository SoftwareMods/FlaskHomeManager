""""
    @purpose: simple module to check if logged in.  If not, it will redirect to the login form
"""
import json, os, re
from flask import flash, make_response, render_template as real_render_template, session, redirect
from cryptography.fernet import Fernet
from nav import NAVIGATION
from pathlib import Path



# use for overriding and passing NAVIGATION to all templates,  Needed in each route.name.py
def render_template(*args, **kwargs):
    r = make_response(real_render_template(*args, **kwargs, navigation=NAVIGATION))
    r.headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
    r.headers.set('X-Content-Type-Options', 'nosniff')
    r.headers.set('X-Frame-Options', 'SAMEORIGIN')
    #r.headers.set('Content-Security-Policy', 'default-src "self"')
    return r

def saveJSONToFile(json_file,json_obj):
    print(f"Saving {json_obj} to {json_file}")
    Path(json_file).write_text(json.dumps(json_obj))
    return True

def loadJSONFromFile(json_file):
    return json.loads(Path(json_file).read_text())

def getNewId(mylist):
    """ Get unused or new id """
    ids = []

    if len(mylist) == 0:
        return 1

    # Get all used ids
    for e in mylist:
        ids.append(e['id'])

    # Put them in order so we can get the last
    # one later if needed
    ids.sort()

    # Get list of missing ids within range of list
    missing_ids = [ele for ele in range(1,max(ids) + 1) if ele not in ids]

    # If there are missing ids, get the first one missing
    # else get the last used id and increase by 1
    if len(missing_ids) > 0:
        this_id = missing_ids[0]
    else:
        this_id = ids[-1] + 1

    return this_id



def encrypt_json(message, key=None) ->str:
    """encrypt the json string
        returns str:   is empty if not a hash_key available
    """
    # login passes key
    if not key and ('auth_key' not in session or not session['auth_key']):
        return ''
    encoded_message = message.encode()
    if key:
        f = Fernet(key)
    else:
        f = Fernet(session['auth_key'].encode())
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message

def unencrypt_json(message, key=None):
    """
        check if testing in message and just do json.loads
        else unencrypt and then json.loads
    """
    # login passes key
    if not key and 'auth_key' in session:
        key = session['auth_key'].encode()
    elif not key: return ''
    if not key: return ''
    if not 'testing' in message:
        # try:
            f = Fernet(key)
            message = f.decrypt(message.lstrip('b').encode())
            if message[0] == 'b':
                message = message.lstrip('b')
                print(f'msg: {message}')
        # except: pass
    return json.loads(message)
