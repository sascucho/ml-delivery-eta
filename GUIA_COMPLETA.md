# 🚀 GUÍA COMPLETA: Proyecto ML Food Delivery ETA

## 👥 EQUIPO
- **Andrés** (sascucho) - Creador del repositorio
- **Laura** - Sube los archivos desde su PC
- **Juan** - Análisis de Tráfico y Distancia
- **Sofía** - Análisis de Clima
- **Andrés** - Análisis de Cliente y Restaurante

---

# FASE 1: LAURA SUBE LOS ARCHIVOS (20 minutos)

## PASO 1.1: Laura instala Git (si no lo tiene)

**SOLO LA PRIMERA VEZ:**

- **Windows:** https://git-scm.com/download/win → Descargar e instalar (siguiente, siguiente...)
- **Mac:** Abre Terminal y escribe: `brew install git`
- **Linux:** Abre Terminal y escribe: `sudo apt install git`

## PASO 1.2: Laura configura Git (si no lo tiene)

Abre **CMD (Windows)** o **Terminal (Mac/Linux)** y escribe:

```bash
git config --global user.name "Laura"
git config --global user.email "laura@correo.com"
```

(Reemplaza con el correo real de Laura)

## PASO 1.3: Laura clona el repositorio

Laura abre **CMD/Terminal** en su PC y escribe:

```bash
cd Desktop
git clone https://github.com/sascucho/ml-delivery-eta.git
cd ml-delivery-eta
```

**¿Qué pasó?**
- Se descargó el repositorio a su Desktop
- Ahora hay una carpeta llamada `ml-delivery-eta`

## PASO 1.4: Laura copia los archivos CSV a la carpeta

**Laura abre el Explorador de Archivos (Windows) o Finder (Mac)** y:

1. Va a la carpeta donde tiene sus archivos:
   - `dataset_original.csv`
   - `dataset_preparado.csv`
   - `limpieza.py` (el código que limpió los datos)

2. Los COPIA y los PEGA en:
   ```
   Desktop/ml-delivery-eta/1_datos/
   ```

**Si la carpeta `1_datos` NO existe, Laura la crea:**
- Click derecho → Nueva carpeta → Nombre: `1_datos`

**Resultado esperado:**
```
ml-delivery-eta/
├── README.md
├── .gitignore
└── 1_datos/
    ├── dataset_original.csv
    ├── dataset_preparado.csv
    └── limpieza.py
```

## PASO 1.5: Laura crea los archivos compartidos en VS Code

Laura abre **VS Code** y abre la carpeta `ml-delivery-eta`.

### Archivo 1: config.py

Botón derecho en la raíz → **New File** → Nombre: `config.py`

```python
import pandas as pd
import numpy as np
from pathlib import Path

# ========== RUTAS ==========
DATA_DIR = Path("1_datos")
DATASET_PREPARADO = DATA_DIR / "dataset_preparado.csv"

# ========== CONFIGURACIÓN ==========
RANDOM_STATE = 42

# Variables categóricas
COLUMNAS_CATEGORICAS = [
    'city', 'weather', 'traffic_level', 'customer_type', 
    'restaurant_type', 'restaurant_primary_category', 
    'day_of_week', 'payment_method'
]

# Variables numéricas principales
COLUMNAS_NUMERICAS = [
    'distance_km', 'items_count', 'subtotal', 'order_total',
    'restaurant_preparation_time_minutes', 'actual_delivery_time_minutes',
    'customer_age', 'restaurant_rating', 'delivery_partner_experience_months',
    'delivery_partner_rating', 'estimated_delivery_time_minutes'
]

# ========== FUNCIÓN PRINCIPAL ==========
def cargar_datos():
    """
    Carga el dataset preparado.
    Esta función la usan TODOS para garantizar que usan los mismos datos.
    """
    try:
        df = pd.read_csv(DATASET_PREPARADO)
        print(f"✅ Dataset cargado: {len(df)} registros, {len(df.columns)} columnas")
        return df
    except FileNotFoundError:
        print(f"❌ Error: No se encontró {DATASET_PREPARADO}")
        return None
```

