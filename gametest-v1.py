import pygame
import random
import time

# 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("캐릭터 이동 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# 캐릭터 클래스
class Character:
    def __init__(self, x, y, size, color, speed):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed
        self.health = 100
        self.last_direction = "UP"  # 초기 정면 방향
        self.skill1_active = False
        self.skill1_end_time = 0
        self.laser_active = False
        self.laser_rect = None
        self.laser_end_time = 0

    def move(self, keys):
        if keys[pygame.K_w]:
            self.y -= self.speed
            self.last_direction = "UP"
        if keys[pygame.K_s]:
            self.y += self.speed
            self.last_direction = "DOWN"
        if keys[pygame.K_a]:
            self.x -= self.speed
            self.last_direction = "LEFT"
        if keys[pygame.K_d]:
            self.x += self.speed
            self.last_direction = "RIGHT"

        # 화면 경계 안에 머물도록 설정
        self.x = max(0, min(WIDTH - self.size, self.x))
        self.y = max(0, min(HEIGHT - self.size, self.y))

    def activate_skill1(self):
        self.skill1_active = True
        self.color = GRAY
        self.skill1_end_time = time.time() + 1  # 1초 지속

    def activate_laser(self):
        self.laser_active = True
        self.laser_end_time = time.time() + 1  # 1초 지속
        if self.last_direction == "UP":
            self.laser_rect = pygame.Rect(self.x + self.size // 2 - 5, 0, 10, self.y)
        elif self.last_direction == "DOWN":
            self.laser_rect = pygame.Rect(self.x + self.size // 2 - 5, self.y + self.size, 10, HEIGHT - self.y - self.size)
        elif self.last_direction == "LEFT":
            self.laser_rect = pygame.Rect(0, self.y + self.size // 2 - 5, self.x, 10)
        elif self.last_direction == "RIGHT":
            self.laser_rect = pygame.Rect(self.x + self.size, self.y + self.size // 2 - 5, WIDTH - self.x - self.size, 10)

    def update(self):
        if self.skill1_active and time.time() > self.skill1_end_time:
            self.skill1_active = False
            self.color = BLUE

        if self.laser_active and time.time() > self.laser_end_time:
            self.laser_active = False
            self.laser_rect = None

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        if self.laser_active and self.laser_rect:
            pygame.draw.rect(screen, YELLOW, self.laser_rect)

# 장애물 클래스
class Obstacle:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.health = 50

    def check_collision(self, character):
        character_rect = pygame.Rect(character.x, character.y, character.size, character.size)
        obstacle_rect = pygame.Rect(self.x, self.y, self.size, self.size)

        # 캐릭터와 장애물의 충돌 처리
        if character_rect.colliderect(obstacle_rect):
            if not character.skill1_active:
                character.health -= 40

        # 레이저와 장애물의 충돌 처리
        if character.laser_active and character.laser_rect and character.laser_rect.colliderect(obstacle_rect):
            self.health -= 10

    def draw(self, screen):
        if self.health > 0:
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # 스킬1 활성화
                character.activate_skill1()
            if event.key == pygame.K_e:  # 스킬2 활성화
                character.activate_laser()

    # 키 입력 받기
    keys = pygame.key.get_pressed()
    character.move(keys)
    character.update()

    # 장애물 충돌 체크
    for obstacle in obstacles:
        obstacle.check_collision(character)

    # 화면 그리기
    screen.fill(WHITE)
    character.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)

    # 화면 업데이트
    pygame.display.flip()

# 종료
pygame.quit()
