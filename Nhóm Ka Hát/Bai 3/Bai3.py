import pygame
import time
pygame.font.init()
#-----------------------------------------------------------------------------------------------
#SETTING
WIDTH = 800
HEIGHT = 600
WHITE = (255,255,255)
BACKGROUND = (33,150,243)
EDGE = (21,21,21)
NODE = WHITE
RED = (235,64,52)
GREEN = (66,245,111)
FNT = pygame.font.SysFont('Times New Roman', 14)
DEPTH = 3
DELAY = 2
#-----------------------------------------------------------------------------------------------
ROOT = pygame.display.set_mode((WIDTH,HEIGHT))
ROOT.fill(BACKGROUND)
display_node = []
display_edge = []
actual_graph = []
linker = []
button_map = []
click_node = 0
root_node = -1
tmp_start = -1
root_node = -1
start_node = None
stop_node = None
clicked = False
choosing = False
drawing = False
deleting = False
run = True
#-----------------------------------------------------------------------------------------------
#KEYBINDING
node_start = pygame.K_LCTRL
node_connect = pygame.K_LSHIFT
node_delete = pygame.K_BACKSPACE
quit_app = pygame.K_ESCAPE
#-----------------------------------------------------------------------------------------------
#UTILITY
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
                color = RED
            elif idx == tmp_start:
                color = GREEN
            else:
                color = NODE
            pygame.draw.rect(ROOT, color, node)
            current_idx = FNT.render(str(idx), True, (0,0,0))
            ROOT.blit(current_idx, node.midtop)
            #ROOT.blit(FNT.render(str(idx), False, EDGE), node.center)
    #move(startX,startY)
    pygame.display.update()
#-----------------------------------------------------------------------------------------------
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovering = -1
        if event.type == pygame.KEYDOWN:
            if event.key == quit_app:
                run = False
            if event.key == node_start:
                choosing = True
            if event.key == node_connect:
                drawing = True
            if event.key == node_delete:
                deleting = True
        if event.type == pygame.KEYUP:
            if event.key == node_start:
                choosing = False
            if event.key == node_connect:
                drawing = False
            if event.key == node_delete:
                deleting = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if reset_button.collidepoint(mouse_x, mouse_y):
                    display_edge.clear()
                    display_node.clear()
                    linker.clear()
                    actual_graph.clear()
                elif show_button.collidepoint(mouse_x, mouse_y):
                    print(actual_graph)
                elif start_button.collidepoint(mouse_x, mouse_y):
                    if root_node != -1:
                        pygame.event.set_blocked(pygame.MOUSEMOTION)
                        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                        pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
                        node_depth = [-1]*len(display_node)
                        node_depth[root_node] = 0
                        extended_list = [False]*len(display_node)
                        tmp_queue = []
                        tmp_queue.append(root_node)
                        tmp_start = root_node
                        extended_list[tmp_start] = True
                        while tmp_queue:
                            tmp_start = tmp_queue.pop(0)
                            for node in actual_graph[tmp_start]:
                                if extended_list[node] == False and (node_depth[tmp_start]+1 <= DEPTH):
                                    extended_list[node] = True
                                    node_depth[node] = node_depth[tmp_start] + 1
                                    tmp_queue.append(node)
                            draw_screen()
                            time.sleep(DELAY)
                        tmp_queue.clear()
                        tmp_start = -1
                        pygame.event.set_allowed(pygame.MOUSEMOTION)
                        pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
                        pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
                elif choosing == True:
                    for idx, node in enumerate(display_node):
                        if node.collidepoint(mouse_x, mouse_y):
                            root_node = idx
                elif drawing == True:
                    for idx, node in enumerate(display_node):
                        x, y = pygame.mouse.get_pos()
                        if node.collidepoint(mouse_x, mouse_y):
                            start_node = idx
                            #selected_node = idx
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
        if event.type == pygame.MOUSEBUTTONUP:
            #print('Mouse up')
            if drawing:
                for idx, node in enumerate(display_node):
                    if node.collidepoint(mouse_x, mouse_y) and idx != start_node:
                        stop_node = idx
                        actual_graph[start_node].append(idx)
                        actual_graph[stop_node].append(start_node)
                        linker.append((start_node, stop_node))
                        #selected_node = -1 
            start_node, stop_node = (-1, -1)
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

