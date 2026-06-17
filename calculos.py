import math

def truncar(numero, decimales=2):
    if numero is None or math.isnan(numero):
        return 0.0
    factor = 10 ** decimales
    return math.trunc(numero * factor) / factor

def calcular_fresnel(distancia_total_km, frecuencia_ghz, distancia_obstaculo_km, porcentaje=100):
    """
    Calcula el radio de la zona de Fresnel
    Args:
        distancia_total_km: Distancia total en km
        frecuencia_ghz: Frecuencia en GHz
        distancia_obstaculo_km: Distancia al obstáculo en km
        porcentaje: Porcentaje de la zona (100 para 100%, 60 para 60%)
    """
    if distancia_total_km <= 0 or frecuencia_ghz <= 0:
        return 0.0
    if distancia_obstaculo_km < 0 or distancia_obstaculo_km > distancia_total_km:
        return 0.0
    
    d1 = distancia_obstaculo_km
    d2 = distancia_total_km - distancia_obstaculo_km
    
    if d1 == 0 or d2 == 0:
        return 0.0
    
    # Fórmula: F1 = 17.32 * sqrt((d1*d2)/(f*D))
    radio = 17.32 * math.sqrt((d1 * d2) / (frecuencia_ghz * distancia_total_km))
    
    # Aplicar el porcentaje (0.6 para 60%)
    return radio * (porcentaje / 100.0)

def calcular_linea_vista(altura_a, altura_b, distancia_total, distancia_obstaculo):
    if distancia_total <= 0:
        return altura_a
    if distancia_obstaculo <= 0:
        return altura_a
    if distancia_obstaculo >= distancia_total:
        return altura_b
    return altura_a + ((altura_b - altura_a) * (distancia_obstaculo / distancia_total))

