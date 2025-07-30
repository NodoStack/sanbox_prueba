from django.apps import AppConfig


class RiccoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ricco_app'

#Para crear el superusuario automáticamente desde apps.py
    def ready(self):
        # Este método se ejecuta cuando Django arranca
        from django.contrib.auth import get_user_model
        from django.db.utils import OperationalError, ProgrammingError

        try:
            User = get_user_model()
            username = 'admin'
            email = 'admin@example.com'
            password = 'adminpassword123'

            if not User.objects.filter(username=username).exists():
                print('🛠️ Creando superusuario...')
                User.objects.create_superuser(username=username, email=email, password=password)
            else:
                print('✅ Superusuario ya existe.')
        except (OperationalError, ProgrammingError):
            # Ocurre si las migraciones aún no se hicieron
            print("⏳ Esperando que se creen las tablas...")
