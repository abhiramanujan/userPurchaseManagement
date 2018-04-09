from flask import Flask, render_template, request, session, redirect, url_for
import MySQLdb
from MySQLdb import escape_string as thwart


app = Flask(__name__)

#conn = MySQLdb.connect(host="localhost", user="root", password="ROOTr()()t1234", db="userPurchase")
conn = MySQLdb.connect(host="localhost", user="abhishekr", password="abhiaqua@123", db="userpurchase")

@app.route("/")
def index():
	return render_template("home.html", title="Welcome")

@app.route("/signUp")
def register():
	return render_template("index2.html", title="User Registration")

def invalidAuthent():
	return render_template("index3.html", title="User Registration Fail")

@app.route("/signUp", methods=["POST"])
def signUp():
	email = str(request.form["email"])
	session['email'] = email
	name = str(request.form["name"])
	password = str(request.form["password"])
	
	
	cursor = conn.cursor()

	cursor.execute("INSERT INTO accounts VALUES(%s,%s,%s)",(email, name, password))
	conn.commit()

	return redirect(url_for("login"))

@app.route("/login")
def login():
	return render_template("login.html", title="Login")

@app.route("/checkUser", methods=["POST"])
def check():
	email = str(request.form["email"])
	password = str(request.form["password"])

	cursor = conn.cursor()
	cursor.execute("SELECT password FROM accounts WHERE email='"+ email +"' and password='"+ password + "'")
	user = cursor.fetchall()

	if len(user) == 1:
		return redirect(url_for("enterData"))
	else:
		return render_template("loginFail.html", title="Login")

@app.route("/enterTest")
def enterData():
	return render_template("enterData.html", title="Test")


@app.route("/enter", methods=["POST"])
def enter():

	#return redirect(url_for("beforeDispData"))
	if request.method == 'POST':
		email = str(request.form["email"])#usn
		dopp = str(request.form["dopp"])#batchid
		exp = int(request.form["exp"])#exp
		product_id = str(request.form["product_id"])#observ
		shop_id = str(request.form["shop_id"])#rec
		#total = cursor.execute("SELECT sum(expn) FROM purchase WHERE dop='"+ dop+ "'")
		cursor = conn.cursor()
		#cursor.execute("CALL send_Detail(%s,%s,%s,%s,%s)",(email, dopp, exp, product_id, shop_id))
		cursor.callproc("userpurchase.sendDetails",(email, dopp, exp, product_id, shop_id))
		#cursor.execute("CREATE VIEW monthExpense AS SELECT SUM(exp) from accounts GROUP BY email") 
		conn.commit()
		return redirect(url_for("enterData"))

    # show the form, it wasn't submitted
	return render_template('dispData.html')

@app.route("/enter")
def whichStudent():
	return render_template("whichStudent.html")

@app.route("/enterStudent", methods=["POST"])
def enterStudent():
	#usn = str(request.form["usn"])
	#batch_id = str(request.form["batch_id"])
	session['email'] = str(request.form["email"])
	#session['dopp'] = int(request.form["dopp"])

	return redirect(url_for("dispData"))



@app.route("/dispData", methods=["GET"])
def dispData():
	cursor = conn.cursor()
	em=session['email']
	#dopp=session['dopp']
	cursor.execute("SELECT * FROM purchase WHERE email= '"+em+ "'")
	data = cursor.fetchall()
	#cursor.execute("SELECT * FROM monthExpense")
	#data1= cursor.fetchall()
	return render_template("dispData.html", data=data)


@app.route("/dispExp", methods=["GET"])
def dispExp():
	cursor = conn.cursor()
	em=session['email']

	#dopp=session['dopp']
	cursor.execute("SELECT email,sum(exp) FROM purchase WHERE email= '"+em+ "'")
	data = cursor.fetchall()
	#cursor.execute("SELECT * FROM monthExpense")
	#data1= cursor.fetchall()
	return render_template("dispExp.html", data=data)


@app.route("/bestProd")
def bestProd1():
	return render_template("bestProd.html", title="hello")
@app.route("/bestProd", methods=["GET","POST"])
def bestProd():
	cursor = conn.cursor()
	#pi=session['product_id']
	#pi=pi[1:]+"%"
	prod_id = str(request.form["prod_id"])#observ
	prod_id='%'+prod_id[1:]
	#product_id=product_id.append('%')
	#dopp=session['dopp']
	cursor.execute("SELECT * FROM shopData WHERE prod_id LIKE +'" +prod_id+ "'")
	data = cursor.fetchall()
	#cursor.execute("SELECT * FROM monthExpense")
	#data1= cursor.fetchall()
	return render_template("bestProd.html", data=data)		


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?WT'

if __name__ == "__main__":
	app.run(debug=True)
