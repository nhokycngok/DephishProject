from functools import wraps
from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from flask_pymongo import PyMongo
import json
import math
import re
from passlib.hash import pbkdf2_sha256
import urllib.parse

page_size = 15

index_tmp = -1

app = Flask(__name__)
app.secret_key = b'\x82}\xb1\xc0J\xa8\xd6\x81\xf9"\x9dm\xd7\xdf\xb7\xb4'
from user.models import User

# config connect to database
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/dephish")
app.config["MONGO_URI"] = "mongodb://localhost:27017/dephish"
mongo = PyMongo(app)
db = mongodb_client.db

# get culumn name from database
def column_name(col):
    temp = col.find_one()
    try:
        del temp['_id']
    except Exception as e:
        print(e)
    data = json.dumps(temp)
    columns = []
    for i in json.loads(data):
        
        columns.append(i)
    return columns


# check login required
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')

    return wrap


# check permisstion must be admin
def check_permisstion_admin():
    user = db.users.find_one({'name': session['user']['name']})
    if user:
        if user['role'] != 'admin':
            User().signout()
            return 0
    else:
        User().signout()
        return 0


# check permistion must be admin or editor
def check_permisstion_editor():
    user = db.users.find_one({'name': session['user']['name']})
    if user:
        if user['role'] != 'admin' and user['role'] != 'editor':
            User().signout()
            return 0
    else:
        User().signout()
        return 0


def check_permisstion_view():
    user = db.users.find_one({'name': session['user']['name']})
    if user:
        if user['role'] == 'viewer':
            return 1
    else:
        return 1

@app.route("/home")
@login_required
def home():
    return render_template("home.html", role=session['user']['role'], username=session['user']['name'], )


@app.route("/")
def home_page():
    if 'logged_in' in session:
        return redirect('/home')
    return render_template("login.html")


@app.route("/signup")
def redirect_signup():
    return render_template("signup.html")

@app.route('/user/signout')
def signout():
    return User().signout()


@app.route('/user/login', methods=['POST'])
def login():
    return User().login()


@app.route("/blacklist/", methods=["GET", "POST"])
@login_required
def black():
    if (request.values.get("domain_search") != None and request.values.get("domain_search") != ''):
        domain_search = request.values.get("domain_search")
        rg = re.compile(".*" + domain_search + ".*", re.IGNORECASE)
        query_search = {"domain": rg}

    else:
        query_search = {}
        domain_search = ''

    max_page = math.ceil(db.blacklist.find(query_search).count() / page_size)
    min_page = 1
    array_page = []
    try:
        page_index = request.args.get('page_index')
        if page_index == "max":
            page_index = max_page
        elif page_index == 'min':
            page_index = min_page
        else:
            page_index = int(page_index)
        if page_index < 1:
            page_index = 1
    except:
        page_index = int(session['index_black'])
        session['index_black'] = 1
    read_index = page_index - 1
    if (page_index <= 3):
        if max_page < 5:
            for i in range(1, max_page + 1, 1):
                array_page.append(i)
        else:
            array_page = [1, 2, 3, 4, 5]
    elif page_index >= max_page - 2:
        for i in range(max_page - 4, max_page + 1, 1):
            array_page.append(i)
    else:
        for i in range(page_index - 2, page_index + 3, 1):
            array_page.append(i)

    urls = db.blacklist.find(query_search).sort("_id", -1).limit(page_size).skip(page_size * read_index)
    columns = column_name(db.blacklist)
    
    view_hidden = ''
    if check_permisstion_view() == 1:
        view_hidden = 'hidden'

    return render_template("index.html", urls=urls, list='black', role=session['user']['role'],
                           username=session['user']['name'],
                           columns=columns, c=view_hidden, b=view_hidden, a=view_hidden, list_name="Blacklist",
                           padging=array_page, padgin_active=page_index, domain_search=domain_search)


