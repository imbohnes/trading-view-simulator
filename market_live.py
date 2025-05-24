import tkinter as tk
import random
import turtle
from turtle import RawTurtle, ScrolledCanvas

class MarketSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading view simulator")
        self.candles = []
        self.candle_width = 20
        self.max_candles = 50

        self.setup_ui()
        self.root.after(100, self.start_simulation)

    def setup_ui(self):
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = ScrolledCanvas(self.canvas_frame, width=1000, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor("black")
        self.t = RawTurtle(self.screen)
        self.t.hideturtle()
        self.t.speed(0)
        self.t.pensize(2)

        self.price_label = tk.Label(self.root, text="Price: 0", font=("Arial", 14))
        self.price_label.pack()

    def start_simulation(self):
        self.draw_all_candles()
        self.auto_generate()

    def generate_candle(self):
        if self.candles:
            prev_close = self.candles[-1]['Close']
        else:
            prev_close = random.uniform(100, 200)

        open_price = prev_close + random.uniform(-5, 5)
        close_price = open_price + random.uniform(-10, 10)
        high_price = max(open_price, close_price) + random.uniform(0, 5)
        low_price = min(open_price, close_price) - random.uniform(0, 5)
        volume = random.randint(100, 1000)

        return {
            'Open': open_price,
            'High': high_price,
            'Low': low_price,
            'Close': close_price,
            'Volume': volume
        }

    def draw_all_candles(self):
        #self.t.clear()

        # Draw grid
        self.t.color("gray")
        for y in range(-250, 300, 50):
            self.t.penup()
            self.t.goto(-500, y)
            self.t.pendown()
            self.t.goto(500, y)

        x_start = -480
        for idx, candle in enumerate(self.candles[-self.max_candles:]):
            x = x_start + idx * (self.candle_width + 2)
            self.draw_candle(x, candle)

    def draw_candle(self, x, candle):
        open_y = candle['Open']
        close_y = candle['Close']
        high_y = candle['High']
        low_y = candle['Low']

        scale = 3
        open_px = open_y * scale - 400
        close_px = close_y * scale - 400
        high_px = high_y * scale - 400
        low_px = low_y * scale - 400

        color = "green" if close_y >= open_y else "red"

        # Wick
        self.t.penup()
        self.t.goto(x, low_px)
        self.t.pendown()
        self.t.color(color)
        self.t.goto(x, high_px)

        # Body
        self.t.penup()
        top = max(open_px, close_px)
        bottom = min(open_px, close_px)
        self.t.goto(x - self.candle_width // 2, bottom)
        self.t.begin_fill()
        self.t.pendown()
        self.t.goto(x + self.candle_width // 2, bottom)
        self.t.goto(x + self.candle_width // 2, top)
        self.t.goto(x - self.candle_width // 2, top)
        self.t.goto(x - self.candle_width // 2, bottom)
        self.t.end_fill()
                # نمایش قیمت روی کندل
        '''self.t.penup()
        self.t.goto(x + self.candle_width, top + 10)  # موقعیت قیمت
        self.t.color("white")
        self.t.write(f"{candle['Close']:.2f}", align="left", font=("Arial", 10, "normal"))'''


    def auto_generate(self):
        try:
            if not self.root.winfo_exists():
                return
            new_candle = self.generate_candle()
            self.candles.append(new_candle)
            self.price_label.config(text=f"Price: {new_candle['Close']:.2f}")
            self.draw_all_candles()
            self.root.after(2000, self.auto_generate)
        except tk.TclError:
            pass

if __name__ == '__main__':
    root = tk.Tk()
    simulator = MarketSimulator(root)
    root.mainloop()
