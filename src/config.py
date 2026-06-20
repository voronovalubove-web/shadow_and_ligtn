#экран фпс
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
LEVEL_SIZE = 40

#цвета
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_AMBER = (250, 155, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 115, 0)
COLOR_BLUE = (86, 86, 252)
COLOR_GRAY = (50, 50, 50)
COLOR_YELLOW = (220, 190, 40)

#настройки игрока
PLAYER_SPEED = 4 
PLAYER_JUMP_POWER = 12
GRAVITY = 0.8
STARS_X_THRESHOLD = 0
MAX_HP = 100
MAX_MANA = 5
MANA_COST_SPELL = 1
BASE_DAMAGE = 10

#настройки света
BASE_LIGHT_DURATION = 30.0
MAGIC_LIGHT_DURATION = 5.0
BASE_LIGHT_RADIUS = 150
BASE_LIGHT_DARK_ALPHA = 245
BASE_LIGHT_NORMAL_ALPHA = 155
RED_LIGHT_RADIUS = 150
GREEN_LIGHT_RADIUS = 150
TWILGHT_OVAL_WIND = 120 
TWILGHT_OVAL_HIGHT = 60 

#баффы
BUFF_DAMAGE = 1.1
BUFF_DEFENSE = 0.85
ENEMY_TOUCH_DAMAGE = 5

FUNNY_SPELLS = [
    ("Погладить мантию", 4),
    ("Почистить сапоги", 3),
    ("Наладить шляпу", 5),
    ("Приготовить чай", 3),
    ("Расчесать бороду", 4),
    ("Протереть очки", 2),
    ("Поправить воротник", 2)
]

STORY_TEXTS = [
    "Странник коснулся тёплого костра. Дальше — только осторожнее.",
    "База активирована. Пещера запоминает ваш путь.",
    "Свет костра согревает душу странника.",
    "Вы чувствуете прилив сил в этом безопасном месте.",
    "Еще одна точка сохранения активирована."
]
