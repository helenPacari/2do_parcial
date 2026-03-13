# update_usuarios.py
from app import create_app, db
from app.models import Usuario

app = create_app()

with app.app_context():
    print("🔄 Actualizando tabla usuarios...")
    
    # Agregar columnas si no existen
    from sqlalchemy import inspect, text
    
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('usuarios')]
    
    if 'primer_inicio' not in columns:
        db.session.execute(text("ALTER TABLE usuarios ADD COLUMN primer_inicio BOOLEAN DEFAULT TRUE"))
        print("✅ Columna 'primer_inicio' agregada")
    
    if 'password_temp' not in columns:
        db.session.execute(text("ALTER TABLE usuarios ADD COLUMN password_temp BOOLEAN DEFAULT FALSE"))
        print("✅ Columna 'password_temp' agregada")
    
    # Actualizar admin existente
    admin = Usuario.query.filter_by(email='admin@farmacia.com').first()
    if admin:
        admin.primer_inicio = False
        admin.password_temp = False
        print("✅ Admin actualizado")
    
    db.session.commit()
    print("🎉 Base de datos actualizada correctamente")