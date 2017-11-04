class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username= StringField('Username',[validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password',[validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
        ])
    confirm = PasswordField('Confirm Password')



class AddingForm(Form):
	id_number = StringField('ID Number', [validators.Length(max=15)])
	first_name = StringField('First Name', [validators.Length(min=1, max=50)])
	last_name = StringField('Last Name', [validators.Length(min=1, max=50)])
	middle_name = StringField('Middle Name', [validators.Length(min=1, max=50)])
	email = StringField('Email', [validators.Length(min=6, max=50)])
	gender = StringField('Gender', [validators.Length(max=20)] )


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
            name = form.name.data
            email = form.email.data
            username = form.username.data
            password = sha256_crypt.encrypt(str(form.password.data))

            # Create cursor
            cur = mysql.connection.cursor()

            # Execute query
            cur.execute("INSERT INTO user(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()

            flash('You are now registered and Can log in anytime!', 'success')

            return redirect(url_for('login'))
    return render_template('register.html', form=form)





@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddingForm(request.form)
    if request.method == 'POST' and form.validate():
            id_number = form.id_number.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            middle_name = form.middle_name.data
            email = form.email.data
           	gender = form.gender.data

            # Create cursor
            cur = mysql.connection.cursor()

            # Execute query
            cur.execute("INSERT INTO Student(id_number, first_name,last_name, middle_name, email, gender ) VALUES(%s, %s, %s, %s, %s, %s )", (id_number, first_name, last_name, middle_name, email,gender))

            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()

            flash('Welcome to MSU-IIT!', 'success')

            return redirect(url_for('home'))
    return render_template('register.html', form=form)