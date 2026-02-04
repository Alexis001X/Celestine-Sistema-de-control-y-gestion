# 💧 Sistema de Facturación de Agua - Celestine

<div align="center">

![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**Sistema completo de facturación para Juntas Administradoras de Agua Potable**

[Características](#-características) • [Instalación](#-instalación) • [Uso](#-uso) • [Documentación](#-documentación)

</div>

---

## 📋 Descripción

**Celestine** es un sistema de gestión y facturación diseñado específicamente para Juntas Administradoras de Agua Potable y Alcantarillado (JAAPC). Proporciona una solución completa para administrar clientes, registrar lecturas de medidores, generar facturas automáticas y gestionar la recaudación.

### 🎯 Desarrollado para

- Juntas de Agua Potable
- Cooperativas de Agua
- Pequeñas empresas de servicios básicos
- Comunidades rurales y urbanas

---

## ✨ Características

### 📊 Gestión Completa

- **Gestión de Clientes**: Registro y administración de usuarios del servicio
- **Lecturas de Medidores**: Registro mensual con cálculo automático de consumo
- **Facturación Inteligente**: Sistema de tarifas por rangos con múltiples servicios
- **Consultas Avanzadas**: Búsqueda de facturas, lecturas y clientes
- **Reportes**: Generación de reportes de recaudación y estadísticas

### 💰 Sistema de Tarifas Flexible

#### Tarifa Básica por Consumo
- 0-10 m³: $1.50
- 11-50 m³: $2.00
- 51-100 m³: $3.00
- 101+ m³: $3.00

#### Tarifa por Excedente (por m³)
- 0-10 m³: $0.30/m³
- 11-25 m³: $0.40/m³
- 26-50 m³: $0.50/m³
- 51+ m³: $0.75/m³

#### Servicios Adicionales
- Servicio básico
- Traspaso de propiedad
- Instalación/cambio de medidor
- Reconexión
- Multas (sesiones, mingas)
- Conexión nueva
- Materiales
- Otros servicios personalizados

### 🔢 Numeración Inteligente de Facturas

- Formato estándar: `001-010-0000000001`
- Detección automática de números disponibles
- Soporte para múltiples secuencias
- Reutilización de números en caso de huecos

### 📄 Generación de PDFs

- Facturas con formato profesional
- Original y copia en la misma hoja (A4)
- Reportes de recaudación
- Reportes de servicios

### 🔐 Seguridad y Auditoría

- Sistema de autenticación de usuarios
- Roles y permisos
- Registro de actividades (logs)
- Respaldos automáticos de base de datos

### 🎁 Características Especiales

- ✅ Descuento para tercera edad
- ✅ Migraciones automáticas de base de datos
- ✅ Importación de bases de datos externas
- ✅ Sistema de respaldos
- ✅ Interfaz gráfica intuitiva

---

## 🛠️ Tecnologías

- **Lenguaje**: Python 3.8+
- **Interfaz Gráfica**: PyQt6
- **Base de Datos**: SQLite
- **Generación de PDFs**: ReportLab
- **Arquitectura**: MVC (Modelo-Vista-Controlador)

---

## 📦 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/sistema-facturacion-agua.git
cd sistema-facturacion-agua
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv .venv
```

3. **Activar entorno virtual**

Windows:
```bash
.venv\Scripts\activate
```

Linux/Mac:
```bash
source .venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Ejecutar la aplicación**
```bash
python main.py
```

---

## 🚀 Uso

### Primera Ejecución

Al ejecutar el sistema por primera vez:

1. Se creará automáticamente la base de datos SQLite
2. Se ejecutarán las migraciones necesarias
3. Se crearán las carpetas de trabajo (`facturas_pdf`, `reportes`, `logs`)

### Credenciales por Defecto

> ⚠️ **Importante**: Se requiere configuracion en la base de datos con la que el sistema trabaje (No incluida)

```
Usuario: admin
Contraseña: admin123
```

### Flujo de Trabajo Típico

1. **Registrar Clientes**: Ingresa la información de los usuarios del servicio
2. **Tomar Lecturas**: Registra las lecturas mensuales de los medidores
3. **Generar Facturas**: El sistema calcula automáticamente los montos
4. **Imprimir Facturas**: Genera PDFs con original y copia
5. **Registrar Pagos**: Actualiza el estado de las facturas
6. **Consultar Reportes**: Visualiza estadísticas de recaudación

---

## 📁 Estructura del Proyecto

```
sistema_facturacion_agua/
├── app/
│   ├── controllers/          # Lógica de negocio
│   ├── models/              # Modelos de datos
│   ├── views/               # Interfaces de usuario
│   ├── helpers/             # Utilidades y funciones auxiliares
│   ├── database/            # Gestión de base de datos
│   └── resources/           # Recursos (iconos, estilos)
├── main.py                  # Punto de entrada de la aplicación
├── requirements.txt         # Dependencias del proyecto
└── README.md               # Este archivo
```

---

## 🗄️ Base de Datos

El sistema utiliza SQLite con las siguientes tablas principales:

- **clientes**: Información de usuarios del servicio
- **lecturas**: Registro de lecturas de medidores
- **facturas**: Facturas generadas
- **secuencias_facturacion**: Control de numeración

### Migraciones Automáticas

El sistema incluye un gestor de migraciones que:
- Verifica la estructura de la base de datos al iniciar
- Crea tablas y campos faltantes automáticamente
- Permite importar bases de datos antiguas

---

## 📖 Documentación

### Módulos Principales

#### 1. Gestión de Clientes
- Crear, editar y eliminar clientes
- Búsqueda avanzada
- Historial de consumo

#### 2. Lecturas de Medidores
- Registro de lecturas mensuales
- Cálculo automático de consumo
- Validación de datos

#### 3. Facturación
- Generación automática de facturas
- Cálculo de tarifas por rangos
- Servicios adicionales
- Descuentos especiales

#### 4. Consultas y Reportes
- Consulta de facturas por cliente, fecha o número
- Historial de lecturas
- Reporte de deudas pendientes
- Estadísticas de recaudación

---

## 🔧 Configuración Avanzada

### Cambiar Ruta de Base de Datos

Puedes especificar una ruta personalizada de tres formas:

1. **Argumento de línea de comandos**:
```bash
python main.py "C:\ruta\a\mi_base_datos.db"
```

2. **Archivo config.txt**: Crea un archivo `config.txt` junto al ejecutable con la ruta de la BD

3. **Importar BD externa**: Coloca un archivo `importar_bd.db` junto al ejecutable

### Personalizar Tarifas

Las tarifas se pueden modificar en:
```python
app/controllers/factura_controller.py
```

---

## 🏗️ Compilar Ejecutable

Para crear un ejecutable de Windows:

```bash
python build_commandline.py
```

El ejecutable se generará en la carpeta `dist/`

---

## 🤝 Contribuir

Las contribuciones son bienvenidas! Por favor:

1. Haz un Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Changelog

### Versión 1.2.0 (Actual)
- ✅ Sistema de numeración secuencial de facturas
- ✅ Soporte para descuento de tercera edad
- ✅ Migraciones automáticas de base de datos
- ✅ Importación de bases de datos externas
- ✅ Sistema de logs mejorado
- ✅ Generación de PDFs optimizada

### Versión 1.1.0
- Sistema de servicios adicionales
- Consultas avanzadas
- Reportes de recaudación

### Versión 1.0.0
- Lanzamiento inicial
- Gestión básica de clientes y facturas

---

## 🐛 Reporte de Bugs

Si encuentras un bug, por favor abre un [Issue](https://github.com/tu-usuario/sistema-facturacion-agua/issues) con:

- Descripción del problema
- Pasos para reproducirlo
- Comportamiento esperado
- Capturas de pantalla (si aplica)

---

## 📧 Contacto

**Desarrollador**: [Tu Nombre]  
**Email**: tu-email@ejemplo.com  
**Proyecto**: [https://github.com/tu-usuario/sistema-facturacion-agua](https://github.com/tu-usuario/sistema-facturacion-agua)

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 🙏 Agradecimientos

- A todas las Juntas de Agua que inspiraron este proyecto
- A la comunidad de Python y PyQt6
- A todos los contribuidores

---

<div align="center">

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub ⭐**

Hecho con ❤️ para las comunidades de Ecuador

</div>
