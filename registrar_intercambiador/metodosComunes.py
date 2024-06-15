from datetime import datetime, timedelta
from .exceptions import edadInvalida

def verificar_edad(fecha_nacimiento_str):
    # Convertir la fecha ingresada a un objeto datetime
    fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d')
    
    # Calcular la edad
    hoy = datetime.now()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    
    # Verificar si la persona tiene al menos 18 años
    return ((edad >= 18) and (edad <= 100))




