from django.apps import AppConfig


class RiccoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ricco_app'

#Para crear el superusuario automáticamente desde apps.py
    def ready(self):
        from django.contrib.auth import get_user_model
        from django.db.utils import OperationalError, ProgrammingError
        try:
            User = get_user_model()
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='adminpassword123'
                )
        except (OperationalError, ProgrammingError) as e:
            print("🚨 No se pudo crear el superusuario todavía:", e)
