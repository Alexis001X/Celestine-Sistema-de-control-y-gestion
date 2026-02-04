# Guía de Inicio Rápido - Sistema Celestine

Esta guía te ayudará a poner en marcha el sistema en menos de 5 minutos.

## 📋 Requisitos Mínimos

- Windows 10 o superior
- Python 3.8 o superior
- 100 MB de espacio en disco
- 2 GB de RAM

## 🚀 Instalación Rápida

### Opción 1: Usando el Ejecutable (Recomendado para usuarios finales)

1. Descarga el instalador desde [Releases](https://github.com/tu-usuario/sistema-facturacion-agua/releases)
2. Ejecuta `Celestine_v1.2.0_Setup.exe`
3. Sigue las instrucciones del instalador
4. ¡Listo! El sistema está instalado

### Opción 2: Desde el Código Fuente (Para desarrolladores)

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/sistema-facturacion-agua.git
cd sistema-facturacion-agua

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar entorno virtual
# En Windows:
.venv\Scripts\activate
# En Linux/Mac:
source .venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar
python main.py
```

## 🔑 Primer Inicio de Sesión

**Credenciales por defecto:**
```
Usuario: admin
Contraseña: admin123
```

> ⚠️ **IMPORTANTE**: Cambia estas credenciales inmediatamente después del primer inicio de sesión.

## 📝 Primeros Pasos

### 1. Registrar un Cliente

1. Ve a **Usuarios** en el menú lateral
2. Haz clic en **Nuevo Cliente**
3. Completa los datos:
   - Cédula
   - Nombre completo
   - Dirección
   - Teléfono
   - Email (opcional)
   - Número de conexión
4. Guarda

### 2. Registrar una Lectura

1. Ve a **Lecturas**
2. Selecciona el cliente
3. Ingresa la lectura actual
4. El sistema calculará automáticamente el consumo
5. Guarda

### 3. Generar una Factura

1. Ve a **Facturación**
2. Selecciona el cliente
3. El sistema cargará automáticamente:
   - Última lectura
   - Consumo
   - Tarifas calculadas
4. Agrega servicios adicionales si es necesario
5. Marca "Tercera edad" si aplica
6. Genera la factura
7. Imprime el PDF

## 🎯 Flujo de Trabajo Mensual

```
1. Tomar lecturas → 2. Generar facturas → 3. Imprimir → 4. Entregar → 5. Registrar pagos
```

## 📞 ¿Necesitas Ayuda?

- 📖 Lee el [README completo](README.md)
- 🐛 Reporta bugs en [Issues](https://github.com/tu-usuario/sistema-facturacion-agua/issues)
- 💬 Consulta la documentación en la carpeta `docs/`

## ✅ Verificación de Instalación

Ejecuta este comando para verificar que todo está correcto:

```bash
python verificar_dependencias.py
```

Si todo está bien, verás:
```
✓ Python 3.8+ instalado
✓ PyQt6 instalado
✓ ReportLab instalado
✓ Base de datos creada
✓ Carpetas de trabajo creadas
```

¡Listo para usar! 🎉
