from time import sleep

import pygame
import random

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
pad_width = 480
pad_height = 640
fighter_width = 36
fighter_height = 38
enemy_width = 26
enemy_height = 20


# 적을 맞춘 개산 계산
def drawScore(count):
    global gamepad
    font = pygame.font.SysFont(None, 20)
    text = font.render('Enemy Kills:' + str(count), True, WHITE)
    gamepad.blit(text, (0, 0))


# 적이 화면 아래로 통과한 개수
def drawPassed(count):
    global gamepad
    font = pygame.font.SysFont(None, 20)
    text = font.render('Enemy Passed:' + str(count), True, RED)
    gamepad.blit(text, (360, 0))


def dispMessage(text):
    global gamepad
    textfont = pygame.font.Font('freesansbold.ttf', 80)
    text = textfont.render(text, True, RED)
    textpos = text.get_rect()
    textpos.center = (pad_width / 2, pad_height / 2)
    gamepad.blit(text, textpos)
    pygame.display.update()
    sleep(2)
    runGame()


# 전투기가 적과 충돌했을 때 메시지 출력
def crash():
    global gamepad
    dispMessage('Crashed!')


# 게임 오버 메시지 보이기
def gameover():
    global gamepad
    dispMessage('Game Over')


# 게임에 등장하는 객체를 드로잉
def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x, y))


# 게임 실행 메인 함수
def runGame():
    global gamepad, clock, fighter, enemy, bullet

    # 전투기 무기에 적이 맞았을 경우 True 로 설정되는 플래그
    isShot = False
    shotcount = 0
    enemypassed = 0

    bullet_xy = []

    # 전투기 초기 위치 설정
    x = pad_width * 0.45
    y = pad_height * 0.9
    x_change = 0

    # 적 초기 위치 설정
    enemy_x = random.randrange(0, pad_width - enemy_width)
    enemy_y = 0
    enemy_speed = 3

    ongame = False
    while not ongame:
        for event in pygame.event.get():
            print(1)
            if event.type == pygame.QUIT:
                print(2)
                ongame = True

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT):
                    x_change -= 5
                elif (event.key == pygame.K_RIGHT):
                    x_change += 5

                # 왼쪽 컨트롤 키를 누르면 무기 발사 무기는 한 번에 2발만 발사됨

                elif (event.key == pygame.K_LCTRL):
                    if len(bullet_xy) < 2:
                        bullet_x = x + fighter_width / 2
                        bullet_y = y - fighter_height
                        bullet_xy.append([bullet_x, bullet_y])

                        # if event.type == pygame.KEYUP:
                        #     if event.KEY == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        #         x_change = 0

        gamepad.fill(BLACK)

        # 전투기 위치 재조정
        x += x_change
        if x < 0:
            x = 0
        elif x > pad_width - fighter_width:
            x = pad_width - fighter_width

            if y < enemy_y + enemy_height:
                if (enemy_x > x and enemy_x < x + fighter_width) or (
                            enemy_x + enemy_width > x and enemy_x + enemy_width < x + fighter_width):
                    crash()
        drawObject(fighter, x, y)

        # 전투기 무기 발사 화면에 그리기
        if len(bullet_xy) != 0:
            for i, bxy in enumerate(bullet_xy):
                bxy[1] -= 10
                bullet_xy[i][1] = bxy[1]

                if bxy[1] < enemy_y:
                    if bxy[0] > enemy_x and bxy[0] < enemy_x + enemy_width:
                        bullet_xy.remove(bxy)
                        isShot = True
                        shotcount += 1

                if bxy[1] <= 0:
                    try:
                        bullet_xy.remove(bxy)
                    except:
                        pass

        if len(bullet_xy) != 0:
            for bx, by in bullet_xy:
                drawObject(bullet, bx, by)

        drawScore(shotcount)

        # 적을 아래로 움직임
        enemy_y += enemy_speed
        if enemy_y > pad_height:
            enemy_y = 0
            enemy_x = random.randrange(0, pad_width - enemy_width)
            enemypassed += 1

        if enemypassed == 3:
            gameover()

        drawPassed(enemypassed)

        if isShot:
            enemy_speed += 1
            if enemy_speed >= 10:
                enemy_speed = 10

            enemy_x = random.randrange(0, pad_width - enemy_width)
            enemy_y = 0
            isShot = False

        drawObject(enemy, enemy_x, enemy_y)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


# 게임 초기화 함수
def initGame():
    global gamepad, clock, fighter, enemy, bullet

    pygame.init()

    gamepad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption('MyGalaga')
    fighter = pygame.image.load('fighter.png')
    enemy = pygame.image.load('enemy.png')
    bullet = pygame.image.load('bullet.png')
    clock = pygame.time.Clock()


initGame()
runGame()
