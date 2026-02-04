# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.2.0] - 2026-02-03

### ✨ Agregado
- Sistema de numeración secuencial de facturas con formato `001-010-XXXXXXXXXX`
- Detección automática de números disponibles (huecos) en la secuencia
- Soporte para descuento de tercera edad en facturas
- Sistema de migraciones automáticas de base de datos
- Importación de bases de datos externas mediante `importar_bd.db`
- Tabla `secuencias_facturacion` para control de numeración
- Campo `tercera_edad` en tabla facturas
- Campo `numero_factura` en tabla facturas
- Sistema de logs mejorado con registro de actividades
- Documentación completa del proyecto

### 🔧 Cambiado
- Mejorado el sistema de conexión a base de datos (patrón Singleton)
- Optimizada la generación de PDFs
- Actualizada la interfaz de usuario con mejor UX

### 🐛 Corregido
- Corrección en el cálculo de tarifas por excedente
- Solución a problemas de secuencia de facturas
- Correcciones en la base de datos aplicadas automáticamente

## [1.1.0] - 2025-11-20

### ✨ Agregado
- Sistema de servicios adicionales (traspaso, medidor, reconexión, etc.)
- Consultas avanzadas de facturas, lecturas y clientes
- Reportes de recaudación con estadísticas
- Módulo de consulta de pagados y deudas
- Generación de reportes en PDF

### 🔧 Cambiado
- Mejorada la estructura de la base de datos
- Optimización del rendimiento general

### 🐛 Corregido
- Correcciones menores en la interfaz
- Mejoras en la validación de datos

## [1.0.0] - 2025-10-15

### ✨ Lanzamiento Inicial
- Gestión de clientes (CRUD completo)
- Registro de lecturas de medidores
- Sistema de facturación básico
- Cálculo automático de tarifas por rangos
- Generación de facturas en PDF
- Sistema de autenticación de usuarios
- Interfaz gráfica con PyQt6
- Base de datos SQLite

### Características Principales
- Tarifa básica por consumo (4 rangos)
- Tarifa por excedente (4 rangos)
- Estados de factura (Pendiente, Pagado, Vencido)
- Generación de PDF con original y copia
- Búsqueda y consulta de datos

---

## Tipos de Cambios

- `✨ Agregado` - para nuevas funcionalidades
- `🔧 Cambiado` - para cambios en funcionalidades existentes
- `🗑️ Deprecado` - para funcionalidades que serán removidas
- `🚫 Removido` - para funcionalidades removidas
- `🐛 Corregido` - para corrección de bugs
- `🔒 Seguridad` - para correcciones de vulnerabilidades

---

## [Unreleased]

### Planeado para futuras versiones
- Soporte para múltiples monedas
- Exportación de datos a Excel
- Gráficos y estadísticas avanzadas
- Notificaciones automáticas de vencimiento
- Integración con sistemas de pago en línea
- Aplicación móvil para toma de lecturas
- API REST para integración con otros sistemas
