import os
import datetime
from pathlib import Path


class SistemaLogs:
    """
    Sistema de logging para registrar acciones de usuarios en el sistema.

    Características:
    - Crea archivos de log por fecha en la carpeta 'logs/'
    - Registra timestamp, usuario, rol y acción
    - Limpieza automática de logs mayores a 5 días
    """

    def __init__(self):
        """Inicializa el sistema de logs y crea el directorio si no existe."""
        # Obtener la ruta base del proyecto
        self.base_path = Path(__file__).parent.parent.parent
        self.logs_dir = self.base_path / "logs"

        # Crear directorio de logs si no existe
        self.logs_dir.mkdir(exist_ok=True)

        # Realizar limpieza de logs antiguos al inicializar
        self.limpiar_logs_antiguos()

    def obtener_nombre_archivo_log(self):
        """
        Genera el nombre del archivo de log basado en la fecha actual.

        Returns:
            Path: Ruta completa al archivo de log del día actual
        """
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        nombre_archivo = f"log_{fecha_actual}.txt"
        return self.logs_dir / nombre_archivo

    def registrar_accion(self, usuario, rol, accion, detalle=""):
        """
        Registra una acción en el archivo de log correspondiente.

        Args:
            usuario (str): Nombre del usuario que realizó la acción
            rol (str): Rol del usuario (Administrador, Recaudador, etc.)
            accion (str): Tipo de acción realizada (LOGIN, CREAR_CLIENTE, etc.)
            detalle (str, optional): Detalles adicionales de la acción
        """
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo_log = self.obtener_nombre_archivo_log()

            # Construir mensaje de log
            mensaje = f"[{timestamp}] [{usuario}] [{rol}] [{accion}]"
            if detalle:
                mensaje += f" - {detalle}"
            mensaje += "\n"

            # Escribir en el archivo (modo append)
            with open(archivo_log, "a", encoding="utf-8") as f:
                f.write(mensaje)

            return True
        except Exception as e:
            print(f"Error al registrar log: {e}")
            return False

    def limpiar_logs_antiguos(self):
        """
        Elimina archivos de log con más de 5 días de antigüedad.
        """
        try:
            fecha_limite = datetime.datetime.now() - datetime.timedelta(days=5)

            # Iterar sobre todos los archivos en el directorio de logs
            for archivo in self.logs_dir.glob("log_*.txt"):
                # Obtener la fecha de modificación del archivo
                fecha_modificacion = datetime.datetime.fromtimestamp(archivo.stat().st_mtime)

                # Eliminar si es más antiguo que 5 días
                if fecha_modificacion < fecha_limite:
                    archivo.unlink()
                    print(f"Log eliminado: {archivo.name}")

            return True
        except Exception as e:
            print(f"Error al limpiar logs antiguos: {e}")
            return False

    # Métodos de conveniencia para acciones específicas

    def log_login(self, usuario, rol):
        """Registra un inicio de sesión exitoso."""
        return self.registrar_accion(usuario, rol, "LOGIN", "Ingreso al sistema exitoso")

    def log_logout(self, usuario, rol):
        """Registra un cierre de sesión."""
        return self.registrar_accion(usuario, rol, "LOGOUT", "Cierre de sesión")

    def log_crear_cliente(self, usuario, rol, cliente_nombre, cliente_ci):
        """Registra la creación de un nuevo cliente."""
        detalle = f"Nuevo cliente: {cliente_nombre} (CI: {cliente_ci})"
        return self.registrar_accion(usuario, rol, "CREAR_CLIENTE", detalle)

    def log_editar_cliente(self, usuario, rol, cliente_id, cliente_nombre):
        """Registra la edición de un cliente."""
        detalle = f"Cliente editado: ID {cliente_id} - {cliente_nombre}"
        return self.registrar_accion(usuario, rol, "EDITAR_CLIENTE", detalle)

    def log_eliminar_cliente(self, usuario, rol, cliente_id, cliente_nombre):
        """Registra la eliminación de un cliente."""
        detalle = f"Cliente eliminado: ID {cliente_id} - {cliente_nombre}"
        return self.registrar_accion(usuario, rol, "ELIMINAR_CLIENTE", detalle)

    def log_crear_lectura(self, usuario, rol, medidor_id, lectura_actual, consumo):
        """Registra la creación de una nueva lectura."""
        detalle = f"Lectura registrada para medidor {medidor_id}: {lectura_actual} m³ (Consumo: {consumo} m³)"
        return self.registrar_accion(usuario, rol, "CREAR_LECTURA", detalle)

    def log_crear_factura(self, usuario, rol, factura_id, cliente_nombre, monto_total):
        """Registra la creación de una nueva factura."""
        detalle = f"Factura #{factura_id} creada para {cliente_nombre} - Monto: ${monto_total:.2f}"
        return self.registrar_accion(usuario, rol, "CREAR_FACTURA", detalle)

    def log_editar_factura(self, usuario, rol, factura_id, cliente_nombre, monto_total):
        """Registra la edición de una factura existente."""
        detalle = f"Factura #{factura_id} editada para {cliente_nombre} - Nuevo monto: ${monto_total:.2f}"
        return self.registrar_accion(usuario, rol, "EDITAR_FACTURA", detalle)

    def log_reimprimir_factura(self, usuario, rol, factura_id, cliente_nombre):
        """Registra la reimpresión de una factura."""
        detalle = f"Factura #{factura_id} reimpresa - Cliente: {cliente_nombre}"
        return self.registrar_accion(usuario, rol, "REIMPRIMIR_FACTURA", detalle)

    def log_crear_servicio(self, usuario, rol, servicio_id, cliente_nombre, monto):
        """Registra la creación de un servicio adicional."""
        detalle = f"Servicio #{servicio_id} creado para {cliente_nombre} - Monto: ${monto:.2f}"
        return self.registrar_accion(usuario, rol, "CREAR_SERVICIO", detalle)

    def log_consulta_facturas(self, usuario, rol, num_resultados):
        """Registra una consulta de facturas."""
        detalle = f"Consulta de facturas realizada - {num_resultados} resultados"
        return self.registrar_accion(usuario, rol, "CONSULTA_FACTURAS", detalle)

    def log_error(self, usuario, rol, accion, mensaje_error):
        """Registra un error durante una acción."""
        detalle = f"Error en {accion}: {mensaje_error}"
        return self.registrar_accion(usuario, rol, "ERROR", detalle)


# Instancia global del sistema de logs
_logger_instance = None

def get_logger():
    """
    Obtiene la instancia global del sistema de logs (patrón Singleton).

    Returns:
        SistemaLogs: Instancia del sistema de logs
    """
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = SistemaLogs()
    return _logger_instance
