"""
Módulo de roles y permisos para AgenteJP.
Autenticación eliminada — acceso directo sin login.
"""

class Roles:
    ADMIN = "ADMIN"
    INVENTARIO = "INVENTARIO"
    LEGAL = "LEGAL"
    RRHH = "RRHH"
    PERMISOS = "PERMISOS"

    @classmethod
    def get_all(cls):
        return [cls.ADMIN, cls.INVENTARIO, cls.LEGAL, cls.RRHH, cls.PERMISOS]
