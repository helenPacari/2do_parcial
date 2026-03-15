from app import create_app, db
from app.models import Categoria, Laboratorio, Medicamento, Usuario
from datetime import date, timedelta
import random

app = create_app()

def crear_datos_prueba():
    with app.app_context():
        print("🌱 Creando datos de prueba...")
        
        # ============================================
        # 1. CREAR CATEGORÍAS
        # ============================================
        print("\n📦 Creando categorías...")
        categorias = [
            {"nombre": "Analgésicos", "descripcion": "Medicamentos para aliviar el dolor"},
            {"nombre": "Antiinflamatorios", "descripcion": "Reducen la inflamación"},
            {"nombre": "Antibióticos", "descripcion": "Combaten infecciones bacterianas"},
            {"nombre": "Antigripales", "descripcion": "Alivian síntomas de gripe y resfriado"},
            {"nombre": "Antihistamínicos", "descripcion": "Para alergias"},
            {"nombre": "Gastrointestinales", "descripcion": "Para problemas estomacales"},
            {"nombre": "Cardiovasculares", "descripcion": "Para el corazón y presión arterial"},
            {"nombre": "Vitaminas y Suplementos", "descripcion": "Complementos nutricionales"},
            {"nombre": "Dermatológicos", "descripcion": "Para la piel"},
            {"nombre": "Oftalmológicos", "descripcion": "Para los ojos"},
            {"nombre": "Sistema Nervioso", "descripcion": "Para trastornos neurológicos"},
            {"nombre": "Respiratorios", "descripcion": "Para problemas respiratorios"},
        ]
        
        categorias_creadas = []
        for cat_data in categorias:
            cat = Categoria.query.filter_by(nombre=cat_data["nombre"]).first()
            if not cat:
                cat = Categoria(**cat_data)
                db.session.add(cat)
                print(f"  ✅ Creada: {cat_data['nombre']}")
            else:
                print(f"  ⏩ Ya existe: {cat_data['nombre']}")
            categorias_creadas.append(cat)
        
        db.session.commit()
        print(f"✅ {len(categorias)} categorías procesadas")

        # ============================================
        # 2. CREAR LABORATORIOS
        # ============================================
        print("\n🏭 Creando laboratorios...")
        laboratorios = [
            {"nombre": "Genfar", "direccion": "Calle 10 #23-45, Bogotá", "telefono": "1234567", "email": "contacto@genfar.com", "contacto": "Juan Pérez"},
            {"nombre": "La Sante", "direccion": "Av. Principal #45-67, Medellín", "telefono": "7654321", "email": "info@lasante.com", "contacto": "María Gómez"},
            {"nombre": "MK", "direccion": "Carrera 8 #12-34, Cali", "telefono": "9876543", "email": "ventas@mk.com", "contacto": "Carlos Rodríguez"},
            {"nombre": "Bayer", "direccion": "Transversal 5 #67-89, Barranquilla", "telefono": "2345678", "email": "contacto@bayer.com", "contacto": "Ana Martínez"},
            {"nombre": "Pfizer", "direccion": "Calle 100 #15-20, Bogotá", "telefono": "3456789", "email": "info@pfizer.com", "contacto": "Luis García"},
            {"nombre": "Novartis", "direccion": "Av. El Dorado #90-10, Bogotá", "telefono": "4567890", "email": "contacto@novartis.com", "contacto": "Diana López"},
            {"nombre": "Roche", "direccion": "Carrera 7 #75-30, Bogotá", "telefono": "5678901", "email": "info@roche.com", "contacto": "Andrés Silva"},
            {"nombre": "Abbott", "direccion": "Calle 80 #45-12, Medellín", "telefono": "6789012", "email": "contacto@abbott.com", "contacto": "Laura Torres"},
            {"nombre": "Sanofi", "direccion": "Av. Américas #45-67, Cali", "telefono": "7890123", "email": "info@sanofi.com", "contacto": "Jorge Ramírez"},
            {"nombre": "GSK", "direccion": "Carrera 50 #20-30, Barranquilla", "telefono": "8901234", "email": "contacto@gsk.com", "contacto": "Patricia Castro"},
        ]
        
        laboratorios_creados = []
        for lab_data in laboratorios:
            lab = Laboratorio.query.filter_by(nombre=lab_data["nombre"]).first()
            if not lab:
                lab = Laboratorio(**lab_data)
                db.session.add(lab)
                print(f"  ✅ Creado: {lab_data['nombre']}")
            else:
                print(f"  ⏩ Ya existe: {lab_data['nombre']}")
            laboratorios_creados.append(lab)
        
        db.session.commit()
        print(f"✅ {len(laboratorios)} laboratorios procesados")

        # ============================================
        # 3. CREAR MEDICAMENTOS
        # ============================================
        print("\n💊 Creando medicamentos...")
        
        # Lista de medicamentos con sus características
        medicamentos_data = [
            # Analgésicos
            {"nombre": "Acetaminofén 500mg", "generico": "Paracetamol", "presentacion": "Tabletas", "concentracion": "500mg", 
             "categoria": "Analgésicos", "precio_compra": 500, "precio_venta": 1200, "stock": 200, "stock_minimo": 50,
             "descripcion": "Analgésico y antipirético para aliviar el dolor y reducir la fiebre"},
            
            {"nombre": "Ibuprofeno 400mg", "generico": "Ibuprofeno", "presentacion": "Tabletas", "concentracion": "400mg",
             "categoria": "Antiinflamatorios", "precio_compra": 800, "precio_venta": 1800, "stock": 150, "stock_minimo": 30,
             "descripcion": "Antiinflamatorio no esteroideo para dolor e inflamación"},
            
            {"nombre": "Naproxeno 250mg", "generico": "Naproxeno", "presentacion": "Tabletas", "concentracion": "250mg",
             "categoria": "Antiinflamatorios", "precio_compra": 900, "precio_venta": 2200, "stock": 80, "stock_minimo": 20,
             "descripcion": "Para dolores musculares y articulares"},
            
            {"nombre": "Diclofenaco 50mg", "generico": "Diclofenaco", "presentacion": "Tabletas", "concentracion": "50mg",
             "categoria": "Antiinflamatorios", "precio_compra": 600, "precio_venta": 1500, "stock": 120, "stock_minimo": 25,
             "descripcion": "Antiinflamatorio para dolores articulares"},
            
            # Antibióticos
            {"nombre": "Amoxicilina 500mg", "generico": "Amoxicilina", "presentacion": "Cápsulas", "concentracion": "500mg",
             "categoria": "Antibióticos", "precio_compra": 1500, "precio_venta": 3500, "stock": 60, "stock_minimo": 15,
             "descripcion": "Antibiótico de amplio espectro - Requiere receta médica", "requiere_receta": True},
            
            {"nombre": "Azitromicina 500mg", "generico": "Azitromicina", "presentacion": "Tabletas", "concentracion": "500mg",
             "categoria": "Antibióticos", "precio_compra": 3000, "precio_venta": 6800, "stock": 45, "stock_minimo": 10,
             "descripcion": "Antibiótico para infecciones respiratorias - Requiere receta", "requiere_receta": True},
            
            {"nombre": "Ciprofloxacino 500mg", "generico": "Ciprofloxacino", "presentacion": "Tabletas", "concentracion": "500mg",
             "categoria": "Antibióticos", "precio_compra": 2200, "precio_venta": 5000, "stock": 35, "stock_minimo": 8,
             "descripcion": "Antibiótico para infecciones urinarias - Requiere receta", "requiere_receta": True},
            
            # Antigripales
            {"nombre": "Dolex Gripa", "generico": "Paracetamol + Fenilefrina", "presentacion": "Tabletas", "concentracion": "500mg/10mg",
             "categoria": "Antigripales", "precio_compra": 2000, "precio_venta": 4500, "stock": 90, "stock_minimo": 20,
             "descripcion": "Alivia síntomas de gripe y resfriado"},
            
            {"nombre": "Actron Gripa", "generico": "Ibuprofeno + Fenilefrina", "presentacion": "Tabletas", "concentracion": "400mg/10mg",
             "categoria": "Antigripales", "precio_compra": 2500, "precio_venta": 5500, "stock": 70, "stock_minimo": 15,
             "descripcion": "Para gripe con dolor e inflamación"},
            
            {"nombre": "Loratadina 10mg", "generico": "Loratadina", "presentacion": "Tabletas", "concentracion": "10mg",
             "categoria": "Antihistamínicos", "precio_compra": 400, "precio_venta": 1000, "stock": 200, "stock_minimo": 40,
             "descripcion": "Antialérgico no sedante"},
            
            {"nombre": "Cetirizina 10mg", "generico": "Cetirizina", "presentacion": "Tabletas", "concentracion": "10mg",
             "categoria": "Antihistamínicos", "precio_compra": 450, "precio_venta": 1100, "stock": 180, "stock_minimo": 35,
             "descripcion": "Para alergias y rinitis alérgica"},
            
            # Gastrointestinales
            {"nombre": "Omeprazol 20mg", "generico": "Omeprazol", "presentacion": "Cápsulas", "concentracion": "20mg",
             "categoria": "Gastrointestinales", "precio_compra": 600, "precio_venta": 1500, "stock": 150, "stock_minimo": 30,
             "descripcion": "Protector gástrico para acidez y reflujo"},
            
            {"nombre": "Hioscina 10mg", "generico": "Butilhioscina", "presentacion": "Tabletas", "concentracion": "10mg",
             "categoria": "Gastrointestinales", "precio_compra": 700, "precio_venta": 1800, "stock": 100, "stock_minimo": 25,
             "descripcion": "Antiespasmódico para cólicos estomacales"},
            
            {"nombre": "Loperamida 2mg", "generico": "Loperamida", "presentacion": "Tabletas", "concentracion": "2mg",
             "categoria": "Gastrointestinales", "precio_compra": 300, "precio_venta": 800, "stock": 120, "stock_minimo": 20,
             "descripcion": "Para el control de la diarrea"},
            
            # Cardiovasculares
            {"nombre": "Losartán 50mg", "generico": "Losartán", "presentacion": "Tabletas", "concentracion": "50mg",
             "categoria": "Cardiovasculares", "precio_compra": 900, "precio_venta": 2200, "stock": 85, "stock_minimo": 20,
             "descripcion": "Para la presión arterial alta - Requiere receta", "requiere_receta": True},
            
            {"nombre": "Enalapril 10mg", "generico": "Enalapril", "presentacion": "Tabletas", "concentracion": "10mg",
             "categoria": "Cardiovasculares", "precio_compra": 700, "precio_venta": 1700, "stock": 95, "stock_minimo": 25,
             "descripcion": "Para hipertensión - Requiere receta", "requiere_receta": True},
            
            {"nombre": "AAS 100mg", "generico": "Ácido Acetilsalicílico", "presentacion": "Tabletas", "concentracion": "100mg",
             "categoria": "Cardiovasculares", "precio_compra": 200, "precio_venta": 500, "stock": 300, "stock_minimo": 50,
             "descripcion": "Antiplaquetario para prevenir problemas cardíacos"},
            
            # Vitaminas
            {"nombre": "Vitamina C 1000mg", "generico": "Ácido Ascórbico", "presentacion": "Tabletas efervescentes", "concentracion": "1000mg",
             "categoria": "Vitaminas y Suplementos", "precio_compra": 1500, "precio_venta": 3500, "stock": 120, "stock_minimo": 30,
             "descripcion": "Fortalece el sistema inmunológico"},
            
            {"nombre": "Complejo B", "generico": "Vitaminas B1, B6, B12", "presentacion": "Tabletas", "concentracion": "50mg",
             "categoria": "Vitaminas y Suplementos", "precio_compra": 1200, "precio_venta": 2800, "stock": 90, "stock_minimo": 20,
             "descripcion": "Para el sistema nervioso y energía"},
            
            {"nombre": "Calcio + Vitamina D", "generico": "Carbonato de Calcio", "presentacion": "Tabletas", "concentracion": "500mg",
             "categoria": "Vitaminas y Suplementos", "precio_compra": 1800, "precio_venta": 4000, "stock": 70, "stock_minimo": 15,
             "descripcion": "Para la salud ósea"},
            
            # Dermatológicos
            {"nombre": "Clotrimazol Crema", "generico": "Clotrimazol", "presentacion": "Crema tópica", "concentracion": "1%",
             "categoria": "Dermatológicos", "precio_compra": 2000, "precio_venta": 4500, "stock": 40, "stock_minimo": 10,
             "descripcion": "Antifúngico para infecciones de la piel"},
            
            {"nombre": "Hidrocortisona Crema", "generico": "Hidrocortisona", "presentacion": "Crema tópica", "concentracion": "1%",
             "categoria": "Dermatológicos", "precio_compra": 1800, "precio_venta": 4000, "stock": 35, "stock_minimo": 8,
             "descripcion": "Para alergias e inflamaciones de la piel"},
            
            # Oftalmológicos
            {"nombre": "Lágrimas Artificiales", "generico": "Carboximetilcelulosa", "presentacion": "Gotas", "concentracion": "0.5%",
             "categoria": "Oftalmológicos", "precio_compra": 2500, "precio_venta": 5500, "stock": 30, "stock_minimo": 10,
             "descripcion": "Para aliviar la sequedad ocular"},
            
            # Respiratorios
            {"nombre": "Salbutamol Inhalador", "generico": "Salbutamol", "presentacion": "Inhalador", "concentracion": "100mcg/dosis",
             "categoria": "Respiratorios", "precio_compra": 5000, "precio_venta": 12000, "stock": 20, "stock_minimo": 5,
             "descripcion": "Para el asma y problemas respiratorios - Requiere receta", "requiere_receta": True},
            
            {"nombre": "Budesonida Inhalador", "generico": "Budesonida", "presentacion": "Inhalador", "concentracion": "200mcg/dosis",
             "categoria": "Respiratorios", "precio_compra": 8000, "precio_venta": 18000, "stock": 15, "stock_minimo": 3,
             "descripcion": "Corticoide inhalado para asma - Requiere receta", "requiere_receta": True},
        ]
        
        # Asignar laboratorios aleatoriamente
        medicamentos_creados = 0
        for med_data in medicamentos_data:
            # Buscar categoría
            categoria = next((c for c in categorias_creadas if c.nombre == med_data["categoria"]), None)
            if not categoria:
                print(f"  ⚠️ Categoría {med_data['categoria']} no encontrada, saltando...")
                continue
            
            # Seleccionar laboratorio aleatorio
            laboratorio = random.choice(laboratorios_creados)
            
            # Verificar si ya existe
            existe = Medicamento.query.filter_by(nombre=med_data["nombre"]).first()
            if not existe:
                # Crear medicamento
                medicamento = Medicamento(
                    nombre=med_data["nombre"],
                    nombre_generico=med_data.get("generico"),
                    presentacion=med_data.get("presentacion"),
                    concentracion=med_data.get("concentracion"),
                    descripcion=med_data.get("descripcion"),
                    categoria_id=categoria.id,
                    laboratorio_id=laboratorio.id,
                    precio_compra=med_data["precio_compra"],
                    precio_venta=med_data["precio_venta"],
                    stock=med_data["stock"],
                    stock_minimo=med_data.get("stock_minimo", 10),
                    requiere_receta=med_data.get("requiere_receta", False),
                    activo=True
                )
                
                # Agregar fechas de vencimiento aleatorias (entre 3 meses y 2 años)
                dias_vencimiento = random.randint(90, 730)
                medicamento.fecha_vencimiento = date.today() + timedelta(days=dias_vencimiento)
                
                db.session.add(medicamento)
                medicamentos_creados += 1
                print(f"  ✅ Creado: {med_data['nombre']} - Cat: {categoria.nombre} - Lab: {laboratorio.nombre}")
            else:
                print(f"  ⏩ Ya existe: {med_data['nombre']}")
        
        db.session.commit()
        print(f"\n✅ {medicamentos_creados} medicamentos creados exitosamente")
        
        # ============================================
        # 4. MOSTRAR RESUMEN
        # ============================================
        print("\n" + "="*50)
        print("📊 RESUMEN FINAL")
        print("="*50)
        
        total_categorias = Categoria.query.count()
        total_laboratorios = Laboratorio.query.count()
        total_medicamentos = Medicamento.query.count()
        
        print(f"📦 Categorías: {total_categorias}")
        print(f"🏭 Laboratorios: {total_laboratorios}")
        print(f"💊 Medicamentos: {total_medicamentos}")
        
        # Mostrar algunos ejemplos
        print("\n🔍 Ejemplos de medicamentos creados:")
        medicamentos_ejemplo = Medicamento.query.limit(5).all()
        for m in medicamentos_ejemplo:
            print(f"   - {m.nombre} | Cat: {m.categoria.nombre if m.categoria else 'N/A'} | Lab: {m.laboratorio.nombre if m.laboratorio else 'N/A'} | Stock: {m.stock} | Precio: ${m.precio_venta}")
        
        print("\n🎉 ¡DATOS DE PRUEBA CREADOS EXITOSAMENTE!")

if __name__ == "__main__":
    crear_datos_prueba()