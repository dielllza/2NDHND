from flask import Flask, render_template, request, redirect, session, flash, json
from mysqlconnection import connectToMySQL
import re
from flask_bcrypt import Bcrypt
import os 



app = Flask("__mame__")
app.secret_key = "save the planet"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^([^0-9]*|[^A-Z]*)$')
bcrypt = Bcrypt(app)
# os.chdir('static/images/products')

@app.route("/")
def index():
	#if session exists return to home.html
	return render_template("index.html")

@app.route("/register")
def register():
	return render_template("register.html")

@app.route("/process/new/user", methods = ["POST"])
def processNewUser():
	valid = True
	if len(request.form['first_name']) < 1 :
		flash("First name is a required field.")
		valid = False
	if len(request.form['last_name']) < 1 :
		flash("Last name is a required field.")
		valid = False
	if len(request.form['email']) < 1 :
		flash("Email address is a required field.")
		valid = False
	if not EMAIL_REGEX.match(request.form['email']):
		flash("Please enter a valid email.")
		valid = False
	if len(request.form['phone_number']) < 1 :
		flash("Phone number is a required field.")
		valid = False
	if len(request.form['password']) < 8 :
		flash("Password must contain at least 8 characters.")
		valid = False
	if request.form['password'] != request.form['confirm_password']:
		flash("Passwords don't match")
		valid = False
	if PASSWORD_REGEX.match(request.form['password']):
		flash("Password must contain at least a number and an uppercase character.")
		valid = False
	connection = connectToMySQL("2ndhnd_db")
	query = 'SELECT email_address from users where email_address = %(email)s'
	data = {
		'email' : request.form['email']
	}
	userEmail =  connection.query_db(query, data)
	if userEmail:
		flash("There already exists an account with that email")
		valid = False
	if valid:
		password_hashed = bcrypt.generate_password_hash(request.form['password'])
		connection = connectToMySQL("2ndhnd_db")
		query = "INSERT INTO users(first_name, last_name, email_address, phone_number, password) VALUES ( %(name)s, %(surname)s, %(email)s, %(phone)s, %(password)s);"
		data = {
			'name' : request.form['first_name'],
			'surname' : request.form['last_name'],
			'email' : request.form['email'],
			'phone' : request.form['phone_number'],
			'password' : password_hashed
		}
		userId = connection.query_db(query, data)
		session['userID'] = userId
		flash("User succesfuly registered")
		return redirect("/categories")
	return redirect("/register")


@app.route("/login")
def login():
	return render_template('login.html')

@app.route("/process/login", methods = ['POST'])
def processLogin():
	connection = connectToMySQL("2ndhnd_db")
	query = 'SELECT * FROM users where email_address = %(email)s;'
	data = {
		'email' : request.form['email']
	}
	user = connection.query_db(query,data)
	if user:
		if bcrypt.check_password_hash(user[0]['password'],request.form['password']):
			session['userID'] = user[0]['id']
			flash(f"Succesfuly logged in. Wellcome back {user[0]['first_name']}")
			return redirect("/success")
	flash("You couldn't be logged in")
	return redirect("/login")


@app.route("/categories")
def categories():
	connection = connectToMySQL('2ndhnd_db')
	query = 'SELECT first_name from users WHERE id = %(ID)s'
	data = {
		'ID' : session['userID']
	}
	name = connection.query_db(query,data)[0]['first_name']
	connection = connectToMySQL('2ndhnd_db')
	query = 'SELECT * from categories;'
	all_categories = connection.query_db(query)
	connection = connectToMySQL('2ndhnd_db')
	# query = 'SELECT categories.id, following_categories.id FROM categories LEFT JOIN following_categories ON categories.id =following_categories.id  JOIN users ON following_categories.user_id = users.id WHERE users.id = 1'
	query = 'SELECT * FROM following_categories WHERE user_id = %(ID)s'
	following_categories = connection.query_db(query,data)
	# follows_list = []
	for category in all_categories:
		category['follows'] = False
		for following in following_categories:
			if category['id'] == following['category_id']:
				category['follows'] = True
	return render_template("categories.html", name = name, all_categories = all_categories)



@app.route("/follow_category/<category_id>")
def followCategory(category_id):
	connection = connectToMySQL('2ndhnd_db')
	query = 'INSERT INTO following_categories(user_id, category_id) VALUES(%(user_id)s,%(category_id)s);'
	data = {
		'user_id' : session['userID'],
		'category_id' : category_id
	}
	connection.query_db(query,data)
	return redirect('/categories')

@app.route("/unfollow_category/<category_id>")
def unfollowCategory(category_id):
	connection = connectToMySQL('2ndhnd_db')
	query = 'DELETE FROM following_categories WHERE user_id = %(user_id)s AND category_id = %(category_id)s;'
	data = {
		'user_id' : session['userID'],
		'category_id' : category_id
	}
	connection.query_db(query,data)
	return redirect('/categories')


