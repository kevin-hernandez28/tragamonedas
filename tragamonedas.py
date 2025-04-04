import random
import threading
import time
import tkinter as tk

# ----------------------------- MODELO -----------------------------
class SlotMachine:
    """
    Clase que representa el modelo del juego tragamonedas.
    Contiene los símbolos, el balance del jugador y la lógica de juego.
    """
    def __init__(self):
        self.symbols = ["🍒", "🍋", "🍊", "🍉", "🍇"]
        self.result = ["❓", "❓", "❓"]
        self.balance = 100
        self.lock = threading.Lock()  # Manejo de sincronización

    def spin(self):
        """Gira los rodillos y genera un resultado aleatorio."""
        with self.lock:
            self.result = [random.choice(self.symbols) for _ in range(3)]

    def calculate_winnings(self, bet):
        """Calcula las ganancias basadas en el resultado de los rodillos."""
        with self.lock:
            if len(set(self.result)) == 1:
                return bet * 10
            elif len(set(self.result)) == 2:
                return bet * 2
            else:
                return 0

    def get_balance(self):
        """Devuelve el balance actual."""
        with self.lock:
            return self.balance

    def update_balance(self, amount):
        """Actualiza el balance del jugador de manera segura."""
        with self.lock:
            self.balance += amount

# ----------------------------- VISTA -----------------------------
class SlotMachineView:
    """
    Clase encargada de mostrar la interfaz gráfica del juego.
    Se comunica con el controlador para recibir y mostrar datos del modelo.
    """
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title("Tragamonedas")
        self.root.geometry("800x600")  # Tamaño aumentado para mejor visualización

        # Colores brillantes para animar el fondo
        self.bg_colors = ["#ff5733", "#33ff57", "#3357ff", "#f39c12", "#9b59b6"]
        self.color_index = 0
        self.animate_background()

        # Contenedor principal con estilo
        self.frame = tk.Frame(root, bg="#111111", bd=20, relief="ridge", padx=30, pady=30)
        self.frame.pack(pady=20, padx=20, expand=True)

        # Etiqueta de balance
        self.balance_label = tk.Label(self.frame, text=f"Balance: ${controller.get_balance()}",
                                      font=("Arial", 24, "bold"), fg="#FFD700", bg="#111111")
        self.balance_label.pack(pady=20)

        # Rodillos (reels)
        self.reel_frame = tk.Frame(self.frame, bg="#111111", bd=10, relief="ridge", pady=10)
        self.reel_frame.pack(pady=30)
        self.reel_labels = [
            tk.Label(self.reel_frame, text="❓", font=("Arial", 60, "bold"),
                     bg="#e74c3c", fg="white", width=5, height=2, relief="raised", bd=5)
            for _ in range(3)
        ]
        for label in self.reel_labels:
            label.pack(side="left", padx=15)

        # Entrada de apuesta
        self.bet_label = tk.Label(self.frame, text="¡Ingresa tu apuesta!", font=("Arial", 18),
                                  fg="#FFD700", bg="#111111")
        self.bet_label.pack(pady=10)

        self.bet_entry = tk.Entry(self.frame, font=("Arial", 18), justify="center",
                                  bg="#FFD700", fg="#111111", relief="solid", bd=2)
        self.bet_entry.pack(pady=10)
        self.bet_entry.insert(0, "10")

        # Botón de girar
        self.spin_button = tk.Button(self.frame, text="🎰 Girar 🎰", font=("Arial", 22, "bold"),
                                     bg="#FF6347", fg="white", relief="raised", borderwidth=5,
                                     command=self.controller.play)
        self.spin_button.pack(pady=20)

    def animate_background(self):
        """Animación cíclica de colores de fondo."""
        self.root.configure(bg=self.bg_colors[self.color_index])
        self.color_index = (self.color_index + 1) % len(self.bg_colors)
        self.root.after(500, self.animate_background)

    def animate_reels(self, final_result):
        """Animación visual del giro de los rodillos."""
        symbols = ["🍒", "🍋", "🍊", "🍉", "🍇"]

        # Giro rápido inicial
        for _ in range(20):
            for i in range(3):
                self.reel_labels[i].config(text=random.choice(symbols), fg="white")
            self.root.update()
            time.sleep(0.05)

        # Desaceleración progresiva con efecto visual
        for i in range(3):
            for _ in range(10 + i * 5):
                self.reel_labels[i].config(text=random.choice(symbols), fg="white")
                self.root.update()
                time.sleep(0.1 + i * 0.05)

            # Efecto de rebote antes de detenerse
            self.reel_labels[i].config(text=random.choice(symbols), fg="yellow")
            self.root.update()
            time.sleep(0.2)

            # Resultado final
            self.reel_labels[i].config(text=final_result[i], fg="#FFD700")
            self.root.update()

    def update_balance(self, balance):
        """Actualiza el texto del balance en la UI."""
        self.balance_label.config(text=f"Balance: ${balance}", fg="#2ecc71")
        self.root.update()
        time.sleep(0.3)
        self.balance_label.config(fg="#FFD700")
        self.root.update()

    def show_message(self, message, win=False):
        """Muestra una ventana emergente con el resultado del giro."""
        message_window = tk.Toplevel(self.root)
        message_window.title("Resultado")
        message_window.geometry("350x200")
        message_window.configure(bg="gold" if win else "red")

        msg_label = tk.Label(message_window, text=message, font=("Arial", 24, "bold"),
                             fg="white", bg=message_window.cget("bg"))
        msg_label.pack(pady=20)

        if win:
            # Parpadeo del mensaje
            for _ in range(5):
                msg_label.config(fg="black" if _ % 2 == 0 else "white")
                self.root.update()
                time.sleep(0.2)
        else:
            # Sacudida de la ventana en caso de pérdida
            for _ in range(10):
                x_offset = (-1) ** _ * 10
                message_window.geometry(f"350x200+{self.root.winfo_x() + x_offset}+{self.root.winfo_y()}")
                self.root.update()
                time.sleep(0.1)
            message_window.destroy()

