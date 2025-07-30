from django.apps import AppConfig


class RiccoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ricco_app'

#Para crear el superusuario automáticamente desde apps.py
    def ready(self):
        from django.contrib.auth import get_user_model
        from django.db.utils import OperationalError, ProgrammingError
        from django.core.management import call_command

        try:
            # APLICAR MIGRACIONES ANTES DE CREAR EL SUPERUSER
            call_command('migrate')
            print("✅ Migraciones aplicadas")

            User = get_user_model()
            if not User.objects.filter(username='admin').exists():
                print('🛠️ Creando superusuario...')
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='adminpassword123'
                )
            else:
                print('✅ Superusuario ya existe.')
        except (OperationalError, ProgrammingError) as e:
            print("🚨 Error de base de datos al iniciar:", e)
        except Exception as e:
            print("❌ Otro error:", e)