Guardar: **Ctrl + S**

### Archivo 2: utils.py

Botón derecho en la raíz → **New File** → Nombre: `utils.py`

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de gráficos
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
sns.set_style("whitegrid")

# ========== FUNCIONES REUTILIZABLES ==========

def resumen_estadistico(df, columna):
    """
    Imprime resumen estadístico de una columna numérica.
    Uso: resumen_estadistico(df, 'distance_km')
    """
    print(f"\n{'='*50}")
    print(f"RESUMEN: {columna}")
    print(f"{'='*50}")
    print(df[columna].describe())
    print(f"Valores nulos: {df[columna].isnull().sum()}")

def resumen_por_grupo(df, columna_valor, columna_grupo):
    """
    Calcula estadísticas de una columna agrupada por otra.
    Uso: resumen_por_grupo(df, 'actual_delivery_time_minutes', 'traffic_level')
    """
    return df.groupby(columna_grupo)[columna_valor].agg([
        'count', 'mean', 'median', 'std', 'min', 'max'
    ]).round(2)

def tasa_retrasos(df, columna_grupo=None):
    """
    Calcula el porcentaje de pedidos tarde.
    Si no especificas grupo, calcula el total.
    Uso: tasa_retrasos(df, 'traffic_level')
    """
    if columna_grupo:
        resultado = df.groupby(columna_grupo)['late_delivery'].apply(
            lambda x: (x.sum() / len(x) * 100)
        ).round(2)
        return resultado
    else:
        return (df['late_delivery'].sum() / len(df) * 100).round(2)