@app.route("/phishingReport/", methods=["GET", "POST"])
@login_required
def vdomain_black():
    if (request.values.get("domain_search") != None and request.values.get("domain_search") != ''):
        domain_search = request.values.get("domain_search")
        rg = re.compile(".*" + domain_search + ".*", re.IGNORECASE)
        query_search = {"domain": rg, "type": "black"}

    else:
        query_search = {"type": "black"}
        domain_search = ''
    
    try:
        max_page = math.ceil(db.verify.find(query_search).count() / page_size)
    except:
        max_page = 0
    min_page = 1
    array_page = []
    try:
        page_index = request.args.get('page_index')
        if page_index == "max":
            page_index = max_page
        elif page_index == 'min':
            page_index = min_page
        else:
            page_index = int(page_index)
        if page_index < 1:
            page_index = 1
    except:
        page_index = 1
    read_index = page_index - 1
    if (page_index <= 3):
        if max_page < 5:
            for i in range(1, max_page + 1, 1):
                array_page.append(i)
        else:
            array_page = [1, 2, 3, 4, 5]
    elif page_index >= max_page - 2:
        for i in range(max_page - 4, max_page + 1, 1):
            array_page.append(i)
    else:
        for i in range(page_index - 2, page_index + 3, 1):
            array_page.append(i)
    try:
        urls = db.verify.find(query_search).sort("_id", -1).limit(page_size).skip(page_size * read_index)
        columns = column_name(db.verify)
    except:
        urls = []
        columns = []
    
    view_hidden = ''
    if check_permisstion_view() == 1:
        view_hidden = 'hidden'
    
    return render_template("vdomainBlack.html", urls=urls,  role=session['user']['role'],
                           username=session['user']['name'],
                           columns=columns, c=view_hidden, b=view_hidden, a=view_hidden,
                           list_name="List black domain that need to verify", padging=array_page,
                           padgin_active=page_index,
                           domain_search=domain_search)


@app.route("/legitimateReport/", methods=["GET", "POST"])
@login_required
def legitimateReport():
    if (request.values.get("domain_search") != None and request.values.get("domain_search") != ''):
        domain_search = request.values.get("domain_search")
        rg = re.compile(".*" + domain_search + ".*", re.IGNORECASE)
        query_search = {"domain": rg, "type": "white"}

    else:
        query_search = {"type": "white"}
        domain_search = ''
    
    try:
        max_page = math.ceil(db.verify.find(query_search).count() / page_size)
    except:
        max_page = 0
    min_page = 1
    array_page = []
    try:
        page_index = request.args.get('page_index')
        if page_index == "max":
            page_index = max_page
        elif page_index == 'min':
            page_index = min_page
        else:
            page_index = int(page_index)
        if page_index < 1:
            page_index = 1
    except:
        page_index = 1
    read_index = page_index - 1
    if (page_index <= 3):
        if max_page < 5:
            for i in range(1, max_page + 1, 1):
                array_page.append(i)
        else:
            array_page = [1, 2, 3, 4, 5]
    elif page_index >= max_page - 2:
        for i in range(max_page - 4, max_page + 1, 1):
            array_page.append(i)
    else:
        for i in range(page_index - 2, page_index + 3, 1):
            array_page.append(i)
    try:
        urls = db.verify.find(query_search).sort("_id", -1).limit(page_size).skip(page_size * read_index)
        columns = column_name(db.verify)
    except:
        urls = []
        columns = []

    view_hidden = ''
    if check_permisstion_view() == 1:
        view_hidden = 'hidden'
    
    return render_template("vdomainWhite.html", urls=urls, role=session['user']['role'],
                           username=session['user']['name'],
                           columns=columns, c=view_hidden, b=view_hidden, a=view_hidden,
                           list_name="List white domain that need to verify", padging=array_page,
                           padgin_active=page_index,
                           domain_search=domain_search)

@app.route("/whitelist/", methods=["GET", "POST"])
@login_required
def white():
    if (request.values.get("domain_search") != None and request.values.get("domain_search") != ''):
        domain_search = request.values.get("domain_search")
        rg = re.compile(".*" + domain_search + ".*", re.IGNORECASE)
        query_search = {"domain": rg}

    else:
        query_search = {}
        domain_search = ''
    max_page = math.ceil(db.whitelist.find(query_search).count() / page_size)    
    min_page = 1
    array_page = []
    try:
        page_index = request.args.get('page_index')
        if page_index == "max":
            page_index = max_page
        elif page_index == 'min':
            page_index = min_page
        else:
            page_index = int(page_index)
        if page_index < 1:
            page_index = 1
    except:
        
        page_index = int(session['index_white'])
        session['index_white'] = 1
    read_index = page_index - 1
    if (page_index <= 3):
        if max_page < 5:
            for i in range(1, max_page + 1, 1):
                array_page.append(i)
        else:
            array_page = [1, 2, 3, 4, 5]
    elif page_index >= max_page - 2:
        for i in range(max_page - 4, max_page + 1, 1):
            array_page.append(i)
    else:
        for i in range(page_index - 2, page_index + 3, 1):
            array_page.append(i)

    urls = db.whitelist.find(query_search).sort("_id", -1).limit(page_size).skip(page_size * read_index)
    columns = column_name(db.whitelist)    
    view_hidden = ''
    if check_permisstion_view() == 1:
        view_hidden = 'hidden'

    return render_template("index.html", urls=urls, list='white', role=session['user']['role'],
                           username=session['user']['name'],
                           columns=columns, c=view_hidden, b=view_hidden, a=view_hidden, list_name="Whitelist",
                           padging=array_page, padgin_active=page_index, domain_search=domain_search)

