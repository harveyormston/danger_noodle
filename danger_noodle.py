import random
from itertools import product

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

PXL = 10
NPX = 50
INITIAL_RATE = 100
RATE_SCALE = 0.99


class MainApplication(tk.Frame):

    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.parent.bind_all('<KeyPress>', self.keypress)
        self.parent.bind_all('<KeyRelease>', self.keyrelease)
        self.height = PXL * NPX
        self.width = PXL * NPX
        self.canvas = tk.Canvas(self.parent, bg="black", height=self.height, width=self.width)
        self.pos = (PXL, PXL)
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.rate = INITIAL_RATE
        self.blocks = []
        self.create_block()
        self.pickup = None
        self.animated = False

        range_x = list(range(PXL, self.width, PXL))
        range_y = list(range(PXL, self.height, PXL))

        self.all_pxls = [(x, y) for x, y in product(range_x, range_y)]

        self.animate()

    def reset(self):

        self.animated = False
        self.parent.config(cursor='')

        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.rate = INITIAL_RATE

        if self.pickup is not None:
            self.canvas.delete(self.pickup)
            self.pickup = None

        for block in self.blocks:
            self.canvas.delete(block)

        self.blocks = []
        self.create_block()
        self.start()

    def win(self):

        self.canvas.configure(background="green")
        self.animated = False
        self.parent.config(cursor='')

    def stop(self):

        self.canvas.configure(background="red")
        self.animated = False
        self.parent.config(cursor='')

    def start(self):

        self.canvas.configure(background="black")

    def keypress(self, event):

        drx, dry = self.direction
        if event.keysym == 'Right':
            if drx != -PXL:
                self.next_direction = (PXL, 0)
                self.animated = True
        elif event.keysym == 'Left':
            if drx != PXL:
                self.next_direction = (-PXL, 0)
                self.animated = True
        elif event.keysym == 'Up':
            if dry != PXL:
                self.next_direction = (0, -PXL)
                self.animated = True
        elif event.keysym == 'Down':
            if dry != -PXL:
                self.next_direction = (0, PXL)
                self.animated = True
        elif event.keysym == 'q':
            self.parent.destroy()
        elif event.keysym == 'p':
            self.animated = False
            self.parent.config(cursor='')
        elif event.keysym == 'r':
            self.reset()

    def keyrelease(self, event):
        pass

    def create_block(self):

        bsx = random.randint(2, NPX - 2) * PXL
        bsy = random.randint(2, NPX - 2) * PXL

        coord = (bsx, bsy, bsx + PXL, bsy, bsx + PXL, bsy + PXL, bsx, bsy + PXL)

        self.blocks.append(
            self.canvas.create_polygon(*coord, fill="white", outline='black'))

        self.canvas.pack()

    def add_pickup(self):

        tail_coords = [tuple(self.canvas.coords(b)[:2]) for b in self.blocks]
        pickup_candidates = [p for p in self.all_pxls if p not in tail_coords]

        if pickup_candidates:
            bsx, bsy = random.choice(pickup_candidates)
            coord = (bsx, bsy, bsx + PXL, bsy, bsx + PXL, bsy + PXL, bsx, bsy + PXL)
            self.pickup = self.canvas.create_polygon(*coord, fill="white", outline='black')
        else:
            self.win()

    def animate(self):

        if self.animated:

            self.parent.config(cursor='none')

            if self.pickup is None:
                self.add_pickup()

            head = self.blocks[0]

            self.direction = self.next_direction

            drx, dry = self.direction
            hcx, hcy = self.canvas.coords(head)[:2]
            pcx, pcy = self.canvas.coords(self.pickup)[:2]

            out_of_bounds_x = not 0 <= hcx < self.width
            out_of_bounds_y = not 0 <= hcy < self.height

            tail_collision = any([
                self.canvas.coords(head) == self.canvas.coords(block)
                for block in self.blocks[1:]])

            if out_of_bounds_x or out_of_bounds_y or tail_collision:

                self.stop()

            else:

                picked_up = (hcx + drx == pcx) and (hcy + dry == pcy)

                if picked_up:
                    self.blocks.append(self.pickup)
                    self.add_pickup()
                    self.rate *= RATE_SCALE

                # move all blocks in the tail forward by one
                new_coords = [self.canvas.coords(block) for block in self.blocks[:-1]]
                for block, nc in zip(self.blocks[1:], new_coords):
                    ncx, ncy = nc[:2]
                    ccx, ccy = self.canvas.coords(block)[:2]
                    self.canvas.move(block, ncx - ccx, ncy - ccy)

                # move the head forward by one
                self.canvas.move(head, drx, dry)

        self.parent.after(int(self.rate), self.animate)


if __name__ == '__main__':

    root = tk.Tk()
    root.title("Danger Noodle")
    root.lift()
    root.attributes("-topmost", True)
    root.after_idle(root.attributes, '-topmost', False)
    root.resizable(width=False, height=False)
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
