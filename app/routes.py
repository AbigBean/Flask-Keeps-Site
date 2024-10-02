from flask import render_template, request, url_for, redirect, session, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Mail, Message

from app import app, lm, db, bc, mail
from app.models import User, Notes
from app.forms  import LoginForm, RegisterForm, NoteForm, ResetPasswordRequestForm, ResetPasswordForm
from app.email_sender.tokengenerator import generate_reset_token, verify_reset_token

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/delete_note/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Notes.query.get_or_404(note_id)

    if note.user_id != current_user.id:
        flash('You are not authorized to delete this note.', 'danger')
        return redirect(url_for('index'))

    db.session.delete(note)
    db.session.commit()
    flash('Note has been deleted successfully!', 'success')
    return redirect(url_for('index'))



@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Notes.query.get_or_404(note_id)

    if note.user_id != current_user.id:
        flash('You are not authorized to edit this note.', 'danger')
        return redirect(url_for('index'))

    form = NoteForm()

    if request.method == 'POST' and form.validate():
        note.content = form.note.data
        db.session.commit()
        flash('Note updated successfully!', 'success')
        return redirect(url_for('index'))

    form.note.data = note.content 
    return render_template('edit_note.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def index():

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    
    form = NoteForm()
    user_id = current_user.id

    if request.method == 'POST' and form.validate():
        new_note = Notes(content=form.note.data, user_id=user_id)
        db.session.add(new_note)
        db.session.commit()

        return redirect(url_for('index'))

    # Fetch notes only for the logged-in user
    user_notes = Notes.query.filter_by(user_id=user_id).all()

    return render_template('home.html', form=form, notes=user_notes)


@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()
    msg = None
    success = False

    if request.method == 'GET': 
        return render_template('register.html', form=form, msg=msg, title='Register')
    
    if form.validate_on_submit():
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 
        email    = request.form.get('email'   , '', type=str)

        user = User.query.filter_by(user=username).first()
        user_by_email = User.query.filter_by(email=email).first()
    
        if user:
            msg = 'Error: User exists!'
        elif user_by_email:
            msg = 'Error: This email exists, chose another one!'
        else:         
            pw_hash = bc.generate_password_hash(password).decode('utf-8')
            user = User(user=username, email=email, password=pw_hash)
            db.session.add(user)
            db.session.commit()
            msg = 'User created'  
            success = True
    else:
        msg = f"Input error: {form.errors}"   

    return render_template( 'register.html', form=form, msg=msg, success=success, title="Register")



@app.route('/login', methods=['GET', 'POST'])
def login():


    form = LoginForm()
    msg = None

    if form.validate_on_submit():

        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str).strip()

        user_name = User.query.filter_by(user=username).first()
        if user_name:
            if bc.check_password_hash(user_name.password, password):
                login_user(user_name)
                return redirect(url_for('index'))
            
            msg = "Unknown user or incorrect password"
        else:
            msg = "Unknown user or incorrect password"

    return render_template('login.html', form=form, msg=msg, title="Login")


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():

    form = ResetPasswordRequestForm()
    temp_message = None
    success = None

    if form.validate_on_submit():
        email = request.form.get('email', '', type=str)
        token = generate_reset_token(email)
        send_reset_email(email, token)
        temp_message = True
        success = True
    
    return render_template('reset_request.html', form=form, temp_message=temp_message)


def send_reset_email(email, token):
    reset_link = url_for('reset_token', token=token, _external=True)
    msg = Message('Password Reset Request', recipients=[email])
    msg.body = f'''To reset your password, visit the following link:
{reset_link}

If you did not make this request, please ignore this email.
'''
    mail.send(msg)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):

    email = verify_reset_token(token)
    form = ResetPasswordForm()
    user = User.query.filter_by(email=email).first()
    
    temp_message = None

    if not email:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))

    if request.method == 'POST':
        new_password = request.form.get('password')
        hashed_password = bc.generate_password_hash(new_password).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        temp_message = True
        flash('Your password has been updated!', 'success')

    return render_template('reset_password.html', token=token, form=form, temp_message=temp_message)