@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    if check_permisstion_editor() == 0:
        return redirect('/')
    if request.method == 'POST':
        if "old_domain" in request.form and "up_domain" in request.form and "up_type" in request.form and "up_level" in request.form:
            # add to black list
            old_domain = request.form['old_domain']
            up_domain = request.form['up_domain']
            up_type = request.form['up_type']
            up_level = request.form['up_level']
            index_black = request.form['index_black']
            try:
                if db.blacklist.find({'domain': up_domain}).count() == 0:
                    result = db.blacklist.update_one({'domain': old_domain},
                                                    {'$set': {'domain': up_domain, "type": up_type, "level": up_level}})
                    if result.matched_count > 0:                    
                        try:
                            session['index_black'] = int(index_black)
                        except:
                            session['index_black'] = 1
                return redirect("/blacklist")
            except Exception as e:                
                return redirect("/blacklist")
            # add to white
        elif "old_domain" in request.form and "up_domain" in request.form:
            old_domain = request.form['old_domain']
            up_domain = request.form['up_domain']
            index_white = request.form['index_white']
            try:
                if db.whitelist.find({'domain': up_domain}).count() == 0:
                    result = db.whitelist.update_one({'domain': old_domain},
                                                    {'$set': {'domain': up_domain}})
                    if result.matched_count > 0:
                        try:
                            session['index_white'] = index_white
                        except:
                            session['index_white'] = 1
                return redirect("/whitelist")
            except Exception as e:                
                return redirect("/whitelist")    
    return render_template("home.html")


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    if check_permisstion_editor() == 0:
        return redirect('/')
    try:
        domain = ''
        list = ''
        domain = request.args.get('domain')
        list = request.args.get('list')
        index_del = request.args.get('index_del')
        if domain != '' and list == 'white':
            result = db.whitelist.remove({'domain': domain})
            delete_number = result['n']
            if delete_number > 0:
                try:
                    session['index_white'] = int(index_del)
                except:
                    session['index_white'] = 1
                return redirect("/whitelist")
            else:
                return redirect("/whitelist")
        elif  list == 'black':
            result = db.blacklist.remove({'domain': domain})
            delete_number = result['n']
            if delete_number > 0:
                try:
                    session['index_black'] = int(index_del)
                except Exception as e:
                    
                    session['index_black'] = 1
                return redirect("/blacklist")
            else:
                return redirect("/blacklist")
    except Exception as e:
        if domain == 'white':
            return redirect("/whitelist")
        elif domain == 'black':
            return redirect("/blacklist")    
    return render_template("home.html")


@app.route("/addblack/", methods=["GET", "POST"])
@login_required
def addblack():
    if check_permisstion_editor() == 0:
        return redirect('/')
    try:
        if request.method == 'POST':
            domain = request.form["domain"]
            url_to_add = db.blacklist.find({"domain": domain}).count()
           
            if url_to_add == 0  and domain != "":
                type = request.form["type"]
                level = request.form["level"]
                db.blacklist.insert_one({'domain': domain, "type": type, "level": level})
                return redirect("/blacklist")
    except:
        return redirect("/blacklist")    
    return redirect("/blacklist")


@app.route("/addwhite/", methods=["GET", "POST"])
@login_required
def addwhite():
    if check_permisstion_editor() == 0:
        return redirect('/')
    try:
        
        if request.method == 'POST':
            domain = request.form["domain"]
            url_to_add = db.whitelist.find({"domain":domain}).count()
            if url_to_add == 0  and domain != "":
                db.whitelist.insert_one({"domain": domain})
                return redirect("/whitelist")
    except:
        return redirect("/whitelist")
    return redirect("/whitelist")

@app.route("/del_from_list_verify", methods=["GET", "POST"])
@login_required
def del_from_list_verify():
    if check_permisstion_editor() == 0:
        return redirect('/')
    domain = ''
    # get domain from client
    type = ''
    try:
        domain = request.args.get('domain')
        type = request.args.get('type')
    except:
        return redirect("/phishingReport")
    if domain != '':
        try:
            # remove domain in verify
            db.verify.remove({'domain': domain})
        except:
            pass
    if type == 'white':
        db.blacklist.insert_one({"domain": domain, "type": "phishing", "level": 'low'})
        return redirect("legitimateReport")
    elif type == "black":
        db.whitelist.insert_one({"domain": domain})
    return redirect("/phishingReport")

