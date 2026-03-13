# app/routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Usuario
from app.forms import RegistroForm, LoginForm, ActualizarPerfilForm, CambiarPasswordForm

bp = Blueprint('auth', __name__)

@bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistroForm()
    if form.validate_on_submit():
        usuario = Usuario(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            telefono=form.telefono.data,
            email=form.email.data
        )
        usuario.set_password(form.password.data)
        
        db.session.add(usuario)
        db.session.commit()
        
        flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/registro.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        
        if usuario and usuario.check_password(form.password.data):
            login_user(usuario, remember=form.recordar.data)
            next_page = request.args.get('next')
            flash(f'¡Bienvenido {usuario.nombre}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Email o contraseña incorrectos.', 'danger')
    
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('main.index'))



@bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    """Ver y editar perfil del usuario"""
    perfil_form = ActualizarPerfilForm()
    password_form = CambiarPasswordForm()
    
    # Procesar actualización de datos personales
    if perfil_form.validate_on_submit() and 'actualizar_datos' in request.form:
        current_user.nombre = perfil_form.nombre.data
        current_user.apellidos = perfil_form.apellidos.data
        current_user.telefono = perfil_form.telefono.data
        db.session.commit()
        flash('✅ Datos actualizados correctamente', 'success')
        return redirect(url_for('auth.perfil'))
    
    # Procesar cambio de contraseña
    if password_form.validate_on_submit() and 'cambiar_password' in request.form:
        if current_user.check_password(password_form.password_actual.data):
            current_user.set_password(password_form.nueva_password.data)
            db.session.commit()
            flash('✅ Contraseña actualizada correctamente', 'success')
            return redirect(url_for('auth.perfil'))
        else:
            flash('❌ Contraseña actual incorrecta', 'danger')
    
    # Cargar datos actuales en el formulario
    if request.method == 'GET':
        perfil_form.nombre.data = current_user.nombre
        perfil_form.apellidos.data = current_user.apellidos
        perfil_form.telefono.data = current_user.telefono
    
    return render_template('auth/perfil.html', 
                         perfil_form=perfil_form,
                         password_form=password_form,
                         usuario=current_user)