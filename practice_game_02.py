from pygame.locals import *
import pygame
from random import choice
import time
import sys
import copy

gridSize = (12, 17)  # 宽 * 高
MinHeight = 2
GameStatus = list(enumerate(["Ready", "Gaming", "GameOver"])) # 用list函数创建一个空的列表再用enumerate函数生成一个可迭代对象，然后赋值给GameStatus变量
ColorList = [(250, 0, 0), (0, 250, 0), (0, 0, 250), (250, 250, 0), (0, 250, 250), (250, 0, 250), (250, 100, 0)]
IDList = list(range(7))
'''
1.		 □□□□   □      □      □    □□     □□     □□    □□□   □□□   □□□     □□    □□      □□       
'''


# 在二维空间（平面直角坐标系）中生成方块的函数
# 一个元组表示一个坐标，一个列表包含多个元组，表示一个方块的多个坐标，合起来就是一个完整的俄罗斯方块
# 根据stuff_id的返回值来确定生成哪个俄罗斯方块
def stuff_list(stuff_id):
    if stuff_id == 0:
        ptr = [[0, 0], [0, 1], [0, 2], [0, 3]]
    elif stuff_id == 1:
        ptr = [[0, 0], [0, 1], [0, 2], [1, 0]]
    elif stuff_id == 2:
        ptr = [[0, 1], [0, 0], [0, 2], [1, 1]]
    elif stuff_id == 3:
        ptr = [[0, 2], [0, 1], [0, 0], [1, 2]]
    elif stuff_id == 4:
        ptr = [[0, 0], [0, 1], [1, 0], [1, 1]]
    elif stuff_id == 5:
        ptr = [[0, 1], [0, 0], [1, 1], [1, 2]]
    else:
        ptr = [[0, 1], [0, 2], [1, 0], [1, 1]]
    return ptr
# 这段代码定义了一个名为`stuff_list`的函数，它接受一个整数参数`stuff_id`，并根据该参数返回一个二维列表。
# 这个二维列表表示一个“东西”的排列，其中每个元素是一个二元组，表示东西在二维空间中的位置。
# 函数根据`stuff_id`的值来决定返回哪个二维列表。
# 具体来说，当`stuff_id`为0时，返回一个包含四个二元组的列表，分别表示东西位于(0, 0)、(0, 1)、(0, 2)和(0, 3)的位置；
# 当`stuff_id`为1时，返回一个包含四个二元组的列表，分别表示东西位于(0, 0)、(0, 1)、(0, 2)和(1, 0)的位置，以此类推。
# 这个函数可以用于模拟一个东西的排列，
# 例如，在一个二维网格中放置一些物品，或者在一个棋盘上放置棋子。需要注意的是，这个函数没有处理`stuff_id`不在指定范围内的情形，
# 如果需要处理这种情况，可以在函数中添加一个`else`语句来返回一个默认的二维列表。
# 这个函数的作用是根据传入的`stuff_id`参数返回一个表示“东西”排列的二维列表。这个二维列表中的每个元素都是一个二元组，表示“东西”在二维空间中的位置。
# 也就是根据‘stuff_id’的值，在二维空间内生成一个不同类型的实体