def graficar_distribucion(df, columna, titulo=""):
    """
    Crea histograma y boxplot de una variable.
    Uso: graficar_distribucion(df, 'distance_km', 'Distancia en km')
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histograma
    ax1.hist(df[columna].dropna(), bins=30, color='steelblue', edgecolor='black')
    ax1.set_xlabel(columna)
    ax1.set_ylabel('Frecuencia')
    ax1.set_title(f'Histograma: {titulo}')
    
    # Boxplot
    ax2.boxplot(df[columna].dropna())
    ax2.set_ylabel(columna)
    ax2.set_title(f'Boxplot: {titulo}')
    
    plt.tight_layout()
    return fig

def graficar_por_grupo(df, columna_valor, columna_grupo, titulo=""):
    """
    Crea boxplot de una variable numérica agrupada por una categórica.
    Uso: graficar_por_grupo(df, 'actual_delivery_time_minutes', 'traffic_level', 'Tiempo por Tráfico')
    """
    plt.figure(figsize=(12, 6))
    df.boxplot(column=columna_valor, by=columna_grupo, figsize=(12, 6))
    plt.suptitle(f'Boxplot: {titulo}')
    plt.title('')
    return plt

def correlacion_numericas(df):
    """
    Calcula matriz de correlación de variables numéricas.
    Retorna la matriz para visualizar.
    """
    from config import COLUMNAS_NUMERICAS
    
    cols_disponibles = [col for col in COLUMNAS_NUMERICAS if col in df.columns]
    return df[cols_disponibles].corr().round(3)
```

Guardar: **Ctrl + S**

### Archivo 3: requirements.txt

Botón derecho en la raíz → **New File** → Nombre: `requirements.txt`

```
pandas==2.0.3
numpy==1.24.3
matplotlib==3.7.2
seaborn==0.12.2
scipy==1.11.2
scikit-learn==1.3.0
```

Guardar: **Ctrl + S**

## PASO 1.6: Laura crea las carpetas

En VS Code, botón derecho en la raíz → **New Folder**

Crear estas carpetas:
- `2_exploracion`
- `3_estadistica`
- `4_modelos`

## PASO 1.7: Laura sube TODO a GitHub

En **VS Code**, abre la **Terminal** (Ctrl + `)

```bash
git add .
git commit -m "Subir datasets y archivos compartidos"
git push origin main
```

**Resultado esperado:**
```
[main abc1234] Subir datasets y archivos compartidos
 5 files changed, ...
 ...
 main -> main
```

**¡LISTO! Laura subió todo a GitHub** ✅

---

# FASE 2: TODOS DESCARGAN EL REPOSITORIO (10 minutos)

## PASO 2.1: Juan, Sofía y Andrés descargan

**JUAN, SOFÍA y ANDRÉS hacen esto (cada uno en su PC):**

Abren **CMD/Terminal** y escriben:

```bash
cd Desktop
git clone https://github.com/sascucho/ml-delivery-eta.git
cd ml-delivery-eta
```

**¿Qué pasó?**
- Se descargó la carpeta con TODO lo que Laura subió
- Están en la rama `main`

## PASO 2.2: Instalar librerías (TODOS lo hacen)

En **VS Code Terminal** (Ctrl + `):

```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn
```

Si tienen error con `pip`, instalen Python desde https://www.python.org/

---

# FASE 3: CREAR LAS RAMAS (5 minutos)

**Cada persona crea su rama SOLO UNA VEZ**

En VS Code Terminal:

## JUAN - Tráfico y Distancia

```bash
git checkout -b feature/analisis-trafico
```

Output esperado:
```
Switched to a new branch 'feature/analisis-trafico'
```

## SOFÍA - Clima

```bash
git checkout -b feature/analisis-clima
```

## ANDRÉS - Cliente y Restaurante

```bash
git checkout -b feature/analisis-cliente
```

---

# FASE 4: ESCRIBIR EL CÓDIGO (El trabajo REAL)

## PASO 4.1: JUAN - Análisis de Tráfico y Distancia

### 4.1.1 Crear archivo

En VS Code, botón derecho en carpeta **2_exploracion** → **New File**

Nombre: `eda_trafico.py`

### 4.1.2 Escribir el código

```python
"""
ANÁLISIS DE TRÁFICO Y DISTANCIA
Autor: Juan
Fecha: Octubre 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from config import cargar_datos
from utils import (
    resumen_estadistico,
    resumen_por_grupo,
    graficar_distribucion,
    graficar_por_grupo
)

# ========== CARGAR DATOS ==========
df = cargar_datos()

# ========== ANÁLISIS 1: TRÁFICO ==========
print("\n" + "="*60)
print("ANÁLISIS 1: EFECTO DEL TRÁFICO EN TIEMPO DE ENTREGA")
print("="*60)

# Resumen por nivel de tráfico
print("\nTiempo de entrega por nivel de tráfico:")
resultado_trafico = resumen_por_grupo(df, 'actual_delivery_time_minutes', 'traffic_level')
print(resultado_trafico)

# Gráfico
print("\nCreando gráficos...")
graficar_por_grupo(df, 'actual_delivery_time_minutes', 'traffic_level', 
                   'Tiempo de Entrega por Nivel de Tráfico')
plt.savefig('2_exploracion/grafico_trafico.png', dpi=100, bbox_inches='tight')
print("✅ Gráfico guardado: grafico_trafico.png")

# ========== ANÁLISIS 2: DISTANCIA ==========
print("\n" + "="*60)
print("ANÁLISIS 2: EFECTO DE LA DISTANCIA EN TIEMPO DE ENTREGA")
print("="*60)

# Resumen general de distancia
print("\nEstadísticas de distancia:")
resumen_estadistico(df, 'distance_km')

# Correlación
print("\nCorrelación entre distancia y tiempo de entrega:")
correlacion = df['distance_km'].corr(df['actual_delivery_time_minutes'])
print(f"Pearson r = {correlacion:.3f} (MUY FUERTE)")

# Gráfico de distribución
print("\nCreando gráfico de distribución...")
graficar_distribucion(df, 'distance_km', 'Distancia en Kilómetros')
plt.savefig('2_exploracion/distribucion_distancia.png', dpi=100, bbox_inches='tight')
print("✅ Gráfico guardado: distribucion_distancia.png")

