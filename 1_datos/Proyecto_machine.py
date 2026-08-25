import os
import numpy as np
import pandas as pd

# ==========================================
# PASO 1: CARGAR EL ARCHIVO EXCEL (.xlsx)
# ==========================================
directorio_actual = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
archivos_entrada = [
    os.path.join(directorio_actual, "Base_de_datos.xlsx"),
    os.path.join(directorio_actual, "Base de datos.xlsx"),
]
ruta_entrada = next((ruta for ruta in archivos_entrada if os.path.exists(ruta)), None)

if ruta_entrada is None:
    raise FileNotFoundError("No se encontró el archivo Excel de datos (.xlsx).")

# Cargar la primera hoja del archivo Excel.
xls = pd.ExcelFile(ruta_entrada)
nombre_hoja = xls.sheet_names[0]
df = pd.read_excel(xls, sheet_name=nombre_hoja)

print("--- ARCHIVO EXCEL CARGADO EXITOSAMENTE ---")
print(f"Hoja procesada: '{nombre_hoja}'")
print(f"Dimensiones iniciales: {df.shape[0]} filas y {df.shape[1]} columnas\n")


# ==========================================
# PASO 2: TRADUCIR ENCABEZADOS Y VALORES AL ESPAÑOL
# ==========================================

# 2.1 TRADUCCIÓN COMPLETA DE ENCABEZADOS
columnas_esp = {
    "order_id": "id_pedido",
    "customer_id": "id_cliente",
    "restaurant_id": "id_restaurante",
    "driver_id": "id_conductor",
    "order_timestamp": "timestamp_pedido",
    "order_date": "fecha_pedido",
    "day_of_week": "dia_semana",
    "hour_of_day": "hora_dia",
    "is_weekend": "es_fin_semana",
    "order_status": "estado_pedido",
    "cancellation_reason": "motivo_cancelacion",
    "payment_method": "metodo_pago",
    "delivery_zone": "zona_entrega",
    "distance_km": "distancia_km",
    "traffic_level": "nivel_trafico",
    "weather_condition": "condicion_clima",
    "vehicle_type": "tipo_vehiculo",
    "estimated_delivery_time_minutes": "tiempo_estimado_entrega_min",
    "actual_delivery_time_minutes": "tiempo_real_entrega_min",
    "late_delivery": "entrega_tardia",
    "restaurant_preparation_time_minutes": "tiempo_preparacion_restaurante_min",
    "subtotal": "subtotal",
    "delivery_fee": "costo_envio",
    "discount_amount": "monto_descuento",
    "tip_amount": "monto_propina",
    "taxes": "impuestos",
    "order_total": "total_pedido",
    "promo_code_used": "codigo_promo_usado",
    "items_count": "cantidad_items",
    "cuisine_type": "tipo_cocina",
    "customer_rating": "calificacion_cliente",
    "is_first_order": "es_primer_pedido",
    "is_prime_member": "es_miembro_prime",
    "delivery_attempts": "intentos_entrega",
    "app_version": "version_app",
    "device_os": "sistema_operativo_dispositivo",
    "support_ticket_created": "ticket_soporte_creado",
    "delivery_area": "area_entrega",
    "customer_age": "edad_cliente",
    "customer_type": "tipo_cliente",
    "restaurant_type": "tipo_restaurante",
    "restaurant_primary_category": "categoria_principal_restaurante",
    "restaurant_rating": "calificacion_restaurante",
    "discount_percent": "porcentaje_descuento",
    "tax_amount": "monto_impuesto",
    "service_fee": "tarifa_servicio",
    "weather": "condicion_clima",
    "delivery_partner_experience_months": "experiencia_repartidor_meses",
    "delivery_partner_rating": "calificacion_repartidor",
}

df.rename(columns=columnas_esp, inplace=True)

