# controllers.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User

# Crea tus Blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
mantenedores_bp = Blueprint('mantenedores', __name__)
mantenedores_usernames_bp = Blueprint('mantenedores_usernames', __name__)


# --- Rutas del Blueprint 'main_bp' ---
@main_bp.route('/')
def index():
    """Ruta de la página de inicio."""
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Ruta del panel de control del usuario."""
    return render_template('dashboard.html', user=current_user)

@main_bp.route('/mantenedorY')
@login_required
def mantenedorY():
    """Ruta para la página principal del mantenedor Y (la lista de nombres de cuentas)."""
    return redirect(url_for('mantenedores_usernames.list_usernames'))


# --- Rutas del Blueprint 'mantenedores_bp' (Usuarios - Mantenedor X) ---
@mantenedores_bp.route('/mantenedoresX')
@login_required
def mantenedor_usuarios():
    """Muestra una lista de todos los usuarios registrados."""
    users = User.query.all()
    return render_template('mantenedorX.html', users=users)

@mantenedores_bp.route('/toggle_user_status/<int:user_id>', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    """Cambia el estado (activo/inactivo) de un usuario."""
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    flash(f'El estado del usuario "{user.username}" ha sido actualizado.', 'success')
    return redirect(url_for('mantenedores.mantenedor_usuarios'))

@mantenedores_bp.route('/mantenedoresX/add', methods=['GET', 'POST'])
@login_required
def add_user():
    """Muestra el formulario para agregar un nuevo usuario y procesa el envío."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash('Por favor, completa todos los campos.', 'danger')
            return redirect(url_for('mantenedores.add_user'))

        existing_user_username = User.query.filter_by(username=username).first()
        existing_user_email = User.query.filter_by(email=email).first()

        if existing_user_username:
            flash('El nombre de usuario ya existe.', 'danger')
            return redirect(url_for('mantenedores.add_user'))
        if existing_user_email:
            flash('El correo electrónico ya está registrado.', 'danger')
            return redirect(url_for('mantenedores.add_user'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f'Usuario "{username}" agregado exitosamente.', 'success')
            return redirect(url_for('mantenedores.mantenedor_usuarios'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar el usuario: {e}', 'danger')
            return redirect(url_for('mantenedores.add_user'))

    return render_template('mantenedoresX/add_user.html')

@mantenedores_bp.route('/mantenedoresX/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """Muestra el formulario para editar un usuario existente y procesa el envío."""
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        is_active = request.form.get('is_active') == 'on'

        if not username or not email:
            flash('El nombre de usuario y el correo electrónico no pueden estar vacíos.', 'danger')
            return redirect(url_for('mantenedores.edit_user', user_id=user.id))

        existing_user_username = User.query.filter(User.username == username, User.id != user.id).first()
        existing_user_email = User.query.filter(User.email == email, User.id != user.id).first()

        if existing_user_username:
            flash('El nombre de usuario ya existe para otro usuario.', 'danger')
            return redirect(url_for('mantenedores.edit_user', user_id=user.id))
        if existing_user_email:
            flash('El correo electrónico ya está registrado para otro usuario.', 'danger')
            return redirect(url_for('mantenedores.edit_user', user_id=user.id))

        user.username = username
        user.email = email
        user.is_active = is_active

        if password:
            user.set_password(password)

        try:
            db.session.commit()
            flash(f'Usuario "{user.username}" actualizado exitosamente.', 'success')
            return redirect(url_for('mantenedores.mantenedor_usuarios'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el usuario: {e}', 'danger')
            return redirect(url_for('mantenedores.edit_user', user_id=user.id))

    return render_template('mantenedoresX/edit_user.html', user=user)


# --- Rutas del Blueprint 'mantenedores_usernames_bp' (Nombres de Cuentas - Mantenedor Y) ---

@mantenedores_usernames_bp.route('/mantenedoresY_usernames')
@login_required
def list_usernames():
    """Muestra una lista de todos los nombres de usuarios registrados (cuentas)."""
    users = User.query.all()
    return render_template('mantenedoresY_usernames/mantenedorY_usernames.html', users=users)

@mantenedores_usernames_bp.route('/toggle_username_status/<int:user_id>', methods=['POST'])
@login_required
def toggle_username_status(user_id):
    """Cambia el estado (activo/inactivo) de una cuenta (usuario)."""
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    flash(f'El estado de la cuenta "{user.username}" ha sido actualizado.', 'success')
    return redirect(url_for('mantenedores_usernames.list_usernames'))

@mantenedores_usernames_bp.route('/mantenedoresY_usernames/add', methods=['GET', 'POST'])
@login_required
def add_username():
    """Muestra el formulario para agregar una nueva cuenta (usuario) y procesa el envío."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash('Por favor, completa todos los campos (nombre de cuenta, correo, contraseña).', 'danger')
            return redirect(url_for('mantenedores_usernames.add_username'))

        existing_user_username = User.query.filter_by(username=username).first()
        existing_user_email = User.query.filter_by(email=email).first()

        if existing_user_username:
            flash('El nombre de cuenta ya existe.', 'danger')
            return redirect(url_for('mantenedores_usernames.add_username'))
        if existing_user_email:
            flash('El correo electrónico ya está registrado.', 'danger')
            return redirect(url_for('mantenedores_usernames.add_username'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f'Cuenta "{username}" agregada exitosamente.', 'success')
            return redirect(url_for('mantenedores_usernames.list_usernames'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar la cuenta: {e}', 'danger')
            return redirect(url_for('mantenedores_usernames.add_username'))

    return render_template('mantenedoresY_usernames/add_username.html')

@mantenedores_usernames_bp.route('/mantenedoresY_usernames/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_username(user_id):
    """Muestra el formulario para editar una cuenta (usuario) existente y procesa el envío."""
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        is_active = request.form.get('is_active') == 'on'

        if not username or not email:
            flash('El nombre de cuenta y el correo electrónico no pueden estar vacíos.', 'danger')
            return redirect(url_for('mantenedores_usernames.edit_username', user_id=user.id))

        existing_user_username = User.query.filter(User.username == username, User.id != user.id).first()
        existing_user_email = User.query.filter(User.email == email, User.id != user.id).first()

        if existing_user_username:
            flash('El nombre de cuenta ya existe para otro usuario.', 'danger')
            return redirect(url_for('mantenedores_usernames.edit_username', user_id=user.id))
        if existing_user_email:
            flash('El correo electrónico ya está registrado para otro usuario.', 'danger')
            return redirect(url_for('mantenedores_usernames.edit_username', user_id=user.id))

        user.username = username
        user.email = email
        user.is_active = is_active

        if password:
            user.set_password(password)

        try:
            db.session.commit()
            flash(f'Cuenta "{user.username}" actualizada exitosamente.', 'success')
            return redirect(url_for('mantenedores_usernames.list_usernames'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la cuenta: {e}', 'danger')
            return redirect(url_for('mantenedores_usernames.edit_username', user_id=user.id))

    return render_template('mantenedoresY_usernames/edit_username.html', user=user)

# --- Rutas de autenticación ---
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Ruta para el registro de nuevos usuarios."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash('Por favor, completa todos los campos.', 'danger')
            return redirect(url_for('auth.register'))

        existing_user_username = User.query.filter_by(username=username).first()
        existing_user_email = User.query.filter_by(email=email).first()

        if existing_user_username:
            flash('El nombre de usuario ya existe.', 'danger')
            return redirect(url_for('auth.register'))
        if existing_user_email:
            flash('El correo electrónico ya está registrado.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registro exitoso. ¡Ahora puedes iniciar sesión!', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el usuario: {e}', 'danger')
            return redirect(url_for('auth.register'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Ruta para el inicio de sesión de usuarios."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me') == 'on'

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            # *** MODIFICACIÓN AQUÍ: Verificar si la cuenta está activa ***
            if not user.is_active:
                flash('Error: Tu cuenta ha sido bloqueada. Contacta al administrador.', 'danger')
                return redirect(url_for('auth.login'))
            # **********************************************************

            login_user(user, remember=remember_me)
            flash('¡Inicio de sesión exitoso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Ruta para cerrar la sesión del usuario."""
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('main.index'))