# Gráfico de correlación (scatter)
plt.figure(figsize=(12, 6))
plt.scatter(df['distance_km'], df['actual_delivery_time_minutes'], alpha=0.3)
plt.xlabel('Distancia (km)')
plt.ylabel('Tiempo de Entrega (minutos)')
plt.title(f'Relación Distancia vs Tiempo (Correlación: {correlacion:.2f})')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('2_exploracion/correlacion_distancia.png', dpi=100, bbox_inches='tight')
print("✅ Gráfico guardado: correlacion_distancia.png")

# ========== ANÁLISIS 3: TRÁFICO + DISTANCIA ==========
print("\n" + "="*60)
print("ANÁLISIS 3: EFECTO COMBINADO (TRÁFICO + DISTANCIA)")
print("="*60)

# Crear categoría de distancia
df['distancia_categoria'] = pd.cut(df['distance_km'], bins=3, 
                                     labels=['Corta', 'Media', 'Larga'])

# Tiempo por tráfico Y distancia
print("\nTiempo de entrega por TRÁFICO y DISTANCIA:")
resultado_combinado = df.groupby(['traffic_level', 'distancia_categoria'])[
    'actual_delivery_time_minutes'
].mean().round(2)
print(resultado_combinado)

print("\n" + "="*60)
print("✅ ANÁLISIS DE TRÁFICO Y DISTANCIA COMPLETADO")
print("="*60)

plt.show()
```

### 4.1.3 Guardar y probar

Guardar: **Ctrl + S**

Abrir Terminal en VS Code (Ctrl + `) y escribir:

```bash
python 2_exploracion/eda_trafico.py
```

Debe mostrar los datos y los gráficos.

---

## PASO 4.2: SOFÍA - Análisis de Clima

### 4.2.1 Crear archivo

En VS Code, botón derecho en carpeta **2_exploracion** → **New File**

Nombre: `eda_clima.py`

### 4.2.2 Escribir el código

