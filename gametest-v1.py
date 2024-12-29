import pygame

# 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("캐릭터 이동 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# 캐릭터 속성
character_size = 50
character_x = WIDTH // 2
character_y = HEIGHT // 2
character_speed = 5

# 게임 루프 변수
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 받기
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        character_y -= character_speed
    if keys[pygame.K_DOWN]:
        character_y += character_speed
    if keys[pygame.K_LEFT]:
        character_x -= character_speed
    if keys[pygame.K_RIGHT]:
        character_x += character_speed

    # 화면 경계 안에 머물도록 설정
    character_x = max(0, min(WIDTH - character_size, character_x))
    character_y = max(0, min(HEIGHT - character_size, character_y))

    # 화면 그리기
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (character_x, character_y, character_size, character_size))

    # 화면 업데이트
    pygame.display.flip()

# 종료
pygame.quit()
