import customtkinter as ctk
from tkinter import messagebox
from calculos import analizar_enlace
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Zona Fresnel López Maxi")
        self.geometry("1550x950")
        self.resizable(False, False)

        self.crear_widgets()

    def crear_widgets(self):

        titulo = ctk.CTkLabel(
            self,
            text="📡 Zona Fresnel - Lopez Maximiliano",
            font=("Arial", 28, "bold")
        )
        titulo.pack(pady=(15, 5))

        subtitulo = ctk.CTkLabel(
            self,
            text="Analizador de Enlaces",
            font=("Arial", 12)
        )
        subtitulo.pack(pady=(0, 15))

        contenedor = ctk.CTkFrame(self)
        contenedor.pack(padx=15, pady=8, fill="both", expand=True)

        frame_controles = ctk.CTkFrame(contenedor, width=300)
        frame_controles.pack(side="left", padx=8, pady=8, fill="both", expand=True)

        frame_resultados = ctk.CTkFrame(contenedor, width=350)
        frame_resultados.pack(side="left", padx=8, pady=8, fill="both", expand=True)

        frame_visual = ctk.CTkFrame(contenedor)
        frame_visual.pack(side="right", padx=8, pady=8, fill="both", expand=True)

        # ====== CONTROLES ======
        ctk.CTkLabel(frame_controles, text="⚙️ CONFIGURACIÓN", font=("Arial", 16, "bold")).pack(pady=(10, 15))

        ctk.CTkLabel(frame_controles, text="🏗️ ANTENA A", font=("Arial", 13, "bold"), text_color="#4CAF50").pack(pady=(5, 2))
        self.altura_a = self.crear_campo(frame_controles, "Altura (m)", "30")
        
        ctk.CTkLabel(frame_controles, text="🏗️ ANTENA B", font=("Arial", 13, "bold"), text_color="#4CAF50").pack(pady=(5, 2))
        self.altura_b = self.crear_campo(frame_controles, "Altura (m)", "30")

        ctk.CTkLabel(frame_controles, text="📡 PARÁMETROS", font=("Arial", 13, "bold"), text_color="#FFC107").pack(pady=(10, 2))
        self.distancia_total = self.crear_campo(frame_controles, "Distancia Total (km)", "10")
        self.frecuencia = self.crear_campo(frame_controles, "Frecuencia (MHz)", "2400")

        ctk.CTkLabel(frame_controles, text="⛰️ OBSTÁCULO", font=("Arial", 13, "bold"), text_color="#F44336").pack(pady=(10, 2))
        self.distancia_obstaculo = self.crear_campo(frame_controles, "Distancia desde A (km)", "5")
        self.altura_obstaculo = self.crear_campo(frame_controles, "Altura (m)", "15")

        # Opciones avanzadas
        ctk.CTkLabel(frame_controles, text="🔧 OPCIONES AVANZADAS", font=("Arial", 13, "bold"), text_color="#9C27B0").pack(pady=(10, 2))
        
        self.curvatura_var = ctk.IntVar(value=0)
        self.check_curvatura = ctk.CTkCheckBox(
            frame_controles,
            text="Considerar curvatura terrestre (k=4/3)",
            variable=self.curvatura_var,
            font=("Arial", 11)
        )
        self.check_curvatura.pack(pady=(5, 8), padx=10, anchor="w")
        
        self.mostrar_60_var = ctk.IntVar(value=1)
        self.check_mostrar_60 = ctk.CTkCheckBox(
            frame_controles,
            text="Mostrar zona al 60% (recomendado)",
            variable=self.mostrar_60_var,
            font=("Arial", 11)
        )
        self.check_mostrar_60.pack(pady=(0, 8), padx=10, anchor="w")

        boton = ctk.CTkButton(
            frame_controles,
            text="🔄 CALCULAR",
            height=45,
            font=("Arial", 14, "bold"),
            command=self.calcular,
            fg_color="#2196F3",
            hover_color="#1976D2"
        )
        boton.pack(padx=20, pady=20, fill="x")

        # ====== RESULTADOS ======
        ctk.CTkLabel(frame_resultados, text="📊 RESULTADOS", font=("Arial", 16, "bold")).pack(pady=(10, 15))

        self.frame_estado = ctk.CTkFrame(frame_resultados, fg_color="transparent")
        self.frame_estado.pack(pady=(5, 10))
        self.indicador_estado = ctk.CTkLabel(self.frame_estado, text="●", font=("Arial", 24), text_color="gray")
        self.indicador_estado.pack(side="left", padx=(0, 8))
        self.estado = ctk.CTkLabel(self.frame_estado, text="⚡ ESPERANDO", font=("Arial", 20, "bold"))
        self.estado.pack(side="left")

        separador1 = ctk.CTkFrame(frame_resultados, height=1, fg_color="gray")
        separador1.pack(fill="x", padx=15, pady=8)

        frame_metricas = ctk.CTkFrame(frame_resultados, fg_color="transparent")
        frame_metricas.pack(pady=8, fill="both", expand=True)

        col_izq = ctk.CTkFrame(frame_metricas, fg_color="transparent")
        col_izq.pack(side="left", padx=8, fill="both", expand=True)

        col_der = ctk.CTkFrame(frame_metricas, fg_color="transparent")
        col_der.pack(side="right", padx=8, fill="both", expand=True)

        # Columna izquierda - Obstrucción
        ctk.CTkLabel(col_izq, text="📈 OBSTRUCCIÓN", font=("Arial", 13, "bold")).pack(pady=(5, 8))

        self.progressbar = ctk.CTkProgressBar(col_izq, width=180, height=20, corner_radius=10)
        self.progressbar.pack(pady=5)
        self.progressbar.set(0)

        self.lbl_libre = ctk.CTkLabel(col_izq, text="✅ Zona libre: -", font=("Arial", 13))
        self.lbl_libre.pack(pady=4)

        self.lbl_obstruida = ctk.CTkLabel(col_izq, text="❌ Zona obstruida: -", font=("Arial", 13))
        self.lbl_obstruida.pack(pady=4)

        # Columna derecha - Parámetros
        ctk.CTkLabel(col_der, text="📐 PARÁMETROS", font=("Arial", 13, "bold")).pack(pady=(5, 8))

        self.lbl_fresnel = ctk.CTkLabel(col_der, text="📡 Radio Fresnel (100%): -", font=("Arial", 12))
        self.lbl_fresnel.pack(pady=4)

        self.lbl_fresnel_60 = ctk.CTkLabel(col_der, text="🎯 Radio Fresnel (60%): -", font=("Arial", 12))
        self.lbl_fresnel_60.pack(pady=4)

        self.lbl_los = ctk.CTkLabel(col_der, text="📏 Altura línea vista: -", font=("Arial", 12))
        self.lbl_los.pack(pady=4)

        self.lbl_clearance = ctk.CTkLabel(col_der, text="🔄 Espacio libre (clearance): -", font=("Arial", 12))
        self.lbl_clearance.pack(pady=4)

        separador2 = ctk.CTkFrame(frame_resultados, height=1, fg_color="gray")
        separador2.pack(fill="x", padx=15, pady=8)

        # Calidad del enlace
        ctk.CTkLabel(frame_resultados, text="📊 CALIDAD DEL ENLACE", font=("Arial", 13, "bold")).pack(pady=(5, 5))

        frame_calidad = ctk.CTkFrame(frame_resultados, fg_color="transparent")
        frame_calidad.pack(pady=5)

        self.lbl_calidad = ctk.CTkLabel(frame_calidad, text="●", font=("Arial", 18), text_color="gray")
        self.lbl_calidad.pack(side="left", padx=5)

        self.lbl_calidad_texto = ctk.CTkLabel(frame_calidad, text="", font=("Arial", 12))
        self.lbl_calidad_texto.pack(side="left", padx=5)

        self.lbl_relacion = ctk.CTkLabel(frame_resultados, text="📊 Relación clearance/Fresnel (60%): -", font=("Arial", 12))
        self.lbl_relacion.pack(pady=5)

        # Recomendación
        ctk.CTkLabel(frame_resultados, text="💡 RECOMENDACIÓN", font=("Arial", 13, "bold")).pack(pady=(10, 5))

        self.lbl_recomendacion = ctk.CTkLabel(
            frame_resultados, 
            text="Ingrese datos y calcule", 
            font=("Arial", 11), 
            wraplength=300,
            justify="center"
        )
        self.lbl_recomendacion.pack(pady=5)

        # ====== VISUALIZACIÓN ======
        ctk.CTkLabel(frame_visual, text="🎨 ZONA DE FRESNEL", font=("Arial", 16, "bold")).pack(pady=(10, 8))

        self.frame_grafico = ctk.CTkFrame(frame_visual, fg_color="#1a1a1a", corner_radius=10)
        self.frame_grafico.pack(fill="both", expand=True, padx=8, pady=8)

        # Configuración de la figura
        self.fig = plt.figure(figsize=(9, 6.5), facecolor='#1a1a1a')
        self.fig.patch.set_facecolor('#1a1a1a')
        
        self.ax_main = self.fig.add_subplot(111)
        self.ax_main.set_facecolor('#2b2b2b')
        
        self.ax_main.set_xlabel("Distancia (km)", fontsize=11, color='white', fontweight='bold')
        self.ax_main.set_ylabel("Altura (m)", fontsize=11, color='white', fontweight='bold')
        self.ax_main.set_title("PRIMERA ZONA DE FRESNEL", fontsize=13, color='white', fontweight='bold', pad=15)
        self.ax_main.grid(True, alpha=0.3, linestyle='--')
        
        for spine in self.ax_main.spines.values():
            spine.set_color('#555555')
            spine.set_linewidth(1)
        
        self.ax_main.tick_params(colors='white', labelsize=9)
        
        plt.tight_layout()
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

        # Footer
        footer = ctk.CTkLabel(
            self, 
            text="© 2026 - Maximiliano Lopez | Basado en ITU-R P.526 | Fresnel al 60% estándar",
            font=("Arial", 10),
            text_color="#666666"
        )
        footer.pack(side="bottom", pady=8)

    def crear_campo(self, parent, texto, valor_default=""):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(pady=(0, 8), fill="x", padx=10)
        
        ctk.CTkLabel(frame, text=texto, font=("Arial", 11)).pack(anchor="w")
        entrada = ctk.CTkEntry(frame, height=28, font=("Arial", 12))
        entrada.pack(fill="x", pady=(2, 0))
        if valor_default:
            entrada.insert(0, valor_default)
        return entrada

    def calcular_calidad_enlace(self, porcentaje_obstruido, clearance, radio_fresnel_60, altura_obstaculo):
        if altura_obstaculo == 0:
            return "🌟 EXCELENTE", "Sin obstáculo - Enlace óptimo"
        
        if radio_fresnel_60 == 0:
            if clearance >= 0:
                return "🌟 EXCELENTE", "Obstáculo en antena - Sin efecto"
            else:
                return "🚫 NULO", "Obstáculo bloquea antena"
        
        # Evaluación basada en el 60% de la zona de Fresnel
        if clearance >= radio_fresnel_60:
            if porcentaje_obstruido == 0:
                return "🌟 EXCELENTE", "Zona de Fresnel completamente despejada"
            elif porcentaje_obstruido < 20:
                return "✅ MUY BUENA", "Pérdidas mínimas"
            elif porcentaje_obstruido <= 40:
                return "✅ BUENA", "Funciona correctamente"
            else:
                return "⚠️ ACEPTABLE", "Aceptable pero mejorable"
        elif clearance >= 0:
            if porcentaje_obstruido <= 60:
                return "⚠️ REGULAR", "Calidad degradada - Requiere mejora"
            else:
                return "❌ MALA", "No recomendado para enlaces críticos"
        else:
            if porcentaje_obstruido <= 80:
                return "❌ MALA", "Enlace muy degradado"
            else:
                return "🚫 NULA", "Enlace inviable"

    def dibujar_visualizacion(self, resultado, datos):
        
        altura_a = datos['altura_a']
        altura_b = datos['altura_b']
        distancia_total = datos['distancia_total']
        distancia_obstaculo = datos['distancia_obstaculo']
        altura_obstaculo = datos['altura_obstaculo']
        frecuencia = datos['frecuencia']
        considerar_curvatura = datos.get('considerar_curvatura', False)
        mostrar_60 = datos.get('mostrar_60', True)
        
        self.ax_main.clear()
        self.ax_main.set_facecolor("#edebeb")
        
        distancias = np.linspace(0, distancia_total, 500)
        
        # Línea de vista
        linea_vista = altura_a + (altura_b - altura_a) * (distancias / distancia_total)
        
        # Curvatura terrestre si está habilitada
        curvatura = np.zeros_like(distancias)
        if considerar_curvatura:
            # k=4/3 (radio efectivo de la Tierra)
            k = 4/3
            for i, d in enumerate(distancias):
                if 0 < d < distancia_total:
                    # Fórmula de curvatura terrestre
                    curvatura[i] = (d * (distancia_total - d)) / (12.74 * k)
        
        # Ajustar alturas por curvatura
        altura_a_curva = altura_a
        altura_b_curva = altura_b
        linea_vista_curva = linea_vista - curvatura
        
        # Calcular zona de Fresnel
        radios = []
        for d in distancias:
            if 0 < d < distancia_total:
                d1 = d
                d2 = distancia_total - d
                frecuencia_ghz = frecuencia / 1000.0
                radio = 17.32 * np.sqrt((d1 * d2) / (frecuencia_ghz * distancia_total))
                radios.append(radio)
            else:
                radios.append(0)
        radios = np.array(radios)
        
        # Zona al 100%
        curva_superior = linea_vista_curva + radios
        curva_inferior = linea_vista_curva - radios
        
        # Zona al 60% (si está habilitada)
        if mostrar_60:
            radios_60 = radios * 0.6
            curva_superior_60 = linea_vista_curva + radios_60
            curva_inferior_60 = linea_vista_curva - radios_60
        
        # Dibujar zona al 100% (transparente)
        self.ax_main.fill_between(distancias, curva_inferior, curva_superior, 
                                   alpha=0.15, color='#00FF00', label='Zona Fresnel 100%')
        
        # Dibujar zona al 60% (más visible)
        if mostrar_60:
            self.ax_main.fill_between(distancias, curva_inferior_60, curva_superior_60, 
                                      alpha=0.35, color='#00FF00', label='Zona Fresnel 60% (Recomendada)')
        
        # Dibujar líneas de la zona de Fresnel
        self.ax_main.plot(distancias, curva_superior, 'g--', linewidth=1, alpha=0.4)
        self.ax_main.plot(distancias, curva_inferior, 'g--', linewidth=1, alpha=0.4)
        
        if mostrar_60:
            self.ax_main.plot(distancias, curva_superior_60, 'g-', linewidth=1.5, alpha=0.6)
            self.ax_main.plot(distancias, curva_inferior_60, 'g-', linewidth=1.5, alpha=0.6)
        
        # Línea de vista
        self.ax_main.plot(distancias, linea_vista_curva, 'cyan', linewidth=2.5, label='Línea de Vista', alpha=0.9)
        
        # Antenas
        self.ax_main.plot(0, altura_a_curva, 'o', markersize=16, color='#4CAF50', 
                         markeredgecolor='white', markeredgewidth=2, zorder=5)
        self.ax_main.annotate(f'Antena A\n{altura_a_curva:.1f}m', xy=(0, altura_a_curva), 
                             xytext=(-35, 25), textcoords='offset points', 
                             fontsize=8, color='white', fontweight='bold', ha='center',
                             bbox=dict(boxstyle="round,pad=0.2", facecolor='#4CAF50', alpha=0.8))
        
        self.ax_main.plot(distancia_total, altura_b_curva, 'o', markersize=16, color='#4CAF50', 
                         markeredgecolor='white', markeredgewidth=2, zorder=5)
        
        if distancia_total > 5:
            self.ax_main.annotate(f'Antena B\n{altura_b_curva:.1f}m', xy=(distancia_total, altura_b_curva), 
                                 xytext=(-35, 25), textcoords='offset points',
                                 fontsize=8, color='white', fontweight='bold', ha='center',
                                 bbox=dict(boxstyle="round,pad=0.2", facecolor='#4CAF50', alpha=0.8))
        else:
            self.ax_main.annotate(f'Antena B\n{altura_b_curva:.1f}m', xy=(distancia_total, altura_b_curva), 
                                 xytext=(-35, -25), textcoords='offset points',
                                 fontsize=8, color='white', fontweight='bold', ha='center',
                                 bbox=dict(boxstyle="round,pad=0.2", facecolor='#4CAF50', alpha=0.8))
        
        # Obstáculo
        if altura_obstaculo > 0:
            # Ajustar altura del obstáculo por curvatura
            if considerar_curvatura:
                idx_obs = np.argmin(np.abs(distancias - distancia_obstaculo))
                altura_obstaculo_curva = altura_obstaculo - curvatura[idx_obs]
                if altura_obstaculo_curva < 0:
                    altura_obstaculo_curva = 0
            else:
                altura_obstaculo_curva = altura_obstaculo
            
            obstaculo_ancho = 0.15
            obstaculo_x = [distancia_obstaculo - obstaculo_ancho/2, 
                          distancia_obstaculo + obstaculo_ancho/2,
                          distancia_obstaculo + obstaculo_ancho/2,
                          distancia_obstaculo - obstaculo_ancho/2]
            obstaculo_y = [0, 0, altura_obstaculo_curva, altura_obstaculo_curva]
            
            # Color del obstáculo según afecte o no a la zona
            idx_obs = np.argmin(np.abs(distancias - distancia_obstaculo))
            clearance = linea_vista_curva[idx_obs] - altura_obstaculo_curva
            
            if clearance >= 0:
                color_obs = '#FF9800'  # Naranja - no bloquea
                alpha_obs = 0.5
            else:
                color_obs = '#F44336'  # Rojo - bloquea
                alpha_obs = 0.8
            
            self.ax_main.fill(obstaculo_x, obstaculo_y, color=color_obs, alpha=alpha_obs, label='Obstáculo')
            self.ax_main.plot(distancia_obstaculo, altura_obstaculo_curva, 'rv', markersize=12, 
                             markeredgecolor='white', markeredgewidth=1.5, zorder=6)
            self.ax_main.axvline(x=distancia_obstaculo, color=color_obs, linestyle='--', alpha=0.4, linewidth=0.8)
            
            self.ax_main.annotate(f'Obstáculo\n{altura_obstaculo_curva:.1f}m', 
                                 xy=(distancia_obstaculo, altura_obstaculo_curva), 
                                 xytext=(15, -25), textcoords='offset points',
                                 fontsize=7, color='white', fontweight='bold',
                                 bbox=dict(boxstyle="round,pad=0.2", facecolor=color_obs, alpha=0.8))
        
        # Terreno
        terreno_y = -curvatura if considerar_curvatura else np.zeros_like(distancias)
        self.ax_main.fill_between(distancias, -5, terreno_y, alpha=0.4, color='#8B4513', label='Terreno')
        self.ax_main.plot(distancias, terreno_y, 'w-', linewidth=0.8, alpha=0.3)
        
        # Punto crítico (máximo radio)
        idx_max = np.argmax(radios)
        d_max = distancias[idx_max]
        radio_max = radios[idx_max]
        
        self.ax_main.plot(d_max, linea_vista_curva[idx_max], 'y*', markersize=12, label='Punto crítico')
        self.ax_main.annotate(f'Radio máx: {radio_max:.1f}m\n(100%)', 
                             xy=(d_max, linea_vista_curva[idx_max]), xytext=(8, 15),
                             textcoords='offset points', fontsize=7, color='yellow',
                             bbox=dict(boxstyle="round,pad=0.2", facecolor='black', alpha=0.6))
        
        # Configurar ejes
        self.ax_main.set_xlabel("Distancia (km)", fontsize=11, color='white', fontweight='bold')
        self.ax_main.set_ylabel("Altura (m)", fontsize=11, color='white', fontweight='bold')
        self.ax_main.set_title("PRIMERA ZONA DE FRESNEL", fontsize=13, color='white', fontweight='bold', pad=15)
        self.ax_main.legend(loc='upper right', fontsize=8, framealpha=0.8, 
                           facecolor='#2b2b2b', edgecolor='white')
        self.ax_main.grid(True, alpha=0.3, linestyle='--')
        
        # Ajustar límites
        y_min = min(-5, min(curva_inferior) - 8)
        y_max = max(altura_a_curva, altura_b_curva, max(curva_superior) + 15)
        if altura_obstaculo > 0:
            y_max = max(y_max, altura_obstaculo_curva + 12)
        
        x_min = -0.5 if distancia_total < 10 else -0.3
        x_max = distancia_total + 0.5 if distancia_total < 10 else distancia_total + 0.3
        
        self.ax_main.set_xlim(x_min, x_max)
        self.ax_main.set_ylim(y_min, y_max)
        
        for spine in self.ax_main.spines.values():
            spine.set_color('#555555')
            spine.set_linewidth(1)
        
        self.ax_main.tick_params(colors='white', labelsize=9)
        
        self.canvas.draw()

    def calcular(self):
        
        try:
            altura_a = float(self.altura_a.get())
            altura_b = float(self.altura_b.get())
            distancia_total = float(self.distancia_total.get())
            distancia_obstaculo = float(self.distancia_obstaculo.get())
            altura_obstaculo = float(self.altura_obstaculo.get())
            frecuencia = float(self.frecuencia.get())
            considerar_curvatura = bool(self.curvatura_var.get())
            mostrar_60 = bool(self.mostrar_60_var.get())

            # Validaciones mejoradas
            if altura_a <= 0 or altura_b <= 0:
                raise ValueError("Las alturas de las antenas deben ser mayores a cero")
            if distancia_total <= 0:
                raise ValueError("La distancia total debe ser mayor a cero")
            if distancia_total > 100:
                messagebox.showwarning("Advertencia", 
                    "Distancias mayores a 100km pueden tener errores significativos\n"
                    "por la curvatura terrestre. Considere habilitar la curvatura.")
            if frecuencia <= 0:
                raise ValueError("La frecuencia debe ser mayor a cero")
            if frecuencia < 300:
                messagebox.showwarning("Advertencia", 
                    "Frecuencia menor a 300 MHz - La zona de Fresnel será muy grande\n"
                    "Considere usar frecuencias más altas para enlaces punto a punto.")
            if distancia_obstaculo < 0 or distancia_obstaculo > distancia_total:
                raise ValueError("Distancia del obstáculo inválida (debe estar entre 0 y la distancia total)")

            resultado = analizar_enlace(
                altura_a, altura_b, distancia_total,
                distancia_obstaculo, altura_obstaculo, frecuencia
            )

            # Actualizar estado
            self.estado.configure(
                text=resultado["estado"],
                text_color=resultado["color"]
            )
            
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

            # Progress bar
            obstruccion = resultado["porcentaje_obstruido"] / 100
            self.progressbar.set(obstruccion)
            
            if obstruccion == 0:
                self.progressbar.configure(progress_color="green")
            elif obstruccion <= 0.40:
                self.progressbar.configure(progress_color="#FFC107")
            else:
                self.progressbar.configure(progress_color="#F44336")

            # Parámetros
            self.lbl_fresnel.configure(
                text=f"📡 Radio Fresnel (100%): {resultado['radio_fresnel_m']} m"
            )
            self.lbl_fresnel_60.configure(
                text=f"🎯 Radio Fresnel (60%): {resultado['radio_fresnel_60_m']} m"
            )
            self.lbl_los.configure(
                text=f"📏 Altura línea vista: {resultado['altura_linea_vista_m']} m"
            )
            self.lbl_clearance.configure(
                text=f"🔄 Espacio libre (clearance): {resultado['clearance_m']} m"
            )
            
            # Color del clearance según relación con el 60%
            clearance = resultado['clearance_m']
            radio_60 = resultado['radio_fresnel_60_m']
            
            if radio_60 == 0:
                if clearance >= 0:
                    self.lbl_clearance.configure(text_color="#4CAF50")
                else:
                    self.lbl_clearance.configure(text_color="#F44336")
            elif clearance < 0:
                self.lbl_clearance.configure(text_color="#F44336")
            elif clearance < radio_60:
                self.lbl_clearance.configure(text_color="#FFC107")
            else:
                self.lbl_clearance.configure(text_color="#4CAF50")

            # Calidad del enlace
            calidad, descripcion = self.calcular_calidad_enlace(
                resultado["porcentaje_obstruido"],
                clearance,
                radio_60,
                altura_obstaculo
            )
            
            if "EXCELENTE" in calidad:
                color_calidad = "gold"
            elif "MUY BUENA" in calidad or "BUENA" in calidad:
                color_calidad = "#4CAF50"
            elif "ACEPTABLE" in calidad:
                color_calidad = "#8BC34A"
            elif "REGULAR" in calidad:
                color_calidad = "#FFC107"
            elif "MALA" in calidad:
                color_calidad = "#FF9800"
            else:
                color_calidad = "#F44336"
            
            self.lbl_calidad.configure(text_color=color_calidad)
            self.lbl_calidad_texto.configure(text=f"{calidad} - {descripcion}", text_color=color_calidad)

            # Relación clearance/Fresnel
            if radio_60 > 0:
                relacion = clearance / radio_60
                if relacion >= 1:
                    self.lbl_relacion.configure(
                        text=f"📊 Relación clearance/Fresnel (60%): {relacion:.2f} (✅ Despejado)",
                        text_color="#4CAF50"
                    )
                elif relacion >= 0.6:
                    self.lbl_relacion.configure(
                        text=f"📊 Relación clearance/Fresnel (60%): {relacion:.2f} (⚠️ Aceptable)",
                        text_color="#FFC107"
                    )
                else:
                    self.lbl_relacion.configure(
                        text=f"📊 Relación clearance/Fresnel (60%): {relacion:.2f} (❌ Insuficiente)",
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
                        text="📊 Relación clearance/Fresnel: N/A",
                        text_color="gray"
                    )

            # Recomendación
            self.lbl_recomendacion.configure(text=resultado["recomendacion"])

            # Datos para visualización
            datos = {
                'altura_a': altura_a,
                'altura_b': altura_b,
                'distancia_total': distancia_total,
                'distancia_obstaculo': distancia_obstaculo,
                'altura_obstaculo': altura_obstaculo,
                'frecuencia': frecuencia,
                'considerar_curvatura': considerar_curvatura,
                'mostrar_60': mostrar_60
            }
            self.dibujar_visualizacion(resultado, datos)

        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")
