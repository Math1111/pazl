import pygame
import random
import os

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROWS = 3  # количество строк в картине
COLS = 3  # количество столбцов
MARGIN = 2  # отступ между фрагментами

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Пазл')
clock = pygame.time.Clock()

# Загружаем случайную картинку из папки pictures
pictures = os.listdir('pictures')  # получаем список файлов в папке
picture = random.choice(pictures)  # выбираем случайный файл
image = pygame.image.load('pictures/' + picture)  # загружаем картинку

# Вычисляем размеры фрагментов
image_width, image_height = image.get_size()
tile_width = image_width // COLS
tile_height = image_height // ROWS

# Разбиваем картинку на фрагменты
tiles = []
for i in range(ROWS):
    for j in range(COLS):
        # Вырезаем прямоугольник из картинки по координатам
        rect = pygame.Rect(j * tile_width, i * tile_height, tile_width, tile_height)
        tile = image.subsurface(rect)
        # Добавляем фрагмент в список
        tiles.append(tile)

# Сохраняем исходное положение фрагментов
origin_tiles = tiles.copy()

# Перемешиваем фрагменты
random.shuffle(tiles)

# Переменные игры
selected = None  # выбранный фрагмент
swaps = 0  # количество перестановок


def draw_tiles():
    """Отрисовка всех фрагментов на экране"""
    for i in range(len(tiles)):
        tile = tiles[i]
        row = i // COLS
        col = i % COLS
        x = col * (tile_width + MARGIN) + MARGIN
        y = row * (tile_height + MARGIN) + MARGIN
        # Если фрагмент выбран - рисуем его с зеленой рамкой
        if i == selected:
            pygame.draw.rect(screen, (0, 255, 0),
                             (x - MARGIN, y - MARGIN,
                              tile_width + MARGIN * 2, tile_height + MARGIN * 2))
        # Рисуем фрагмент на экране
        screen.blit(tile, (x, y))


def draw_swaps():
    """Отрисовка количества перестановок"""
    font = pygame.font.SysFont('Arial', 32)
    text = font.render(f'Количество перестановок: {swaps}', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
    pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(4, 4))
    screen.blit(text, text_rect)


def game_over():
    """Функция завершения игры"""
    font = pygame.font.SysFont('Arial', 64)
    text = font.render('Ура, картинка собрана!', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(4, 4))
    screen.blit(text, text_rect)


# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обработка клика мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Проверяем, на какой фрагмент кликнули
            for i in range(len(tiles)):
                row = i // COLS
                col = i % COLS
                x = col * (tile_width + MARGIN) + MARGIN
                y = row * (tile_height + MARGIN) + MARGIN

                if x <= mouse_x <= x + tile_width and y <= mouse_y <= y + tile_height:
                    # Если уже выбран другой фрагмент - меняем их местами
                    if selected is not None and selected != i:
                        tiles[i], tiles[selected] = tiles[selected], tiles[i]
                        selected = None
                        swaps += 1
                    # Если кликнули на тот же фрагмент - сбрасываем выбор
                    elif selected == i:
                        selected = None
                    # Если не выбран ни один фрагмент - запоминаем выбор
                    else:
                        selected = i

    # Отрисовка
    screen.fill((0, 0, 0))
    draw_tiles()
    draw_swaps()

    # Проверка на завершение игры
    if tiles == origin_tiles:
        game_over()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
exit()