```python
"""
ANÁLISIS DE CLIMA Y CONDICIONES AMBIENTALES
Autor: Sofía
Fecha: Octubre 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from config import cargar_datos
from utils import (
    resumen_estadistico,
    resumen_por_grupo,
    graficar_distribucion,
    graficar_por_grupo,
    tasa_retrasos
)

# ========== CARGAR DATOS ==========
df = cargar_datos()

# ========== ANÁLISIS 1: CLIMA ==========
print("\n" + "="*60)
print("ANÁLISIS 1: EFECTO DEL CLIMA EN TIEMPO DE ENTREGA")
print("="*60)

# Resumen por condición climática
print("\nTiempo de entrega por condición climática:")
resultado_clima = resumen_por_grupo(df, 'actual_delivery_time_minutes', 'weather')
print(resultado_clima)

# Gráfico
print("\nCreando gráficos...")
graficar_por_grupo(df, 'actual_delivery_time_minutes', 'weather', 
                   'Tiempo de Entrega por Condición Climática')
plt.savefig('2_exploracion/grafico_clima.png', dpi=100, bbox_inches='tight')
print("✅ Gráfico guardado: grafico_clima.png")

# ========== ANÁLISIS 2: TASA DE RETRASOS POR CLIMA ==========
print("\n" + "="*60)
print("ANÁLISIS 2: TASA DE RETRASOS POR CLIMA")
print("="*60)

print("\nPorcentaje de pedidos tarde por clima:")
tasa_por_clima = tasa_retrasos(df, 'weather')
print(tasa_por_clima)

# Gráfico de barras
plt.figure(figsize=(10, 6))
tasa_por_clima.plot(kind='bar', color='coral', edgecolor='black')
plt.xlabel('Condición Climática')
plt.ylabel('Tasa de Retrasos (%)')
plt.title('Porcentaje de Pedidos Tarde por Clima')
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('2_exploracion/tasa_retrasos_clima.png', dpi=100, bbox_inches='tight')
print("✅ Gráfico guardado: tasa_retrasos_clima.png")

# ========== ANÁLISIS 3: CONTEO DE PEDIDOS POR CLIMA ==========
print("\n" + "="*60)
print("ANÁLISIS 3: DISTRIBUCIÓN DE PEDIDOS POR CLIMA")
print("="*60)

print("\nCantidad de pedidos por clima:")
conteo_clima = df['weather'].value_counts()
print(conteo_clima)

# Gráfico de pastel
plt.figure(figsize=(10, 6))
conteo_clima.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.ylabel('')
plt.title('Distribución de Pedidos por Condición Climática')
plt.tight_layout()
plt.savefig('2_exploracion/distribucion_clima.png', dpi=100, bbox_inches='tight')
print("✅ Gráfico guardado: distribucion_clima.png")

# ========== ANÁLISIS 4: CLIMA + TRÁFICO ==========
print("\n" + "="*60)
print("ANÁLISIS 4: EFECTO COMBINADO (CLIMA + TRÁFICO)")
print("="*60)

print("\nTiempo de entrega por CLIMA y TRÁFICO:")
resultado_combinado = df.groupby(['weather', 'traffic_level'])[
    'actual_delivery_time_minutes'
].mean().round(2)
print(resultado_combinado)

# Heatmap
plt.figure(figsize=(10, 6))
pivot_table = df.pivot_table(
    values='actual_delivery_time_minutes',
    index='weather',
    columns='traffic_level',
    aggfunc='mean'
)
sns.heatmap(pivot_table, annot=True, fmt='.1f', cmap='RdYlGn_r', cbar_kws={'label': 'Minutos'})
plt.title('Tiempo de Entrega: Clima x Tráfico')
plt.tight_layout()
plt.savefig('2_exploracion/heatmap_clima_trafico.png', dpi=100, bbox_inches='tight')
print("✅ Gráfico guardado: heatmap_clima_trafico.png")

print("\n" + "="*60)
print("✅ ANÁLISIS DE CLIMA COMPLETADO")
print("="*60)

plt.show()
```

### 4.2.3 Guardar y probar

Guardar: **Ctrl + S**

Terminal:

```bash
python 2_exploracion/eda_clima.py
```

---

## PASO 4.3: ANDRÉS - Análisis de Cliente y Restaurante

### 4.3.1 Crear archivo

En VS Code, botón derecho en carpeta **2_exploracion** → **New File**

Nombre: `eda_cliente_restaurante.py`

### 4.3.2 Escribir el código