# ----------------------------- CONTROLADOR -----------------------------
class SlotMachineController:
    """
    Clase que controla el flujo del juego.
    Conecta el modelo con la vista y maneja la lógica de interacción.
    """
    def __init__(self, root):
        self.model = SlotMachine()
        self.view = SlotMachineView(root, self)

    def get_balance(self):
        """Obtiene el balance del modelo."""
        return self.model.get_balance()

    def play(self):
        """Ejecuta una ronda del juego cuando el usuario hace clic en 'Girar'."""
        try:
            bet = int(self.view.bet_entry.get())

            if bet <= 0:
                self.view.show_message("La apuesta debe ser mayor que 0.")
                return

            if bet > self.model.get_balance():
                self.view.show_message("Saldo insuficiente para apostar.")
                return

            self.model.update_balance(-bet)
            self.view.update_balance(self.model.get_balance())
            self.view.spin_button.config(state="disabled")

            # Hilo para manejar el giro sin bloquear la interfaz
            def spin_reels():
                self.model.spin()
                self.view.animate_reels(self.model.result)
                winnings = self.model.calculate_winnings(bet)
                self.model.update_balance(winnings)
                self.view.update_balance(self.model.get_balance())
                self.view.show_message(
                    f"¡Ganaste ${winnings}! 🎉" if winnings > 0 else "No ganaste esta vez. 😞",
                    win=winnings > 0
                )
                self.view.spin_button.config(state="normal")

            threading.Thread(target=spin_reels, daemon=True).start()

        except ValueError:
            self.view.show_message("Por favor, introduce un número válido.")

# ----------------------------- EJECUCIÓN -----------------------------
if __name__ == "__main__":
    # Crea la ventana principal y lanza el controlador
    root = tk.Tk()
    controller = SlotMachineController(root)
    root.mainloop()