@app.route("/add_to_list", methods=["GET", "POST"])
@login_required
def add_to_list():
    if check_permisstion_editor() == 0:
        return redirect('/')
    domain = ''
    list = ''
    try:
        domain = request.args.get('domain')
        list = request.args.get('list')
    except:
        return redirect("/phishingReport")
    if domain != '' and  list == 'black':
        try:
            type = request.args.get('type')
            level = request.args.get('level')
        except:
            return redirect("/phishingReport")
        try:
            if db.blacklist.find({"domain": domain}).count() == 0:
                db.blacklist.insert_one({'domain': domain, "type": type, "level": level})
                db.verify.remove({'domain': domain})
        except:
            pass
    elif domain != '' and   list == 'white':
        try:
            if db.whitelist.find({"domain": domain}).count() == 0:
                db.whitelist.insert_one({"domain": domain})
                db.verify.remove({'domain': domain})
        except:
            pass
    if list == 'white':
        return redirect("legitimateReport")
    return redirect("/phishingReport")

@app.route("/deleteMember/", methods=["GET", "POST"])
@login_required
def deleteMember():
    if check_permisstion_admin() == 0:
        return redirect("/")
    try:
        if request.method == 'GET':
            username = request.args["username"]                        
            db.users.remove({"name": username})            
    except:
        pass
    return redirect("/all_member")


@app.route("/addMember/", methods=["GET", "POST"])
@login_required
def addMember():
    if check_permisstion_admin() == 0:
        return redirect("/")
    try:
        if request.method == 'POST':
            username = request.form["username"]
            role = request.form["role"]
            password = request.form["password"]
            repassword = request.form["repassword"]
            if repassword != password:                
                return redirect("/all_member")
            if role != 'editor' and role != 'viewer':            
                return redirect("/all_member")
            name_to_add = db.users.find_one({"name": username})
            if name_to_add == None and username != "":
                user = {
                    "name": username,
                    "password": password,
                    "role": role
                }
                user['password'] = pbkdf2_sha256.encrypt(user['password'])
                db.users.insert_one(user)                    
    except:
        pass
    return redirect("/all_member")


@app.route("/all_member")
@login_required
def all_member():
    if check_permisstion_admin() == 0:
        return redirect("/")
    if (request.values.get("username_search") != None and request.values.get("username_search") != ''):
        username_search = request.values.get("username_search")
        rg = re.compile(".*" + username_search + ".*", re.IGNORECASE)
        query_search = {"name": rg}

    else:
        query_search = {}
        username_search = ''
    max_page = math.ceil(db.users.find(query_search).count() / page_size)
    min_page = 1
    array_page = []
    try:
        page_index = request.args.get('page_index')
        if page_index == "max":
            page_index = max_page
        elif page_index == 'min':
            page_index = min_page
        else:
            page_index = int(page_index)
        if page_index < 1:
            page_index = 1
    except:
        page_index = 1
    read_index = page_index - 1
    if (page_index <= 3):
        if max_page < 5:
            for i in range(1, max_page + 1, 1):
                array_page.append(i)
        else:
            array_page = [1, 2, 3, 4, 5]
    elif page_index >= max_page - 2:
        for i in range(max_page - 4, max_page + 1, 1):
            array_page.append(i)
    else:
        for i in range(page_index - 2, page_index + 3, 1):
            array_page.append(i)

    all_member = db.users.find(query_search).sort("_id", -1).limit(page_size).skip(page_size * read_index)
    columns = ['Username', 'role', '']    
    return render_template("member.html", role='admin', all_member=all_member, columns=columns, list_name='List Members',
                           username=session['user']['name'],
                           padging=array_page, padgin_active=page_index,
                           username_search=username_search)


@app.route("/reset", methods=["GET", "POST"])
@login_required
def reset():
    if check_permisstion_admin() == 0:
        return redirect("/")
    try:
        name = request.args.get('name')
        if db.users.find({"name": name}).count() ==0 :
            return redirect("/all_member")
        db.users.update_one({'name': name}, {'$set': {'password': pbkdf2_sha256.encrypt('Dephish@123')}})    
        if name == session['user']['name']:
            User().signout()
        return redirect("/all_member")
    except Exception as e:        
        return redirect("/all_member")    
    return render_template("home.html")


@app.route("/change_pass", methods=["GET", "POST"])
@login_required
def to_change_pass():
    return render_template("change_pass.html", role=session['user']['role'], username=session['user']['name'])


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    return render_template("profile.html", role=session['user']['role'], username=session['user']['name'])


@app.route('/user/change_pass', methods=['POST'])
def change_pass():
    if User().changePassword() == 1:
        return jsonify({"success": "Change password unsuccessful"}), 200
    return jsonify({"error": "Change password unsuccessful"}), 400


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=8080)
