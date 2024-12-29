import pygame
import random

# 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("캐릭터 이동 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# 캐릭터 클래스
class Character:
    def __init__(self, x, y, size, color, speed):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed

    def move(self, keys):
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

        # 화면 경계 안에 머물도록 설정
        self.x = max(0, min(WIDTH - self.size, self.x))
        self.y = max(0, min(HEIGHT - self.size, self.y))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

# 장애물 클래스
class Obstacle:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

# 객체 생성
character = Character(WIDTH // 2, HEIGHT // 2, 50, BLUE, 2.5)
obstacles = [
    Obstacle(random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 50), 50, RED)
    for _ in range(2)
]

# 게임 루프 변수
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 받기
    keys = pygame.key.get_pressed()
    character.move(keys)

    # 화면 그리기
    screen.fill(WHITE)
    character.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)

    # 화면 업데이트
    pygame.display.flip()

# 종료
pygame.quit()
