import os
import django

# Configuramos el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ricco.settings')
django.setup()

from django.contrib.auth import get_user_model

def crear_superuser():
    User = get_user_model()
    username = 'admin_render'  # Puedes cambiar este nombre
    email = 'admin@gmail.com'
    password = 'Admin.123'     # ¡Usa una clave que recuerdes!

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"✅ Superusuario '{username}' creado con éxito.")
    else:
        print(f"⚠️ El usuario '{username}' ya existe, no se hizo nada.")

if __name__ == "__main__":
    crear_superuser()