```python
"""
ANÁLISIS DE CLIENTE Y RESTAURANTE
Autor: Andrés
Fecha: Octubre 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from config import cargar_datos
from utils import (
    resumen_estadistico,
    resumen_por_grupo,
    graficar_distribucion,
    graficar_por_grupo,
    tasa_retrasos
)

# ========== CARGAR DATOS ==========
df = cargar_datos()

# ========== ANÁLISIS 1: TIPO DE CLIENTE ==========
print("\n" + "="*60)
print("ANÁLISIS 1: TIPO DE CLIENTE Y TIEMPO DE ENTREGA")
print("="*60)

# Resumen por tipo de cliente
print("\nTiempo de entrega por tipo de cliente:")
resultado_cliente = resumen_por_grupo(df, 'actual_delivery_time_minutes', 'customer_type')
print(resultado_cliente)

# Gráfico
print("\nCreando gráficos...")
graficar_por_grupo(df, 'actual_delivery_time_minutes', 'customer_type', 
                   'Tiempo de Entrega por Tipo de Cliente')
plt.savefig('2_exploracion/grafico_cliente.png', dpi=100, bbox_inches='tight')
print("✅ Gráfico guardado: grafico_cliente.png")

# ========== ANÁLISIS 2: TASA DE RETRASOS POR CLIENTE ==========
print("\n" + "="*60)
print("ANÁLISIS 2: TASA DE RETRASOS POR TIPO DE CLIENTE")
print("="*60)

print("\nPorcentaje de pedidos tarde por tipo de cliente:")
tasa_por_cliente = tasa_retrasos(df, 'customer_type')
print(tasa_por_cliente)

# Gráfico
plt.figure(figsize=(10, 6))
tasa_por_cliente.plot(kind='bar', color='skyblue', edgecolor='black')
plt.xlabel('Tipo de Cliente')
plt.ylabel('Tasa de Retrasos (%)')
plt.title('Porcentaje de Pedidos Tarde por Tipo de Cliente')
plt.xticks(rotation=0)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('2_exploracion/tasa_retrasos_cliente.png', dpi=100, bbox_inches='tight')
print("✅ Gráfico guardado: tasa_retrasos_cliente.png")

# ========== ANÁLISIS 3: EDAD DEL CLIENTE ==========
print("\n" + "="*60)
print("ANÁLISIS 3: EDAD DEL CLIENTE")
print("="*60)

print("\nEstadísticas de edad:")
resumen_estadistico(df, 'customer_age')

# Gráfico de distribución
graficar_distribucion(df, 'customer_age', 'Edad del Cliente')
plt.savefig('2_exploracion/distribucion_edad.png', dpi=100, bbox_inches='tight')
print("✅ Gráfico guardado: distribucion_edad.png")

# Correlación edad vs tiempo entrega
correlacion_edad = df['customer_age'].corr(df['actual_delivery_time_minutes'])
print(f"\nCorrelación Edad vs Tiempo Entrega: {correlacion_edad:.3f} (DÉBIL)")

# ========== ANÁLISIS 4: TIPO DE RESTAURANTE ==========
print("\n" + "="*60)
print("ANÁLISIS 4: TIPO DE RESTAURANTE")
print("="*60)

print("\nTiempo de entrega por tipo de restaurante:")
resultado_restaurante = resumen_por_grupo(df, 'actual_delivery_time_minutes', 'restaurant_type')
print(resultado_restaurante)

# Gráfico
graficar_por_grupo(df, 'actual_delivery_time_minutes', 'restaurant_type', 
                   'Tiempo de Entrega por Tipo de Restaurante')
plt.savefig('2_exploracion/grafico_restaurante.png', dpi=100, bbox_inches='tight')
print("✅ Gráfico guardado: grafico_restaurante.png")

# ========== ANÁLISIS 5: NÚMERO DE ITEMS ==========
print("\n" + "="*60)
print("ANÁLISIS 5: CANTIDAD DE ITEMS EN EL PEDIDO")
print("="*60)

print("\nEstadísticas de cantidad de items:")
resumen_estadistico(df, 'items_count')

# Correlación items vs tiempo entrega
correlacion_items = df['items_count'].corr(df['actual_delivery_time_minutes'])
print(f"\nCorrelación Items vs Tiempo Entrega: {correlacion_items:.3f} (MODERADO)")

# Gráfico scatter
plt.figure(figsize=(12, 6))
plt.scatter(df['items_count'], df['actual_delivery_time_minutes'], alpha=0.3)
plt.xlabel('Cantidad de Items')
plt.ylabel('Tiempo de Entrega (minutos)')
plt.title(f'Relación Items vs Tiempo (Correlación: {correlacion_items:.2f})')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('2_exploracion/correlacion_items.png', dpi=100, bbox_inches='tight')
print("✅ Gráfico guardado: correlacion_items.png")

# ========== ANÁLISIS 6: TIEMPO PREPARACIÓN RESTAURANTE ==========
print("\n" + "="*60)
print("ANÁLISIS 6: TIEMPO DE PREPARACIÓN DEL RESTAURANTE")
print("="*60)

print("\nEstadísticas de tiempo de preparación:")
resumen_estadistico(df, 'restaurant_preparation_time_minutes')

# Correlación
correlacion_prep = df['restaurant_preparation_time_minutes'].corr(df['actual_delivery_time_minutes'])
print(f"\nCorrelación Tiempo Prep vs Tiempo Entrega: {correlacion_prep:.3f} (MODERADO)")

# Gráfico scatter
plt.figure(figsize=(12, 6))
plt.scatter(df['restaurant_preparation_time_minutes'], df['actual_delivery_time_minutes'], alpha=0.3)
plt.xlabel('Tiempo de Preparación (minutos)')
plt.ylabel('Tiempo de Entrega (minutos)')
plt.title(f'Relación Preparación vs Tiempo Entrega (Correlación: {correlacion_prep:.2f})')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('2_exploracion/correlacion_preparacion.png', dpi=100, bbox_inches='tight')
print("✅ Gráfico guardado: correlacion_preparacion.png")

print("\n" + "="*60)
print("✅ ANÁLISIS DE CLIENTE Y RESTAURANTE COMPLETADO")
print("="*60)

plt.show()
```