@app.route("/success")
def success():
	connection = connectToMySQL('2ndhnd_db')
	query = 'SELECT users.first_name, categories.category_name,products.id, products.users_id, products.product_name, products.price, products.product_description, products.image FROM users LEFT JOIN following_categories ON users.id = following_categories.user_id JOIN categories ON following_categories.category_id = categories.id JOIN products ON categories.id = products.categories_id WHERE users.id = %(ID)s;'
	#query = 'SELECT users1.first_name AS user_first_name, users2.first_name AS owner_first_name, users2.last_name AS owner_last_name, users2.email_address AS owner_email_address, users2.phone_number AS owner_email_address, categories.category_name,products.id, products.product_name, products.price, products.product_description, products.image FROM users AS users1 JOIN following_categories ON users1.id = following_categories.user_id JOIN categories ON following_categories.category_id = categories.id JOIN products ON categories.id = products.categories_id JOIN users AS users2 ON products.users_id = users2.id WHERE users1.id = %(ID)s;'
	data = {
		'ID' : session['userID']
	}
	all_products = connection.query_db(query,data)
	return render_template("home.html", all_products = all_products, loggedUser =  session['userID'] )
 
	

@app.route('/add/product')
def addProduct():
	connection = connectToMySQL('2ndhnd_db')
	query = 'SELECT * from categories;'
	all_categories = connection.query_db(query)
	return render_template("add_product.html", all_categories = all_categories)

@app.route('/process/new/product', methods = ["POST"])
def newProduct():
	valid = True
	if len(request.form['product_name']) < 1 :
		flash("Product name is a required field.")
		valid = False
	if len(request.form['price']) < 1 :
		flash("Price is a required field.")
		valid = False
	if len(request.form['product_description']) < 1 :
		flash("Product description is a required field.")
		valid = False
	if not request.files['upload-img'] :
		flash("Image is a required field.")
		valid = False
	if valid:
		if(os.getcwd().find("static") == -1):
			os.chdir('static/images/products')
			f = request.files['upload-img']  
			f.save(f.filename) 
			print('*'*55)
			print(f.filename)
			print('*'*55)
			connection = connectToMySQL('2ndhnd_db')
			query = 'INSERT INTO products(users_id,product_name,categories_id,price,product_description,image) VALUES (%(user)s,%(prod_name)s,%(category)s,%(price)s,%(desc)s,%(img)s);'
			data = {
				'user' : session['userID'],
				'prod_name' : request.form['product_name'],
				'category' : request.form['select_category'] ,
				'price' : request.form['price'],
				'desc' : request.form['product_description'],
				'img' :  f.filename
			}
			product_id = connection.query_db(query,data)
			unique_path = str(product_id) + f.filename
			os.rename(f.filename,unique_path) 
			connection = connectToMySQL('2ndhnd_db')
			query = 'UPDATE products SET image = %(unique_path)s WHERE id = %(i)s;'
			data = {
				'i' : product_id,
				'unique_path' : unique_path
			}
			connection.query_db(query,data)
			os.chdir('../../../')
			return redirect(f'/view/product/{product_id}')
	return redirect('/add/product')



@app.route('/view/product/<product_ID>')
def viewProduct(product_ID):
	connection = connectToMySQL('2ndhnd_db')
	query =  'SELECT * FROM products JOIN users ON products.users_id = users.id JOIN categories ON products.categories_id = categories.id WHERE products.id = %(i)s;'
	data = {
		'i' : product_ID
	}
	product_info = connection.query_db(query,data)[0]
	return render_template('product_info.html', product_info = product_info, loggedUser =  session['userID'] )


@app.route('/save/product/<product_id>')
def saveProduct(product_id):
	connection = connectToMySQL('2ndhnd_db')
	query = 'INSERT INTO saves(user_id,product_id) VALUES(%(userID)s, %(productID)s)'
	data = {
		'userID' : session['userID'],
		'productID' : product_id
	}
	connection.query_db(query,data)
	return redirect('/all/products/saved')

@app.route('/edit/product/<product_id>')
def editProduct(product_id):
	connection = connectToMySQL('2ndhnd_db')
	query =  'SELECT * FROM products JOIN categories ON products.categories_id = categories.id WHERE products.id = %(i)s;'
	data = {
		'i' : product_id
	}
	product_info = connection.query_db(query,data)[0]
	connection = connectToMySQL('2ndhnd_db')
	query = 'SELECT * from categories;'
	all_categories = connection.query_db(query)
	return render_template('edit_product.html', product_info = product_info, all_categories = all_categories )


