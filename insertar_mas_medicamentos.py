from app import create_app, db
from app.models import Categoria, Laboratorio, Medicamento
from datetime import date, timedelta
import random

app = create_app()

def crear_medicamentos_masivos():
    with app.app_context():
        print("="*60)
        print("🌱 CREANDO MÁS DE 100 MEDICAMENTOS PARA PRUEBAS")
        print("="*60)
        
        # ============================================
        # 1. CATEGORÍAS DETALLADAS
        # ============================================
        print("\n📦 Creando categorías detalladas...")
        categorias = [
            # Dolor e Inflamación
            {"nombre": "Analgésicos", "descripcion": "Medicamentos para aliviar el dolor"},
            {"nombre": "Antiinflamatorios", "descripcion": "Reducen la inflamación"},
            {"nombre": "Relajantes Musculares", "descripcion": "Para contracturas y dolores musculares"},
            {"nombre": "Antimigrañosos", "descripcion": "Específicos para migraña"},
            
            # Infecciones
            {"nombre": "Antibióticos", "descripcion": "Combaten infecciones bacterianas"},
            {"nombre": "Antifúngicos", "descripcion": "Para infecciones por hongos"},
            {"nombre": "Antivirales", "descripcion": "Para infecciones virales"},
            {"nombre": "Antiparasitarios", "descripcion": "Para parásitos intestinales"},
            
            # Respiratorio
            {"nombre": "Antigripales", "descripcion": "Alivian síntomas de gripe y resfriado"},
            {"nombre": "Antitusivos", "descripcion": "Para la tos"},
            {"nombre": "Expectorantes", "descripcion": "Ayudan a expulsar flemas"},
            {"nombre": "Broncodilatadores", "descripcion": "Para el asma y problemas respiratorios"},
            
            # Alergias
            {"nombre": "Antihistamínicos", "descripcion": "Para alergias"},
            {"nombre": "Corticoides", "descripcion": "Antiinflamatorios potentes"},
            
            # Sistema Digestivo
            {"nombre": "Antiácidos", "descripcion": "Para la acidez estomacal"},
            {"nombre": "Antiespasmódicos", "descripcion": "Para cólicos y espasmos"},
            {"nombre": "Antidiarreicos", "descripcion": "Para la diarrea"},
            {"nombre": "Laxantes", "descripcion": "Para el estreñimiento"},
            {"nombre": "Protectores Gástricos", "descripcion": "Protegen la mucosa del estómago"},
            {"nombre": "Antieméticos", "descripcion": "Para las náuseas y vómitos"},
            
            # Cardiovascular
            {"nombre": "Antihipertensivos", "descripcion": "Para la presión arterial alta"},
            {"nombre": "Diuréticos", "descripcion": "Eliminan líquidos"},
            {"nombre": "Antiarritmicos", "descripcion": "Regulan el ritmo cardíaco"},
            {"nombre": "Anticoagulantes", "descripcion": "Previenen coágulos"},
            {"nombre": "Hipolipemiantes", "descripcion": "Reducen el colesterol"},
            
            # Sistema Nervioso
            {"nombre": "Antidepresivos", "descripcion": "Para la depresión"},
            {"nombre": "Ansiolíticos", "descripcion": "Para la ansiedad"},
            {"nombre": "Antipsicóticos", "descripcion": "Para trastornos psiquiátricos"},
            {"nombre": "Antiepilépticos", "descripcion": "Para la epilepsia"},
            {"nombre": "Hipnóticos", "descripcion": "Para el insomnio"},
            
            # Vitaminas y Suplementos
            {"nombre": "Vitaminas", "descripcion": "Suplementos vitamínicos"},
            {"nombre": "Minerales", "descripcion": "Suplementos minerales"},
            {"nombre": "Aminoácidos", "descripcion": "Suplementos de aminoácidos"},
            
            # Dermatología
            {"nombre": "Antibióticos Tópicos", "descripcion": "Para infecciones de la piel"},
            {"nombre": "Antifúngicos Tópicos", "descripcion": "Para hongos en la piel"},
            {"nombre": "Corticoides Tópicos", "descripcion": "Para inflamaciones de la piel"},
            {"nombre": "Cicatrizantes", "descripcion": "Ayudan a cicatrizar heridas"},
            {"nombre": "Antiacné", "descripcion": "Para el acné"},
            
            # Oftalmología
            {"nombre": "Antibióticos Oftálmicos", "descripcion": "Para infecciones oculares"},
            {"nombre": "Lubricantes Oculares", "descripcion": "Para ojos secos"},
            {"nombre": "Antialérgicos Oftálmicos", "descripcion": "Para alergias en los ojos"},
            
            # Otorrinolaringología
            {"nombre": "Descongestionantes", "descripcion": "Para la congestión nasal"},
            {"nombre": "Antisépticos Bucales", "descripcion": "Para infecciones de garganta"},
            
            # Ginecología
            {"nombre": "Anticonceptivos", "descripcion": "Para el control de la natalidad"},
            {"nombre": "Antimicóticos Vaginales", "descripcion": "Para infecciones vaginales"},
            
            # Pediatría
            {"nombre": "Pediatría", "descripcion": "Medicamentos para niños"},
            
            # Geriatría
            {"nombre": "Geriatría", "descripcion": "Medicamentos para adultos mayores"},
        ]
        
        categorias_dict = {}
        for cat_data in categorias:
            cat = Categoria.query.filter_by(nombre=cat_data["nombre"]).first()
            if not cat:
                cat = Categoria(**cat_data)
                db.session.add(cat)
                print(f"  ✅ Creada: {cat_data['nombre']}")
            else:
                print(f"  ⏩ Ya existe: {cat_data['nombre']}")
            categorias_dict[cat_data["nombre"]] = cat
        
        db.session.commit()
        print(f"✅ {len(categorias)} categorías procesadas")

        # ============================================
        # 2. LABORATORIOS
        # ============================================
        print("\n🏭 Creando laboratorios...")
        laboratorios = [
            {"nombre": "Genfar", "pais": "Colombia"},
            {"nombre": "La Sante", "pais": "Colombia"},
            {"nombre": "MK", "pais": "Colombia"},
            {"nombre": "Bayer", "pais": "Alemania"},
            {"nombre": "Pfizer", "pais": "USA"},
            {"nombre": "Novartis", "pais": "Suiza"},
            {"nombre": "Roche", "pais": "Suiza"},
            {"nombre": "Abbott", "pais": "USA"},
            {"nombre": "Sanofi", "pais": "Francia"},
            {"nombre": "GSK", "pais": "Reino Unido"},
            {"nombre": "Merck", "pais": "USA"},
            {"nombre": "Johnson & Johnson", "pais": "USA"},
            {"nombre": "AstraZeneca", "pais": "Reino Unido"},
            {"nombre": "Eli Lilly", "pais": "USA"},
            {"nombre": "Bristol Myers", "pais": "USA"},
            {"nombre": "Tecnoquímicas", "pais": "Colombia"},
            {"nombre": "Procaps", "pais": "Colombia"},
            {"nombre": "Bussié", "pais": "Colombia"},
            {"nombre": "Cophar", "pais": "Colombia"},
            {"nombre": "Chalver", "pais": "Colombia"},
        ]
        
        laboratorios_lista = []
        for lab_data in laboratorios:
            lab = Laboratorio.query.filter_by(nombre=lab_data["nombre"]).first()
            if not lab:
                lab = Laboratorio(
                    nombre=lab_data["nombre"],
                    direccion=f"Planta principal en {lab_data['pais']}",
                    telefono=f"{random.randint(1000000, 9999999)}",
                    email=f"contacto@{lab_data['nombre'].lower().replace(' ', '')}.com",
                    contacto=f"Representante en {lab_data['pais']}"
                )
                db.session.add(lab)
                print(f"  ✅ Creado: {lab_data['nombre']}")
            else:
                print(f"  ⏩ Ya existe: {lab_data['nombre']}")
            laboratorios_lista.append(lab)
        
        db.session.commit()
        print(f"✅ {len(laboratorios)} laboratorios procesados")

        # ============================================
        # 3. MEDICAMENTOS MASIVOS POR SÍNTOMAS
        # ============================================
        print("\n💊 Creando más de 100 medicamentos...")
        
        # Base de datos de medicamentos por síntoma
        medicamentos_por_sintoma = {
            # DOLOR DE CABEZA
            "dolor de cabeza": [
                {"nombre": "Acetaminofén 500mg", "generico": "Paracetamol", "precio_compra": 500, "precio_venta": 1200, "stock": 200},
                {"nombre": "Ibuprofeno 400mg", "generico": "Ibuprofeno", "precio_compra": 800, "precio_venta": 1800, "stock": 150},
                {"nombre": "Naproxeno 250mg", "generico": "Naproxeno", "precio_compra": 900, "precio_venta": 2200, "stock": 80},
                {"nombre": "Diclofenaco 50mg", "generico": "Diclofenaco", "precio_compra": 600, "precio_venta": 1500, "stock": 120},
                {"nombre": "Ketorolaco 10mg", "generico": "Ketorolaco", "precio_compra": 700, "precio_venta": 1800, "stock": 60},
                {"nombre": "Metamizol 500mg", "generico": "Dipirona", "precio_compra": 550, "precio_venta": 1300, "stock": 90},
            ],
            
            # MIGRAÑA
            "migraña": [
                {"nombre": "Sumatriptán 50mg", "generico": "Sumatriptán", "precio_compra": 5000, "precio_venta": 12000, "stock": 30, "receta": True},
                {"nombre": "Rizatriptán 10mg", "generico": "Rizatriptán", "precio_compra": 6000, "precio_venta": 15000, "stock": 25, "receta": True},
                {"nombre": "Ergotamina 1mg", "generico": "Ergotamina", "precio_compra": 4000, "precio_venta": 9500, "stock": 20, "receta": True},
            ],
            
            # FIEBRE
            "fiebre": [
                {"nombre": "Acetaminofén 500mg Infantil", "generico": "Paracetamol", "precio_compra": 400, "precio_venta": 1000, "stock": 180},
                {"nombre": "Ibuprofeno Infantil", "generico": "Ibuprofeno", "precio_compra": 600, "precio_venta": 1500, "stock": 120},
                {"nombre": "Acetaminofén 650mg", "generico": "Paracetamol", "precio_compra": 550, "precio_venta": 1400, "stock": 200},
                {"nombre": "Ácido Acetilsalicílico 500mg", "generico": "Aspirina", "precio_compra": 450, "precio_venta": 1100, "stock": 150},
            ],
            
            # GRIPE Y RESFRIADO
            "gripe": [
                {"nombre": "Dolex Gripa", "generico": "Paracetamol + Fenilefrina", "precio_compra": 2000, "precio_venta": 4500, "stock": 90},
                {"nombre": "Actron Gripa", "generico": "Ibuprofeno + Fenilefrina", "precio_compra": 2500, "precio_venta": 5500, "stock": 70},
                {"nombre": "Tapsin", "generico": "Paracetamol + Clorfenamina", "precio_compra": 1800, "precio_venta": 4000, "stock": 85},
                {"nombre": "Vick Day", "generico": "Multisíntomas", "precio_compra": 2200, "precio_venta": 5000, "stock": 60},
                {"nombre": "Vick Night", "generico": "Multisíntomas + Antihistamínico", "precio_compra": 2400, "precio_venta": 5300, "stock": 55},
                {"nombre": "Theraflu", "generico": "Multisíntomas", "precio_compra": 3000, "precio_venta": 6800, "stock": 40},
            ],
            
            # TOS
            "tos": [
                {"nombre": "Dextrometorfano Jarabe", "generico": "Dextrometorfano", "precio_compra": 1800, "precio_venta": 4000, "stock": 60},
                {"nombre": "Bromhexina Jarabe", "generico": "Bromhexina", "precio_compra": 1500, "precio_venta": 3500, "stock": 70},
                {"nombre": "Ambroxol Jarabe", "generico": "Ambroxol", "precio_compra": 1600, "precio_venta": 3800, "stock": 65},
                {"nombre": "Acetilcisteína", "generico": "Acetilcisteína", "precio_compra": 2000, "precio_venta": 4500, "stock": 50},
                {"nombre": "Codeína Jarabe", "generico": "Codeína", "precio_compra": 3000, "precio_venta": 7000, "stock": 30, "receta": True},
                {"nombre": "Levodropropizina", "generico": "Levodropropizina", "precio_compra": 2500, "precio_venta": 5800, "stock": 40},
            ],
            
            # ALERGIAS
            "alergia": [
                {"nombre": "Loratadina 10mg", "generico": "Loratadina", "precio_compra": 400, "precio_venta": 1000, "stock": 200},
                {"nombre": "Cetirizina 10mg", "generico": "Cetirizina", "precio_compra": 450, "precio_venta": 1100, "stock": 180},
                {"nombre": "Desloratadina 5mg", "generico": "Desloratadina", "precio_compra": 800, "precio_venta": 2000, "stock": 120},
                {"nombre": "Fexofenadina 120mg", "generico": "Fexofenadina", "precio_compra": 1000, "precio_venta": 2500, "stock": 90},
                {"nombre": "Levocetirizina 5mg", "generico": "Levocetirizina", "precio_compra": 900, "precio_venta": 2200, "stock": 85},
                {"nombre": "Ebastina 10mg", "generico": "Ebastina", "precio_compra": 700, "precio_venta": 1800, "stock": 95},
            ],
            
            # DOLOR MUSCULAR
            "dolor muscular": [
                {"nombre": "Diclofenaco Gel", "generico": "Diclofenaco", "precio_compra": 1500, "precio_venta": 3500, "stock": 70},
                {"nombre": "Ketoprofeno Gel", "generico": "Ketoprofeno", "precio_compra": 1800, "precio_venta": 4000, "stock": 60},
                {"nombre": "Metocarbamol 500mg", "generico": "Metocarbamol", "precio_compra": 1200, "precio_venta": 2800, "stock": 80},
                {"nombre": "Ciclobenzaprina 10mg", "generico": "Ciclobenzaprina", "precio_compra": 1100, "precio_venta": 2600, "stock": 75},
                {"nombre": "Parche de Lidocaína", "generico": "Lidocaína", "precio_compra": 2500, "precio_venta": 6000, "stock": 40},
                {"nombre": "Crema Calmante", "generico": "Mentol + Alcanfor", "precio_compra": 1200, "precio_venta": 3000, "stock": 90},
            ],
            
            # DOLOR DE ESTÓMAGO
            "dolor de estómago": [
                {"nombre": "Omeprazol 20mg", "generico": "Omeprazol", "precio_compra": 600, "precio_venta": 1500, "stock": 150},
                {"nombre": "Pantoprazol 40mg", "generico": "Pantoprazol", "precio_compra": 900, "precio_venta": 2200, "stock": 120},
                {"nombre": "Esomeprazol 40mg", "generico": "Esomeprazol", "precio_compra": 1000, "precio_venta": 2500, "stock": 100},
                {"nombre": "Ranitidina 150mg", "generico": "Ranitidina", "precio_compra": 500, "precio_venta": 1300, "stock": 140},
                {"nombre": "Famotidina 40mg", "generico": "Famotidina", "precio_compra": 550, "precio_venta": 1400, "stock": 130},
                {"nombre": "Antiácido Masticable", "generico": "Hidróxido de Aluminio/Magnesio", "precio_compra": 400, "precio_venta": 1000, "stock": 200},
            ],
            
            # ACIDEZ
            "acidez": [
                {"nombre": "Alka-Seltzer", "generico": "Bicarbonato + Ácido Cítrico", "precio_compra": 2000, "precio_venta": 4500, "stock": 60},
                {"nombre": "Mylanta", "generico": "Hidróxidos", "precio_compra": 1800, "precio_venta": 4000, "stock": 55},
                {"nombre": "Rennie", "generico": "Carbonato de Calcio", "precio_compra": 1500, "precio_venta": 3500, "stock": 70},
            ],
            
            # DIARREA
            "diarrea": [
                {"nombre": "Loperamida 2mg", "generico": "Loperamida", "precio_compra": 300, "precio_venta": 800, "stock": 120},
                {"nombre": "Racecadotrilo", "generico": "Racecadotrilo", "precio_compra": 800, "precio_venta": 2000, "stock": 80},
                {"nombre": "Solución de Rehidratación", "generico": "Sales de rehidratación", "precio_compra": 200, "precio_venta": 500, "stock": 300},
                {"nombre": "Probioticos", "generico": "Lactobacillus", "precio_compra": 1500, "precio_venta": 3500, "stock": 90},
            ],
            
            # ESTREÑIMIENTO
            "estreñimiento": [
                {"nombre": "Lactulosa", "generico": "Lactulosa", "precio_compra": 1000, "precio_venta": 2500, "stock": 70},
                {"nombre": "Bisacodilo 5mg", "generico": "Bisacodilo", "precio_compra": 400, "precio_venta": 1000, "stock": 100},
                {"nombre": "Senósidos", "generico": "Sen", "precio_compra": 350, "precio_venta": 900, "stock": 120},
                {"nombre": "Polietilenglicol", "generico": "PEG", "precio_compra": 1200, "precio_venta": 3000, "stock": 60},
            ],
            
            # PRESIÓN ALTA
            "presión alta": [
                {"nombre": "Losartán 50mg", "generico": "Losartán", "precio_compra": 900, "precio_venta": 2200, "stock": 85, "receta": True},
                {"nombre": "Enalapril 10mg", "generico": "Enalapril", "precio_compra": 700, "precio_venta": 1700, "stock": 95, "receta": True},
                {"nombre": "Valsartán 80mg", "generico": "Valsartán", "precio_compra": 1200, "precio_venta": 3000, "stock": 70, "receta": True},
                {"nombre": "Amlodipino 5mg", "generico": "Amlodipino", "precio_compra": 800, "precio_venta": 2000, "stock": 80, "receta": True},
                {"nombre": "Hidroclorotiazida 25mg", "generico": "Hidroclorotiazida", "precio_compra": 500, "precio_venta": 1300, "stock": 100, "receta": True},
            ],
            
            # COLESTEROL
            "colesterol": [
                {"nombre": "Atorvastatina 20mg", "generico": "Atorvastatina", "precio_compra": 1500, "precio_venta": 3500, "stock": 75, "receta": True},
                {"nombre": "Simvastatina 20mg", "generico": "Simvastatina", "precio_compra": 1200, "precio_venta": 2800, "stock": 80, "receta": True},
                {"nombre": "Rosuvastatina 10mg", "generico": "Rosuvastatina", "precio_compra": 2000, "precio_venta": 4800, "stock": 60, "receta": True},
                {"nombre": "Ezetimiba 10mg", "generico": "Ezetimiba", "precio_compra": 1800, "precio_venta": 4200, "stock": 50, "receta": True},
            ],
            
            # ANSIEDAD
            "ansiedad": [
                {"nombre": "Alprazolam 0.5mg", "generico": "Alprazolam", "precio_compra": 600, "precio_venta": 1500, "stock": 60, "receta": True},
                {"nombre": "Clonazepam 0.5mg", "generico": "Clonazepam", "precio_compra": 700, "precio_venta": 1800, "stock": 55, "receta": True},
                {"nombre": "Diazepam 5mg", "generico": "Diazepam", "precio_compra": 500, "precio_venta": 1300, "stock": 70, "receta": True},
                {"nombre": "Fluoxetina 20mg", "generico": "Fluoxetina", "precio_compra": 800, "precio_venta": 2000, "stock": 90, "receta": True},
                {"nombre": "Sertralina 50mg", "generico": "Sertralina", "precio_compra": 900, "precio_venta": 2200, "stock": 85, "receta": True},
            ],
            
            # INSOMNIO
            "insomnio": [
                {"nombre": "Melatonina 3mg", "generico": "Melatonina", "precio_compra": 500, "precio_venta": 1300, "stock": 120},
                {"nombre": "Zolpidem 10mg", "generico": "Zolpidem", "precio_compra": 1000, "precio_venta": 2500, "stock": 50, "receta": True},
                {"nombre": "Doxilamina", "generico": "Doxilamina", "precio_compra": 800, "precio_venta": 2000, "stock": 60},
                {"nombre": "Valeriana", "generico": "Extracto de Valeriana", "precio_compra": 700, "precio_venta": 1800, "stock": 80},
            ],
            
            # DEPRESIÓN
            "depresión": [
                {"nombre": "Escitalopram 10mg", "generico": "Escitalopram", "precio_compra": 1200, "precio_venta": 3000, "stock": 70, "receta": True},
                {"nombre": "Paroxetina 20mg", "generico": "Paroxetina", "precio_compra": 1100, "precio_venta": 2700, "stock": 65, "receta": True},
                {"nombre": "Venlafaxina 75mg", "generico": "Venlafaxina", "precio_compra": 1500, "precio_venta": 3600, "stock": 55, "receta": True},
                {"nombre": "Mirtazapina 30mg", "generico": "Mirtazapina", "precio_compra": 1300, "precio_venta": 3200, "stock": 50, "receta": True},
            ],
            
            # ANTIBIÓTICOS (Infecciones)
            "infección bacteriana": [
                {"nombre": "Amoxicilina 500mg", "generico": "Amoxicilina", "precio_compra": 1500, "precio_venta": 3500, "stock": 60, "receta": True},
                {"nombre": "Azitromicina 500mg", "generico": "Azitromicina", "precio_compra": 3000, "precio_venta": 6800, "stock": 45, "receta": True},
                {"nombre": "Ciprofloxacino 500mg", "generico": "Ciprofloxacino", "precio_compra": 2200, "precio_venta": 5000, "stock": 35, "receta": True},
                {"nombre": "Cefalexina 500mg", "generico": "Cefalexina", "precio_compra": 1800, "precio_venta": 4200, "stock": 40, "receta": True},
                {"nombre": "Trimetoprim 160mg", "generico": "Trimetoprim + Sulfa", "precio_compra": 1200, "precio_venta": 2800, "stock": 50, "receta": True},
                {"nombre": "Nitrofurantoína 100mg", "generico": "Nitrofurantoína", "precio_compra": 2000, "precio_venta": 4800, "stock": 30, "receta": True},
                {"nombre": "Metronidazol 500mg", "generico": "Metronidazol", "precio_compra": 1000, "precio_venta": 2400, "stock": 80, "receta": True},
                {"nombre": "Claritromicina 500mg", "generico": "Claritromicina", "precio_compra": 3500, "precio_venta": 8000, "stock": 25, "receta": True},
            ],
            
            # ANTIFÚNGICOS
            "hongos": [
                {"nombre": "Fluconazol 150mg", "generico": "Fluconazol", "precio_compra": 2000, "precio_venta": 4800, "stock": 50, "receta": True},
                {"nombre": "Ketoconazol Crema", "generico": "Ketoconazol", "precio_compra": 1500, "precio_venta": 3500, "stock": 60},
                {"nombre": "Clotrimazol Crema", "generico": "Clotrimazol", "precio_compra": 1200, "precio_venta": 2800, "stock": 70},
                {"nombre": "Miconazol Crema", "generico": "Miconazol", "precio_compra": 1300, "precio_venta": 3000, "stock": 65},
                {"nombre": "Terbinafina Crema", "generico": "Terbinafina", "precio_compra": 1800, "precio_venta": 4200, "stock": 55},
            ],
            
            # PIEL (Dermatología)
            "problemas de piel": [
                {"nombre": "Hidrocortisona Crema", "generico": "Hidrocortisona", "precio_compra": 1800, "precio_venta": 4000, "stock": 35},
                {"nombre": "Betametasona Crema", "generico": "Betametasona", "precio_compra": 2000, "precio_venta": 4800, "stock": 30, "receta": True},
                {"nombre": "Mupirocina Crema", "generico": "Mupirocina", "precio_compra": 2500, "precio_venta": 6000, "stock": 25, "receta": True},
                {"nombre": "Ácido Fusídico Crema", "generico": "Ácido Fusídico", "precio_compra": 2200, "precio_venta": 5200, "stock": 28, "receta": True},
                {"nombre": "Peróxido de Benzoilo", "generico": "Peróxido de Benzoilo", "precio_compra": 1500, "precio_venta": 3500, "stock": 40},
                {"nombre": "Tretinoína Crema", "generico": "Tretinoína", "precio_compra": 3000, "precio_venta": 7200, "stock": 20, "receta": True},
                {"nombre": "Urea 40% Crema", "generico": "Urea", "precio_compra": 2800, "precio_venta": 6500, "stock": 25},
            ],
            
            # OJOS
            "ojos irritados": [
                {"nombre": "Lágrimas Artificiales", "generico": "Carboximetilcelulosa", "precio_compra": 2500, "precio_venta": 5500, "stock": 30},
                {"nombre": "Solución Salina", "generico": "Cloruro de Sodio", "precio_compra": 800, "precio_venta": 2000, "stock": 50},
                {"nombre": "Lágrimas con Ácido Hialurónico", "generico": "Ácido Hialurónico", "precio_compra": 4000, "precio_venta": 9000, "stock": 20},
                {"nombre": "Antibiótico Oftálmico", "generico": "Tobramicina", "precio_compra": 3000, "precio_venta": 7000, "stock": 25, "receta": True},
                {"nombre": "Antialérgico Oftálmico", "generico": "Ketotifeno", "precio_compra": 3500, "precio_venta": 8000, "stock": 22},
            ],
            
            # VITAMINAS
            "vitaminas": [
                {"nombre": "Vitamina C 1000mg", "generico": "Ácido Ascórbico", "precio_compra": 1500, "precio_venta": 3500, "stock": 120},
                {"nombre": "Complejo B", "generico": "Vitaminas B1, B6, B12", "precio_compra": 1200, "precio_venta": 2800, "stock": 90},
                {"nombre": "Calcio + Vitamina D", "generico": "Carbonato de Calcio", "precio_compra": 1800, "precio_venta": 4000, "stock": 70},
                {"nombre": "Magnesio", "generico": "Citrato de Magnesio", "precio_compra": 1400, "precio_venta": 3200, "stock": 80},
                {"nombre": "Zinc", "generico": "Gluconato de Zinc", "precio_compra": 1000, "precio_venta": 2400, "stock": 100},
                {"nombre": "Vitamina D3 2000UI", "generico": "Colecalciferol", "precio_compra": 2000, "precio_venta": 4800, "stock": 60},
                {"nombre": "Vitamina E 400UI", "generico": "Tocoferol", "precio_compra": 1600, "precio_venta": 3800, "stock": 55},
                {"nombre": "Multivitamínico", "generico": "Complejo multivitamínico", "precio_compra": 2500, "precio_venta": 6000, "stock": 85},
            ],
            
            # DEPORTISTAS
            "deportistas": [
                {"nombre": "Proteína Whey", "generico": "Suero de leche", "precio_compra": 30000, "precio_venta": 65000, "stock": 15},
                {"nombre": "Creatina", "generico": "Monohidrato de Creatina", "precio_compra": 25000, "precio_venta": 55000, "stock": 12},
                {"nombre": "BCAA", "generico": "Aminoácidos ramificados", "precio_compra": 28000, "precio_venta": 60000, "stock": 10},
                {"nombre": "Glutamina", "generico": "L-Glutamina", "precio_compra": 20000, "precio_venta": 45000, "stock": 14},
            ],
        }
        
        # Crear medicamentos
        medicamentos_creados = 0
        total_medicamentos = 0
        
        for sintoma, medicamentos_list in medicamentos_por_sintoma.items():
            for med_data in medicamentos_list:
                total_medicamentos += 1
                
                # Determinar categoría según el síntoma
                categoria = None
                if sintoma in ["dolor de cabeza", "migraña"]:
                    categoria = categorias_dict.get("Analgésicos")
                elif sintoma == "fiebre":
                    categoria = categorias_dict.get("Antigripales")
                elif sintoma in ["gripe", "tos"]:
                    categoria = categorias_dict.get("Antitusivos")
                elif sintoma == "alergia":
                    categoria = categorias_dict.get("Antihistamínicos")
                elif sintoma == "dolor muscular":
                    categoria = categorias_dict.get("Relajantes Musculares")
                elif sintoma in ["dolor de estómago", "acidez"]:
                    categoria = categorias_dict.get("Antiácidos")
                elif sintoma == "diarrea":
                    categoria = categorias_dict.get("Antidiarreicos")
                elif sintoma == "estreñimiento":
                    categoria = categorias_dict.get("Laxantes")
                elif sintoma == "presión alta":
                    categoria = categorias_dict.get("Antihipertensivos")
                elif sintoma == "colesterol":
                    categoria = categorias_dict.get("Hipolipemiantes")
                elif sintoma in ["ansiedad", "insomnio", "depresión"]:
                    categoria = categorias_dict.get("Ansiolíticos")
                elif sintoma == "infección bacteriana":
                    categoria = categorias_dict.get("Antibióticos")
                elif sintoma == "hongos":
                    categoria = categorias_dict.get("Antifúngicos")
                elif sintoma == "problemas de piel":
                    categoria = categorias_dict.get("Dermatológicos")
                elif sintoma == "ojos irritados":
                    categoria = categorias_dict.get("Oftalmológicos")
                elif sintoma == "vitaminas":
                    categoria = categorias_dict.get("Vitaminas")
                else:
                    categoria = categorias_dict.get("Analgésicos")  # Por defecto
                
                if not categoria:
                    # Buscar cualquier categoría
                    categoria = Categoria.query.first()
                
                # Seleccionar laboratorio aleatorio
                laboratorio = random.choice(laboratorios_lista)
                
                # Verificar si ya existe
                existe = Medicamento.query.filter_by(nombre=med_data["nombre"]).first()
                if not existe:
                    # Crear medicamento
                    presentaciones = ["Tabletas", "Cápsulas", "Jarabe", "Crema", "Inyectable", "Gotas", "Inhalador", "Solución"]
                    medicamento = Medicamento(
                        nombre=med_data["nombre"],
                        nombre_generico=med_data.get("generico", ""),
                        presentacion=random.choice(presentaciones),
                        concentracion=med_data.get("precio_venta", ""),
                        descripcion=f"Para {sintoma}. {med_data['generico'] if 'generico' in med_data else ''}",
                        categoria_id=categoria.id,
                        laboratorio_id=laboratorio.id,
                        precio_compra=med_data["precio_compra"],
                        precio_venta=med_data["precio_venta"],
                        stock=med_data["stock"],
                        stock_minimo=random.randint(5, 20),
                        requiere_receta=med_data.get("receta", False),
                        activo=True
                    )
                    
                    # Agregar fechas de vencimiento aleatorias
                    dias_vencimiento = random.randint(90, 730)
                    medicamento.fecha_vencimiento = date.today() + timedelta(days=dias_vencimiento)
                    
                    db.session.add(medicamento)
                    medicamentos_creados += 1
                    
                    if medicamentos_creados % 20 == 0:
                        db.session.commit()
                        print(f"  ✅ {medicamentos_creados} medicamentos creados...")
        
        db.session.commit()
        
        # ============================================
        # 4. MOSTRAR RESUMEN
        # ============================================
        print("\n" + "="*60)
        print("📊 RESUMEN FINAL")
        print("="*60)
        
        total_categorias = Categoria.query.count()
        total_laboratorios = Laboratorio.query.count()
        total_medicamentos = Medicamento.query.count()
        
        print(f"📦 Categorías: {total_categorias}")
        print(f"🏭 Laboratorios: {total_laboratorios}")
        print(f"💊 Medicamentos: {total_medicamentos}")
        print(f"✨ Medicamentos nuevos creados: {medicamentos_creados}")
        
        # Mostrar estadísticas por categoría
        print("\n🔍 MEDICAMENTOS POR CATEGORÍA:")
        categorias_conteo = db.session.query(
            Categoria.nombre, 
            db.func.count(Medicamento.id)
        ).join(Medicamento).group_by(Categoria.id).order_by(db.func.count(Medicamento.id).desc()).all()
        
        for cat, count in categorias_conteo[:10]:  # Top 10
            print(f"   • {cat}: {count} medicamentos")
        
        # Mostrar algunos ejemplos aleatorios
        print("\n🎲 EJEMPLOS ALEATORIOS DE MEDICAMENTOS:")
        medicamentos_ejemplo = Medicamento.query.order_by(db.func.random()).limit(10).all()
        for m in medicamentos_ejemplo:
            receta = "🔴 REQUIERE RECETA" if m.requiere_receta else "🟢 Venta libre"
            print(f"   • {m.nombre} - ${m.precio_venta:,.0f} | Stock: {m.stock} | {receta}")
        
        print("\n" + "="*60)
        print("🎉 ¡BASE DE DATOS POBLADA CON MÁS DE 100 MEDICAMENTOS!")
        print("="*60)

if __name__ == "__main__":
    crear_medicamentos_masivos()
