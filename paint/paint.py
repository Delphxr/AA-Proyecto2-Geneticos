import pygame,math,random,time,sys
from pygame.locals import *
from PIL import Image,ImageChops
import copy


#parametros importantes:
numero_generaciones_totales = 20
individuos_por_generacion = 10
subindividuos_generacion = 10 ##como hay aleatoriedad en la creacion vamos a crear varios arboles para cada miembro de la generacion



screen = pygame.display.set_mode((1280, 720))


#paleta de colores del 1 al 5, de mas claro a mas oscuro:
COLOR_1 = pygame.Color("#c7f9cc")
COLOR_2 = pygame.Color("#80ed99")
COLOR_3 = pygame.Color("#57cc99")
COLOR_4 = pygame.Color("#38a3a5")
COLOR_5 = pygame.Color("#22577a")

#constantes:
TREE_POS_X = 955
TREE_POS_Y = 359



pygame.init()


## font setup
menu_font = pygame.font.Font("font.ttf", 17) #pygame.font.SysFont("consolas", 17)
clear_text = menu_font.render("Limpiar", True, COLOR_1)
brush_text = menu_font.render("Herramientas", True, COLOR_1)
save_text = menu_font.render("Iniciar", True, COLOR_1)


draw = False
brush_size = 5
brush_color = COLOR_5


menu_rect = pygame.Rect(0, 0, 150, 360)




tree_rect = pygame.Rect(640, 0, 640, 720)
tree_drawing_canvas_rect = pygame.Rect(795, 20, 320, 360)

porcentaje_rect = pygame.Rect(27, 600, 260, 200)

left_scr_rect = pygame.Rect(0, 0, 640, 720)
drawing_canvas_rect = pygame.Rect(160, 20, 320, 360)
drawing_canvas_shadow_rect = pygame.Rect(170, 30, 320, 360)

pygame.draw.rect(screen, COLOR_2, tree_rect)
pygame.draw.rect(screen, COLOR_3, left_scr_rect)
pygame.draw.rect(screen, COLOR_2, tree_rect)


pygame.draw.rect(screen, COLOR_4, drawing_canvas_shadow_rect)


eraser_rect = pygame.Rect(27, 95, 40, 40)
draw_rect = pygame.Rect(72, 95, 40, 40)

thin_brush = pygame.Rect(72, 140, 40, 40)
medium_brush = pygame.Rect(72, 185, 40, 40)
thick_brush = pygame.Rect(27, 140, 40, 40)
supa_brush = pygame.Rect(27, 185, 40, 40)

clear_rect = pygame.Rect(27, 290, 90, 25)
save_rect = pygame.Rect(27, 260, 90, 25)
save_flag = False


names_par = menu_font.render("profundidad,tamanno,cantidad_ramas, ancho_tronco,random1, random2", True, COLOR_1)



def get_diferencia(dibujo,arbol,generacion,individuo,subindividuo,parametros=[]):
    """[vara de prueba para ver las diferencias entre imagenes]

    Args:
        imagen ([pygame image]): [imagen que vamos a comparar]
    """    
    pil_string_dibujo = pygame.image.tostring(dibujo, "RGB",False)
    pil_dibujo = Image.frombytes("RGB",(320,360),pil_string_dibujo)
    #convertimos la imagen de pygame en una imagen de pillow
    pil_string_arbol = pygame.image.tostring(arbol, "RGB",False)
    pil_arbol = Image.frombytes("RGB",(320,360),pil_string_arbol)
    #convertimos la imagen de pygame en una imagen de pillow


    diff = ImageChops.difference(pil_dibujo,pil_arbol)
    porcentaje = 100
    if diff.getbbox():
        #diff.show()
        img = pygame.image.fromstring(diff.tobytes(), diff.size, diff.mode)

        img = pygame.transform.scale(img, (220,248))
        porcentaje = get_black_percentage((220,248),img)
        porcentaje_txt = menu_font.render("{:.5f}".format(porcentaje) + "%", True, COLOR_1)
        info_txt = menu_font.render("G: " + str(generacion+1) + "- M: " + str(individuo+1) + "- SM: " + str(subindividuo+1), True, COLOR_1)
        par_txt = menu_font.render(str(parametros), True, COLOR_1)
        pygame.draw.rect(screen, COLOR_3, porcentaje_rect)

        screen.blit(porcentaje_txt, (27, 600))
        screen.blit(info_txt, (27, 620))
        screen.blit(par_txt, (27, 640))
        screen.blit(names_par, (27, 660))

        screen.blit(img, (300, 410))
    return porcentaje