# 2.2 TRADUCCIÓN DEL CONTENIDO TEXTUAL DE LAS CELDAS
mapeos = {
    "dia_semana": {
        "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
        "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
    },
    "estado_pedido": {
        "Completed": "Completado", "Cancelled": "Cancelado", "Pending": "Pendiente"
    },
    "metodo_pago": {
        "Credit Card": "Tarjeta de Crédito", "Debit Card": "Tarjeta de Débito",
        "Cash": "Efectivo", "Digital Wallet": "Billetera Digital", "PayPal": "PayPal"
    },
    "zona_entrega": {
        "North": "Norte", "South": "Sur", "East": "Este", "West": "Oeste",
        "Central": "Centro", "Downtown": "Centro Urbano", "Suburbs": "Suburbios"
    },
    "area_entrega": {
        "North": "Norte", "South": "Sur", "East": "Este", "West": "Oeste",
        "Central": "Centro", "Downtown": "Centro Urbano", "Suburbs": "Suburbios",
        "Urban": "Urbano", "Suburban": "Suburbano", "Rural": "Rural"
    },
    "nivel_trafico": {
        "Low": "Bajo", "Medium": "Medio", "High": "Alto", "Jam": "Embotellamiento", "Heavy": "Pesado"
    },
    "condicion_clima": {
        "Clear": "Despejado", "Sunny": "Soleado", "Rain": "Lluvia", "Rainy": "Lluvioso",
        "Heavy Rain": "Lluvia Fuerte", "Stormy": "Tormentoso", "Cloudy": "Nublado", "Foggy": "Niebla",
        "Windy": "Ventoso", "Snow": "Nieve"
    },
    "tipo_vehiculo": {
        "Motorcycle": "Motocicleta", "Bicycle": "Bicicleta", "Car": "Automóvil",
        "Scooter": "Patineta Eléctrica", "Walking": "A Pie"
    },
    "tipo_cocina": {
        "Italian": "Italiana", "Burger": "Hamburguesas", "Burgers": "Hamburguesas",
        "Pizza": "Pizza", "Sushi": "Sushi", "Mexican": "Mexicana", "Chinese": "China",
        "Colombian": "Colombiana", "Fast Food": "Comida Rápida", "Bakery": "Repostería/Panadería",
        "Desserts": "Postres", "Healthy": "Saludable"
    },
    "categoria_principal_restaurante": {
        "Italian": "Italiana", "Burger": "Hamburguesas", "Burgers": "Hamburguesas",
        "Pizza": "Pizza", "Sushi": "Sushi", "Mexican": "Mexicana", "Chinese": "China",
        "Colombian": "Colombiana", "Fast Food": "Comida Rápida", "Bakery": "Repostería/Panadería",
        "Desserts": "Postres", "Healthy": "Saludable", "Asian": "Asiática", "American": "Americana"
    },
    "tipo_cliente": {
        "New": "Nuevo", "Returning": "Recurrente", "Regular": "Habitual",
        "VIP": "VIP", "Corporate": "Corporativo", "Prime": "Prime"
    },
    "tipo_restaurante": {
        "Fast Food": "Comida Rápida", "Casual Dining": "Restaurante Casual",
        "Fine Dining": "Alta Cocina", "Bakery": "Panadería/Pastelería",
        "Cafeteria": "Cafetería", "Cloud Kitchen": "Cocina Oculta"
    },
    "sistema_operativo_dispositivo": {
        "Android": "Android", "iOS": "iOS", "Web": "Web"
    }
}

for columna, diccionario in mapeos.items():
    if columna in df.columns:
        df[columna] = df[columna].replace(diccionario)

print("--- TRADUCCIÓN COMPLETA REALIZADA CON ÉXITO ---\n")


# ==========================================
# PASO 3: DIAGNÓSTICO INICIAL Y CONTEO
# ==========================================
print("==========================================")
print("          DIAGNÓSTICO INICIAL             ")
print("==========================================")

# 1. Duplicados
col_id = "id_pedido" if "id_pedido" in df.columns else df.columns[0]
duplicados_id = df.duplicated(subset=[col_id]).sum()
duplicados_filas = df.duplicated().sum()
print(f"Duplicados por '{col_id}': {duplicados_id}")
print(f"Filas completamente duplicadas: {duplicados_filas}\n")

# 2. Contar valores nulos por columna
print("--- VALORES NULOS Y REGISTROS POR COLUMNA ---")
resumen_celdas = pd.DataFrame({
    'Valores No Nulos': df.notnull().sum(),
    'Valores Nulos': df.isnull().sum(),
    'Tipo de Dato': df.dtypes
})
print(resumen_celdas, "\n")

# 3. Outliers con IQR
columnas_outliers = [
    "distancia_km",
    "tiempo_preparacion_restaurante_min",
    "tiempo_real_entrega_min",
    "subtotal",
    "monto_propina",
    "total_pedido",
    "costo_envio",
    "monto_impuesto",
    "tarifa_servicio",
    "porcentaje_descuento"
]

