# Crear nuevo archivo
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Usuario
from app.forms import AdminCrearUsuarioForm
from functools import wraps

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Decorador para verificar si es admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != 'admin':
            flash('❌ Acceso denegado. Se requieren permisos de administrador.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/usuarios')
@login_required
@admin_required
def listar_usuarios():
    """Lista todos los usuarios (solo admin)"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Usuario.query
    
    if search:
        query = query.filter(
            db.or_(
                Usuario.nombre.ilike(f'%{search}%'),
                Usuario.apellidos.ilike(f'%{search}%'),
                Usuario.email.ilike(f'%{search}%')
            )
        )
    
    pagination = query.paginate(page=page, per_page=10, error_out=False)
    usuarios = pagination.items
    
    return render_template('admin/usuarios.html', 
                         usuarios=usuarios, 
                         pagination=pagination,
                         search=search)

@bp.route('/usuarios/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_usuario():
    """Crear un nuevo usuario (solo admin)"""
    form = AdminCrearUsuarioForm()
    
    if form.validate_on_submit():
        # Generar contraseña temporal
        temp_pass = Usuario().generar_password_temporal()
        
        # Crear usuario
        usuario = Usuario(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            telefono=form.telefono.data,
            email=form.email.data,
            rol=form.rol.data,
            primer_inicio=True,
            password_temp=True
        )
        usuario.set_password(temp_pass)
        
        db.session.add(usuario)
        db.session.commit()
        
        flash(f'✅ Usuario {form.email.data} creado exitosamente!', 'success')
        flash(f'🔑 Contraseña temporal: {temp_pass}', 'info')
        
        return redirect(url_for('admin.listar_usuarios'))
    
    return render_template('admin/crear_usuario.html', form=form)

@bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_usuario(id):
    """Editar un usuario (solo admin)"""
    usuario = Usuario.query.get_or_404(id)
    form = AdminCrearUsuarioForm(obj=usuario)
    
    if form.validate_on_submit():
        usuario.nombre = form.nombre.data
        usuario.apellidos = form.apellidos.data
        usuario.telefono = form.telefono.data
        usuario.rol = form.rol.data
        # El email no se puede cambiar
        
        db.session.commit()
        flash(f'✅ Usuario {usuario.email} actualizado!', 'success')
        return redirect(url_for('admin.listar_usuarios'))
    
    return render_template('admin/editar_usuario.html', form=form, usuario=usuario)

@bp.route('/usuarios/reset-password/<int:id>', methods=['POST'])
@login_required
@admin_required
def reset_password(id):
    """Resetear contraseña de un usuario (solo admin)"""
    usuario = Usuario.query.get_or_404(id)
    
    # Generar nueva contraseña temporal
    temp_pass = usuario.generar_password_temporal()
    usuario.set_password(temp_pass)
    usuario.primer_inicio = True
    usuario.password_temp = True
    
    db.session.commit()
    
    flash(f'✅ Contraseña reseteada para {usuario.email}', 'success')
    flash(f'🔑 Nueva contraseña temporal: {temp_pass}', 'info')
    
    return redirect(url_for('admin.listar_usuarios'))

@bp.route('/usuarios/activar/<int:id>', methods=['POST'])
@login_required
@admin_required
def activar_usuario(id):
    """Activar/Desactivar usuario"""
    usuario = Usuario.query.get_or_404(id)
    usuario.activo = not usuario.activo
    db.session.commit()
    
    estado = "activado" if usuario.activo else "desactivado"
    flash(f'✅ Usuario {usuario.email} {estado}', 'success')
    
    return redirect(url_for('admin.listar_usuarios'))