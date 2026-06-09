import math

def truncar(numero, decimales=2):
    """Trunca un número a los decimales especificados"""
    if numero is None or math.isnan(numero):
        return 0.0
    factor = 10 ** decimales
    return math.trunc(numero * factor) / factor

def calcular_fresnel(distancia_total_km, frecuencia_ghz, distancia_obstaculo_km):
    """
    Calcula el radio de la primera zona de Fresnel
    FÓRMULA: F₁ = 8.656 × √(d₁ × d₂ / (f × D))
    """
    if distancia_total_km <= 0 or frecuencia_ghz <= 0:
        return 0.0
    
    if distancia_obstaculo_km < 0 or distancia_obstaculo_km > distancia_total_km:
        return 0.0
    
    d1 = distancia_obstaculo_km
    d2 = distancia_total_km - distancia_obstaculo_km
    
    if d1 == 0 or d2 == 0:
        return 0.0
    
    return 8.656 * math.sqrt((d1 * d2) / (frecuencia_ghz * distancia_total_km))

def calcular_linea_vista(altura_a, altura_b, distancia_total, distancia_obstaculo):
    """Calcula la altura de la línea de vista"""
    if distancia_total <= 0:
        return altura_a
    
    if distancia_obstaculo <= 0:
        return altura_a
    if distancia_obstaculo >= distancia_total:
        return altura_b
    
    return altura_a + ((altura_b - altura_a) * (distancia_obstaculo / distancia_total))

