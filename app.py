"""Blogly application."""

from flask import Flask, redirect, url_for, render_template, request, flash
from models import db, connect_db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'session_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/biology'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return redirect(url_for('user_listing'))


@app.route('/users')
def user_listing():
    users = User.query.all()
    return render_template('user_listing.html', users=users)


@app.route('/users/new', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url']


        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

        flash('User added successfully', 'success')  # Optional flash message
        return redirect(url_for('user_listing'))

    return render_template('add_user.html')


@app.route('/users/<int:user_id>')
def user_details(user_id):
    user = User.query.get(user_id)
    return render_template('user_details.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get(user_id)

    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('user_listing'))

    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']

        db.session.commit()

        flash('User updated successfully', 'success')
        return redirect(url_for('user_listing'))

    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('user_listing'))


    db.session.delete(user)
    db.session.commit()

    flash('User deleted successfully', 'success')
    return redirect(url_for('user_listing'))


if __name__ == '__main__':
    app.run(debug=True, port=3000)
