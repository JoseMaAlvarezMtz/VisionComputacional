from PIL import Image, ImageDraw
import sys
from math import*
from time import*
import math
import random
 
def dfs(image, punto, visitados):

    pix = image.load()
    x, y = image.size
    toma_o = list()
    toma_o.append(punto)
    posibles = list()
    color = pix[tuple(punto)]
    if color != (255,255,255):
        return
 
    while len(toma_o) > 0:
        toma_actual = toma_o.pop(0)
        posibles.append(toma_actual)
        visitados[tuple(toma_actual)] = True
 
        for h in range(toma_actual[0]-1, toma_actual[0]+2):
            for l in range(toma_actual[1]-1, toma_actual[1]+2):
                if h >= 0 and l >= 0 and h < x and l < y:
                    if not visitados[h, l]:
                        if color == pix[h,l]:
                            if not [h, l] in toma_o:
                                toma_o.append([h, l])
    wrap(posibles, image)
    
 
def punto_visitado(x,y):

    visitados = dict()
    for i in range(x):
        for j in range(y):
            visitados[i,j] = False
    return visitados

def giro(env1, env2): #toma angulo para envolvimiento
  return float(sum((a*b) for a, b in zip(env1, env2)))
 
def toma_giro(p1, p2, p3):
    env1 = (p2[0]-p1[0], p2[1]-p1[1])
    env2 = (p2[0]-p3[0], p2[1]-p3[1])
 
    punto_env = giro(env1,env2)
    punto_forma = math.sqrt(giro(env1,env1))*math.sqrt(giro(env2,env2))
    a_linea = 0.0
    if punto_forma != 0:
        a_linea = punto_env / punto_forma
        if a_linea >= 1.0:
            return 0.0
        elif a_linea <= -1.0:
            return math.pi
        else:
            a_linea = math.degrees(math.acos(a_linea))
    return a_linea
 
def wrap(posibles, image): #metodo de wrapping o marcha de jarvis
    env_hull = min(posibles)
    wrap = list()
    i = 0
 
    while False is not True:
        wrap.append(env_hull)
        final = [posibles[0], 0.0]
            
        for j in range(0, len(posibles)): #para dibujar las lineas segun su angulo y los puntos seleccionados 
            if len(wrap) > 1:
                inclina = toma_giro(wrap[i-1], wrap[i], posibles[j])
            else:
                toma = (wrap[0][0], wrap[0][1]-1) 
                inclina = toma_giro(toma, wrap[i], posibles[j])
 
            if (final[0] == env_hull) or inclina > final[1]:
                final[0] = posibles[j]
                final[1] = inclina
        i = i+1
        env_hull = final[0]
        if final[0] == wrap[0]:
            break
#aplica wrap 
    draw = ImageDraw.Draw(image)
    for i in range(1, len(wrap)):
	draw.rectangle((wrap[i-1][0], wrap[i-1][1], wrap[i][0], wrap[i][1]) , outline="blue")

        draw.line((wrap[i-1][0], wrap[i-1][1], wrap[i][0], wrap[i][1]) , fill=(255,0,0))
    #draw.rectangle((wrap[i-1][0], wrap[i-1][1], wrap[i][0], wrap[i][1]) , outline="blue")
    #draw.rectangle((wrap[len(wrap)-1][0], wrap[len(wrap)-1][1], wrap[0][0], wrap[0][1]) , outline="blue")
    
    draw.line((wrap[len(wrap)-1][0], wrap[len(wrap)-1][1], wrap[0][0], wrap[0][1]) , fill=(255,0,0))
    draw.rectangle((wrap[len(wrap)-1][0], wrap[len(wrap)-1][1], wrap[0][0], wrap[0][1]) , outline="blue")
    
def main():
    image = Image.open(sys.argv[1])
    
    x,y = image.size
    visitados = punto_visitado(x,y)
    #draw = ImageDraw.Draw(image)
     
    for i in range(x):
        for j in range(y):
            if not visitados[i, j]:
                dfs(image, [i, j], visitados)
    #draw.line((visitados[i-1][0], visitados[i-1][1], visitados[i][0], visitados[i][1]) , fill=(255,0,0))
    image.save('hull.png')
    return x,y
if __name__ == "__main__":
     main()

