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

        self.title("Zona Fresnel López Maxi- Visualización Interactiva")
        self.geometry("1550x950")
        self.resizable(False, False)

        self.crear_widgets()

    def crear_widgets(self):

        titulo = ctk.CTkLabel(
            self,
            text="📡 Zona Fresnel - Visualización Interactiva",
            font=("Arial", 28, "bold")
        )
        titulo.pack(pady=(15, 5))

        subtitulo = ctk.CTkLabel(
            self,
            text="Fórmula: F₁ = 8.656 × √(d₁ × d₂ / (f × D))",
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

        ctk.CTkLabel(col_izq, text="📈 OBSTRUCCIÓN", font=("Arial", 13, "bold")).pack(pady=(5, 8))

        self.progressbar = ctk.CTkProgressBar(col_izq, width=180, height=20, corner_radius=10)
        self.progressbar.pack(pady=5)
        self.progressbar.set(0)

        self.lbl_libre = ctk.CTkLabel(col_izq, text="✅ Zona libre: -", font=("Arial", 13))
        self.lbl_libre.pack(pady=4)

        self.lbl_obstruida = ctk.CTkLabel(col_izq, text="❌ Zona obstruida: -", font=("Arial", 13))
        self.lbl_obstruida.pack(pady=4)

        ctk.CTkLabel(col_der, text="📐 PARÁMETROS", font=("Arial", 13, "bold")).pack(pady=(5, 8))

        self.lbl_fresnel = ctk.CTkLabel(col_der, text="📡 Radio Fresnel: -", font=("Arial", 12))
        self.lbl_fresnel.pack(pady=4)

        self.lbl_los = ctk.CTkLabel(col_der, text="📏 Altura línea vista: -", font=("Arial", 12))
        self.lbl_los.pack(pady=4)

        self.lbl_clearance = ctk.CTkLabel(col_der, text="🔄 Espacio libre: -", font=("Arial", 12))
        self.lbl_clearance.pack(pady=4)

        separador2 = ctk.CTkFrame(frame_resultados, height=1, fg_color="gray")
        separador2.pack(fill="x", padx=15, pady=8)

        ctk.CTkLabel(frame_resultados, text="📊 CALIDAD", font=("Arial", 13, "bold")).pack(pady=(5, 5))

        frame_calidad = ctk.CTkFrame(frame_resultados, fg_color="transparent")
        frame_calidad.pack(pady=5)

        self.lbl_calidad = ctk.CTkLabel(frame_calidad, text="●", font=("Arial", 18), text_color="gray")
        self.lbl_calidad.pack(side="left", padx=5)

        self.lbl_calidad_texto = ctk.CTkLabel(frame_calidad, text="", font=("Arial", 12))
        self.lbl_calidad_texto.pack(side="left", padx=5)

        self.lbl_relacion = ctk.CTkLabel(frame_resultados, text="📊 Relación clearance/Fresnel: -", font=("Arial", 12))
        self.lbl_relacion.pack(pady=5)

        ctk.CTkLabel(frame_resultados, text="💡 RECOMENDACIÓN", font=("Arial", 13, "bold")).pack(pady=(10, 5))

        self.lbl_recomendacion = ctk.CTkLabel(
            frame_resultados, 
            text="Ingrese datos y calcule", 
            font=("Arial", 11), 
            wraplength=300,
            justify="center"
        )
        self.lbl_recomendacion.pack(pady=5)

        ctk.CTkLabel(frame_visual, text="🎨 ZONA DE FRESNEL", font=("Arial", 16, "bold")).pack(pady=(10, 8))

        self.frame_grafico = ctk.CTkFrame(frame_visual, fg_color="#1a1a1a", corner_radius=10)
        self.frame_grafico.pack(fill="both", expand=True, padx=8, pady=8)

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

        footer = ctk.CTkLabel(
            self, 
            text="© 2026 - Maximiliano Lopez | Basado en ITU-R P.526",
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

    def calcular_calidad_enlace(self, porcentaje_obstruido, clearance, radio_fresnel, altura_obstaculo):
        if altura_obstaculo == 0:
            return "🌟 EXCELENTE", "Sin obstáculo - Enlace óptimo"
        
        if radio_fresnel == 0:
            if clearance >= 0:
                return "🌟 EXCELENTE", "Obstáculo en antena - Sin efecto"
            else:
                return "🚫 NULO", "Obstáculo bloquea antena"
        
        if porcentaje_obstruido == 0:
            return "🌟 EXCELENTE", "Enlace óptimo"
        elif porcentaje_obstruido < 20:
            return "✅ BUENA", "Funciona correctamente"
        elif porcentaje_obstruido <= 40:
            return "⚠️ REGULAR", "Calidad degradada"
        elif porcentaje_obstruido <= 60:
            return "❌ MALA", "No recomendado"
        else:
            return "🚫 NULA", "Enlace inviable"

    def dibujar_visualizacion(self, resultado, datos):
        
        altura_a = datos['altura_a']
        altura_b = datos['altura_b']
        distancia_total = datos['distancia_total']
        distancia_obstaculo = datos['distancia_obstaculo']
        altura_obstaculo = datos['altura_obstaculo']
        frecuencia = datos['frecuencia']
        
        self.ax_main.clear()
        self.ax_main.set_facecolor('#2b2b2b')
        
        distancias = np.linspace(0, distancia_total, 500)
        
        linea_vista = altura_a + (altura_b - altura_a) * (distancias / distancia_total)
        
        radios = []
        for d in distancias:
            if 0 < d < distancia_total:
                d1 = d
                d2 = distancia_total - d
                frecuencia_ghz = frecuencia / 1000.0
                radio = 8.656 * np.sqrt((d1 * d2) / (frecuencia_ghz * distancia_total))
                radios.append(radio)
            else:
                radios.append(0)
        radios = np.array(radios)
        
        curva_superior = linea_vista + radios
        curva_inferior = linea_vista - radios
        
        self.ax_main.fill_between(distancias, curva_inferior, curva_superior, 
                                   alpha=0.25, color='#00FF00', label='Zona de Fresnel')
        
        self.ax_main.plot(distancias, curva_superior, 'g--', linewidth=1.2, alpha=0.6)
        self.ax_main.plot(distancias, curva_inferior, 'g--', linewidth=1.2, alpha=0.6)
        
        self.ax_main.plot(distancias, linea_vista, 'cyan', linewidth=2, label='Línea de Vista', alpha=0.9)
        
        self.ax_main.plot(0, altura_a, 'o', markersize=16, color='#4CAF50', markeredgecolor='white', 
                         markeredgewidth=2, zorder=5)
        self.ax_main.annotate(f'Antena A\n{altura_a}m', xy=(0, altura_a), xytext=(-35, 25),
                              textcoords='offset points', fontsize=8, color='white',
                              fontweight='bold', ha='center', bbox=dict(boxstyle="round,pad=0.2", 
                              facecolor='#4CAF50', alpha=0.8))
        
        self.ax_main.plot(distancia_total, altura_b, 'o', markersize=16, color='#4CAF50', 
                         markeredgecolor='white', markeredgewidth=2, zorder=5)
        
        if distancia_total > 5:
            self.ax_main.annotate(f'Antena B\n{altura_b}m', xy=(distancia_total, altura_b), xytext=(-35, 25),
                                  textcoords='offset points', fontsize=8, color='white',
                                  fontweight='bold', ha='center', bbox=dict(boxstyle="round,pad=0.2",
                                  facecolor='#4CAF50', alpha=0.8))
        else:
            self.ax_main.annotate(f'Antena B\n{altura_b}m', xy=(distancia_total, altura_b), xytext=(-35, -25),
                                  textcoords='offset points', fontsize=8, color='white',
                                  fontweight='bold', ha='center', bbox=dict(boxstyle="round,pad=0.2",
                                  facecolor='#4CAF50', alpha=0.8))
        
        self.ax_main.plot([0, 0], [0, altura_a], 'w--', alpha=0.2, linewidth=0.8)
        self.ax_main.plot([distancia_total, distancia_total], [0, altura_b], 'w--', alpha=0.2, linewidth=0.8)
        
        if altura_obstaculo > 0:
            obstaculo_ancho = 0.15
            obstaculo_x = [distancia_obstaculo - obstaculo_ancho/2, 
                          distancia_obstaculo + obstaculo_ancho/2,
                          distancia_obstaculo + obstaculo_ancho/2,
                          distancia_obstaculo - obstaculo_ancho/2]
            obstaculo_y = [0, 0, altura_obstaculo, altura_obstaculo]
            
            self.ax_main.fill(obstaculo_x, obstaculo_y, color='#F44336', alpha=0.6, label='Obstáculo')
            self.ax_main.plot(distancia_obstaculo, altura_obstaculo, 'rv', markersize=12, 
                             markeredgecolor='white', markeredgewidth=1.5, zorder=6)
            self.ax_main.axvline(x=distancia_obstaculo, color='#F44336', linestyle='--', alpha=0.4, linewidth=0.8)
            
            self.ax_main.annotate(f'Obstáculo\n{altura_obstaculo}m', 
                                 xy=(distancia_obstaculo, altura_obstaculo), 
                                 xytext=(15, -25), textcoords='offset points',
                                 fontsize=7, color='white', fontweight='bold',
                                 bbox=dict(boxstyle="round,pad=0.2", facecolor='#F44336', alpha=0.8))
        
        self.ax_main.fill_between(distancias, -5, 0, alpha=0.4, color='#8B4513', label='Terreno')
        self.ax_main.plot(distancias, np.zeros_like(distancias), 'w-', linewidth=0.8, alpha=0.4)
        
        idx_max = np.argmax(radios)
        d_max = distancias[idx_max]
        radio_max = radios[idx_max]
        
        self.ax_main.plot(d_max, linea_vista[idx_max], 'y*', markersize=12, label='Punto crítico')
        self.ax_main.annotate(f'Radio máx: {radio_max:.1f}m', 
                             xy=(d_max, linea_vista[idx_max]), xytext=(8, 15),
                             textcoords='offset points', fontsize=7, color='yellow',
                             bbox=dict(boxstyle="round,pad=0.2", facecolor='black', alpha=0.6))
        
        self.ax_main.set_xlabel("Distancia (km)", fontsize=11, color='white', fontweight='bold')
        self.ax_main.set_ylabel("Altura (m)", fontsize=11, color='white', fontweight='bold')
        self.ax_main.set_title("PRIMERA ZONA DE FRESNEL", fontsize=13, color='white', fontweight='bold', pad=15)
        self.ax_main.legend(loc='upper right', fontsize=8, framealpha=0.8, facecolor='#2b2b2b', edgecolor='white')
        self.ax_main.grid(True, alpha=0.3, linestyle='--')
        
        y_min = min(0, min(curva_inferior) - 8)
        y_max = max(altura_a, altura_b, max(curva_superior) + 15)
        if altura_obstaculo > 0:
            y_max = max(y_max, altura_obstaculo + 12)
        
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

            if altura_a <= 0 or altura_b <= 0:
                raise ValueError("Las alturas de las antenas deben ser mayores a cero")
            if distancia_total <= 0:
                raise ValueError("La distancia total debe ser mayor a cero")
            if frecuencia <= 0:
                raise ValueError("La frecuencia debe ser mayor a cero")
            if distancia_obstaculo < 0 or distancia_obstaculo > distancia_total:
                raise ValueError("Distancia del obstáculo inválida")

            resultado = analizar_enlace(
                altura_a, altura_b, distancia_total,
                distancia_obstaculo, altura_obstaculo, frecuencia
            )

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

            self.lbl_libre.configure(
                text=f"✅ Zona libre: {resultado['porcentaje_libre']} %"
            )
            self.lbl_obstruida.configure(
                text=f"❌ Zona obstruida: {resultado['porcentaje_obstruido']} %"
            )

            obstruccion = resultado["porcentaje_obstruido"] / 100
            self.progressbar.set(obstruccion)
            
            if obstruccion == 0:
                self.progressbar.configure(progress_color="green")
            elif obstruccion <= 0.40:
                self.progressbar.configure(progress_color="#FFC107")
            else:
                self.progressbar.configure(progress_color="#F44336")

            self.lbl_fresnel.configure(
                text=f"📡 Radio Fresnel: {resultado['radio_fresnel_m']} m"
            )
            self.lbl_los.configure(
                text=f"📏 Altura línea vista: {resultado['altura_linea_vista_m']} m"
            )
            self.lbl_clearance.configure(
                text=f"🔄 Espacio libre: {resultado['clearance_m']} m"
            )
            
            clearance = resultado['clearance_m']
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

            calidad, descripcion = self.calcular_calidad_enlace(
                resultado["porcentaje_obstruido"],
                clearance,
                resultado['radio_fresnel_m'],
                altura_obstaculo
            )
            
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
                        text="📊 Relación clearance/Fresnel: N/A",
                        text_color="gray"
                    )

            self.lbl_recomendacion.configure(text=resultado["recomendacion"])

            datos = {
                'altura_a': altura_a,
                'altura_b': altura_b,
                'distancia_total': distancia_total,
                'distancia_obstaculo': distancia_obstaculo,
                'altura_obstaculo': altura_obstaculo,
                'frecuencia': frecuencia
            }
            self.dibujar_visualizacion(resultado, datos)

        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")