# ------------------------------------- #
def modificar_parametro(parametro,mutacion=0,decimales=False):
    """[recibimos un parametro y lo retornamos mutado (positivo para evitar cosas raras)]

    Args:
        parametro ([int]): [parametro que vamos a mutar]
        mutacion (int, optional): [cantidad de mutacion que hay, mas alto mas deberia cambiar]. Defaults to 0.

    Returns:
        [int]: [parame mutado]
    """    
    multiplier = 0
    if decimales:
        multiplier = get_random(mutacion)

    multiplier = random.choice([-1,1]) #hacemos negativo o positivo
    
    parametro += multiplier
    parametro = round(parametro, 2)

    

    return abs(parametro)

def mutar_parametros(par,mutacion=0):
    """[mutamos un parametro al azar de la lista de parametros]

    Args:
        parametros ([lista]): [lista con los parametros]
        mutacion (int, optional): [indice de mutacionm, se recomienda que el maximo sea 3 para que no cambie mucho]. Defaults to 0.

    Returns:
        [list]: [nueva lista de parametros]
    """    
    par_copy = copy.deepcopy(par)
    allow_decimales = [1,4,5]
    parametro_a_mutar = random.choice(par_copy)
    indice_pam = par_copy.index(parametro_a_mutar)


    parametro_a_mutar = modificar_parametro(parametro_a_mutar,1,indice_pam in allow_decimales)


    par_copy[indice_pam] = parametro_a_mutar

    #random angle
    if par_copy[4] > 45:
        par_copy[4] = 45

    #random size
    if par_copy[5] > 10:
        par_copy[5] = 10

    #profundidad
    if par_copy[0] > 6:
        par_copy[0] = 5
    
        if par_copy[2] > 5:
            par_copy[2] = 5


    return par_copy


def get_black_percentage(size,img):
    color = pygame.Color((0, 0, 0, 255))

    width = size[0]
    height = size[1]
    total_number_of_pixels = width * height
    number_of_pixels = 0

    for x in range(0, width):
        for y in range(0, height):
            #print(img.get_at((x, y)))
            if img.get_at((x, y)) == color:
                number_of_pixels += 1

    percentage = number_of_pixels / total_number_of_pixels * 100
    return percentage

def get_parametros_random():
    """[lo usamos para obtener parametros para la poblacion inicial]

    Returns:
        [array]: [lista con los parametros]
    """    
    profundidad = random.randint(3,7)
    tamanno = random.randint(10,15)
    cantidad_ramas = random.randint(0,6)
    ancho_tronco=8 #esto lo hacemos constante por que siempre va a ser igual al dibujo
    random1 = random.randint(1,20) #el de angulos
    random2 = random.randint(1,10) #este no puede ser tan grande o se hace algo rarisimo

    if profundidad > 5:
        tamanno = random.randint(5,8)
        cantidad_ramas = random.randint(2,4)



    return [profundidad,tamanno,cantidad_ramas,ancho_tronco,random1,random2]
    #tree(x1=TREE_POS_X,y1=TREE_POS_Y,profundidad=5,tamanno=10,cantidad_ramas=3,ancho_tronco=8,random1=5,random2=5)


def get_nueva_generacion(palangana,cantidad=8,mutacion=1,numero_generacion=0):

    img1 = get_draw_image() #imagen de la silueta que dimos
    poblacion = []
    parametros_poblacion = []
    porcentajes = []
    porcentaje_temporal = 0

    
 


    x = palangana
    parametros_mutados = palangana
    

    for i in range(0,cantidad):
        porcentaje_temporal = 0

        for j in range (0,subindividuos_generacion):
            tree(x1=TREE_POS_X,y1=TREE_POS_Y,profundidad=parametros_mutados[0],tamanno=parametros_mutados[1],cantidad_ramas=parametros_mutados[2],ancho_tronco=8,random1=parametros_mutados[4],random2=parametros_mutados[5])
            pygame.display.update()
            img2 = get_tree_image()
            poblacion += [img2]
            porcentaje = get_diferencia(img1,img2,numero_generacion,i,j,parametros_mutados)
            porcentaje_temporal += porcentaje
            clean_tree_canvas()
            pygame.event.clear()
        
        parametros_poblacion += [parametros_mutados]

        porcentaje_temporal = porcentaje_temporal/subindividuos_generacion
        porcentajes += [porcentaje_temporal]

        parametros_mutados = x
        parametros_mutados = mutar_parametros(parametros_mutados,1)

        
        
        
    
    index_best_porcentage = porcentajes.index(max(porcentajes)) #obtenemos el index del porcentage mas alto

    best_parametros = parametros_poblacion[index_best_porcentage]
    return best_parametros

