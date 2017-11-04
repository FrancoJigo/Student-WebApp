from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators


app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'frankeejigzz123'
app.config['MYSQL_DB'] = 'StudentDatabase'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MYSQL
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
		return render_template('about.html')

class AddingForm(Form):
	id_number = StringField('ID Number', [validators.Length(max=15)])
	first_name = StringField('First Name', [validators.Length(min=1, max=50)])
	last_name = StringField('Last Name', [validators.Length(min=1, max=50)])
	middle_name = StringField('Middle Name', [validators.Length(min=1, max=50)])
	gender = StringField('Gender', [validators.Length(max=20)] )
	email = StringField('Email', [validators.Length(min=6, max=50)])


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddingForm(request.form)
    if request.method == 'POST' and form.validate():
            id_number = form.id_number.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            middle_name = form.middle_name.data
            gender = form.gender.data
            email = form.email.data
           	

            # Create cursor
            cur = mysql.connection.cursor()

            # Execute query
            cur.execute("INSERT INTO Student(id_number, first_name,last_name, middle_name, email, gender ) VALUES(%s, %s, %s, %s, %s, %s )", (id_number, first_name, last_name, middle_name, email,gender))

            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()

            flash('Welcome to MSU-IIT!','success')

            return redirect(url_for('home'))
    return render_template('add.html', form=form)

class DeleteForm(Form):
	id_number = StringField('Enter ID Number', [validators.Length(max=15)])

@app.route('/delete', methods=['GET','POST'])
def delete():
	form = DeleteForm(request.form)
	if request.method == 'POST' and form.validate():
			id_number = form.id_number.data
			
			cur = mysql.connection.cursor()
			
			cur.execute("DELETE FROM Student WHERE id_number=id_number")

			mysql.connection.commit()

			cur.close()

			flash('All informations about this ID number were deleted!')
	return render_template('delete.html', form=form)


@app.route('/list')
def list():
		cur = mysql.connection.cursor()

		cur.execute("SELECT * FROM Student")

		rows = cur.fetchall()

		cur.close()

		return render_template("show.html",rows = rows)

@app.route('/update_info/<id_number>',methods=['GET','POST'])
def update_info(id_number):
	
	cur = mysql.connection.cursor()

	result = cur.execute("SELECT * FROM Student WHERE id_number=%s", [id_number])

	rows = cur.fetchone()

	form = AddingForm(request.form)

	form.first_name.data = rows['first_name']
	form.last_name.data = rows['last_name']
	form.middle_name.data = rows['middle_name']
	form.email.data = rows['email']
	form.gender.data = rows['gender']

	if request.method == 'POST' and form.validate():
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		middle_name = request.form['middle_name']
		email = request.form['email']
		gender = request.form['gender']

		cur = mysql.connection.cursor()


		cur.execute("UPDATE Student SET first_name=%s , last_name=%s, middle_name=%s, email=%s , gender=%s where id_number=%s", (first_name,last_name,middle_name,email,gender, id_number))

		mysql.connection.commit()

		cur.close()

		flash('Student Information Updated', 'success')

		return render_template('successupdate.html')	
			
	return render_template('update.html', form=form)





class SearchForm(Form):
	search = StringField('Enter Something Here:',[validators.Length(min = 1 , max=50)])

@app.route('/search', methods= ['GET','POST'])
def search():
	form = SearchForm(request.form)
	if request.method == 'POST' and form.validate():
		search = form.search.data

		cur = mysql.connection.cursor()

		results = cur.execute("SELECT * FROM Student WHERE id_number=%s or first_name=%s or last_name=%s or middle_name=%s or email=%s",[search,search,search,search,search])

		rows = cur.fetchall()

		if results > 0 :

			flash('Here are the Search Results!' , 'success')

			return render_template('searchresult.html', rows=rows)

		else:

			error = 'No informations found, retry again!'

			return render_template('search.html', error=error)
			
		cur.close()

	return render_template('search.html', form=form)
	


if __name__== '__main__':
    app.secret_key= 'secret123'
    app.run(debug=True)