### 4.3.3 Guardar y probar

Guardar: **Ctrl + S**

Terminal:

```bash
python 2_exploracion/eda_cliente_restaurante.py
```

---

# FASE 5: SUBIR LOS CAMBIOS A GITHUB

## PASO 5.1: JUAN sube su análisis

En VS Code Terminal:

```bash
git add .
git commit -m "Agregar análisis de tráfico y distancia"
git push origin feature/analisis-trafico
```

Expected output:
```
[feature/analisis-trafico abc1234] Agregar análisis de tráfico y distancia
 ...
 feature/analisis-trafico -> feature/analisis-trafico
```

## PASO 5.2: SOFÍA sube su análisis

En VS Code Terminal:

```bash
git add .
git commit -m "Agregar análisis de clima"
git push origin feature/analisis-clima
```

## PASO 5.3: ANDRÉS sube su análisis

En VS Code Terminal:

```bash
git add .
git commit -m "Agregar análisis de cliente y restaurante"
git push origin feature/analisis-cliente
```

---

# FASE 6: HACER PULL REQUEST EN GITHUB

**Cuando termina cada persona:**

1. Ve a https://github.com/sascucho/ml-delivery-eta
2. Haz clic en **"Pull Requests"** (pestaña arriba)
3. Haz clic en **"New Pull Request"**
4. En **"Compare"** selecciona tu rama:
   - Juan: `feature/analisis-trafico`
   - Sofía: `feature/analisis-clima`
   - Andrés: `feature/analisis-cliente`
5. Haz clic en **"Create Pull Request"**
6. Escribe un título:
   ```
   Agregar análisis de [tu tema]
   ```
7. Haz clic en **"Create Pull Request"**

**Laura (o profesor) revisa y hace clic en "Merge Pull Request"** ✅

---

# FASE 7: DESCARGAR CAMBIOS DE OTROS

**Cuando Laura hace merge:**

Todos hacen esto en Terminal:

```bash
git checkout main
git pull origin main
```

Esto descarga todo lo que otros subieron.

---

## 📋 RESUMEN DE TAREAS

| Persona | Archivo Principal | Qué Analiza |
|---------|-------------------|-----------|
| **Laura** | config.py, utils.py, requirements.txt | Prepara datos y crea funciones compartidas |
| **Juan** | 2_exploracion/eda_trafico.py | Tráfico, distancia, correlaciones |
| **Sofía** | 2_exploracion/eda_clima.py | Clima, retrasos, combinado con tráfico |
| **Andrés** | 2_exploracion/eda_cliente_restaurante.py | Cliente, restaurante, items, preparación |

---

## ✅ CHECKLIST PARA EMPEZAR

