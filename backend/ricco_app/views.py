from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from django.http import JsonResponse
import json
import mercadopago
from datetime import datetime
from .serializers import UsuarioSerializers,RegistroSerializers, RolSerializer, ProductoSerializer, DireccionSerializer, CompraSerializer,DetalleSerializer, PedidoSerializer,PermisoSerializer, Rol_PermisoSerializer, PerfilUsuarioSerializer
from .models import Rol, Producto,Direccion, Compra,Detalle,Pedido,Permiso, Rol_Permiso
from django.conf import settings
from django.utils import timezone
from ricco_app.permissions import EsAdministradorPorRol
import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser

sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

User = get_user_model()


def bienvenida (request): 
    message = """
    <h1>Bienvenido a RICCO BURGUER</h1>
    <p>Gracias por visitar nuestra aplicación. Aquí puedes acceder a las siguientes secciones:</p>
    
    <h2>1. Acceso al Panel de Administración:</h2>
    <p>Para acceder al panel de administración de Django, ve a <a href="/admin/">/admin/</a>.</p>
    
    
    <h2>2. Acceso a las API:</h2>
    <p>Para interactuar con las API, puedes acceder a las siguientes rutas:</p>
    <ul>        
        <li><a href="/api/rol/">/api/rol/</a></li>
        <li><a href="/api/producto/">/api/producto/</a></li>
    </ul>
    <p>Recuerda que estas rutas corresponden a la API de nuestra aplicación.</p>
    """
    return HttpResponse(message)
logger = logging.getLogger(__name__)

#______________________________________
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_pagos_view(request):
    
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        user = User.objects.get(id=data["user"])
    except Exception as e:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    try:
        total = 0
        items = []

        for detalle_data in data["detalles"]:
            producto = Producto.objects.get(id_producto=detalle_data["id_producto"])  # pylint: disable=no-member
            cantidad = int(detalle_data["cantidad"])
            if producto.stock < cantidad:
                return JsonResponse({"error": f"Stock insuficiente para {producto.nombre_producto}"}, status=400)

        compra = Compra.objects.create(  # pylint: disable=no-member
            descripcion="",
            user=user,
            fecha=datetime.now(),
            precio_total=0.0,
            estado="pendiente",
        )

        for detalle_data in data["detalles"]:
            producto = Producto.objects.get(id_producto=detalle_data["id_producto"])  # pylint: disable=no-member
            cantidad = int(detalle_data["cantidad"])
            precio_unitario = float(producto.precio)
            precio_calculado = cantidad * precio_unitario
            total += precio_calculado

            Detalle.objects.create(  # pylint: disable=no-member
                cantidad=cantidad,
                precio_calculado=precio_calculado,
                producto=producto,
                compra=compra,
            )

            producto.stock -= cantidad
            producto.save()

            items.append({
                "title": producto.nombre_producto,
                "quantity": cantidad,
                "unit_price": precio_unitario,
                "currency_id": "ARS",
            })

        compra.precio_total = total
        compra.descripcion = ", ".join([
            f"{d['cantidad']} {Producto.objects.get(id_producto=d['id_producto']).nombre_producto}"  # pylint: disable=no-member
            for d in data["detalles"]])  
        compra.save()

        # 🔁 Redirección directa a Google según estado
        preference_data = {
            "items": items,
            "back_urls": {
                "success": "https://www.google.com/?estado=aprobado",
                "failure": "https://www.google.com/?estado=rechazado",
                "pending": "https://www.google.com/?estado=pendiente",
            },
            "auto_return": "approved",
            "metadata": {"compra_id": compra.id_compra},
        }

        preference_response = sdk.preference().create(preference_data)

        if preference_response.get("status") != 201:
            return JsonResponse({"error": "Error al generar preferencia"}, status=500)

        return JsonResponse({
            "init_point": preference_response["response"]["init_point"],
            "preference_id": preference_response["response"]["id"],
        }, status=201)

    except Exception as e:        
        return JsonResponse({"error": str(e)}, status=500)

class CancelarPedidoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id_compra):
        print(f"Recibiendo solicitud para cancelar la compra con id: {id_compra}")
        try:
            compra = Compra.objects.get(id_compra=id_compra, user=request.user) # pylint: disable=no-member   
            print(f"Compra encontrada: {compra}")

            # Verifica si ya fue cancelada
            if compra.estado == 'cancelado':
                return Response({'error': 'Esta compra ya fue cancelada.'}, status=status.HTTP_400_BAD_REQUEST)

            # Verifica que la fecha de cancelación no sea None
            if compra.cancelable_hasta is None:
                print(f"Fecha de cancelación excedida. Ahora: {timezone.now()} - Cancelable hasta: {compra.cancelable_hasta}") 
                return Response({'error': 'La fecha de cancelación no está definida para esta compra.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            # Compara con la zona horaria correcta
            if timezone.now() > compra.cancelable_hasta:
                return Response({'error': 'Ya no puedes cancelar esta compra.'}, status=status.HTTP_400_BAD_REQUEST)

            # Cancela la compra
            compra.estado = 'cancelado'
            compra.save()
            print(f"Compra {compra.id_compra} cancelada exitosamente")


            return Response({'mensaje': 'Compra cancelada exitosamente.'}, status=status.HTTP_200_OK)

        except Compra.DoesNotExist: # pylint: disable=no-member   
            logger.error(f"Compra no encontrada o no pertenece al usuario. ID: {id_compra}")
            print(f"Compra no encontrada o no pertenece al usuario. ID: {id_compra}")
            return Response({'error': 'Compra no encontrada o no pertenece al usuario.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception(f"Error inesperado al cancelar compra ID: {id_compra}. Excepción: {str(e)}")
            print(f"Error inesperado al cancelar la compra {id_compra}: {str(e)}")
            return Response({'error': f'Error inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    #@method_decorator(csrf_exempt)
    permission_classes=[AllowAny]
    def post(self, request):
        print(f"Datos recibidos en la solicitud: {request.data}")
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        print(f"Intentando autenticar con email: {email}, password: {password}")
        usuario = authenticate(request, username=email, password=password)
        print(f"Resultado de autenticate():{usuario}")

        if usuario:
            login(request, usuario)
            isAdmin = usuario.is_staff
            tokens = self.get_tokens_for_user(usuario)
            user_data = UsuarioSerializers(usuario).data
            return Response({
    'token': tokens['access'],
    'access': tokens['access'],
    'refresh': tokens['refresh'],
    'user': UsuarioSerializers(usuario).data
}, status=status.HTTP_200_OK)


        else:
            return Response({'error': 'Credenciales de inicio de sesión incorrectas'}, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        refresh['first_name'] = user.first_name 
        refresh['last_name'] = user.last_name
        refresh['is_staff'] = user.is_staff 
        access = refresh.access_token 
        access['first_name'] = user.first_name 
        access['last_name'] = user.last_name
        access['is_staff']= user.is_staff 
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def get(self, request):
        return Response(data={'message': 'GET request processed successfully'})
class LogoutView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
    

class RegistroView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistroSerializers
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')

        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                # Reactivar y actualizar usuario inactivo
                user.first_name = data.get('first_name', user.first_name)
                user.last_name = data.get('last_name', user.last_name)
                user.telefono = data.get('telefono', user.telefono)
                if 'password' in data:
                    user.set_password(data['password'])
                user.is_active = True
                user.save()

                token, _ = Token.objects.get_or_create(user=user) # pylint: disable=no-member   
                serializer = self.serializer_class(user)
                return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Este correo ya está registrado.'}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            # Crear nuevo usuario normalmente
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                user = serializer.save()
                token, _ = Token.objects.get_or_create(user=user) # pylint: disable=no-member   
                return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class PerfilUsuarioView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PerfilUsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
 
class RolViewSet(viewsets.ModelViewSet):
    queryset=Rol.objects.all() # pylint: disable=no-member   
    serializer_class= RolSerializer
 
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all() # pylint: disable=no-member    
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id_producto'  
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        print(f"Usuario autenticado en productos: {user} - Is staff: {getattr(user, 'is_staff', False)}")
        if user.is_authenticated and user.is_staff:
            
            return Producto.objects.all() # pylint: disable=no-member   
        else:
            
            return Producto.objects.filter(visible=True) # pylint: disable=no-member   

    def get_serializer_context(self):
        return {'request': self.request}  
    
    def create(self, request, *args, **kwargs):
      print("Datos recibidos EN EL BACKEND:", request.data)
      serializer = self.get_serializer(data=request.data)
      if not serializer.is_valid():
        print("Errores de validación:", serializer.errors)
      return super().create(request, *args, **kwargs)

 
class DireccionViewSet(viewsets.ModelViewSet):
    queryset=Direccion.objects.all() # pylint: disable=no-member   
    serializer_class= DireccionSerializer

class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all() # pylint: disable=no-member   
    serializer_class = CompraSerializer   
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        compras = Compra.objects.select_related('user').all() # pylint: disable=no-member   
        for compra in compras:
            print(f'Compra ID: {compra.id}, Usuario: {compra.user.first_name} {compra.user.last_name}')
        return compras

@method_decorator(csrf_exempt, name='dispatch')
class CambiarEstadoCompraAPIView(APIView):
    permission_classes = [EsAdministradorPorRol]  

    def patch(self, request, pk):
        print("ROL:", getattr(request.user.rol, 'nombre_rol', 'Sin rol'))
        try:
            compra = Compra.objects.get(pk=pk) # pylint: disable=no-member   
        except Compra.DoesNotExist: # pylint: disable=no-member   
            return Response({'error': 'Compra no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        nuevo_estado = request.data.get('estado')
        if not nuevo_estado:
            return Response({'error': 'Debe proporcionar un estado'}, status=status.HTTP_400_BAD_REQUEST)
        
        if nuevo_estado not in dict(Compra.ESTADO_CHOICES):
            return Response({'error': 'Estado inválido'}, status=status.HTTP_400_BAD_REQUEST)

        compra.estado = nuevo_estado
        compra.save()

        return Response({'mensaje': f'Estado actualizado a {nuevo_estado}'}, status=status.HTTP_200_OK)
    
class MisComprasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        compras = Compra.objects.filter(user=request.user) # pylint: disable=no-member   

        for compra in compras:
            # Si el estado es pendiente y ya venció el tiempo de cancelación
            if (
                compra.estado == 'pendiente'
                and compra.cancelable_hasta
                and timezone.now() > compra.cancelable_hasta
            ):
                compra.estado = 'En Preparación'
                compra.save()

        serializer = CompraSerializer(compras, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data.pop('descripcion', None)  # Elimina si viene del frontend
        data['user'] = request.user.id
        serializer = CompraSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class TodasComprasView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        
        print("Encabezados de la solicitud:", request.headers)

        if (not request.user.is_staff) and (not request.user.rol or request.user.rol.nombre_rol != "Administrador"):
            print(f"Acceso denegado: el rol del usuario es {request.user.rol.nombre_rol if request.user.rol else 'ninguno'}")
            return Response(
                {"error": "No tienes permisos para acceder a este recurso."},
                status=403
            )

        compras = Compra.objects.all() # pylint: disable=no-member   
        print("Compras obtenidas en el backend:")
        for compra in compras:
            usuario_email = compra.user.email if compra.user else "Usuario eliminado"
            print(f"Compra ID: {compra.id_compra}, Usuario: {compra.user.email}, Total: {compra.precio_total}")  

        serializer = CompraSerializer(compras, many=True)
        return Response(serializer.data)

    def post(self, request):
        
        print("Encabezados de la solicitud:", request.headers)

        if not request.user.rol or request.user.rol.nombre_rol != "Administrador":
            print(f"Acceso denegado: el rol del usuario es {request.user.rol.nombre_rol if request.user.rol else 'ninguno'}")
            return Response(
                {"error": "No tienes permisos para acceder a este recurso."},
                status=403
            )

        data = request.data
        serializer = CompraSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print("Compra creada con éxito:", serializer.data)
            return Response(serializer.data, status=201)
        print("Errores en la creación de la compra:", serializer.errors)
        return Response(serializer.errors, status=400)

    
class DetalleViewSet(viewsets.ModelViewSet):
    queryset=Detalle.objects.all() # pylint: disable=no-member   
    serializer_class= DetalleSerializer  
    
 
class PermisoViewSet(viewsets.ModelViewSet):
    queryset=Permiso.objects.all() # pylint: disable=no-member   
    serializer_class= PermisoSerializer                
    
class Rol_PermisoViewSet(viewsets.ModelViewSet):
    queryset=Rol_Permiso.objects.all() # pylint: disable=no-member   
    serializer_class= Rol_PermisoSerializer        
       
class PedidoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Pedido.objects.all() # pylint: disable=no-member   
    serializer_class = PedidoSerializer 

    def create(self, request, *args, **kwargs):
        print("Datos recibidos:", request.data)  # Ver qué datos están llegando
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            pedido = serializer.save()
            print("Pedido registrado con éxito:", pedido)
            return Response(serializer.data, status=201)
        print("Errores al registrar pedido:", serializer.errors)  # Ver errores específicos
        return Response(serializer.errors, status=400)
class AdminView(APIView):
    permission_classes = [IsAdminUser]  

    def get(self, request):
        print(f"GET llamado por: {request.user}")
        return Response({"message": "Bienvenido al panel de administración"}, status=status.HTTP_200_OK)    

class ActualizarComprasView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ahora = timezone.now()
        compras_actualizadas = []

        compras = Compra.objects.filter(estado='pendiente', cancelable_hasta__lt=ahora) # pylint: disable=no-member   
        for compra in compras:
            compra.estado = 'preparacion'
            compra.save()
            compras_actualizadas.append(compra.id_compra)

        return Response({
            "mensaje": f"Se actualizaron {len(compras_actualizadas)} compras.",
            "compras_actualizadas": compras_actualizadas
        })
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def desactivar_cuenta(request):
    user = request.user
    user.is_active = False
    user.deleted_at = timezone.now()
    user.save()

    return Response({'mensaje': 'Cuenta ha sido eliminada exitosamente.'}, status=200)
#______________________________________
# Lo nuevo para Mercado Pago
# @csrf_exempt
# def crear_pagos_view(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             user = User.objects.get(id=data["user"])

#             total = 0
#             items = []
#             descripcion_items = []

#             # Verificar stock y armar detalles
#             for detalle_data in data["detalles"]:
#                 producto = Producto.objects.get(id_producto=detalle_data["id_producto"])
#                 cantidad = int(detalle_data["cantidad"])

#                 if producto.stock < cantidad:
#                     return JsonResponse({
#                         "error": f"Stock insuficiente para {producto.nombre_producto}"
#                     }, status=400)

#             # Crear compra
#             compra = Compra.objects.create(
#                 descripcion="",
#                 user=user,
#                 fecha=datetime.now(),
#                 precio_total=0.0,
#                 estado="pendiente"
#             )

#             # Crear detalles + descontar stock
#             for detalle_data in data["detalles"]:
#                 producto = Producto.objects.get(id_producto=detalle_data["id_producto"])
#                 cantidad = int(detalle_data["cantidad"])
#                 precio_unitario = float(producto.precio)
#                 precio_calculado = cantidad * precio_unitario
#                 total += precio_calculado

#                 Detalle.objects.create(
#                     cantidad=cantidad,
#                     precio_calculado=precio_calculado,
#                     producto=producto,
#                     compra=compra
#                 )

#                 producto.stock -= cantidad
#                 producto.save()

#                 descripcion_items.append(f"{cantidad} {producto.nombre_producto}")

#                 items.append({
#                     "title": producto.nombre_producto,
#                     "quantity": cantidad,
#                     "unit_price": precio_unitario,
#                     "currency_id": "ARS",
#                 })

#             compra.precio_total = total
#             compra.descripcion = ", ".join(descripcion_items)
#             compra.save()

#             # Crear preferencia Mercado Pago
#             preference_data = {
#                 "items": items,
#                 "back_urls": {
#                     "success": "https://ricco-web-frontend.onrender.com/pago-exitoso",
#                     "failure": "https://ricco-web-frontend.onrender.com/pago-fallido",
#                     "pending": "https://ricco-web-frontend.onrender.com/pago-pendiente",
#                 },
#                 "auto_return": "approved",
#                 "notification_url": "https://ricco-backend.onrender.com/webhook/mercadopago/",
#                 "metadata": {
#                     "compra_id": compra.id_compra
#                 }
#             }

#             preference_response = sdk.preference().create(preference_data)
#             if preference_response["status"] != 201:
#                 return JsonResponse({
#                     "error": "Error al generar preferencia",
#                     "detalle": preference_response["response"]
#                 }, status=500)

#             return JsonResponse({
#                 "init_point": preference_response["response"]["init_point"],
#                 "preference_id": preference_response["response"]["id"]
#             }, status=201)

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"error": "Método no permitido"}, status=405)


# @csrf_exempt
# def mercadopago_webhook(request):
#     if request.method == "GET":
#         # Mercado Pago usa GET para verificar el endpoint
#         return JsonResponse({"message": "Webhook OK"}, status=200)

#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             print("Webhook recibido:", data)

#             payment_id = None
#             if "data" in data and "id" in data["data"]:
#                 payment_id = data["data"]["id"]
#             elif "id" in data:
#                 payment_id = data["id"]

#             if not payment_id:
#                 return JsonResponse({"error": "Falta payment_id"}, status=400)

#             # Consultar pago en Mercado Pago
#             payment_info = sdk.payment().get(payment_id)
#             status_pago = payment_info["response"]["status"]
#             compra_id = payment_info["response"]["metadata"].get("compra_id")

#             if compra_id:
#                 compra = Compra.objects.get(id_compra=compra_id)

#                 # Mapear estados de Mercado Pago a tus estados internos
#                 estados_validos = {
#                     "approved": "preparacion",
#                     "pending": "pendiente",
#                     "rejected": "cancelado",
#                 }
#                 compra.estado = estados_validos.get(status_pago, "pendiente")
#                 compra.save()

#             return JsonResponse({"message": "OK"}, status=200)

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"error": "Método no permitido"}, status=405)
