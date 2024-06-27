import pygame
import time

# Класс игрока
class Player:
    def __init__(self, screen_width, screen_height):
        # Размеры
        # Игрок занимает 1/14 по ширине и 1/10 по высоте игрового экрана
        # Игровой спрайт
        self.__sprite = pygame.transform.smoothscale(
            pygame.image.load("player.png").convert_alpha(),
            (screen_width // 14, screen_height // 10)
        )
        self.__rect = self.__sprite.get_rect()
        self.__horizontal_move_flag = 0
        self.__vertical_move_flag = 0
        self.__speed = 1

        # Установка начального положения игрока
        self.__rect.x = 100
        self.__rect.y = 380

    def get_rect(self):
        return self.__rect.copy()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.__horizontal_move_flag = -1
                self.__sprite = pygame.transform.smoothscale(
                    pygame.image.load("player_a.png").convert_alpha(),
                    (600 // 14, 488 // 10)
                )
            elif event.key == pygame.K_d:
                self.__horizontal_move_flag = 1
                self.__sprite = pygame.transform.smoothscale(
                    pygame.image.load("player_d.png").convert_alpha(),
                    (600 // 14, 488 // 10)
                )
            elif event.key == pygame.K_w:
                self.__vertical_move_flag = -1
                self.__sprite = pygame.transform.smoothscale(
                    pygame.image.load("player.png").convert_alpha(),
                    (600 // 14, 488 // 10)
                )
            elif event.key == pygame.K_s:
                self.__vertical_move_flag = 1
                self.__sprite = pygame.transform.smoothscale(
                    pygame.image.load("player_s.png").convert_alpha(),
                    (600 // 14, 488 // 10)
                )
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_a, pygame.K_d]:
                self.__horizontal_move_flag = 0
            elif event.key in [pygame.K_w, pygame.K_s]:
                self.__vertical_move_flag = 0

    def update(self, screen_width, screen_height, objects):
        # Сохраняем предыдущую позицию
        prev_rect = self.__rect.copy()

        # Обновляем позицию игрока
        self.__rect.x += self.__horizontal_move_flag * self.__speed
        self.__rect.y += self.__vertical_move_flag * self.__speed

        # Проверяем коллизии и корректируем позицию
        self.resolve_collision(objects, prev_rect)

        # Проверка на телепортацию
        self.check_logic(screen_width, screen_height)

    def check_logic(self, screen_width, screen_height):
        if 364 <= self.__rect.x <= 410 and 225 <= self.__rect.y <= 271:
            self.__rect.x = 500
            self.__rect.y = 160
            time.sleep(0.1)
        elif 420 <= self.__rect.x <= 460 and 240 <= self.__rect.y <= 281:
            self.__rect.x = 371
            self.__rect.y = 88
            time.sleep(0.1)
        else:
            # Обычная проверка на выход за границы экрана
            self.__rect.x = max(0, min(self.__rect.x, screen_width - self.__rect.width))
            self.__rect.y = max(0, min(self.__rect.y, screen_height - self.__rect.height))

    def resolve_collision(self, objects, prev_rect):
        collision_names = [
            "Wall2",
            "Wall1",
            "Wall3",
            "Wall4",
            "Wall5"
        ]
        for obj in objects:
            if self.__rect.colliderect(obj.get_rect()) and obj.name in collision_names:
                self.__rect = prev_rect
                break

    def draw(self, screen):
        screen.blit(self.__sprite, self.__rect)

# Класс объектов
class Objects:
    def __init__(self, name, image_path, position):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=position)

    def get_rect(self):
        return self.rect.copy()

    def collision(self, player):
        return self.rect.colliderect(player.get_rect())

    def info(self):
        return f"{self.name}"

# Инициализация Pygame
pygame.init()
width, height = 600, 488
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('SoloProject')
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)

# Начало
begin_image = pygame.image.load('Begin.png')
begin_image = pygame.transform.scale(begin_image, (width, height))
screen.blit(begin_image, (0, 0))
pygame.display.flip()
time.sleep(10)

# Загрузка фона
background = pygame.image.load('Background.png')
background = pygame.transform.scale(background, (width, height))

# Создание игрока
player = Player(600, 488)

# Создание списка объектов
computers = [
    Objects("Это комп все ещё открыт VSCode", "Computer without background.png", (100, 16)),
    Objects("Компьютер", "Computer without background.png", (520, 16)),
    Objects("Компьютер", "Computer without background.png", (350,12)),
    Objects("Это телевизор очень важная часть отдыха", "TV.png", (460,16)),
    Objects(f"Окно,через него можно смотреть на реальный мир", "window.png", (15,13)),
    Objects(f"Окно через него видно улицу", "window.png", (250,13)),
    Objects("Растение нужно для подачи кислорода", "plant.png", (560,400)),
    Objects("Холодильник, видимо это комната отдыха", "fridge.png", (480, 380)),
    Objects("Компьютер открыты Unittest", "PC.png", (16,200)),
    Objects("Компьютер видимо тут делают графику", "PC.png", (240,200)),
    Objects("Wall1","Wall1.jpg",(200,151)),
    Objects("Wall2", "Wall2.png", (430, 13)),
    Objects("Wall3", "Wall3.png", (385,375)),
    Objects("Wall4", "Wall4.png", (380,168)),
    Objects("Wall5", "Wall5.png", (495,168)),
]
texts_shown = 0
total_texts = len(computers) - 5
end_game = False
info_text = None
info_start_time = 0
# Основной игровой цикл. Обработка событий, включая выход из игры и управление игроком.
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        player.handle_event(event)

    # Проверка логики игрока (ограничение движения по границам экрана).
    player.update(width, height, computers)
    # Проверка коллизии с объектами для отображения информации
    for computer in computers:
        if computer.collision(player) and info_text is None and computer.name not in ["Wall1", "Wall2", "Wall3", "Wall4", "Wall5"]:
            info_text = computer.info()
            info_start_time = time.time()
            texts_shown += 1

    # Рисование фона и компьютеров на экране.
    screen.blit(background, (0, 0))
    for computer in computers:
        screen.blit(computer.image, computer.rect)

    # Отображение информации о столкновении на экране в течение 2 секунд.
    if info_text is not None:
        font = pygame.font.Font(None, 36)
        text = font.render(info_text, True, (205, 0, 205))
        screen.blit(text, (width // 2 - text.get_width() // 2,460))
        if time.time() - info_start_time > 1:
            info_text = None

    # Рисование игрока на экране и обновление экрана.
    player.draw(screen)
    pygame.display.flip()

    # Проверка условия завершения игры
    if texts_shown == total_texts and not end_game:
        end_image = pygame.image.load('End.png')
        end_image = pygame.transform.scale(end_image, (width, height))
        screen.blit(end_image, (0, 0))
        pygame.display.flip()
        time.sleep(10)
        end_game = True
        pygame.quit()
        break

# Завершение работы Pygame.
pygame.quit()
