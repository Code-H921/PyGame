import random
import pygame

# 初始化pygame
pygame.init()

# 设置窗口大小
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('贪吃蛇')

# 游戏屏幕字体
SCORE_FONT = pygame.font.Font('./fonts/simsun.ttf', 25)
RESULT_FONT = pygame.font.Font('./fonts/simsun.ttf', 25)

# 颜色设置
BLACK = (0, 0, 0)  # 黑色（屏幕颜色）
WHITE = (255, 255, 255)  # 白色（得分颜色）
GREEN = (0, 255, 0)  # 绿色（蛇的颜色）
RED = (255, 0, 0)  # 红色（食物的颜色，游戏结果颜色）

# 蛇区块大小（正方形）和游动速度
SNAKE_BLOCK = 10
SNAKE_SPEED = 8


def draw_score(score):
    """绘制当前分数"""
    score_text = SCORE_FONT.render("总分数：" + str(score), True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 20))
    SCREEN.blit(score_text, score_rect)


def draw_snake(snake_list):
    """绘制蛇的身体"""
    for x in snake_list:
        pygame.draw.rect(SCREEN, GREEN, [x[0], x[1], SNAKE_BLOCK, SNAKE_BLOCK])


def food_position():
    """随机计算食物坐标"""
    x_food = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK, SNAKE_BLOCK))
    y_food = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK, SNAKE_BLOCK))
    return x_food, y_food


def draw_result(snake_length):
    """绘制游戏结果"""
    # 在屏幕中央显示文本
    game_over_text = RESULT_FONT.render('游戏结束', True, RED)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    SCREEN.blit(game_over_text, game_over_rect)

    # 显示最终得分文本
    final_score_text = RESULT_FONT.render(f'总得分: {snake_length - 1}', True, RED)
    final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    SCREEN.blit(final_score_text, final_score_rect)

    # 显示重新开始游戏的提示文本
    restart_text = RESULT_FONT.render('按`Q`退出游戏，按`C`重新开始游戏', True, RED)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    SCREEN.blit(restart_text, restart_rect)


def game_loop():
    """游戏主循环函数"""
    game_over = False  # 退出游戏
    game_close = False  # 单次游戏结束

    # 初始化蛇的坐标和坐标增量
    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2
    x1_change = 0
    y1_change = 0

    # 蛇的身体列表，初始长度为1
    snake_list = []
    snake_length = 1

    # 随机生成食物的位置
    x_food, y_food = food_position()

    while not game_over:
        # 如果游戏结束但未选择退出或重玩，则进入此循环
        while game_close:
            # 清空屏幕，准备下一轮绘制
            SCREEN.fill(BLACK)
            draw_result(snake_length)
            pygame.display.update()  # 刷新屏幕

            # 等待按键
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True  # 退出游戏
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()  # 重新开始游戏

        # 处理键盘事件，改变蛇的移动方向
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True  # 退出游戏
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # 左：X坐标减少1个区块，Y坐标不变
                    x1_change = -1
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    # 右：X坐标增加1个区块，Y坐标不变
                    x1_change = 1
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    # 上：X坐标不变，Y坐标减少1个区块
                    x1_change = 0
                    y1_change = -1
                elif event.key == pygame.K_DOWN:
                    # 下：X坐标不变，Y坐标增加1个区块
                    x1_change = 0
                    y1_change = 1

        # 退出游戏
        if game_over:
            break

        # 检测蛇是否触墙
        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True

        # 更新蛇的位置
        x1 += x1_change * SNAKE_BLOCK
        y1 += y1_change * SNAKE_BLOCK

        # 清空屏幕，准备下一轮绘制
        SCREEN.fill(BLACK)

        # 画食物
        pygame.draw.rect(SCREEN, RED, [x_food, y_food, SNAKE_BLOCK, SNAKE_BLOCK])

        # 新的蛇头位置，同时删除最后蛇尾区块，以保持蛇的总长度不变
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]  # 删除蛇尾

        # 检查蛇头是否碰到蛇的身体
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        # 绘制蛇
        draw_snake(snake_list)

        # 绘制得分
        draw_score(snake_length - 1)

        # 刷新屏幕
        pygame.display.update()

        # 检查蛇头是否碰到食物，若碰到则增加长度并重新生成食物
        if x1 == x_food and y1 == y_food:
            x_food, y_food = food_position()
            snake_length += 1

        # 控制游戏帧率
        clock = pygame.time.Clock()
        clock.tick(SNAKE_SPEED)

    # 游戏结束时清理pygame环境
    # pygame.quit()
    # quit()


# 开始游戏
if __name__ == '__main__':
    game_loop()
