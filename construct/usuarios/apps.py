from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'construct.usuarios'

    def ready(self):
        import construct.usuarios.signals