### LAURA:
- [ ] Instalar Git (si no lo tiene)
- [ ] Configurar Git con su nombre y correo
- [ ] Clonar: `git clone https://github.com/sascucho/ml-delivery-eta.git`
- [ ] Copiar CSV a carpeta `1_datos/`
- [ ] Crear `config.py`
- [ ] Crear `utils.py`
- [ ] Crear `requirements.txt`
- [ ] Crear carpetas: `2_exploracion`, `3_estadistica`, `4_modelos`
- [ ] Subir todo: `git add .` → `git commit -m "..."` → `git push origin main`
- [ ] Avisar que está listo

### JUAN:
- [ ] Instalar Git (si no lo tiene)
- [ ] Configurar Git (si no lo tiene)
- [ ] Clonar: `git clone https://github.com/sascucho/ml-delivery-eta.git`
- [ ] Instalar librerías: `pip install pandas numpy matplotlib seaborn scipy scikit-learn`
- [ ] Crear rama: `git checkout -b feature/analisis-trafico`
- [ ] Crear archivo: `2_exploracion/eda_trafico.py`
- [ ] Escribir código
- [ ] Probar: `python 2_exploracion/eda_trafico.py`
- [ ] Subir: `git add .` → `git commit -m "..."` → `git push origin feature/analisis-trafico`
- [ ] Hacer Pull Request en GitHub

### SOFÍA:
- [ ] Instalar Git (si no lo tiene)
- [ ] Configurar Git (si no lo tiene)
- [ ] Clonar: `git clone https://github.com/sascucho/ml-delivery-eta.git`
- [ ] Instalar librerías: `pip install pandas numpy matplotlib seaborn scipy scikit-learn`
- [ ] Crear rama: `git checkout -b feature/analisis-clima`
- [ ] Crear archivo: `2_exploracion/eda_clima.py`
- [ ] Escribir código
- [ ] Probar: `python 2_exploracion/eda_clima.py`
- [ ] Subir: `git add .` → `git commit -m "..."` → `git push origin feature/analisis-clima`
- [ ] Hacer Pull Request en GitHub

### ANDRÉS:
- [ ] Instalar Git (si no lo tiene)
- [ ] Configurar Git (si no lo tiene)
- [ ] Clonar: `git clone https://github.com/sascucho/ml-delivery-eta.git`
- [ ] Instalar librerías: `pip install pandas numpy matplotlib seaborn scipy scikit-learn`
- [ ] Crear rama: `git checkout -b feature/analisis-cliente`
- [ ] Crear archivo: `2_exploracion/eda_cliente_restaurante.py`
- [ ] Escribir código
- [ ] Probar: `python 2_exploracion/eda_cliente_restaurante.py`
- [ ] Subir: `git add .` → `git commit -m "..."` → `git push origin feature/analisis-cliente`
- [ ] Hacer Pull Request en GitHub

---

## 🆘 PROBLEMAS COMUNES

### ❌ "Error: No module named 'pandas'"
**Solución:**
```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn
```

### ❌ "Error: comando git no encontrado"
**Solución:** Instala Git desde https://git-scm.com/

### ❌ "No encuentro la carpeta"
**Solución:** En VS Code, File → Open Folder → Selecciona `ml-delivery-eta`

### ❌ "Mi rama no está actualizada"
**Solución:**
```bash
git checkout main
git pull origin main
git checkout tu-rama
git merge main
```

### ❌ "¿Cómo veo lo que cambié?"
**Solución:**
```bash
git status
```

### ❌ "¿Cómo veo mi historial?"
**Solución:**
```bash
git log --oneline
```

---

## 📞 CONTACTO

Si tienen dudas:
1. Revisar esta guía
2. Preguntar a Laura
3. Crear un Issue en GitHub (Issues → New Issue)

---

## 🎓 PRÓXIMA FASE

Después de que todos terminen el análisis exploratorio:
- Fase 3: **Estadística Descriptiva** (3_estadistica/)
- Fase 4: **Modelado ML** (4_modelos/)

Mismo proceso: crear ramas, trabajar en paralelo, hacer Pull Requests.

---

**¡BIENVENIDOS AL PROYECTO ML! 🚀**
