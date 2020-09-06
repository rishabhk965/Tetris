import pygame
import random
pygame.font.init()
WIDTH=900
HEIGHT=700
game_width=450
game_height=600
block_size=30

top_left_x=(WIDTH - game_width) // 2
top_left_y=HEIGHT - game_height

S=[['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z=[['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I=[['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O=[['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J=[['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L=[['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T=[['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes=[S, Z, I, O, J, L, T]
colors=[(204,0,0),(0,0,153),(102,204,0),(255,255,0),(255,0,127),(153,0,153),(255,128,0)]

class Piece(object):
    rows=20
    columns=15
    def __init__(self, column, row, shape):
        self.x=column
        self.y=row
        self.shape=shape
        self.color=colors[shapes.index(shape)]
        self.rotation=0


def create_BOX(locked_positions={}):
    BOX=[[(0,0,0) for x in range(15)] for x in range(20)]
    for i in range(len(BOX)):
        for j in range(len(BOX[i])):
            if (j,i) in locked_positions:
                c=locked_positions[(j,i)]
                BOX[i][j]=c
    return BOX

def convert_shape_format(shape):
    positions=[]
    format=shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row=list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions):
        positions[i]=(pos[0] - 2, pos[1] - 4)
    return positions

def valid_space(shape, BOX):
    accepted_positions=[[(j, i) for j in range(15) if BOX[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions=[j for sub in accepted_positions for j in sub]
    formatted=convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x,y=pos
        if y < 1:
            return True
    return False

def get_shape():
    global shapes, colors
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(surface,text, size, color):
    font=pygame.font.SysFont('arial', size, bold=True)
    label=font.render(text, 1, color)
    surface.blit(label, (top_left_x + game_width/2 - (label.get_width() / 2), top_left_y + game_height/2 - label.get_height()/2))

def draw_BOX(surface, row, col):
    sx=top_left_x
    sy=top_left_y
    for i in range(row):
        pygame.draw.line(surface, (255,255,255), (sx, sy+ i*30), (sx + game_width, sy + i * 30))
        for j in range(col):
            pygame.draw.line(surface, (255,255,255), (sx + j * 30, sy), (sx + j * 30, sy + game_height))

def clear_rows(BOX, locked):
    inc=0
    for i in range(len(BOX)-1,-1,-1):
        row=BOX[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind=i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y=key
            if y < ind:
                newKey=(x, y + inc)
                locked[newKey]=locked.pop(key)
    return inc

def draw_next_shape(shape, surface,score):
    font=pygame.font.SysFont('arial', 20)
    label=font.render('Next Shape', 1, (255,255,255))
    sx=top_left_x + game_width + 45
    sy=top_left_y + game_height/2 - 90
    format=shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row=list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)
    surface.blit(label, (sx + 15, sy- 30))

def draw_window(surface,BOX,score=0):
    surface.fill((0,0,0))
    font=pygame.font.SysFont('arial', 60)
    labelT=font.render('T', 1, (204,0,0))
    labelE=font.render('E', 1, (102,204,0))
    labelR=font.render('R', 1, (255,0,127))
    labelI=font.render('I', 1, (0,0,153))
    labelS=font.render('S', 1, (255,255,0))
    surface.blit(labelT, (top_left_x - 80 + game_width / 2 - (labelT.get_width() / 2), 30))
    surface.blit(labelE, (top_left_x - 40 + game_width / 2 - (labelE.get_width() / 2), 30))
    surface.blit(labelT, (top_left_x - 0 + game_width / 2 - (labelT.get_width() / 2), 30))
    surface.blit(labelR, (top_left_x + 40 + game_width / 2 - (labelR.get_width() / 2), 30))
    surface.blit(labelI, (top_left_x + 80 + game_width / 2 - (labelI.get_width() / 2), 30))
    surface.blit(labelS, (top_left_x + 120 + game_width / 2 - (labelS.get_width() / 2), 30))
    font=pygame.font.SysFont('arial', 20)
    label=font.render('Your Score: '+str(score), 1, (255,255,255))
    sx=top_left_x + game_width + 45
    sy=top_left_y  + game_height/2 - 200
    surface.blit(label, (sx + 15, sy- 30))
    for i in range(len(BOX)):
        for j in range(len(BOX[i])):
            pygame.draw.rect(surface, BOX[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)
    draw_BOX(surface, 20, 15)
    pygame.draw.rect(surface, (255, 255, 255), (top_left_x, top_left_y, game_width, game_height), 5)

def main(win):
    global BOX
    locked_positions={}
    BOX=create_BOX(locked_positions)

    change_piece=False
    run=True
    current_piece=get_shape()
    next_piece=get_shape()
    clock=pygame.time.Clock()
    fall_time=0
    fall_speed=0.27
    level_time=0
    score=0
    while run:
        BOX=create_BOX(locked_positions)
        fall_time += clock.get_rawtime()
        level_time+=clock.get_rawtime()
        clock.tick()
        if level_time/1000>5:
            level_time=0
            if level_time>0.12:
                level_time-=0,005
        if fall_time/1000 >= fall_speed:
            fall_time=0
            current_piece.y += 1
            if not (valid_space(current_piece, BOX)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece=True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, BOX):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, BOX):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation=current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, BOX):
                        current_piece.rotation=current_piece.rotation - 1 % len(current_piece.shape)
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, BOX):
                        current_piece.y -= 1
        shape_pos=convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x, y=shape_pos[i]
            if y > -1:
                BOX[y][x]=current_piece.color
        if change_piece:
            for pos in shape_pos:
                p=(pos[0], pos[1])
                locked_positions[p]=current_piece.color
            current_piece=next_piece
            next_piece=get_shape()
            change_piece=False
            score+=clear_rows(BOX, locked_positions)*10
        draw_window(win,BOX,score)
        draw_next_shape(next_piece, win,score)
        pygame.display.update()
        if check_lost(locked_positions):
            draw_text_middle(win,"Game Over! Score: "+str(score), 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(3500)
            run=False
            
def main_menu(win):
    run=True
    while run:
        win.fill((0,0,0))
        draw_text_middle(win,'Press any key to begin.', 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type == pygame.KEYDOWN:
                main(win)
    pygame.quit()

win=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tetris')

main_menu(win)