print("--- DETECCIÓN DE OUTLIERS (MÉTODO IQR) ---")
for col in columnas_outliers:
    if col in df.columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR

        outliers = df[(df[col] < limite_inferior) | (df[col] > limite_superior)]
        cant_outliers = len(outliers)
        pct_outliers = (cant_outliers / len(df)) * 100

        print(f"Columna '{col}': {cant_outliers} outliers detectados ({pct_outliers:.2f}%)")
        print(f"   Rango aceptado: [{limite_inferior:.2f}, {limite_superior:.2f}]\n")


# ==========================================
# PASO 4: TRATAMIENTO DE CALIDAD
# ==========================================
print("==========================================")
print("          TRATAMIENTO DE CALIDAD          ")
print("==========================================")

# 1. Filtrar únicamente pedidos completados
if "estado_pedido" in df.columns:
    df = df[df["estado_pedido"].isin(["Completado", "Completed"])].copy()
    print(f"Filtrado por pedidos completados realizado. Filas restantes: {len(df)}")

# 2. Convertir columnas de tiempo a tipo datetime
for col_fecha in ["timestamp_pedido", "fecha_pedido"]:
    if col_fecha in df.columns:
        df[col_fecha] = pd.to_datetime(df[col_fecha])
        print(f"Columna '{col_fecha}' convertida a formato datetime.")

# 3. Eliminar la columna 'motivo_cancelacion'
if "motivo_cancelacion" in df.columns:
    df.drop(columns=["motivo_cancelacion"], inplace=True)
    print("Columna 'motivo_cancelacion' eliminada exitosamente.")

# 4. Crear la columna 'minutos_retraso' si existen los tiempos
if "tiempo_real_entrega_min" in df.columns and "tiempo_estimado_entrega_min" in df.columns:
    df["minutos_retraso"] = df["tiempo_real_entrega_min"] - df["tiempo_estimado_entrega_min"]
    print("Nueva columna 'minutos_retraso' creada con éxito.\n")


# ==========================================
# PASO 5: ELIMINAR COLUMNAS NO USABLES PARA MODELAR (MATRIZ X)
# ==========================================
print("==========================================")
print("   PREPARACIÓN DE VARIABLES PREDICTORAS (X) ")
print("==========================================")

columnas_a_eliminar = [
    # Identificadores: solo identifican entidades y pueden hacer que el modelo memorice registros.
    "id_pedido", "id_cliente", "id_restaurante", "id_conductor",

    # Fecha/hora originales: no se usan directamente; ya existen variables temporales derivadas.
    "timestamp_pedido", "fecha_pedido",

    # Fuga de información: solo se conocen después de que la entrega termina.
    "tiempo_real_entrega_min", "entrega_tardia", "minutos_retraso",
    "estado_pedido", "monto_propina", "calificacion_cliente"
]

columnas_existentes_a_eliminar = [col for col in columnas_a_eliminar if col in df.columns]

df_limpio = df.drop(columns=columnas_existentes_a_eliminar)
X = df_limpio.copy()

print(f"Columnas eliminadas exitosamente para evitar fuga de información y redundancia: {len(columnas_existentes_a_eliminar)}")
print(f"Dimensiones de la matriz de características X: {X.shape[0]} filas y {X.shape[1]} columnas\n")


# ==========================================
# PASO 6: EXPORTAR LOS ARCHIVOS PROCESADOS A EXCEL
# ==========================================
nombre_archivo_salida_completo = "Base_de_datos_modificada.xlsx"
nombre_archivo_salida_X = "Matriz_X_Predictores.xlsx"

ruta_salida_completo = os.path.join(directorio_actual, nombre_archivo_salida_completo)
ruta_salida_X = os.path.join(directorio_actual, nombre_archivo_salida_X)

df_limpio.to_excel(ruta_salida_completo, index=False)
X.to_excel(ruta_salida_X, index=False)

print("==========================================")
print("--- ARCHIVOS EXCEL GUARDADOS CON ÉXITO ---")
print(f"Base traducida y depurada: {nombre_archivo_salida_completo}")
print(f"Matriz de características (X): {nombre_archivo_salida_X}")
print("==========================================")