@app.route('/process/edit/product/<product_id>', methods = ['POST'])
def processEdit(product_id):
	valid = True
	if len(request.form['product_name']) < 1 :
		flash("Product name is a required field.")
		valid = False
	if len(request.form['price']) < 1 :
		flash("Price is a required field.")
		valid = False
	if len(request.form['product_description']) < 1 :
		flash("Product description is a required field.")
		valid = False
	if not request.files['upload-img'] :
		flash("Image is a required field.")
		valid = False
	connection = connectToMySQL('2ndhnd_db')
	query = 'SELECT image FROM products WHERE id = %(id)s;'
	data = {
		'id' : product_id
	}
	filename = connection.query_db(query,data)[0]['image']
	if(os.getcwd().find("static") == -1):
			os.chdir('static/images/products')
	os.remove(filename)
	os.chdir('../../../')
	if valid:
		if(os.getcwd().find("static") == -1):
			os.chdir('static/images/products')
		f = request.files['upload-img']  
		f.save(f.filename) 
		connection = connectToMySQL('2ndhnd_db')
		unique_path = str(product_id) + f.filename
		os.rename(f.filename,unique_path)
		#query = 'INSERT INTO products(users_id,product_name,categories_id,price,product_description,image) VALUES (%(user)s,%(prod_name)s,%(category)s,%(price)s,%(desc)s,%(img)s);'
		query = 'UPDATE products SET product_name = %(prod_name)s, categories_id  = %(category)s, price = %(price)s,product_description = %(desc)s, image = %(img)s WHERE users_id = %(user)s AND id = %(prod_id)s '
		data = {
			'user' : session['userID'],
			'prod_name' : request.form['product_name'],
			'category' : request.form['select_category'] ,
			'price' : request.form['price'],
			'desc' : request.form['product_description'],
			'img' :  unique_path,
			'prod_id' : product_id
		}
		connection.query_db(query,data)
		os.chdir('../../../')
		return redirect(f'/view/product/{product_id}')
	return redirect(f'/edit/product/{product_id}')	

@app.route('/delete/<product_id>')
def deleteProduct(product_id):
	connection = connectToMySQL('2ndhnd_db')
	query = 'SELECT image FROM products WHERE users_id = %(user_id)s AND id = %(id)s;'
	data = {
		'user_id' : session['userID'],
		'id' : product_id
	}
	filename = connection.query_db(query,data)[0]['image']
	if(os.getcwd().find("static") == -1):
			os.chdir('static/images/products')
	os.remove(filename)
	os.chdir('../../../')
	connection = connectToMySQL('2ndhnd_db')
	query = 'DELETE FROM products WHERE users_id = %(user_id)s AND id = %(id)s;'
	connection.query_db(query,data)
	return render_template('deleated.html')

@app.route('/profile')
def profile():
	connection = connectToMySQL('2ndhnd_db')
	query = 'SELECT * FROM products WHERE users_id = %(user_id)s  ORDER BY updated_at DESC LIMIT 3'
	data = {
		'user_id' : session['userID']
	}
	products_on_sale = connection.query_db(query,data)
	connection = connectToMySQL('2ndhnd_db')
	query = 'SELECT * FROM products JOIN saves ON products.id = saves.product_id JOIN users ON saves.user_id = users.id WHERE users.id = %(user_id)s ORDER BY products.updated_at DESC LIMIT 3'
	data = {
		'user_id' : session['userID']
	}
	saved_products = connection.query_db(query,data)
	return render_template('profile.html', products_on_sale = products_on_sale, saved_products = saved_products)

@app.route('/all/products/sale')
def allProdsOnSale():
	connection = connectToMySQL('2ndhnd_db')
	query = 'SELECT * FROM products JOIN categories ON products.categories_id = categories.id WHERE users_id = %(user_id)s ORDER BY updated_at DESC'
	data = {
		'user_id' : session['userID']
	}
	products_on_sale = connection.query_db(query,data)
	return render_template('all_products_on_sale.html', products_on_sale = products_on_sale, loggedUser =  session['userID'])

@app.route('/all/products/saved')
def  allProductsSaved():
	connection = connectToMySQL('2ndhnd_db')
	query = 'SELECT * FROM products JOIN categories ON products.categories_id = categories.id JOIN saves ON products.id = saves.product_id JOIN users ON saves.user_id = users.id  WHERE users.id = %(user_id)s ORDER BY products.updated_at DESC'
	data = {
		'user_id' : session['userID']
	}
	saved_products = connection.query_db(query,data)
	return render_template('all_saved_products.html', saved_products = saved_products, loggedUser =  session['userID'])



@app.route("/logout")
def logout():
	session.clear()
	return redirect('/login')




if __name__ == "__main__":
	app.run(debug = True)