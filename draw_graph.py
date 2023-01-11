"""Simple and not very good Tk program that draws dependencies graphs."""
import tkinter as tk

from dep_graph import get_graph

graph = get_graph({
    "pkg1": ["pkg2", "pkg3"],
    "pkg2": ["pkg4"],
    "pkg3": [],
    "pkg4": ["pkg5"],
    "pkg5": ["pkg6"],
    "pkg6": ["pkg7"],
    "pkg7": ["pkg8"],
    "pkg8": ["pkg9"],
    "pkg9": ["pkg3"]
})

window = tk.Tk()
canvas = tk.Canvas(window)
canvas.pack()

# This can be done nicely by using a yield
powers_of_two = [2 ** n for n in range(100)]

x = 180
y = 40
index = 0
x_offset = 0
last_two_power = 0
next_two_power = 2

locations = {}
radius = 23
for node in graph._nodes:
    if (index + 1) == next_two_power:
        last_two_power = next_two_power
        next_two_power *= 2
        y += 50
        x_offset += 35

    x = 150 + (x_offset if ((index + 1) >
                            (next_two_power / 2)) == 0 else -x_offset)

    locations[node] = canvas.create_rectangle(x,
                                              y,
                                              x + 35,
                                              y + 35,
                                              fill="blue")
    canvas.create_text(x + 18,
                       y + 15,
                       text=node,
                       fill="white",
                       justify=tk.CENTER)
    index += 1

for edge in graph._edges:
    if edge.source == edge.target:
        continue

    ax0, ay0, ax1, ay1 = canvas.coords(locations[edge.source])
    bx0, by0, bx1, by1 = canvas.coords(locations[edge.target])

    x0 = (ax0 + ax1) / 2
    y0 = (ay0 + ay1) / 2

    x1 = (bx0 + bx1) / 2
    y1 = (by0 + by1) / 2

    x0 += 15 if x0 < x1 else -15
    y0 += 15 if y0 < y1 else -15
    x1 += 15 if x0 > x1 else -15
    y1 += 15 if y0 > y1 else -15

    if (y0 == y1):
        y1 += 15
        y0 += 15

    line_id = canvas.create_line(x0, y0, x1, y1, arrow=tk.LAST)
    canvas.tag_lower(line_id)

window.mainloop()
