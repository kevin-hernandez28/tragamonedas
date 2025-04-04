# 🎰 Juego de Tragamonedas en Python (MVC + Concurrencia)

Este proyecto es un **juego de tragamonedas** desarrollado en Python, utilizando el patrón de diseño **Modelo-Vista-Controlador (MVC)** y técnicas de **concurrencia** con hilos (`threading`). La interfaz gráfica está construida con `Tkinter`, e incluye animaciones, control de apuestas, sincronización y mensajes interactivos.

---

## ✅ Objetivos del Proyecto

- Aplicar el patrón de diseño **MVC** para separar responsabilidades.
- Utilizar **programación orientada a objetos (POO)** de forma estructurada.
- Implementar **concurrencia** para mantener la interfaz fluida durante el juego.
- Manejar la **sincronización** para proteger recursos compartidos como el balance del jugador.

---

## 🖥️ Requisitos

- Python 3.10 o superior

---

## 🚀 Cómo Ejecutar

1. Clona este repositorio:

```bash
git clone https://github.com/kevin-hernandez28/tragamonedas.git
cd tragamonedas
```

2. Ejecuta el archivo principal:

```bash
python tragamonedas.py
```

---

## 🧠 Diseño MVC

### Modelo (Model)
- Clase `SlotMachine`: gestiona símbolos, resultados, balance y cálculo de ganancias.
- Usa `threading.Lock` para sincronizar el acceso al balance.

### Vista (View)
- Clase `SlotMachineView`: interfaz gráfica con `Tkinter`, muestra balance, apuestas, rodillos y resultados.
- Contiene animaciones y efectos visuales.

### Controlador (Controller)
- Clase `SlotMachineController`: maneja la lógica del juego y la interacción entre modelo y vista.
- Lanza hilos para que las animaciones no bloqueen la interfaz.

---

## 🔄 Concurrencia y Sincronización

- Usa `threading.Thread` para mantener la interfaz responsiva mientras se ejecuta la lógica del juego.
- Usa `threading.Lock` para proteger operaciones críticas:

```python
with self.lock:
    self.result = [random.choice(self.symbols) for _ in range(3)]
```

---

## ✨ Funcionalidades

- Animaciones de rodillos con símbolos de frutas.
- Control de apuestas y validación de saldo.
- Cálculo automático de ganancias.
- Protección del balance con sincronización.
- Interfaz colorida con mensajes personalizados.

---

## 📌 Aprendizajes

- Uso de MVC en aplicaciones Python.
- Manejo de hilos y concurrencia con `threading`.
- Sincronización de acceso a datos compartidos.
- Mejores prácticas de programación orientada a objetos.