def get_poblacion_inicial(cantidad=8):
    """[obtenemos la poblacion inicial]

    Args:
        cantidad (int, optional): [cantidad de individuos de la poblacion inicial]. Defaults to 8.

    Returns:
        [array]: [lista con los parametros del mejor arbol de la poblacion inicial]
    """    
    img1 = get_draw_image()
    poblacion_inicial = []
    parametros_poblacion_inicial = []
    porcentajes = []
    for i in range(0,cantidad):
        parametros = get_parametros_random() #obtenemos los parametros
        parametros_poblacion_inicial += [parametros]

        clean_tree_canvas()
        tree(x1=TREE_POS_X,y1=TREE_POS_Y,profundidad=parametros[0],tamanno=parametros[1],cantidad_ramas=parametros[2],ancho_tronco=parametros[3],random1=parametros[4],random2=parametros[5])
        
        pygame.display.update()
        img2 = get_tree_image()
        poblacion_inicial += [img2]
        porcentaje = get_diferencia(img1,img2,0,0,0)
        porcentajes += [porcentaje]
    
    index_best_porcentage = porcentajes.index(max(porcentajes)) #obtenemos el index del porcentage mas alto

    best_parametros = parametros_poblacion_inicial[index_best_porcentage]

    
    return best_parametros



#----------------------------------------#

def get_random(range=1):
    return random.uniform(-range, range) * random.choice([-1,1])

def reduce_num(num):
    if num == 1:
        return num
    else:
        return num - 0.75


def get_tree_image():
    """[guardamos una imagen del arbl generado]

    Returns:
        [imagen/surface]: [retornamos la variable con la imagen]
    """    
    save_surface_tree = pygame.Surface((320, 360))
    save_surface_tree.blit(screen, (0, 0), (795, 20, 320, 360))
    return save_surface_tree

def get_draw_image():
    save_surface_draw = pygame.Surface((320, 360))
    save_surface_draw.blit(screen, (0, 0), (160, 20, 320, 360))
    return save_surface_draw

def drawTree(x1, y1, angle, depth, angulo_inicio, tamanno,cantidad_ramas=4,grueso=2, random=0,random2=0):
    
    base_len = tamanno
    if depth > 0:
        x2 = x1 + int(math.cos(math.radians(angle))*depth*base_len)
        y2 = y1 + int(math.sin(math.radians(angle))*depth*base_len)


        pygame.draw.line(screen, COLOR_5, (x1, y1), (x2, y2), grueso)

       
        angle_diference = 0
        if cantidad_ramas < 2:
            initial_angle = -90
            angle_diference = 0

        else:
            angle_diference = (-180)/cantidad_ramas + get_random(random) 
            initial_angle = (angulo_inicio) - (180)/(cantidad_ramas)  + get_random(random)
        if cantidad_ramas==2:
            initial_angle+=45

        for i in range(0,cantidad_ramas):
            drawTree(x2, y2, initial_angle, depth - 1, initial_angle, tamanno + get_random(random2),cantidad_ramas,random=random,random2= reduce_num(random2))
            initial_angle -= angle_diference - get_random(random)
    

def tree(x1,y1,profundidad,tamanno,cantidad_ramas, ancho_tronco,random1, random2):
    """[generamos un arbo dados loa parametros, 
        lo que hacemos es llamar la funcion y aqui preparamos los parametros]

    Args:
        x1 ([int]): [posicion en x del tronco]
        y1 ([int]): [posicion en y del tronco]
        profundidad ([int]): [cantidad de subdiviciones]
        tamanno ([int]): [tamaño del arbol (largo de las ramas)]
        cantidad_ramas ([int]): [cantidad de amas]
        ancho_tronco ([int]): [hancho del tronco del arbol]
        random1 ([int]): [random en los angulos de las hojas]
        random2 ([int]): [random en el largo de las hojas]
    """
    if (cantidad_ramas-1) == 0:
        cantidad_ramas = 2
    angulo_inicio =180+(180/(cantidad_ramas-1))
    if cantidad_ramas==2:
        angulo_inicio-=90

    angulo_tronco = -90
    drawTree(x1,y1, angulo_tronco, profundidad ,angulo_inicio ,tamanno,cantidad_ramas,ancho_tronco,random1,random2)



# -------------------------------------- #



def clean_draw_canvas():
    pygame.draw.rect(screen, COLOR_4, drawing_canvas_rect, 5)
    pygame.draw.rect(screen, COLOR_1, drawing_canvas_rect)

    #dibujamos el tronco
    pygame.draw.rect(screen, COLOR_5, pygame.Rect(317, 300, 8, 60))
    
    pass

def clean_tree_canvas():
    #pygame.draw.rect(screen, COLOR_2, tree_rect)
    pygame.draw.rect(screen, COLOR_2, tree_rect)
    pygame.draw.rect(screen, COLOR_4, tree_drawing_canvas_rect, 5)
    pygame.draw.rect(screen, COLOR_1, tree_drawing_canvas_rect)

    
    pass

