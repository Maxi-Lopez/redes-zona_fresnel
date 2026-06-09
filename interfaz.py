import customtkinter as ctk
from tkinter import messagebox
from calculos import analizar_enlace

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Zona Fresnel - Análisis Profesional de Enlaces")
        self.geometry("1200x900")
        self.resizable(False, False)

        self.crear_widgets()

    def crear_widgets(self):

        # Título principal
        titulo = ctk.CTkLabel(
            self,
            text="📡 Zona Fresnel",
            font=("Arial", 32, "bold")
        )
        titulo.pack(pady=(20, 5))

        subtitulo = ctk.CTkLabel(
            self,
            text="Análisis de la Primera Zona de Fresnel | Fórmula: F₁ = 8.656 × √(d₁ × d₂ / (f × D))",
            font=("Arial", 13)
        )
        subtitulo.pack(pady=(0, 20))

        # Contenedor principal
        contenedor = ctk.CTkFrame(self)
        contenedor.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )

        # Frame de entrada (izquierda)
        frame_entrada = ctk.CTkFrame(contenedor)
        frame_entrada.pack(
            side="left",
            padx=15,
            pady=15,
            fill="both",
            expand=True
        )

        # Frame de resultados (derecha)
        frame_resultado = ctk.CTkFrame(contenedor)
        frame_resultado.pack(
            side="right",
            padx=15,
            pady=15,
            fill="both",
            expand=True
        )

        # ========== SECCIÓN DE ENTRADA ==========
        ctk.CTkLabel(
            frame_entrada,
            text="📋 DATOS DE ENTRADA",
            font=("Arial", 20, "bold")
        ).pack(pady=(15, 20))

        # Campos de entrada
        self.altura_a = self.crear_campo(
            frame_entrada,
            "🏗️ Altura Antena A (m)"
        )

        self.altura_b = self.crear_campo(
            frame_entrada,
            "🏗️ Altura Antena B (m)"
        )

        self.distancia_total = self.crear_campo(
            frame_entrada,
            "📏 Distancia Total (km)"
        )

        self.frecuencia = self.crear_campo(
            frame_entrada,
            "📡 Frecuencia (MHz)"
        )

        self.altura_obstaculo = self.crear_campo(
            frame_entrada,
            "⛰️ Altura del Obstáculo (m)"
        )

        self.distancia_obstaculo = self.crear_campo(
            frame_entrada,
            "📍 Distancia del Obstáculo desde A (km)"
        )


        # Botón de cálculo
        boton = ctk.CTkButton(
            frame_entrada,
            text="🔍 CALCULAR ENLACE",
            height=50,
            font=("Arial", 16, "bold"),
            command=self.calcular
        )
        boton.pack(padx=30, pady=20, fill="x")

        # ========== SECCIÓN DE RESULTADOS ==========
        ctk.CTkLabel(
            frame_resultado,
            text="📊 RESULTADOS DEL ANÁLISIS",
            font=("Arial", 20, "bold")
        ).pack(pady=(15, 20))

        # Estado general con indicador
        self.frame_estado = ctk.CTkFrame(frame_resultado, fg_color="transparent")
        self.frame_estado.pack(pady=(10, 15))
        
        self.indicador_estado = ctk.CTkLabel(
            self.frame_estado,
            text="●",
            font=("Arial", 28),
            text_color="gray"
        )
        self.indicador_estado.pack(side="left", padx=(0, 10))
        
        self.estado = ctk.CTkLabel(
            self.frame_estado,
            text="⚡ ESPERANDO CÁLCULO",
            font=("Arial", 24, "bold")
        )
        self.estado.pack(side="left")

        # Separador
        separador1 = ctk.CTkFrame(frame_resultado, height=2, fg_color="gray")
        separador1.pack(fill="x", padx=20, pady=10)

        # Métricas principales en 2 columnas
        frame_metricas = ctk.CTkFrame(frame_resultado, fg_color="transparent")
        frame_metricas.pack(pady=10, fill="both", expand=True)

        # Columna izquierda de métricas
        col_izq = ctk.CTkFrame(frame_metricas, fg_color="transparent")
        col_izq.pack(side="left", padx=10, fill="both", expand=True)

        # Columna derecha de métricas
        col_der = ctk.CTkFrame(frame_metricas, fg_color="transparent")
        col_der.pack(side="right", padx=10, fill="both", expand=True)

        # Porcentajes (Columna izquierda)
        ctk.CTkLabel(
            col_izq,
            text="📈 NIVEL DE OBSTRUCCIÓN",
            font=("Arial", 14, "bold")
        ).pack(pady=(5, 10))

        self.progressbar = ctk.CTkProgressBar(
            col_izq,
            width=250,
            height=25,
            corner_radius=12
        )
        self.progressbar.pack(pady=5)
        self.progressbar.set(0)

        self.lbl_libre = ctk.CTkLabel(
            col_izq,
            text="✅ Zona libre: -",
            font=("Arial", 15),
            anchor="w"
        )
        self.lbl_libre.pack(pady=5)

        self.lbl_obstruida = ctk.CTkLabel(
            col_izq,
            text="❌ Zona obstruida: -",
            font=("Arial", 15),
            anchor="w"
        )
        self.lbl_obstruida.pack(pady=5)

        # Datos técnicos (Columna derecha)
        ctk.CTkLabel(
            col_der,
            text="📐 PARÁMETROS TÉCNICOS",
            font=("Arial", 14, "bold")
        ).pack(pady=(5, 10))

        self.lbl_fresnel = ctk.CTkLabel(
            col_der,
            text="📡 Radio Fresnel: -",
            font=("Arial", 14),
            anchor="w"
        )
        self.lbl_fresnel.pack(pady=5)

        self.lbl_los = ctk.CTkLabel(
            col_der,
            text="📏 Altura línea vista: -",
            font=("Arial", 14),
            anchor="w"
        )
        self.lbl_los.pack(pady=5)

        self.lbl_clearance = ctk.CTkLabel(
            col_der,
            text="🔄 Espacio libre (clearance): -",
            font=("Arial", 14),
            anchor="w"
        )
        self.lbl_clearance.pack(pady=5)

        # Separador
        separador2 = ctk.CTkFrame(frame_resultado, height=2, fg_color="gray")
        separador2.pack(fill="x", padx=20, pady=10)

        # Información adicional
        frame_info = ctk.CTkFrame(frame_resultado, fg_color="transparent")
        frame_info.pack(pady=10, fill="both", expand=True)

        ctk.CTkLabel(
            frame_info,
            text="💡 RECOMENDACIÓN",
            font=("Arial", 14, "bold")
        ).pack(pady=(5, 5))

        self.lbl_recomendacion = ctk.CTkLabel(
            frame_info,
            text="Ingrese los datos y presione calcular",
            font=("Arial", 13),
            wraplength=450,
            justify="center"
        )
        self.lbl_recomendacion.pack(pady=5)

        # Métricas de calidad de enlace
        ctk.CTkLabel(
            frame_info,
            text="📊 CALIDAD DEL ENLACE",
            font=("Arial", 14, "bold")
        ).pack(pady=(15, 5))

        frame_calidad = ctk.CTkFrame(frame_info, fg_color="transparent")
        frame_calidad.pack(pady=5)

        self.lbl_calidad = ctk.CTkLabel(
            frame_calidad,
            text="●",
            font=("Arial", 20),
            text_color="gray"
        )
        self.lbl_calidad.pack(side="left", padx=5)

        self.lbl_calidad_texto = ctk.CTkLabel(
            frame_calidad,
            text="",
            font=("Arial", 13)
        )
        self.lbl_calidad_texto.pack(side="left", padx=5)

        # Pérdidas estimadas
        self.lbl_perdidas = ctk.CTkLabel(
            frame_info,
            text="📉 Pérdidas por obstrucción: -",
            font=("Arial", 13)
        )
        self.lbl_perdidas.pack(pady=5)

        # Relación clearance/Fresnel
        self.lbl_relacion = ctk.CTkLabel(
            frame_info,
            text="📊 Relación clearance/Fresnel: -",
            font=("Arial", 13)
        )
        self.lbl_relacion.pack(pady=5)

        # Footer
        footer = ctk.CTkLabel(
            self,
            text="© 2026 - Maximiliano Lopez",
            font=("Arial", 11)
        )
        footer.pack(side="bottom", pady=15)

    def crear_campo(self, parent, texto):
        """Crea un campo de entrada con etiqueta"""
        
        ctk.CTkLabel(
            parent,
            text=texto,
            font=("Arial", 14)
        ).pack(pady=(8, 2), anchor="w")

        entrada = ctk.CTkEntry(
            parent,
            width=300,
            height=35,
            font=("Arial", 13)
        )
        entrada.pack(pady=(0, 10), fill="x")
        
        return entrada

    def calcular_perdidas_estimadas(self, porcentaje_obstruido, radio_fresnel, clearance):
        """Calcula pérdidas estimadas en dB según obstrucción"""
        if radio_fresnel == 0:
            return "0 dB (sin pérdidas - obstáculo en la antena)"
        
        if porcentaje_obstruido <= 0:
            return "0 dB (sin pérdidas)"
        elif porcentaje_obstruido < 20:
            return f"{porcentaje_obstruido * 0.15:.1f} dB (pérdidas mínimas)"
        elif porcentaje_obstruido <= 40:
            return f"{3 + (porcentaje_obstruido - 20) * 0.2:.1f} dB (pérdidas moderadas)"
        elif porcentaje_obstruido <= 60:
            return f"{7 + (porcentaje_obstruido - 40) * 0.3:.1f} dB (pérdidas significativas)"
        else:
            return f"> 15 dB (pérdidas severas - enlace no recomendado)"

    def calcular_calidad_enlace(self, porcentaje_obstruido, clearance, radio_fresnel, altura_obstaculo):
        """Determina la calidad del enlace"""
        # Caso especial: no hay obstáculo
        if altura_obstaculo == 0:
            return "🌟 EXCELENTE", "Sin obstáculo - Enlace óptimo"
        
        if radio_fresnel == 0:
            if clearance >= 0:
                return "🌟 EXCELENTE", "Obstáculo en antena - Sin efecto en el enlace"
            else:
                return "🚫 NULO", "Obstáculo bloquea la antena - Enlace imposible"
        
        if porcentaje_obstruido == 0:
            return "🌟 EXCELENTE", "Calidad premium - Enlace óptimo"
        elif porcentaje_obstruido < 20:
            return "✅ BUENA", "Calidad aceptable - Funciona correctamente"
        elif porcentaje_obstruido <= 40:
            return "⚠️ REGULAR", "Calidad degradada - Posibles intermitencias"
        elif porcentaje_obstruido <= 60:
            return "❌ MALA", "Calidad pobre - No recomendado para aplicaciones críticas"
        else:
            return "🚫 NULA", "Enlace inviable - Se requiere rediseño"

    def calcular(self):
        """Realiza el cálculo del enlace"""
        
        try:
            # Obtener valores
            altura_a = float(self.altura_a.get())
            altura_b = float(self.altura_b.get())
            distancia_total = float(self.distancia_total.get())
            distancia_obstaculo = float(self.distancia_obstaculo.get())
            altura_obstaculo = float(self.altura_obstaculo.get())
            frecuencia = float(self.frecuencia.get())

            # Validaciones
            if altura_a <= 0 or altura_b <= 0:
                raise ValueError("Las alturas de las antenas deben ser mayores a cero.")

            if distancia_total <= 0:
                raise ValueError("La distancia total debe ser mayor a cero.")

            if frecuencia <= 0:
                raise ValueError("La frecuencia debe ser mayor a cero.")

            if altura_obstaculo < 0:
                raise ValueError("La altura del obstáculo no puede ser negativa.")

            if distancia_obstaculo < 0:
                raise ValueError("La distancia del obstáculo no puede ser negativa.")

            if distancia_obstaculo > distancia_total:
                raise ValueError("La distancia del obstáculo no puede superar la distancia total.")

            # Calcular
            resultado = analizar_enlace(
                altura_a,
                altura_b,
                distancia_total,
                distancia_obstaculo,
                altura_obstaculo,
                frecuencia
            )

            # Actualizar estado principal
            self.estado.configure(
                text=resultado["estado"],
                text_color=resultado["color"]
            )
            
            # Actualizar indicador de estado
            if resultado["porcentaje_obstruido"] == 0:
                self.indicador_estado.configure(text_color="green")
            elif resultado["porcentaje_obstruido"] < 40:
                self.indicador_estado.configure(text_color="#FFC107")
            else:
                self.indicador_estado.configure(text_color="#F44336")

            # Actualizar porcentajes
            self.lbl_libre.configure(
                text=f"✅ Zona libre: {resultado['porcentaje_libre']} %"
            )
            self.lbl_obstruida.configure(
                text=f"❌ Zona obstruida: {resultado['porcentaje_obstruido']} %"
            )

            # Actualizar barra de progreso
            obstruccion = resultado["porcentaje_obstruido"] / 100
            self.progressbar.set(obstruccion)
            
            if obstruccion == 0:
                self.progressbar.configure(progress_color="green")
            elif obstruccion <= 0.40:
                self.progressbar.configure(progress_color="#FFC107")
            else:
                self.progressbar.configure(progress_color="#F44336")

            # Actualizar parámetros técnicos
            self.lbl_fresnel.configure(
                text=f"📡 Radio Fresnel: {resultado['radio_fresnel_m']} m"
            )
            self.lbl_los.configure(
                text=f"📏 Altura línea vista: {resultado['altura_linea_vista_m']} m"
            )
            
            clearance = resultado['clearance_m']
            self.lbl_clearance.configure(
                text=f"🔄 Espacio libre (clearance): {clearance} m"
            )
            
            # Cambiar color del clearance según su valor
            if resultado['radio_fresnel_m'] == 0:
                if clearance >= 0:
                    self.lbl_clearance.configure(text_color="#4CAF50")
                else:
                    self.lbl_clearance.configure(text_color="#F44336")
            elif clearance < 0:
                self.lbl_clearance.configure(text_color="#F44336")
            elif clearance < resultado['radio_fresnel_m']:
                self.lbl_clearance.configure(text_color="#FFC107")
            else:
                self.lbl_clearance.configure(text_color="#4CAF50")

            # Actualizar recomendación
            self.lbl_recomendacion.configure(
                text=resultado["recomendacion"]
            )

            # Calcular y mostrar calidad del enlace
            calidad, descripcion = self.calcular_calidad_enlace(
                resultado["porcentaje_obstruido"],
                clearance,
                resultado['radio_fresnel_m'],
                altura_obstaculo
            )
            
            # Asignar color según calidad
            if "EXCELENTE" in calidad:
                color_calidad = "gold"
            elif "BUENA" in calidad:
                color_calidad = "#4CAF50"
            elif "REGULAR" in calidad:
                color_calidad = "#FFC107"
            elif "MALA" in calidad:
                color_calidad = "#FF9800"
            else:
                color_calidad = "#F44336"
            
            self.lbl_calidad.configure(text_color=color_calidad)
            self.lbl_calidad_texto.configure(text=f"{calidad} - {descripcion}", text_color=color_calidad)

            # Calcular y mostrar pérdidas estimadas
            perdidas = self.calcular_perdidas_estimadas(
                resultado["porcentaje_obstruido"],
                resultado['radio_fresnel_m'],
                clearance
            )
            self.lbl_perdidas.configure(text=f"📉 Pérdidas por obstrucción: {perdidas}")

            # Calcular relación clearance/Fresnel
            if resultado['radio_fresnel_m'] > 0:
                relacion = clearance / resultado['radio_fresnel_m']
                if relacion >= 1:
                    self.lbl_relacion.configure(
                        text=f"📊 Relación clearance/Fresnel: {relacion:.2f} (✅ Despejado)",
                        text_color="#4CAF50"
                    )
                elif relacion >= 0.6:
                    self.lbl_relacion.configure(
                        text=f"📊 Relación clearance/Fresnel: {relacion:.2f} (⚠️ Aceptable)",
                        text_color="#FFC107"
                    )
                else:
                    self.lbl_relacion.configure(
                        text=f"📊 Relación clearance/Fresnel: {relacion:.2f} (❌ Insuficiente)",
                        text_color="#F44336"
                    )
            else:
                if altura_obstaculo == 0:
                    self.lbl_relacion.configure(
                        text="📊 Relación clearance/Fresnel: N/A (Sin obstáculo)",
                        text_color="#4CAF50"
                    )
                else:
                    self.lbl_relacion.configure(
                        text="📊 Relación clearance/Fresnel: N/A (Obstáculo en antena)",
                        text_color="gray"
                    )

        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")