def analizar_enlace(altura_a, altura_b, distancia_total_km, distancia_obstaculo_km, 
                   altura_obstaculo, frecuencia_mhz):
    """
    Analiza un enlace de microondas
    """
    
    # ========== CASO ESPECIAL: NO HAY OBSTÁCULO ==========
    # Si la altura del obstáculo es 0, significa que no hay obstáculo
    if altura_obstaculo == 0:
        radio_fresnel = calcular_fresnel(
            distancia_total_km,
            frecuencia_mhz / 1000.0,
            distancia_obstaculo_km
        )
        
        altura_linea_vista = calcular_linea_vista(
            altura_a,
            altura_b,
            distancia_total_km,
            distancia_obstaculo_km
        )
        
        clearance = altura_linea_vista - 0
        
        return {
            "radio_fresnel_m": truncar(radio_fresnel),
            "altura_linea_vista_m": truncar(altura_linea_vista),
            "clearance_m": truncar(clearance),
            "porcentaje_libre": 100.0,
            "porcentaje_obstruido": 0.0,
            "estado": "EXCELENTE",
            "color": "green",
            "recomendacion": "No hay obstáculo - Zona de Fresnel completamente despejada",
            "fresnel_requerido_m": truncar(radio_fresnel)
        }
    
    # ========== CASO ESPECIAL: OBSTÁCULO EN LA ANTENA ==========
    # Si el obstáculo está exactamente en la posición de una antena
    if distancia_obstaculo_km <= 0 or distancia_obstaculo_km >= distancia_total_km:
        radio_fresnel = calcular_fresnel(
            distancia_total_km,
            frecuencia_mhz / 1000.0,
            distancia_obstaculo_km
        )
        
        altura_linea_vista = calcular_linea_vista(
            altura_a,
            altura_b,
            distancia_total_km,
            distancia_obstaculo_km
        )
        
        clearance = altura_linea_vista - altura_obstaculo
        
        if clearance >= 0:
            porcentaje_libre = 100.0
            porcentaje_obstruido = 0.0
            estado = "EXCELENTE"
            color = "green"
            recomendacion = "Obstáculo en la posición de la antena - No afecta el enlace"
        else:
            porcentaje_libre = 0.0
            porcentaje_obstruido = 100.0
            estado = "NO FUNCIONA"
            color = "#F44336"
            recomendacion = "Obstáculo bloquea la antena - Enlace imposible"
        
        return {
            "radio_fresnel_m": truncar(radio_fresnel),
            "altura_linea_vista_m": truncar(altura_linea_vista),
            "clearance_m": truncar(clearance),
            "porcentaje_libre": truncar(porcentaje_libre),
            "porcentaje_obstruido": truncar(porcentaje_obstruido),
            "estado": estado,
            "color": color,
            "recomendacion": recomendacion,
            "fresnel_requerido_m": truncar(radio_fresnel)
        }
    
    # ========== CASO NORMAL: HAY UN OBSTÁCULO REAL ==========
    # Convertir MHz a GHz
    frecuencia_ghz = frecuencia_mhz / 1000.0
    
    # Calcular radio de Fresnel
    radio_fresnel = calcular_fresnel(
        distancia_total_km,
        frecuencia_ghz,
        distancia_obstaculo_km
    )
    
    # Calcular altura de línea de vista en el obstáculo
    altura_linea_vista = calcular_linea_vista(
        altura_a,
        altura_b,
        distancia_total_km,
        distancia_obstaculo_km
    )
    
    # Calcular clearance
    clearance = altura_linea_vista - altura_obstaculo
    
    # Caso: Radio Fresnel es 0 (frecuencia muy alta o distancias extremas)
    if radio_fresnel == 0:
        if clearance >= 0:
            porcentaje_libre = 100.0
            porcentaje_obstruido = 0.0
        else:
            porcentaje_libre = 0.0
            porcentaje_obstruido = 100.0
    
    # Caso: Clearance mayor o igual al radio Fresnel (totalmente despejado)
    elif clearance >= radio_fresnel:
        porcentaje_libre = 100.0
        porcentaje_obstruido = 0.0
    
    # Caso: Clearance negativo (obstáculo toca o supera línea de vista)
    elif clearance <= 0:
        porcentaje_libre = 0.0
        porcentaje_obstruido = 100.0
    
    # Caso: Obstrucción parcial
    else:
        porcentaje_libre = (clearance / radio_fresnel) * 100
        porcentaje_obstruido = 100 - porcentaje_libre
        
        # Limitar entre 0 y 100
        porcentaje_libre = max(0, min(100, porcentaje_libre))
        porcentaje_obstruido = max(0, min(100, porcentaje_obstruido))
    
    # Determinar estado y recomendación
    if porcentaje_obstruido == 0:
        estado = "EXCELENTE"
        color = "green"
        recomendacion = "Zona de Fresnel completamente despejada - Enlace óptimo"
    
    elif porcentaje_obstruido < 20:
        estado = "OPTIMO"
        color = "#4CAF50"
        recomendacion = f"Obstrucción del {truncar(porcentaje_obstruido)}% - Pérdidas mínimas (menos de 3 dB)"
    
    elif porcentaje_obstruido <= 40:
        estado = "PUEDE FUNCIONAR"
        color = "#FFC107"
        recomendacion = f"Obstrucción del {truncar(porcentaje_obstruido)}% - Pérdidas moderadas (3-6 dB)"
    
    elif porcentaje_obstruido <= 60:
        estado = "CRITICO"
        color = "#FF9800"
        recomendacion = f"Obstrucción del {truncar(porcentaje_obstruido)}% - Pérdidas significativas (6-12 dB)"
    
    else:
        estado = "NO FUNCIONA"
        color = "#F44336"
        recomendacion = f"Obstrucción del {truncar(porcentaje_obstruido)}% - Enlace inviable, se requiere elevar antenas"
    
    return {
        "radio_fresnel_m": truncar(radio_fresnel),
        "altura_linea_vista_m": truncar(altura_linea_vista),
        "clearance_m": truncar(clearance),
        "porcentaje_libre": truncar(porcentaje_libre),
        "porcentaje_obstruido": truncar(porcentaje_obstruido),
        "estado": estado,
        "color": color,
        "recomendacion": recomendacion,
        "fresnel_requerido_m": truncar(radio_fresnel)
    }