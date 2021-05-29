import pygame , sys ,random, time#импортируем библиотеку для написания игры


def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,750))
    screen.blit(floor_surface,(floor_x_pos + 576,750))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes 

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 750:
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,200))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score:{int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,180))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score:{int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288,350))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score

# pygame.mixer.pre_init(frequency= 44100, size = 16, channels= 1, buffer= 512)
pygame.init()
screen = pygame.display.set_mode((576,1024))#задаём размер игры
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()#создаём для частоты обновления картинки
FPS = 120
game_font = pygame.font.Font('script.ttf',40)


gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

bg_surface_night = pygame.image.load('assets/background-night.png').convert()
bg_surface_night = pygame.transform.scale2x(bg_surface_night)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 480))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)


pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,900)
pipe_height = [400,600, 700]


game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,480))



flap_sound = pygame.mixer.Sound('sound/sound_sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sound_sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sound_sfx_point.wav')
score_sound_countdown = 100

# prev_time = time.time()

while True:

    # now = time.time()
    # dt = now - prev_time
    # prev_time = now

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 480)
                bird_movement = 0
                score = 0
                

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface,bird_rect = bird_animation()
    screen.blit(bg_surface, (0,0))
    if 50 <= score <= 100:
        screen.blit(bg_surface_night, (0,0))
    else:
       screen.blit(bg_surface, (0,0))
    

    if game_active:
        #Движение птицы
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        


        #Трубы
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_display('main_game')
        # score_sound_countdown -= 1
        # if score_sound_countdown <= 0:
        #     score_sound.play()
        #     score_sound_countdown = 100

    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Пол
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0
    
    pygame.display.update()
    clock.tick(120)
    # if score < 10:
    #     clock.tick(FPS)
    # else:
    #     clock.tick(FPS)*0,5
    