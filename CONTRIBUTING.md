# Guía de Contribución - Sistema Celestine

¡Gracias por tu interés en contribuir al Sistema de Facturación Celestine! 🎉

## 📋 Código de Conducta

Este proyecto se adhiere a un código de conducta. Al participar, se espera que mantengas este código.

## 🚀 ¿Cómo puedo contribuir?

### Reportar Bugs

Si encuentras un bug:

1. Verifica que el bug no haya sido reportado anteriormente en [Issues](https://github.com/tu-usuario/sistema-facturacion-agua/issues)
2. Abre un nuevo issue con:
   - Título descriptivo
   - Pasos detallados para reproducir el problema
   - Comportamiento esperado vs comportamiento actual
   - Capturas de pantalla si aplica
   - Versión de Python y sistema operativo

### Sugerir Mejoras

Las sugerencias son bienvenidas:

1. Abre un issue con la etiqueta "enhancement"
2. Describe claramente la mejora propuesta
3. Explica por qué sería útil para el proyecto

### Pull Requests

1. **Fork** el repositorio
2. Crea una **rama** desde `main`:
   ```bash
   git checkout -b feature/mi-nueva-funcionalidad
   ```
3. Realiza tus cambios siguiendo las guías de estilo
4. **Commit** tus cambios:
   ```bash
   git commit -m "feat: agregar nueva funcionalidad X"
   ```
5. **Push** a tu fork:
   ```bash
   git push origin feature/mi-nueva-funcionalidad
   ```
6. Abre un **Pull Request**

## 📝 Guías de Estilo

### Código Python

- Sigue [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Usa nombres descriptivos para variables y funciones
- Documenta funciones complejas con docstrings
- Mantén las funciones pequeñas y enfocadas

### Commits

Usa mensajes de commit descriptivos siguiendo [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Cambios de formato (no afectan el código)
- `refactor:` Refactorización de código
- `test:` Agregar o modificar tests
- `chore:` Tareas de mantenimiento

Ejemplo:
```
feat: agregar soporte para múltiples monedas
fix: corregir cálculo de tarifa excedente
docs: actualizar README con nuevas instrucciones
```

## 🏗️ Estructura del Proyecto

Respeta la arquitectura MVC:

```
app/
├── controllers/  # Lógica de negocio
├── models/      # Modelos de datos
├── views/       # Interfaces de usuario
├── helpers/     # Utilidades
└── database/    # Gestión de BD
```

## ✅ Checklist antes de Pull Request

- [ ] El código sigue las guías de estilo
- [ ] He comentado el código en áreas difíciles de entender
- [ ] He actualizado la documentación si es necesario
- [ ] Mis cambios no generan nuevas advertencias
- [ ] He probado que todo funciona correctamente
- [ ] He actualizado el CHANGELOG si aplica

## 🤝 Proceso de Revisión

1. Un mantenedor revisará tu PR
2. Pueden solicitar cambios o aclaraciones
3. Una vez aprobado, se fusionará con `main`
4. Tu contribución será reconocida en el proyecto

## 💡 ¿Necesitas Ayuda?

- Abre un issue con la etiqueta "question"
- Contacta a los mantenedores

¡Gracias por contribuir! 🙌