class Stuff:
    def __init__(self, stuff_id):
        self.space = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 记录已固定的方块
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.id = stuff_id
        self.ptr = []
        self.new_stuff(stuff_id)  # 调用new_stuff方法根据stuff_id创建新的方块

    def new_stuff(self, stuff_id):
        self.id = stuff_id
        if self.id == 0:
            self.ptr = [[0, 4], [0, 3], [0, 5], [0, 6]]
        elif self.id == 1:
            self.ptr = [[0, 4], [0, 3], [0, 5], [1, 3]]
        elif self.id == 2:
            self.ptr = [[0, 4], [0, 3], [0, 5], [1, 4]]
        elif self.id == 3:
            self.ptr = [[0, 4], [0, 5], [0, 3], [1, 5]]
        elif self.id == 4:
            self.ptr = [[0, 4], [0, 3], [1, 3], [1, 4]]
        elif self.id == 5:
            self.ptr = [[0, 4], [0, 3], [1, 4], [1, 5]]
        else:
            self.ptr = [[0, 4], [0, 5], [1, 3], [1, 4]]

    def crash(self):#定义一个方法crash，用于判断方块是否碰撞
        """
        return:     0: no crash
                    1: down crash
                    2: up crash
                    3: left crash
                    4: right crash
                    5: note crash
        """
        for i in range(4):
            if self.ptr[i][0] > gridSize[1] - 1:
                return 1
            elif self.ptr[i][0] < 0:
                return 2
            elif self.ptr[i][1] > gridSize[0] - 1:
                return 3
            elif self.ptr[i][1] < 0:
                return 4
            elif self.space[self.ptr[i][0]][self.ptr[i][1]] != 0:
                return 5
        return 0

    def fix_stuff(self):  # 固定
        for ptr in self.ptr:
            self.space[ptr[0]][ptr[1]] = self.id + 1 # 更新二维列表self.space中的元素ptr[0]ptr[1]是要被更新的元素
        del_list = [] # 创建一个新的列表del_list，用于存储需要删除的行
        for i in range(len(self.space)):  # 判断是否满行
            flag = True # 定义flag变量使其表示为真
            for g in self.space[i]: # self.space[i]表示遍历self.space中的每一行
                if g == 0: # 判断该行是否满了（所有元素都不为0）
                    flag = False
                    break # 如果都不为0则将flag设置为假并且跳出循环
            if flag: # 判断flag是否为真
                del_list.append(i) # 如果flag为真则将i添加到del_list中
        for i in del_list:
            del self.space[i] # 遍历列表中的每一个元素索引i，并且删除该元素self.space[i]
            self.space.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) # 将一个为0的新列表插入到space列表开头
        # return len(del_list)		此处可加一个返回，用于方便计算分数

    def down(self): # 定义down函数实现方块向下移动
        temp_ptr = copy.deepcopy(self.ptr) # 用copy.deepcopy()方法对self.ptr进行复制，将复制的对象赋值给temp_ptr
        for i in range(4): # 遍历游戏版的每一行
            self.ptr[i][0] += 1 # 将当前行的第一个元素+1 表示在当前位置放置一个棋子
        crash_result = self.crash() # 用self.crash()方法判断是否碰撞
        if crash_result != 0:  # 对碰撞结果进行判断
            self.ptr = copy.deepcopy(temp_ptr) # 如果碰撞结果为0 则表示可以放置 并将self.ptr更新为复制后的对象temp_ptr
            return False
        return True

    def up(self): # 定义up函数实现方块的向上移动
        temp_ptr = copy.deepcopy(self.ptr)
        for i in range(4):
            self.ptr[i][0] -= 1
        crash_result = self.crash()
        if crash_result != 0:
            self.ptr = copy.deepcopy(temp_ptr)
            return False
        return True

    def left(self): # 定义left函数实现方块向左移动
        temp_ptr = copy.deepcopy(self.ptr)
        for i in range(4):
            self.ptr[i][1] -= 1
        crash_result = self.crash()
        if crash_result != 0:
            self.ptr = copy.deepcopy(temp_ptr)
            return False
        return True

    def right(self): # 定义right函数实现方块向右移动
        temp_ptr = copy.deepcopy(self.ptr)
        for i in range(4):
            self.ptr[i][1] += 1
        crash_result = self.crash()
        if crash_result != 0:
            self.ptr = copy.deepcopy(temp_ptr)
            return False
        return True

    def rotate(self):  # 旋转方块
        temp_ptr = copy.deepcopy(self.ptr)
        for i in range(1, 4):
            temp_y, temp_x = temp_ptr[0][0], temp_ptr[0][1]
            i_y, i_x = temp_ptr[i][0], temp_ptr[i][1]
            self.ptr[i] = [temp_ptr[0][0] - temp_ptr[i][1] + temp_ptr[0][1],  # 逆时针旋转
                           temp_ptr[0][1] + temp_ptr[i][0] - temp_ptr[0][0]]
            # self.ptr[i][0] = temp_ptr[0][0] + temp_ptr[i][1] - temp_ptr[0][1]
        crash_result = self.crash()
        if crash_result == 0:
            return True
        elif crash_result == 1:
            if self.up():
                return True
        elif crash_result == 2:
            if self.down():
                return True
        elif crash_result == 3:
            if self.left():
                return True
        elif crash_result == 4:
            if self.right():
                return True
        self.ptr = copy.deepcopy(temp_ptr)
        return False

    def over(self):  # 游戏结束判断
        for i in range(1):
            for value in self.space[i]:
                if value != 0: # value表示当前空格子的值，如果value不为0则表示该空格子已经被占用，此时游戏结束
                    return True
        return False

