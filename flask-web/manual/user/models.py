from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
import uuid

import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client.dephish


def mess(mess):
    session['messages'] = mess
    session['check_message'] = 1


class User:

    def start_session(self, user):
        del user['password']
        # del user['role']
        session['logged_in'] = True
        session['user'] = user
        session['index_black'] = 1
        session['index_white'] = 1
        session['index_vdomain'] = 1
        return jsonify(user), 200

    def signup(self):
        user = {
            # "_id": uuid.uuid4().hex,
            "name": request.form.get('uname'),
            "password": request.form.get('psw'),
            "role": 'viewer'
        }
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
        if db.users.find_one({'name': user['name']}):
            return jsonify({"error": "Username already in use"}), 400
        if db.users.insert_one(user):
            return self.start_session(user)
        return jsonify({"error": "Signup failed"}), 400

    def login(self):
        try:
            user = db.users.find_one({
                "name": request.form.get('uname')
            })
        except:
            user = None
        if user != None:
            del user['_id']
        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)

        return jsonify({"error": "Invalid login credentials"}), 401

    def changePassword(self):

        try:
            if request.form.get('new_password') != request.form.get('new_password_'):
                return jsonify({"error": "Confirm error"}), 400
            user = db.users.find_one({
                "name": request.form.get('name')
            })
        except:
            user = None
        if user != None:
            # print(request.form.get('old_password'))
            if user and pbkdf2_sha256.verify(request.form.get('old_password'), user['password']):
                result = db.users.update_one({"name": request.form.get('name')},
                                             {"$set": {
                                                 "password": pbkdf2_sha256.encrypt(request.form.get('new_password'))}})
                if result.matched_count > 0:
                    session.clear()
                    return 1
                else:

                    return 0
            else:
                return 0
        else:
            return 0

    def signout(self):
        session.clear()
        return redirect('/')
