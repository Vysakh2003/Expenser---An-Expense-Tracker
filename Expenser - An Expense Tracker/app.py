from flask import Flask, render_template, request, redirect, flash, session, make_response, send_file
from pymongo import MongoClient
from datetime import date
import pdfkit

app = Flask(__name__)
app.secret_key = "satya"
client = MongoClient("mongodb://localhost:27017/")
# db = connect("localhost:27017/expense_tracker")
db = client["expense_tracker"]
if "signup" not in db.list_collection_names():
    db.create_collection("signup")
if "expenses" not in db.list_collection_names():
    db.create_collection("expenses")
# print(client.list_database_names())
users_collection = db["signup"]

collection = db["expenses"]

@app.route("/")
def home():
    return render_template("home1.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('pass')

        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            # return redirect(url_for("index1"))
            print(user["email"])
            session['email'] = user["email"]
            return redirect(location="/home2")
            
        else:
            flash("Invalid username or password")
            return redirect(location="/signup")
       
    return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():

    if request.method == "POST":
        username = request.form.get('username1')
        password = request.form.get('pass1')
        repeat_password = request.form.get('conpass1')
        email = request.form.get('email1')

        existing_user = users_collection.find_one({'username': username,'password':password,'email':email})
        same_name = users_collection.find_one({'username': username})
        if same_name:
            flash("Username already exist. Try another!")
            return render_template('signup.html')
        
        if existing_user:
            flash("User already exist!")
            return redirect(location="/login")

        if password != repeat_password:
            flash("Passwords do not match. Please try again.")
            return render_template('signup.html')

        user = {
            'username': username,
            'password': password,
            'email' : email
        }
        users_collection.insert_one(user)
        flash("Registered successfully!")
        return redirect(location="/login")

    print(users_collection)
    return render_template('signup.html')

@app.route("/home2")
def index1():
    email = session["email"]
    existing_user = users_collection.find_one({'email': email})
    user_record = collection.find_one({'email': email})
    if user_record:
        if user_record["amount"]==[]:
            return render_template("home2.html",values = existing_user["username"])
        else:

            list_amount = user_record["amount"]
            sum_amount = sum(list_amount)
            return render_template("home2.html",values = existing_user["username"],value1 = sum_amount)
    return render_template("home2.html",values = existing_user["username"])

@app.route("/add_expense", methods=["POST", "GET"])
def add_expense():
    email = session["email"]
    existing_user = users_collection.find_one({'email': email})
    print(existing_user["username"],"po")
    if request.method == "POST":
        print(12335)
        amount = request.form.get('amount')
        note = request.form.get('note')
        today = date.today()
        print(amount,note,today)
        user_record = collection.find_one({'email': email})
        if user_record:
            collection.update_one({"email": email}, {"$push": {"id_no": user_record["id_no"][-1]+1 if user_record["id_no"] else 1}})
            collection.update_one({"email": email}, {"$push": {"note": note}})
            collection.update_one({"email": email}, {"$push": {"amount": int(amount)}})
            collection.update_one({"email": email}, {"$push": {"date": today.strftime("%d/%m/%Y")}})
            flash("Expense Recorded!")
            return redirect(location="/add_expense")
        else:
            expense_record = {
                'email' : email,
                'id_no' : [1],
                'amount': [int(amount)],
                'note': [note],
                'date': [today.strftime("%d/%m/%Y")]
            }
            collection.insert_one(expense_record)
            flash("Expense Recorded!")
            return redirect(location="/add_expense")
    return render_template("addexpense.html",values = existing_user["email"])

@app.route('/display_expense', methods=['GET', 'POST'])
def display_expense():
    email = session["email"]

    expenses = collection.find({"email" : email})
    id_number = []
    amunt_lst = []
    notes_lst = []
    date_lst = []
    for expense in expenses:
        id_number.append(expense["id_no"])
        amunt_lst.append(expense["amount"])
        notes_lst.append(expense["note"])
        date_lst.append(expense["date"])
    print(id_number,amunt_lst,notes_lst,date_lst)
    if id_number==[]:
            return render_template('displayexpense.html')
    return render_template('displayexpense.html', val1=id_number[0], val2=amunt_lst[0], val3=notes_lst[0], val4=date_lst[0])

@app.route('/remove_expense', methods=['GET', 'POST'])
def remove_expense():
    email = session["email"]
    if request.method == 'POST':
        expense_id = request.form.get('option')
        
        user_record = collection.find_one({'email': email})
        if user_record and expense_id!='no-action':
            r = r1 = user_record["note"]
            am = am1 = user_record["amount"]
            dat  = dt1= user_record["date"]
            print(r,am,dat)
            lenh = len(user_record["id_no"])
            id_del= [i for i in range(1,len(r))]
            del r[int(expense_id)-1]
            del am[int(expense_id)-1]
            del dat[int(expense_id)-1]
            print(id_del , r,am,dat)
            collection.update_one({"email": email}, {"$set": {"id_no": id_del}})
            collection.update_one({"email": email}, {"$set": {"note": r}})
            collection.update_one({"email": email}, {"$set": {"amount": am}})
            collection.update_one({"email": email}, {"$set": {"date": dat}})
            expense_id = 'no-action'
    
    expenses = collection.find({"email" : email})
    id_number = []
    amunt_lst = []
    notes_lst = []
    date_lst = []
    for expense in expenses:
        id_number.append(expense["id_no"])
        amunt_lst.append(expense["amount"])
        notes_lst.append(expense["note"])
        date_lst.append(expense["date"])
    print(id_number,amunt_lst,notes_lst,date_lst)
    if id_number==[]:
            return render_template('displayexpense.html')
    return render_template('removeexpense.html', val1=id_number[0], val2=amunt_lst[0], val3=notes_lst[0], val4=date_lst[0])


@app.route("/statement")
def statement():

    email = session["email"]
    existing_user = users_collection.find_one({'email': email})
    expenses = collection.find({"email" : email})
    today = date.today()
    id_number = []
    amunt_lst = []
    notes_lst = []
    date_lst = []
    for expense in expenses:
        id_number.append(expense["id_no"])
        amunt_lst.append(expense["amount"])
        notes_lst.append(expense["note"])
        date_lst.append(expense["date"])
    if id_number==[]:
            return render_template('statement.html', name = existing_user["username"],email = existing_user["email"],date =today.strftime("%B %d, %Y"))
    print(id_number,amunt_lst,notes_lst,date_lst)
    if expense:
        list_amount = expense["amount"]
        sum_amount = sum(list_amount)
    else:
        sum_amount=0
    return render_template('statement.html', name = existing_user["username"],email = existing_user["email"],date =today.strftime("%B %d, %Y"),val1=id_number[0], val2=amunt_lst[0], val3=notes_lst[0], val4=date_lst[0], val5=sum_amount)
    

@app.route("/about")
def about():
    
    return render_template('about.html')

@app.route("/logout")
def logout():
    if "email" in session:
        flash("You have been logged out successfully!", "info")
        session.pop("email", None)
    return redirect(location="/login")