"""
文本显示模块
"""
# 定义一个show_text函数，用于在屏幕上显示文本
# 参数说明：
# screen：屏幕显示对象
# pos：文本位置
# text：文本内容
# text_color：文本颜色
# font_bold：是否加粗
# font_size：字体大小
# font_italic：是否使用斜体
# font_mediate：是否居中 font_mediate为True时，文本将居中显示，否则将按照pos参数指定的位置显示

def show_text(screen, pos, text, text_color, font_bold=False, font_size=60, font_italic=False, font_mediate=True):
    # 获取系统字体，并设置文字大小
    cur_font = pygame.font.SysFont("宋体", font_size)
    # 设置是否加粗属性
    cur_font.set_bold(font_bold)
    # 设置是否斜体属性
    cur_font.set_italic(font_italic)
    # 设置文字内容
    text_fmt = cur_font.render(text, 1, text_color)
    text_pos = text_fmt.get_rect()
    text_pos.midtop = pos
    # 绘制文字
    if font_mediate:
        # 判断是否居中
        screen.blit(text_fmt, text_pos)
    else:
        screen.blit(text_fmt, pos)


def main():
    pygame.init()
    ftpsClock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Tetris")
    GAME_STATUS = 0 # 游戏状态，0表示准备，1表示游戏进行中
    next_stuff = choice(IDList)
    curr_stuff = choice(IDList)
    stuff = Stuff(curr_stuff)
    next_ptr = stuff_list(next_stuff)
    gamingTime = time.time()
    while True:
        screen.fill((150, 150, 150))
        pygame.draw.rect(screen, (50, 50, 50), (50, 50, 500, 700))
        pygame.draw.rect(screen, (100, 100, 100), (60, 60, 480, 80))
        if GAME_STATUS == 0:  # Ready
            for event in pygame.event.get():  # 事件遍历
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:  # 按键按下
                    if event.key in [K_RETURN, K_KP_ENTER]:
                        GAME_STATUS = 1
            show_text(screen, (400, 400), "Enter play", (250, 250, 0), font_size=80)
        elif GAME_STATUS == 1:  # 游戏中
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key in [K_UP, K_w, K_SPACE]:
                        stuff.rotate()
                    if event.key in [K_LEFT, K_a]:
                        stuff.left()
                    if event.key in [K_RIGHT, K_d]:
                        stuff.right()
                    if event.key in [K_DOWN, K_s]:  # 这里因为只判断了KEYDOWN，所以无论你按多久，都只会触发一次
                        stuff.down()  # 如果想实现长按快速下落这个效果可以和KEYUP事件一起食用
            if time.time() - gamingTime > 0.5:
                gamingTime = time.time()
                if not stuff.down():
                    stuff.fix_stuff()
                    curr_stuff = next_stuff
                    next_stuff = choice(IDList)
                    stuff.new_stuff(curr_stuff)
                    next_ptr = stuff_list(next_stuff)
            for pos in next_ptr:
                pygame.draw.rect(screen, ColorList[next_stuff], (601 + 50 * pos[1], 101 + 50 * pos[0], 48, 48))
            for i in range(gridSize[1]):
                for j in range(gridSize[0]):
                    ID = stuff.space[i][j]
                    if ID != 0:
                        pygame.draw.rect(screen, ColorList[ID - 1], (61 + 40 * j, 61 + 40 * i, 38, 38))
            for pos in stuff.ptr:
                pygame.draw.rect(screen, ColorList[stuff.id], (61 + 40 * pos[1], 61 + 40 * pos[0], 38, 38))
            if stuff.over():
                GAME_STATUS = 2
        elif GAME_STATUS == 2:  # Game over
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key in [K_RETURN, K_KP_ENTER]:
                        GAME_STATUS = 0
                        next_stuff = choice(IDList)
                        curr_stuff = choice(IDList)
                        stuff = Stuff(curr_stuff)
                        next_ptr = stuff_list(next_stuff)
            show_text(screen, (400, 350), "GameOver", (250, 250, 0), font_size=80)
            show_text(screen, (400, 450), "Press enter to start game", (250, 250, 0), font_size=80)
        pygame.display.flip()
        ftpsClock.tick(20)  # 每秒20帧


if __name__ == '__main__':
    main()
