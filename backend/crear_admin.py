import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ricco.settings')
django.setup()

from django.contrib.auth import get_user_model

def crear_superuser():
    User = get_user_model()
    # Solo usamos email y password como me dijiste
    email = 'admin@mail.com' 
    password = 'Admin.1234'

    if not User.objects.filter(email=email).exists():
        # Pasamos los argumentos como nombres para que no haya error de posición
        User.objects.create_superuser(email=email, password=password)
        print(f"✅ Superusuario con email '{email}' creado con éxito.")
    else:
        print(f"⚠️ El usuario con email '{email}' ya existe.")

if __name__ == "__main__":
    crear_superuser()