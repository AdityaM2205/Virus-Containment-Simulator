import random
import tkinter as tk
from PIL import Image, ImageTk


SIZE = 10
CELL = 50


Col = {'E': 'white', 'I': 'red', 'Q': 'blue', 'S': 'green', 'G': 'black'}


INFECT_CHANCE = 0.7
MOVES_MAX = 3
moves = MOVES_MAX

grid = [['E' for _ in range(SIZE)] for _ in range(SIZE)]
turns = 0


for _ in range(3):
    x, y = random.randint(0, SIZE-1), random.randint(0, SIZE-1)
    grid[x][y] = 'I'


DIRECTIONS = [(0,1), (1,0), (0,-1), (-1,0)]

def score():
    return sum(1 for row in grid for cell in row if cell == 'E')

def load_img(file, size):
    img = Image.open(file).resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

def show_popup(title, msg, img_file):
    pop = tk.Toplevel(root)
    pop.title(title)
    pop.geometry("300x300")
    tk.Label(pop, text=msg, font=("Arial", 12)).pack()
    try:
        img = load_img(img_file, (200, 200))
        lbl = tk.Label(pop, image=img)
        lbl.image = img
        lbl.pack()
    except Exception as e:
        print(f"Error loading {img_file}: {e}")
    tk.Button(pop, text="OK", command=pop.destroy).pack()
    pop.wait_window()

def infect_new():
    if random.random() < 0.2:
        empty = [(x, y) for x in range(SIZE) for y in range(SIZE) if grid[x][y] == 'E']
        if empty:
            x, y = random.choice(empty)
            grid[x][y] = 'I'

def draw():
    canvas.delete("all")
    for x in range(SIZE):
        for y in range(SIZE):
            canvas.create_rectangle(y*CELL, x*CELL, (y+1)*CELL, (x+1)*CELL, fill=Col[grid[x][y]], outline=Col['G'])

def outbreak_stopped():
    return all(grid[x][y] != 'I' or all(grid[nx][ny] != 'E' for dx, dy in DIRECTIONS if 0 <= (nx:=x+dx) < SIZE and 0 <= (ny:=y+dy) < SIZE) for x in range(SIZE) for y in range(SIZE))

def spread():
    new_inf = [(nx, ny) for x in range(SIZE) for y in range(SIZE) if grid[x][y] == 'I' for dx, dy in DIRECTIONS if 0 <= (nx:=x+dx) < SIZE and 0 <= (ny:=y+dy) < SIZE and grid[nx][ny] == 'E' and random.random() < INFECT_CHANCE]
    for x, y in new_inf:
        grid[x][y] = 'I'

def place(event):
    global moves
    if moves > 0:
        x, y = event.y // CELL, event.x // CELL
        if grid[x][y] == 'E':
            grid[x][y] = 'S' if turns >= 3 and random.random() < 0.1 else 'Q'
            moves = moves - 1
            moves_lb.config(text=f"Moves: {moves}")
            draw()

def turn():
    global turns, moves
    if outbreak_stopped():
        show_popup("Victory!", f"You stopped the outbreak!\nTurns: {turns}\nScore: {score()}", "victory.jpg")
        root.quit()
        return
    spread()
    infect_new()
    for x in range(SIZE):
        for y in range(SIZE):
            if grid[x][y] == 'S':
                for dx, dy in DIRECTIONS:
                    if 0 <= (nx:=x+dx) < SIZE and 0 <= (ny:=y+dy) < SIZE and grid[nx][ny] == 'I':
                        grid[nx][ny] = 'E'
    moves = MOVES_MAX
    turns += 1
    turns_lb.config(text=f"Turns: {turns}")
    moves_lb.config(text=f"Moves: {moves}")
    draw()
    if score() == 0:
        show_popup("Game Over", f"The city is fully infected!\nTurns: {turns}\nScore: {score()}", "loss.png")
        root.quit()

root = tk.Tk()
root.title("Virus Containment Simulator")
canvas = tk.Canvas(root, width=SIZE*CELL, height=SIZE*CELL)
canvas.pack()
turns_lb = tk.Label(root, text=f"Turns: {turns}")
turns_lb.pack()
moves_lb = tk.Label(root, text=f"Moves: {moves}")
moves_lb.pack()
canvas.bind("<Button-1>", place)
tk.Button(root, text="Next Turn", command=turn).pack()
draw()
root.mainloop()
