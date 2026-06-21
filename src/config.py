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
COLOR_PURPLE = (128, 0, 128)
COLOR_DARK_BLUE = (20, 20, 35)
COLOR_GOLD = (255, 215, 0)
COLOR_GOLD_GLOW = (255, 190, 30)

#настройки игрока
PLAYER_SPEED = 4.6 
PLAYER_JUMP_POWER = 12
GRAVITY = 0.8
MAX_HP = 100
MAX_MANA = 5
MANA_COST_SPELL = 1
BASE_DAMAGE = 10

#настройки света
BASE_LIGHT_DURATION = 15.0
MAGIC_LIGHT_DURATION = 5.0
BASE_LIGHT_RADIUS = 150
BASE_LIGHT_DARK_ALPHA = 245
BASE_LIGHT_NORMAL_ALPHA = 155
RED_LIGHT_RADIUS = 150
GREEN_LIGHT_RADIUS = 150

#баффы
BUFF_DAMAGE = 1.5
BUFF_DEFENSE = 0.8
ENEMY_TOUCH_DAMAGE = 10
BOSS_TOUCH_DAMAGE = 12

#настройки поведения врагов
ENEMY_PATROL_SPEED = 1.0
ENEMY_CHASE_SPEED = 3.5
ENEMY_DARK_SPEED_MULTIPLIER = 0.2
ENEMY_PATROL_RADIUS = 80
ENEMY_DETECTION_RADIUS = 220
ENEMY_DARK_DAMAGE_MULTIPLIER = 1.6
ENEMY_CRIT_CHANCE = 0.15
ENEMY_CRIT_MULTIPLIER = 2.0

FUNNY_SPELLS = [
    ("Магия цветочного поля", 2),
    ("Почисать спину в недоступном месте", 3),
    ("Магия превращающая кислый виноград в сладкий", 3),
    ("Магия заставляющая светиться лицо в темноте", 1),
    ("Магия создающая иллюзию уставших глаз", 2),
    ("Магия заставляющая чесаться язык", 2),
    ("Магия сбивающая с ног при каждом использовании", 3),
]

STORY_TEXTS = [
    "Впереди затухшие пещеры, в которые не попадает ни единого лучика света. \
В них затеряно большое количество заклинаний, но так же вас ждет много опасностей,\
если вы не уверены в своих силах - не суйте свой нос.",
    "Ты смельчак, но твоя смелость погубит тебя. С каждым шагом становится становится опаснее, \
аккуратнее не наткнись на Владыку Тьмы.",
    "Чтож путник, видимо тут и оборвется твоя жизнь. Только очень сильный маг сможет одолеть владыку. \
Никому этого еще не удавалось..."
]



