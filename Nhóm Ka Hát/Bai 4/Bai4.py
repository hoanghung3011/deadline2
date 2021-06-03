import pygame
import time
import math
from tkinter import messagebox, Tk
pygame.font.init()
#-----------------------------------------------------------------------------------------------
WIDTH = 800
HEIGHT = 600
ROOT = pygame.display.set_mode((WIDTH,HEIGHT))
WHITE = (255,255,255)
BACKGROUND = (33,150,243)
EDGE = (21,21,21)
NODE = WHITE
HOVER = (69,230,112)
RED = (235,64,52)
GREEN = (66,245,111)
YELLOW = (240,252,3)
FNT = pygame.font.SysFont('Times New Roman', 14)
DELAY = 2
MAX_DISTANCE = 200
#-----------------------------------------------------------------------------------------------
ROOT.fill(BACKGROUND)
display_node = []
distance_matrix = []
actual_graph = []
found_path = []
linker = []
click_node = 0
hovering = -1
tmp_start = -1
root_node = -1
end_node = -1
clicked = False
choose_start = False
choose_end = False
deleting = False
run = True
#-----------------------------------------------------------------------------------------------
#KEYBINDING
key_start = pygame.K_s
key_end = pygame.K_e
node_connect = pygame.K_LSHIFT
node_delete = pygame.K_BACKSPACE
quit_app = pygame.K_ESCAPE
#-----------------------------------------------------------------------------------------------
#BUTTON
start_button = pygame.Rect(20,20,100,40)
reset_button = pygame.Rect(130,20,100,40)
show_button = pygame.Rect(240,20,100,40)
start_text = FNT.render("Start", True, WHITE)
stop_text = FNT.render("Reset", True, WHITE)
show_graph = FNT.render("Show", True, WHITE)
#-----------------------------------------------------------------------------------------------
#FUNCTION
def draw_screen():
    if len(linker) != 0:
        for edge in linker:
            pygame.draw.line(ROOT,EDGE,display_node[edge[0]].center,display_node[edge[1]].center,2)
    if len(display_node) != 0:
        for idx, node in enumerate(display_node):
            if idx == root_node:
                color = GREEN
            elif idx == end_node:
                color = RED
            elif found_path!= None and idx in found_path:
                color = YELLOW
            else:
                color = NODE
            pygame.draw.rect(ROOT, color, node)
            current_idx = FNT.render(str(idx), True, (0,0,0))
            ROOT.blit(current_idx, node.midleft)
            #ROOT.blit(FNT.render(str(idx), False, EDGE), node.center)
    #move(startX,startY)
    pygame.display.update()
def euclid_distance(point_a, point_b):
    return round(math.sqrt(pow((point_a[0]-point_b[0]),2)+pow((point_a[1]-point_b[1]),2)),1)
def path_find(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not start in range(len(graph)):
        return None
    shortest_path = None
    for node in graph[start]:
        if node not in path:
            new_path = path_find(graph, node, end, path)
            if new_path: 
                if not shortest_path or len(shortest_path) > len(new_path):
                    shortest_path = new_path 
    return shortest_path
#-----------------------------------------------------------------------------------------------
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.KEYDOWN:
            #print(pygame.key.name(event.key))
            if event.key == quit_app:
                run = False
            if event.key == key_start:
                choose_start = True
                print(choose_start)
            if event.key == key_end:
                choose_end = True
                print(choose_end)
        elif event.type == pygame.KEYUP:
            if event.key == key_start:
                choose_start = False
                print(choose_start)
            if event.key == key_end:
                choose_end = False
                print(choose_end)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if reset_button.collidepoint(mouse_x, mouse_y):
                    #display_edge.clear()
                    display_node.clear()
                    linker.clear()
                    actual_graph.clear()
                elif show_button.collidepoint(mouse_x, mouse_y):
                    print(f"root_node: {root_node}")
                    print(f"end_node: {end_node}")
                    print(actual_graph)
                    print(distance_matrix)
                elif start_button.collidepoint(mouse_x, mouse_y):
                    #if root_node != -1 and end_node != -1 :
                    pygame.event.set_blocked(pygame.MOUSEMOTION)
                    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                    pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
                    if root_node != -1 and end_node != -1:
#-----------------------------------------------------------------------------------------------
#Preprocess
                        found_path.clear()
                        linker.clear()
                        for node in distance_matrix:
                            node.clear()
                        for node in actual_graph:
                            node.clear()
                        for idx, node in enumerate(display_node):
                                for connection in display_node:
                                    distance_matrix[idx].append(euclid_distance(node.center, connection.center))
                        for idx in range(len(display_node)):
                            for node, distance in enumerate(distance_matrix[idx]):
                                if distance < MAX_DISTANCE and distance != 0:
                                    actual_graph[idx].append(node)
                        for idx,node in enumerate(actual_graph):
                            for connection in node:
                                linker.append((idx,connection))
                        found_path = path_find(actual_graph, root_node, end_node)                    
                        if found_path == None:
                            Tk().wm_withdraw()
                            messagebox.showwarning('Error','No valid path')
                    pygame.event.set_allowed(pygame.MOUSEMOTION)
                    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
                    pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
                elif choose_start:
                    for idx, node in enumerate(display_node):
                        if node.collidepoint(mouse_x, mouse_y):
                            root_node = idx
                elif choose_end:
                    for idx, node in enumerate(display_node):
                        if node.collidepoint(mouse_x, mouse_y):
                            end_node = idx
                else:
                    for idx, node in enumerate(display_node):
                        if node.collidepoint(mouse_x,mouse_y):
                            #print(f'node {idx} clicked')
                            click_node = idx
                            clicked = True
                            break
            elif event.button == 3:
                #print(f'{x} {y}')
                node = pygame.rect.Rect(mouse_x,mouse_y,30,30)
                display_node.append(node)
                actual_graph.append([])
                distance_matrix.append([])
        if event.type == pygame.MOUSEBUTTONUP:
        #    #print('Mouse up')
        #    if drawing:
        #        for idx, node in enumerate(display_node):
        #            if node.collidepoint(mouse_x, mouse_y) and idx != start_node:
        #               stop_node = idx
        #                actual_graph[start_node].append(idx)
        #                actual_graph[stop_node].append(start_node)
        #                linker.append((start_node, stop_node))
        #                #selected_node = -1 
        #    start_node, stop_node = (-1, -1)
            clicked = False
        if event.type == pygame.MOUSEMOTION:
            #print(clicked)
            #print(pygame.mouse.get_pos())
            if clicked:
                #x, y = pygame.mouse.get_pos()
                #display_node[click_node].x = x - display_node[click_node].width/2
                #display_node[click_node].y = y - display_node[click_node].height/2
                display_node[click_node].move_ip(event.rel)
    ROOT.fill(BACKGROUND)
    pygame.draw.rect(ROOT, RED, start_button)
    pygame.draw.rect(ROOT, RED, reset_button)
    pygame.draw.rect(ROOT, RED, show_button)
    ROOT.blit(start_text, (55, 33))
    ROOT.blit(stop_text, (165, 33))
    ROOT.blit(show_graph, (275, 33))
    draw_screen()
