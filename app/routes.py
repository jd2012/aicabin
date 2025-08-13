from datetime import datetime, date
from flask import (Blueprint, render_template, request, redirect, url_for,
                   flash, jsonify)
from flask_login import login_user, login_required, logout_user, current_user

from . import db
from .models import User, Reservation, is_available

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.portal'))
    return redirect(url_for('main.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('User already exists')
            return redirect(url_for('main.register'))
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful, please log in')
        return redirect(url_for('main.login'))
    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.portal'))
        flash('Invalid credentials')
    return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@bp.route('/portal')
@login_required
def portal():
    today = date.today()
    upcoming = Reservation.query.filter(Reservation.user_id == current_user.id, Reservation.start_date >= today).order_by(Reservation.start_date).all()
    past = Reservation.query.filter(Reservation.user_id == current_user.id, Reservation.end_date < today).order_by(Reservation.start_date.desc()).all()
    return render_template('portal.html', upcoming=upcoming, past=past)


@bp.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html')


@bp.route('/api/reservations')
@login_required
def reservation_feed():
    reservations = Reservation.query.all()
    return jsonify([r.as_dict() for r in reservations])


@bp.route('/reservations/new', methods=['GET', 'POST'])
@login_required
def new_reservation():
    if request.method == 'POST':
        start = datetime.strptime(request.form['start'], '%Y-%m-%d').date()
        end = datetime.strptime(request.form['end'], '%Y-%m-%d').date()
        if end < start:
            flash('End date must be after start date')
            return redirect(url_for('main.new_reservation'))
        if not is_available(start, end):
            flash('Selected dates are not available')
            return redirect(url_for('main.new_reservation'))
        reservation = Reservation(user_id=current_user.id, start_date=start, end_date=end)
        db.session.add(reservation)
        db.session.commit()
        flash('Reservation created')
        return redirect(url_for('main.portal'))
    return render_template('reservation_form.html', reservation=None)


@bp.route('/reservations/<int:res_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_reservation(res_id):
    reservation = Reservation.query.get_or_404(res_id)
    if reservation.user_id != current_user.id:
        flash('Not authorized')
        return redirect(url_for('main.portal'))
    if request.method == 'POST':
        start = datetime.strptime(request.form['start'], '%Y-%m-%d').date()
        end = datetime.strptime(request.form['end'], '%Y-%m-%d').date()
        if end < start:
            flash('End date must be after start date')
            return redirect(url_for('main.edit_reservation', res_id=res_id))
        if not is_available(start, end, exclude_id=res_id):
            flash('Selected dates are not available')
            return redirect(url_for('main.edit_reservation', res_id=res_id))
        reservation.start_date = start
        reservation.end_date = end
        db.session.commit()
        flash('Reservation updated')
        return redirect(url_for('main.portal'))
    return render_template('reservation_form.html', reservation=reservation)
