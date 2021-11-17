import tkinter as tk
import numpy as np
from model import Model

RADIUS = 100
XCENTER = 200
YCENTER = 200


def create_circle(x, y, r, canvasName): # center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1)

def polar_to_rect(r, theta):
    x = int(XCENTER + r * np.cos(theta))
    y = int(YCENTER + r * np.sin(theta))

    return x, y


class Animation(tk.Frame):
    def __init__(self, parent, model, paused):
        super().__init__()

        self.model = model
        self.paused = paused

        sim_frm = tk.Frame(master=parent)
        sim_frm.pack()

        self.canvas = tk.Canvas(width=XCENTER * 2, height=YCENTER * 2, master=sim_frm)
        self.canvas.pack()

    def reset_parameters(self, model, paused):
        self.model = model
        self.paused = paused

    def draw(self):
        self.canvas.delete("all")

        # Unit circle
        create_circle(XCENTER, YCENTER, RADIUS, self.canvas)

        if not self.paused:
            # Masses
            for t in self.model.theta:
                x, y = polar_to_rect(RADIUS, t)
                create_circle(x, y, 5, self.canvas)
                self.model.advance()

            # Center of Mass
            avg_theta = np.average(self.model.theta)
            R = (1 / self.model.N) * np.abs(np.sum(np.e ** (1j * self.model.theta)))
            avg_x, avg_y = polar_to_rect(R * RADIUS, avg_theta)

            self.canvas.create_line(XCENTER, YCENTER, avg_x, avg_y)

        self.after(10, self.draw)


class View(tk.Tk):
    def __init__(self):
        super().__init__()

        self.paused = True
        self.model = Model(100, 10)

        ### Title
        title_frm = tk.Frame(master=self)
        title_frm.pack()
        title_lbl = tk.Label(text="Kuramoto Simulation", master=title_frm)
        title_lbl.pack(fill=tk.X, side=tk.TOP)

        ### Simulation Frame
        anim_frm = Animation(self, self.model, self.paused)
        anim_frm.draw()

        ### Control Frame
        def start_callback():
            nonlocal anim_frm
            # Get N and K from Text
            try:
                K = int(K_ent.get())
                N = int(N_ent.get())
            except ValueError:
                error_lbl.config(text="Bad input. Try again.")
                return

            error_lbl.config(text="")

            self.model = Model(N, K)
            anim_frm.model = self.model
            anim_frm.paused = False

        def pause_callback():
            nonlocal anim_frm
            anim_frm.paused = True

        control_frm = tk.Frame(master=self)
        control_frm.pack()
        start_btn = tk.Button(text="Start Simulation",
                              height=2,
                              width=12,
                              master=control_frm,
                              command=start_callback)
        start_btn.pack()
        pause_btn = tk.Button(text="Reset",
                              height=2,
                              width=6,
                              master=control_frm,
                              command=pause_callback)
        pause_btn.pack()

        K_frm = tk.Frame(master=self)
        K_frm.pack()
        K_lbl = tk.Label(text="K", master=K_frm)
        K_lbl.pack(side=tk.LEFT)
        K_ent = tk.Entry(width=1,
                         master=K_frm)
        K_ent.pack(side=tk.RIGHT)

        N_frm = tk.Frame(master=self)
        N_frm.pack()
        N_lbl = tk.Label(text="N", master=N_frm)
        N_lbl.pack(side=tk.LEFT)
        N_ent = tk.Entry(width=3,
                         master=N_frm)
        N_ent.pack(side=tk.RIGHT)

        error_lbl = tk.Label(text="")
        error_lbl.pack()
