from PIL import Image 
from PIL import ImageDraw
import random
from sys import argv

(TURN_LEFT, TURN_RIGHT, TURN_NONE) = (1, -1, 0)


def turn(p, q, r):
    n = cmp((q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1]- p[1]), 0)
    return n


def _dist(p, q):
    (dx, dy) = (q[0] - p[0], q[1] - p[1])
    return dx * dx + dy * dy


def _next_hull_pt(points, p):
    q = p
    for r in points:
        t = turn(p, q, r)
        if t == TURN_RIGHT or t == TURN_NONE and _dist(p, r) > _dist(p,
                q):
            q = r
    return q


def convex_hull(points):
    hull = [min(points)]

    # print hull

    for p in hull:
        q = _next_hull_pt(points, p)
        if q != hull[0]:
            hull.append(q)

    # print hull

    return hull


def bfs(
    imagen,
    rcolor,
    px,
    altura,
    ancho,
    ):
    pixeles = imagen.load()
    (fila, columna) = px
    original = pixeles[fila, columna]
    cola = [(fila, columna)]
    cola2 = []
    while len(cola) > 0:
        (fila, columna) = cola.pop(0)
        actual = pixeles[fila, columna]
        if actual == original or actual == rcolor:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    candidato = (fila + dy, columna + dx)
                    if candidato[0] >= 0 and candidato[0] < altura \
                        and candidato[1] >= 0 and candidato[1] < ancho:
                        contenido = pixeles[candidato[0], candidato[1]]
                        if contenido == original:
                            pixeles[candidato[0], candidato[1]] = rcolor
                            cola.append(candidato)
                            cola2.append(candidato)
    return (imagen, cola2)


def main(archivo):
    imagen = Image.open(archivo)
    pixeles = imagen.load()
    d = imagen.size
    colores = []
    cantidades = []
    hulls = []
    for x in range(d[0]):
        for y in range(d[1]):
            if pixeles[x, y] == (0, 0, 0):
                rcolor = (random.randint(0, 256), random.randint(0,
                          256), random.randint(0, 256))
                (imagen2, cola2) = bfs(imagen, rcolor, (x, y), d[0],
                        d[1])
                colores.append(rcolor)
                hulls.append(convex_hull(cola2))

    # checar el color mas usado

    for i in range(len(colores)):
        cantidades.insert(i, colores.count(i))
    maximo = max(cantidades)
    lugar = cantidades.index(maximo)
    c_fondo = colores[lugar]

    # print c_fondo

    pixeles2 = imagen2.load()
    for i in range(0, d[0]):  # aplico gris al fondo
        for j in range(0, d[1]):
            p = pixeles2[i, j]
            if p == c_fondo:
                pixeles2[i, j] = (p[0], p[0], p[0])

    for i in range(len(hulls)):
        for j in range(len(hulls[i]) - 1):
            pixeles2[i, j] = (255, 0, 0)
    draw = ImageDraw.Draw(imagen2)  # dibujo las lineas

    for i in range(len(hulls)):
        for j in range(len(hulls[i]) - 1):
            draw.line((hulls[i][j], hulls[i][j + 1]),
                      fill='rgb(0, 0, 255)')
    imagen2.save('final_line.jpg')


archivo = argv[1]
main(archivo)