def analizar_enlace(altura_a, altura_b, distancia_total_km, distancia_obstaculo_km, altura_obstaculo, frecuencia_mhz):
    frecuencia_ghz = frecuencia_mhz / 1000.0
    
    # Calcular radio Fresnel al 100% y 60%
    radio_fresnel_100 = calcular_fresnel(
        distancia_total_km,
        frecuencia_ghz,
        distancia_obstaculo_km,
        100
    )
    
    radio_fresnel_60 = calcular_fresnel(
        distancia_total_km,
        frecuencia_ghz,
        distancia_obstaculo_km,
        60
    )
    
    altura_linea_vista = calcular_linea_vista(
        altura_a,
        altura_b,
        distancia_total_km,
        distancia_obstaculo_km
    )
    
    clearance = altura_linea_vista - altura_obstaculo
    
    # Caso especial: sin obstáculo
    if altura_obstaculo == 0:
        return {
            "radio_fresnel_m": truncar(radio_fresnel_100),
            "radio_fresnel_60_m": truncar(radio_fresnel_60),
            "altura_linea_vista_m": truncar(altura_linea_vista),
            "clearance_m": truncar(clearance),
            "porcentaje_libre": 100.0,
            "porcentaje_obstruido": 0.0,
            "estado": "EXCELENTE",
            "color": "green",
            "recomendacion": "Sin obstáculo - Zona de Fresnel completamente despejada",
            "fresnel_requerido_m": truncar(radio_fresnel_60)
        }
    
    # Caso especial: obstáculo en antenas
    if distancia_obstaculo_km <= 0 or distancia_obstaculo_km >= distancia_total_km:
        if clearance >= 0:
            return {
                "radio_fresnel_m": truncar(radio_fresnel_100),
                "radio_fresnel_60_m": truncar(radio_fresnel_60),
                "altura_linea_vista_m": truncar(altura_linea_vista),
                "clearance_m": truncar(clearance),
                "porcentaje_libre": 100.0,
                "porcentaje_obstruido": 0.0,
                "estado": "EXCELENTE",
                "color": "green",
                "recomendacion": "Obstáculo en posición de antena - No afecta el enlace",
                "fresnel_requerido_m": truncar(radio_fresnel_60)
            }
        else:
            return {
                "radio_fresnel_m": truncar(radio_fresnel_100),
                "radio_fresnel_60_m": truncar(radio_fresnel_60),
                "altura_linea_vista_m": truncar(altura_linea_vista),
                "clearance_m": truncar(clearance),
                "porcentaje_libre": 0.0,
                "porcentaje_obstruido": 100.0,
                "estado": "NO FUNCIONA",
                "color": "#F44336",
                "recomendacion": "Obstáculo bloquea la antena - Enlace imposible",
                "fresnel_requerido_m": truncar(radio_fresnel_60)
            }
    
    # Caso normal: obstáculo entre antenas
    # Calcular el porcentaje de obstrucción basado en el radio al 100%
    if radio_fresnel_100 == 0:
        if clearance >= 0:
            porcentaje_obstruido = 0
        else:
            porcentaje_obstruido = 100
    elif clearance >= radio_fresnel_100:
        porcentaje_obstruido = 0
    elif clearance <= 0:
        porcentaje_obstruido = 100
    else:
        # El clearance está entre 0 y el radio al 100%
        porcentaje_obstruido = ((radio_fresnel_100 - clearance) / radio_fresnel_100) * 100
    
    porcentaje_obstruido = max(0, min(100, porcentaje_obstruido))
    porcentaje_libre = 100 - porcentaje_obstruido
    
    # Evaluar usando el 60% como referencia (recomendación ITU-R)
    if clearance >= radio_fresnel_60:
        # Suficiente espacio libre (60% despejado)
        if porcentaje_obstruido == 0:
            estado = "EXCELENTE"
            color = "green"
            recomendacion = f"Zona de Fresnel completamente despejada - Enlace óptimo"
        elif porcentaje_obstruido < 20:
            estado = "OPTIMO"
            color = "#4CAF50"
            recomendacion = f"Obstrucción del {truncar(porcentaje_obstruido)}% - Pérdidas mínimas (< 3 dB)"
        elif porcentaje_obstruido <= 40:
            estado = "BUENO"
            color = "#8BC34A"
            recomendacion = f"Obstrucción del {truncar(porcentaje_obstruido)}% - Pérdidas moderadas (3-6 dB)"
        else:
            estado = "ACEPTABLE"
            color = "#FFC107"
            recomendacion = f"Obstrucción del {truncar(porcentaje_obstruido)}% - Se recomienda mejorar"
    elif clearance >= 0:
        # El clearance está entre 0 y el 60%
        if porcentaje_obstruido <= 60:
            estado = "CRITICO"
            color = "#FF9800"
            recomendacion = f"Obstrucción del {truncar(porcentaje_obstruido)}% - Pérdidas significativas (6-12 dB)"
        else:
            estado = "MUY CRITICO"
            color = "#FF5722"
            recomendacion = f"Obstrucción del {truncar(porcentaje_obstruido)}% - Se requiere elevar antenas"
    else:
        # Obstáculo sobre la línea de vista
        if porcentaje_obstruido <= 80:
            estado = "NO RECOMENDADO"
            color = "#F44336"
            recomendacion = f"Obstrucción del {truncar(porcentaje_obstruido)}% - Enlace muy degradado"
        else:
            estado = "NO FUNCIONA"
            color = "#D32F2F"
            recomendacion = f"Obstrucción del {truncar(porcentaje_obstruido)}% - Enlace inviable"
    
    return {
        "radio_fresnel_m": truncar(radio_fresnel_100),
        "radio_fresnel_60_m": truncar(radio_fresnel_60),
        "altura_linea_vista_m": truncar(altura_linea_vista),
        "clearance_m": truncar(clearance),
        "porcentaje_libre": truncar(porcentaje_libre),
        "porcentaje_obstruido": truncar(porcentaje_obstruido),
        "estado": estado,
        "color": color,
        "recomendacion": recomendacion,
        "fresnel_requerido_m": truncar(radio_fresnel_60)
    }