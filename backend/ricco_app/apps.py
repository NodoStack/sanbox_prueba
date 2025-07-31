from django.apps import AppConfig

class RiccoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ricco_app'

    # Este método se ejecuta cuando se inicia el servidor Django
    def ready(self):
        from django.contrib.auth import get_user_model
        from django.db.utils import OperationalError, ProgrammingError
        from django.core.management import call_command

        try:
            # 🟡 Aplicamos migraciones pendientes automáticamente
            call_command('migrate')
            print("✅ Migraciones aplicadas")

            # 🔐 Obtenemos el modelo de usuario personalizado
            User = get_user_model()

            # ✨ Crear superusuario solo si no existe
            if not User.objects.filter(email='admin@example.com').exists():
                print('🛠️ Creando superusuario...')
                User.objects.create_superuser(
                    email='admin@example.com',
                    password='adminpassword123',
                    telefono='0000000000',        # Campo requerido personalizado
                    is_active=True,
                    is_staff=True,
                    is_superuser=True
                )
                print("✅ Superusuario creado.")
            else:
                print('✅ Superusuario ya existe.')
        
        except (OperationalError, ProgrammingError) as e:
            print("🚨 Error de base de datos al iniciar:", e)
        except Exception as e:
            print("❌ Otro error inesperado:", e)
