
from Application import app, db
from flask import render_template, request, json, Response, redirect, flash, url_for, session
from Application.models import User, Course, Enrollment
from Application.forms import LoginForm, RegisterForm


courseData = [
    {"courseID": "1111", "title": "PHP 111", "description": "Intro to PHP", "credits": "3", "term": "Fall, Spring"},
    {"courseID": "2222", "title": "Java 1", "description": "Intro to Java Programming", "credits": "4",
     "term": "Spring"},
    {"courseID": "3333", "title": "Adv PHP 201", "description": "Advanced PHP Programming", "credits": "3",
     "term": "Fall"}, {"courseID": "4444", "title": "Angular 1", "description": "Intro to Angular", "credits": "3",
                       "term": "Fall, Spring"},
    {"courseID": "5555", "title": "Java 2", "description": "Advanced Java Programming", "credits": "4",
     "term": "Fall"}]

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)


@app.route("/Includes/Favorites")
@app.route("/Includes/Favorites/<term>")
def Favorites(term = None):
    if term is None:
        term = "Spring 2019"
        classes = Course.objects.all()
    return render_template("favorites.html", courseData=classes, Favorites = True, term=term)

#@app.route("/login", methods=["GET", "POST"])
#def login():
#    form = LoginForm()
#    return render_template("login.html", title="Login", form=form, login=True)

#**********************************Start
@app.route("/login", methods=['GET','POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        email       = form.email.data
        password    = form.password.data
        print(email)
        user = User.objects(email=email).first()
        print(user.password)
        print(user.get_password(password))
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect("/index")
        else:
            flash("Sorry, something went wrong.","danger")
    return render_template("login.html", title="Login", form=form, login=True )





@app.route("/register", methods=['POST','GET'])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
    form = RegisterForm()

    if form.validate_on_submit():
        user_id     = User.objects.count()
        user_id     += 1

        email       = form.email.data

        password    = form.password.data
        first_name  = form.first_name.data
        last_name   = form.last_name.data

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        flash("You are successfully registered!","success")
        return redirect(url_for('index'))
    return render_template("register.html", title="Register", form=form, register=True)


#*************************************End

@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    if not session.get('username'):
        return redirect(url_for('login'))

    courseID = request.form.get('courseID')
    coursetitle = request.form.get('title')
    user_id = 1 #request.form.get('user_id')

    if courseID:
        if  Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(f"Oops! You are already registered in this courser {coursetitle}!", "danger")
            return  redirect(url_for("Favorites"))
        else:

            Enrollment(user_id=user_id, courseID=courseID).save()
            flash(f"You are enrolled in {coursetitle}!", "success")
    classes = list(User.objects.aggregate(*[
    {
        '$lookup': {
            'from': 'enrollment',
            'localField': 'user_id',
            'foreignField': 'user_id',
            'as': 'r1'
        }
    }, {
        '$lookup': {
            'from': 'course',
            'localField': 'r1.courseID',
            'foreignField': 'courseID',
            'as': 'r2'
        }
    }, {
        '$unwind': {
            'path': '$r2',
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$match': {
            'user_id': user_id
        }
    }, {
        '$sort': {
            'courseID': 1
        }
    }
]))

    return render_template("enrollment.html", enrollment = True, title="Enrollment", classes=classes)


@app.route("/api/")
@app.route("/api/<idx>")
def api(idx= None):
    if(idx == None):
        jdata = courseData
    else:
        jdata = courseData[int(idx)]

    return Response(json.dumps(jdata), mimetype="application/json")


@app.route("/user")
def user():
     #User(user_id=1, first_name="Christian", last_name="Hur", email="christian@uta.com", password="abc1234").save()
     #User(user_id=2, first_name="Mary", last_name="Jane", email="mary.jane@uta.com", password="password123").save()
     users = User.objects.all()
     return render_template("user.html", users=users)

@app.route("/logout")
def logout():
    session['user_id'] = False
    session.pop('username', None)
    return redirect(url_for('index'))