clean_draw_canvas()
clean_tree_canvas()
running_evolution = False
while True:
    if running_evolution == False:
    
        for event in [pygame.event.poll()]:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                draw = True
            elif event.type == MOUSEBUTTONUP:
                draw = False
                save_flag = False


        
    # dibujamos un circulo si se esta haciendo click
    mouse_pos = pygame.mouse.get_pos()
    if draw == True and drawing_canvas_rect.collidepoint(mouse_pos):
        pygame.draw.circle(screen, brush_color, mouse_pos, brush_size)
        save_flag = False





    ## Detectamos si se hizo click en el boton del borrador
    if draw == True:
        if eraser_rect.collidepoint(mouse_pos):
            brush_color = COLOR_1
    
    ## Detectamos si se hizo click en el boton del lapiz
    if draw == True:
        if draw_rect.collidepoint(mouse_pos):
            brush_color = COLOR_5
    
    ## Detectamos si se hizo click en limpiar
    if draw == True:
        if clear_rect.collidepoint(mouse_pos):
            clean_draw_canvas()

            
    
    pygame.draw.rect(screen, COLOR_3, menu_rect)
    
    pygame.draw.rect(screen, COLOR_4, clear_rect)
    screen.blit(clear_text, (30, 295))


    screen.blit(brush_text, (27, 70))
    

    pygame.draw.rect(screen, COLOR_4, save_rect)
    screen.blit(save_text, (30, 262))
    




    #detectamos si se hizo click en guardar
    if draw == True and save_flag == False:
        save_flag = True
        
        if save_rect.collidepoint(mouse_pos):
            running_evolution = True
            parametros = get_poblacion_inicial(8)
            for i in range(0,numero_generaciones_totales):
                new_parametros = get_nueva_generacion(parametros,individuos_por_generacion,1,i)
                parametros = new_parametros
                a = pygame.event.poll()
                pygame.event.clear()
            running_evolution = False
            

            
            """
            print("File has been saved :P")
            
            clean_tree_canvas()
            tree(x1=TREE_POS_X,y1=TREE_POS_Y,profundidad=5,tamanno=10,cantidad_ramas=3,ancho_tronco=8,random1=5,random2=5)

            save_surface_draw = pygame.Surface((320, 360))
            save_surface_draw.blit(screen, (0, 0), (160, 20, 320, 360))

            #guardamos el arbol
            save_surface_tree = pygame.Surface((320, 360))
            save_surface_tree.blit(screen, (0, 0), (795, 20, 320, 360))
            get_diferencia(save_surface_draw,save_surface_tree)
            save_flag = True
            """
            
        




 ## collision detectin for BRUSH SIZE
    if draw == True:
        if thin_brush.collidepoint(mouse_pos):
            brush_size = 1
        if medium_brush.collidepoint(mouse_pos):
            brush_size = 3
        if thick_brush.collidepoint(mouse_pos):
            brush_size = 5
        if supa_brush.collidepoint(mouse_pos):
            brush_size = 10
    




    
    
    

    pygame.draw.rect(screen, COLOR_1, eraser_rect)
    if brush_color == COLOR_1:
        border = 3
    else:
        border = 1
    pygame.draw.rect(screen, COLOR_4, eraser_rect, border)

    pygame.draw.rect(screen, COLOR_5, draw_rect)
    if brush_color == COLOR_5:
        border = 3
    else:
        border = 1
    
    pygame.draw.rect(screen, COLOR_2, draw_rect, border)
 
 



    # Rect for brush size

    
    if brush_size == 1:
        brush_border = 3
    else:
        brush_border = 1
    pygame.draw.rect(screen, COLOR_1, thin_brush, brush_border)
    pygame.draw.circle(screen, COLOR_1, thin_brush.center, 1)
    pygame.draw.rect(screen, COLOR_1, thin_brush, brush_border)
    
    
    if brush_size == 3:
        brush_border = 3
    else:
        brush_border = 1
    pygame.draw.rect(screen, COLOR_1, medium_brush, brush_border)
    pygame.draw.circle(screen, COLOR_1, medium_brush.center, 3)
    pygame.draw.rect(screen, COLOR_1, medium_brush, brush_border)
    
    
    if brush_size == 5:
        brush_border = 3
    else:
        brush_border = 1
    pygame.draw.rect(screen, COLOR_1, thick_brush, 1)
    pygame.draw.circle(screen, COLOR_1, thick_brush.center, 5)
    pygame.draw.rect(screen, COLOR_1, thick_brush, brush_border)
    
    
    if brush_size == 10:
        brush_border = 3
    else:
        brush_border = 1
    pygame.draw.rect(screen, COLOR_1, supa_brush, brush_border)
    pygame.draw.circle(screen, COLOR_1, supa_brush.center, 10)
    pygame.draw.rect(screen, COLOR_1, supa_brush, brush_border)


    




    pygame.display.update()



