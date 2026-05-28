from flask import Flask, render_template, redirect, url_for, flash, request
from models import db, User, Task
from forms import RegisterForm, LoginForm, TaskForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
@app.after_request
def add_security_headers(response):

    response.headers['X-Frame-Options'] = 'SAMEORIGIN'

    response.headers['X-Content-Type-Options'] = 'nosniff'

    response.headers['Content-Security-Policy'] = "default-src 'self'"

    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    return response

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db.init_app(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        role = 'admin' if form.email.data == 'admin@example.com' else 'user'

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            role=role
        )

        db.session.add(user)
        db.session.commit()

        flash('Account created successfully!', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):

            login_user(user)

            return redirect(url_for('dashboard'))

        else:
            flash('Login failed', 'danger')

    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    form = TaskForm()

    if form.validate_on_submit():

        task = Task(
            title=form.title.data,
            description=form.description.data,
            user_id=current_user.id
        )

        db.session.add(task)
        db.session.commit()

        flash('Task created!', 'success')

    tasks = Task.query.filter_by(user_id=current_user.id).all()

    return render_template('dashboard.html', form=form, tasks=tasks)


@app.route('/admin')
@login_required
def admin():

    if current_user.role != 'admin':
        return "Access Denied"

    users = User.query.all()

    return render_template('admin.html', users=users)
@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):

    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        return "Unauthorized"

    form = TaskForm()

    if form.validate_on_submit():

        task.title = form.title.data
        task.description = form.description.data

        db.session.commit()

        flash('Task updated!', 'success')

        return redirect(url_for('dashboard'))

    elif request.method == 'GET':

        form.title.data = task.title
        form.description.data = task.description

    return render_template('edit_task.html', form=form)
@app.route('/delete_task/<int:task_id>')
@login_required
def delete_task(task_id):

    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        return "Unauthorized"

    db.session.delete(task)
    db.session.commit()

    flash('Task deleted!', 'success')

    return redirect(url_for('dashboard'))
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)