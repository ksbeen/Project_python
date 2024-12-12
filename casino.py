import pygame
import random
import sys
import platform
import time


# Pygame 초기화
pygame.init()

# 화면 설정
screen_width, screen_height = 1000, 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (255,215,0)
GREEN = (0, 255, 0)
DARK_BLUE = (0, 0, 139) 


# 글꼴 설정
if platform.system() == "Windows":
    font_name = "Arial"  # 윈도우 기본 폰트
else:
    font_name = "Apple SD Gothic Neo"  # 맥 기본 폰트

font = pygame.font.SysFont(font_name, 36, bold=True)

# 카드 이미지 경로
CARD_FOLDER = "card"

money= 1000

target = 1200

# 색상 정의
black = (0, 0, 0)

# 플레이어 이미지 로드
player_image = pygame.image.load("player1-1.png")
player_rect = player_image.get_rect()
# 플레이어 이미지 로드 및 초기 설정
player_images = {
    'stand':pygame.image.load("player1-1.png"),
    'walk_right':pygame.image.load("player1-2.png"),
    'walk_left':pygame.image.load("player1-3.png")
    }
# 플레이어 애니메이션 상태
current_player_state = 'stand'

# 플레이어 애니메이션 프레임 인덱스
player_frame_index = 0
player_animation_frames = 4  # 각 애니메이션 상태에 대한 프레임 수

# 플레이어 애니메이션 상태 업데이트 함수에 변수 추가
last_frame_change_time = time.time()
# 플레이어 애니메이션 상태 업데이트 함수
def update_player_animation(keys):
    global player_frame_index, current_player_state, frame_change_delay, last_frame_change_time

    # 각 프레임 변경 간격을 정의합니다 (단위: 초)
    frame_change_delay = 0.2

    # 현재 시간을 가져옵니다
    current_time = time.time()

    # 프레임 변경 간격 이내에는 애니메이션을 변경하지 않습니다
    if current_time - last_frame_change_time < frame_change_delay:
        return
    if keys[pygame.K_LEFT]:
        current_player_state = 'walk_left' 
    elif keys[pygame.K_RIGHT]:
        current_player_state = 'walk_right' 
    else:
        current_player_state = 'stand'

    player_frame_index = (player_frame_index + 1) % player_animation_frames



    # 프레임 변경 시간을 갱신합니다
    last_frame_change_time = current_time
# 이미지 크기 조정
player_image = pygame.transform.scale(player_image, (player_image.get_width() // 10, player_image.get_height() // 10))
player_rect = player_image.get_rect()
player_rect.center = (825, 1350)

# 플레이어 이동 속도
player_speed = 1

# NPC 클래스 정의
class NPC:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        # 이미지 크기 조정
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

# NPC 인스턴스 생성
roulette_npc = NPC("slot.png", 1085, 1020)
roulette_npc1 = NPC("slot.png", 1185, 1020)
roulette_npc2 = NPC("slot.png", 1135, 1020)
blackjack_npc = NPC("blackjack_dealer1.png", 825, 1165)
dice_npc = NPC("dice_game.png", 1450, 1160) # 이미지는 <a href="https://www.flaticon.com/kr/free-icons/" title="주사위 아이콘">주사위 아이콘 제작자: Hilmy Abiyyu A. - Flaticon에서 가져왔습니다.
arena_npc = NPC("arena_icon.png", 200, 1120)
arena_npc.image = pygame.transform.scale(
    arena_npc.image, 
    (arena_npc.image.get_width() // 4, arena_npc.image.get_height() // 4)  # 크기 줄임
)


def play_blackjack():
    global money  # 전역 변수로 돈 관리
    bet_amount = 100  # 기본 배팅 금액
    # 게임 시작 시 기존 음악 중지 후 블랙잭 음악 재생
    pygame.mixer.music.stop()
    pygame.mixer.music.load('blackjack_music.mp3')#Music by <a href="https://pixabay.com/ko/users/sunsides-36828350/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=210447">Mykhailo Kyryliuk</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=210447">Pixabay</a>
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
    def reset_game():
        nonlocal deck, player_hand, dealer_hand, message, reveal_dealer_cards
        # 덱 초기화 및 섞기
        deck = [f"{value}{suit}" for suit in suits for value in values]
        random.shuffle(deck)
        # 손패 초기화
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]
        # 게임 상태 초기화
        message = ""
        reveal_dealer_cards = False

    # 카드 덱 생성 및 섞기
    suits = ['H', 'D', 'C', 'S']
    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    deck = [f"{value}{suit}" for suit in suits for value in values]
    random.shuffle(deck)
    background_image = pygame.image.load('blackjack_background.png')
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    
    # 게임 상태 초기화
    player_hand = []
    dealer_hand = []
    message = ""
    reveal_dealer_cards = False
    
    # 게임 초기화
    reset_game()
    # 점수 계산 함수
    def calculate_score(hand):
        score = 0
        ace_count = 0

        for card in hand:
            value = card[:-1] 
            if value in ['J', 'Q', 'K']:
                score += 10
            elif value == 'A':
                ace_count += 1
                score += 11
            else:
                score += int(value)

        # A의 값 조정 
        while score > 21 and ace_count:
            score -= 10
            ace_count -= 1

        return score


    def determine_winner():
        nonlocal message
        global money
        player_score = calculate_score(player_hand)
        dealer_score = calculate_score(dealer_hand)

        if player_score > 21:
            money -= bet_amount
            return f"플레이어 Bust! 딜러 Wins! (-${bet_amount}) 남은 금액: ${money}"
        elif dealer_score > 21:
            money += bet_amount
            return f"딜러 Bust! 플레이어 Wins! (+${bet_amount}) 남은 금액: ${money}"
        elif player_score > dealer_score:
            money += bet_amount
            return f"플레이어 Wins! (+${bet_amount}) 남은 금액: ${money}"
        elif player_score < dealer_score:
            money -= bet_amount
            return f"딜러 Wins! (-${bet_amount}) 남은 금액: ${money}"
        else:
            return f"무승부! 남은 금액: ${money}"

    def draw_blackjack(message, reveal_dealer=False):
        screen.blit(background_image, (0, 0))
        
        # 배팅 금액과 현재 잔액 표시
        bet_text = font.render(f"배팅 금액: ${bet_amount}", True, WHITE)
        money_text = font.render(f"현재 잔액: ${money}", True, WHITE)
        screen.blit(bet_text, (screen_width - 250, 650))
        screen.blit(money_text, (screen_width - 320, 10))

        player_text = font.render("플레이어의 손패:", True, WHITE)
        dealer_text = font.render("딜러의 손패:", True, WHITE)
        screen.blit(player_text, (50, screen_height - 180))
        screen.blit(dealer_text, (50, 50))

        for i, card in enumerate(player_hand):
            card_image = pygame.image.load(f"{CARD_FOLDER}/{card}.png")
            card_image = pygame.transform.scale(card_image, (100, 150))
            screen.blit(card_image, (50 + i * 120, screen_height - 130))

        for i, card in enumerate(dealer_hand):
            if i == 0 and not reveal_dealer:
                card_image = pygame.image.load(f"{CARD_FOLDER}/card-back.png")
            else:
                card_image = pygame.image.load(f"{CARD_FOLDER}/{card}.png")
            card_image = pygame.transform.scale(card_image, (100, 150))
            screen.blit(card_image, (50 + i * 120, 100))

        message_text = font.render(message, True, WHITE)
        screen.blit(message_text, (screen_width // 2 - message_text.get_width() // 2, screen_height // 2))

        if reveal_dealer_cards:
            continue_text = font.render("스페이스바를 눌러 다시 시작", True, WHITE)
            screen.blit(continue_text, (screen_width // 2 - continue_text.get_width() // 2, screen_height // 2 + 40))

    running_blackjack = True
    while running_blackjack and money >= bet_amount:
        if money >= target: 
            game_ending_text = font.render("돈을 다 모았습니다!!!", True, WHITE)
            screen.blit(game_ending_text, (screen_width // 2 - game_ending_text.get_width() // 2, screen_height // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            happy_ending()
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_blackjack = False
                    if not running_blackjack:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('main_menu_music.mp3')
                        pygame.mixer.music.play(-1)
                elif event.key == pygame.K_SPACE:
                    if reveal_dealer_cards:
                        reset_game()
                    else:
                        message = determine_winner()
                        reveal_dealer_cards = True
                elif event.key == pygame.K_h and not reveal_dealer_cards:
                    player_hand.append(deck.pop())
                    if calculate_score(player_hand) > 21:
                        message = determine_winner()
                        reveal_dealer_cards = True
                elif event.key == pygame.K_s and not reveal_dealer_cards:
                    while calculate_score(dealer_hand) < 17:
                        dealer_hand.append(deck.pop())
                    message = determine_winner()
                    reveal_dealer_cards = True

        draw_blackjack(message, reveal_dealer=reveal_dealer_cards)
        pygame.display.flip()



    if money < bet_amount: 
        game_over_text = font.render("게임 오버! 잔액이 부족합니다.", True, WHITE)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        sad_ending()
        return

def play_slot_machine():
    global money  # 전역 변수로 돈 관리
    bet_amount = 100  # 기본 배팅 금액

    image_filenames = ['lemon.png', 'seven.png', 'apple.png', 'cherry.png']
    jackpot_image = pygame.image.load('jackpot.png')
    background_image = pygame.image.load('slot_background.png')
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    reel_positions = [screen_width // 4, screen_width // 2, screen_width // 4 * 3]
    reel_y = screen_height // 2 - 100
    images = [pygame.transform.scale(pygame.image.load(img), (100, 100)) for img in image_filenames]

    reels_spinning = [False, False, False]
    current_images = [None, None, None]
    spin_sequence = [None, None, None]
    jackpot_triggered = False

    pygame.mixer.music.stop()
    pygame.mixer.music.load('casino_music.mp3')#Music by <a href="https://pixabay.com/ko/users/mfcc-28627740/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=120443">Mykola Sosin</a> from <a href="https://pixabay.com/music//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=120443">Pixabay</a>
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    def spin_reels():
        nonlocal spin_sequence
        spin_sequence = [random.choice(images) for _ in range(3)]

    def check_jackpot():
        return spin_sequence[0] == spin_sequence[1] == spin_sequence[2]

    def draw_slot_machine():
        screen.blit(background_image, (0, 0))

        # 배팅 금액과 현재 잔액 표시
        bet_text = font.render(f"배팅 금액: ${bet_amount}", True, WHITE)
        money_text = font.render(f"현재 잔액: ${money}", True, WHITE)
        screen.blit(bet_text, (screen_width - 250, 30))
        screen.blit(money_text, (screen_width - 250, 70))

        # 슬롯머신 제목 및 안내
        title_text = font.render("슬롯머신", True, WHITE)
        instruction_text = font.render("스페이스를 누르세요", True, WHITE)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4))
        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, screen_height // 4 + 50))

        # 릴 그리기
        for i in range(3):
            if current_images[i] is not None:
                screen.blit(current_images[i], (reel_positions[i] - images[0].get_width() // 2, reel_y))

        # 잭팟 발생 시 잭팟 이미지 표시
        if jackpot_triggered:
            jackpot_text = font.render("잭팟!!!", True, RED)
            screen.blit(jackpot_text, (screen_width // 2 - jackpot_text.get_width() // 2, screen_height // 2))
            screen.blit(jackpot_image, (screen_width // 2 - jackpot_image.get_width() // 2, screen_height // 3))

    running_slots = True
    reel_index_to_stop = 0

    while running_slots and money >= bet_amount:
        if money >= target:
            game_ending_text = font.render("돈을 다 모았습니다!!!", True, WHITE)
            screen.blit(game_ending_text, (screen_width // 2 - game_ending_text.get_width() // 2, screen_height // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            happy_ending()
            return
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not running_slots:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('main_menu_music.mp3')
                        pygame.mixer.music.play(-1)
                    running_slots = False
                    

                elif event.key == pygame.K_SPACE:
                    if not any(reels_spinning):  # 모든 릴이 멈춰있으면 스핀 시작
                        reels_spinning = [True, True, True]
                        spin_reels()

                        if money >= bet_amount:
                            money -= bet_amount  # 배팅 금액 차감
                        else:
                            message_text = font.render("잔액이 부족합니다!", True, RED)
                            screen.blit(message_text, (screen_width // 2 - message_text.get_width() // 2, screen_height // 2))
                            pygame.display.flip()
                            pygame.time.wait(2000)
                            running_slots = False

                    else:  # 릴을 하나씩 멈춤
                        if reel_index_to_stop < len(reels_spinning):
                            reels_spinning[reel_index_to_stop] = False
                            current_images[reel_index_to_stop] = spin_sequence[reel_index_to_stop]
                            reel_index_to_stop += 1

                        if all(not spinning for spinning in reels_spinning):  # 모든 릴이 멈추면 잭팟 확인
                            jackpot_triggered = check_jackpot()
                            if jackpot_triggered:
                                money += bet_amount * 100  # 잭팟: 배팅 금액의 10배

                            reel_index_to_stop = 0

        # 릴이 회전 중일 때 랜덤 이미지 표시
        for i in range(3):
            if reels_spinning[i]:
                current_images[i] = random.choice(images)

        draw_slot_machine()
        pygame.display.flip()

    if money < bet_amount:
        game_over_text = font.render("게임 오버! 잔액이 부족합니다.", True, WHITE)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        sad_ending()
        return
    
def play_odd_even(): 
    global money
    bet_amount = 100
    num_dice = 2  # 사용할 주사위 개수
    player_choice = None  # 플레이어의 홀/짝 선택
    final_dice_results = []  # 최종 결과 저장

    background_image = pygame.image.load('dice_inside.png')  # 배경 이미지 로드
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # 화면 크기에 맞게 조정
    # 소리 로드
    pygame.mixer.init()
    dice_roll_sound = pygame.mixer.Sound("dice_roll.mp3")  # 주사위 굴릴 때 나는 소리(출처:픽사베이)
    pygame.mixer.music.stop()
    pygame.mixer.music.load('background_music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    # 배경음악 재생
    pygame.mixer.music.set_volume(0.5)  # 배경음악 볼륨 (0.0 ~ 1.0)
    pygame.mixer.music.play(-1)  # 무한 반복 재생

    def draw_dice_face(x, y, number):
        pygame.draw.rect(screen, WHITE, (x, y, 100, 100), border_radius=10)
        dot_positions = [
            [(50, 50)],  # 1
            [(25, 25), (75, 75)],  # 2
            [(25, 25), (50, 50), (75, 75)],  # 3
            [(25, 25), (25, 75), (75, 25), (75, 75)],  # 4
            [(25, 25), (25, 75), (50, 50), (75, 25), (75, 75)],  # 5
            [(25, 25), (25, 50), (25, 75), (75, 25), (75, 50), (75, 75)],  # 6
        ]
        for dot in dot_positions[number - 1]:
            pygame.draw.circle(screen, BLACK, (x + dot[0], y + dot[1]), 10)

    def roll_dice_animation(num_dice):
        dice_results = []
        for _ in range(num_dice):
            dice_results.append(random.randint(1, 6))  # 최종 결과

        dice_width = 100
        total_dice_width = num_dice * dice_width + (num_dice - 1) * 50  # 주사위 간격 50px
        start_x = (screen_width - total_dice_width) // 2  # 중앙 시작 X 좌표
        y = (screen_height - dice_width) // 2  # 중앙 Y 좌표

        for _ in range(10):  # 애니메이션 효과
            # 주사위 굴림 소리 재생
            dice_roll_sound.play()


            for i in range(num_dice):
                random_face = random.randint(1, 6)  # 임시로 랜덤 눈 표시
                draw_dice_face(start_x + i * (dice_width + 50), y, random_face)
            pygame.display.flip()
            pygame.time.wait(100)  # 짧은 딜레이로 효과 추가

        return dice_results

    def calculate_dice_results(dice_results):
        total = sum(dice_results)
        if total % 2 == 0:
            return "짝수", total
        else:
            return "홀수", total

    running_game = True
    message = "홀짝을 선택하세요: 홀(Odd) / 짝(Even)"
    result_message = ""

    while running_game and money >= bet_amount:
        if money >= target: 
            game_ending_text = font.render("돈을 다 모았습니다!!!", True, WHITE)
            screen.blit(game_ending_text, (screen_width // 2 - game_ending_text.get_width() // 2, screen_height // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            happy_ending()
            return
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not play_odd_even:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('main_menu_music.mp3')
                        pygame.mixer.music.play(-1)
                    running_game = False
                    
                elif event.key == pygame.K_o:  # 홀 선택
                    player_choice = "odd"
                elif event.key == pygame.K_e:  # 짝 선택
                    player_choice = "even"

                if player_choice:
                    # 주사위 굴리기
                    final_dice_results = roll_dice_animation(num_dice)
                    result, total = calculate_dice_results(final_dice_results)

                    # 결과 판단
                    if (result == "홀수" and player_choice == "odd") or (result == "짝수" and player_choice == "even"):
                        money += bet_amount
                        result_message = f"주사위 결과: {final_dice_results} (합계: {total}) - {result} 승리! (+${bet_amount}) 남은 금액: ${money}"
                    else:
                        money -= bet_amount
                        result_message = f"주사위 결과: {final_dice_results} (합계: {total}) - {result} 패배! (-${bet_amount}) 남은 금액: ${money}"
                    player_choice = None

        # 화면 업데이트
        screen.blit(background_image, (0, 0))  # 배경 그리기

        # 배팅 금액과 현재 잔액
        bet_text = font.render(f"배팅 금액: ${bet_amount}", True, WHITE)
        money_text = font.render(f"현재 잔액: ${money}", True, WHITE)
        message_text = font.render(message, True, WHITE)
        result_text = font.render(result_message, True, WHITE)

        screen.blit(bet_text, (50, 50))
        screen.blit(money_text, (50, 100))
        screen.blit(message_text, (50, 150))
        screen.blit(result_text, (50, 200))

        # 최종 주사위 결과 그리기
        dice_width = 100
        total_dice_width = num_dice * dice_width + (num_dice - 1) * 50
        start_x = (screen_width - total_dice_width) // 2
        y = (screen_height - dice_width) // 2

        for i, dice_value in enumerate(final_dice_results):
            draw_dice_face(start_x + i * (dice_width + 50), y, dice_value)

        pygame.display.flip()

    if money < bet_amount:
        game_over_text = font.render("게임 오버! 잔액이 부족합니다.", True, WHITE)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        sad_ending()
        return
    
def arena_game():
    global money
    bet_amount = 100  # 베팅 금액 고정

    # 색상 정의
    DARK_BLUE = (0, 0, 139)
    #배경음악
    pygame.mixer.music.stop()
    pygame.mixer.music.load('221109-piano-gothic-fantasy-mystery-horror-155650.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    scratch_sound = pygame.mixer.Sound("scratch.mp3")#출처 pixabay
    darksight_sound = pygame.mixer.Sound("darksight.mp3")#출처 pixabay
    holyshield_sound = pygame.mixer.Sound("holyshield.mp3")#출처 pixabay

    class Unit:
        def __init__(self, name, health, attack, defense, speed, image_path, x, y, skill_image=None, darksight_image=None):
            self.name = name
            self.health = health
            self.max_health = health
            self.attack = attack
            self.defense = defense
            self.speed = speed
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (100, 100))
            self.skill_image = pygame.image.load(skill_image).convert_alpha() if skill_image else None
            self.darksight_image = pygame.image.load( darksight_image).convert_alpha() if darksight_image else None
            if self.skill_image:
                self.skill_image = pygame.transform.scale(self.skill_image, (50, 50))
            if self.darksight_image:
                self.darksight_image = pygame.transform.scale(self.darksight_image, (50, 50))
            self.skill_timer = None
            self.darksight_timer = None
            self.x = x
            self.y = y

        def take_damage(self, damage):
            if self.name == "시프마스터" and random.random() < 0.2:
                self.darksight_timer = pygame.time.get_ticks()
                return True  # 회피 성공
            actual_damage = max(0, damage - self.defense)
            self.health -= actual_damage
            return False  # 회피 실패

        def use_savage_blow(self, target):
            if random.random() < 0.4:
                self.skill_timer = pygame.time.get_ticks()
                for _ in range(6):
                    damage = int(self.attack * 0.6)
                    target.take_damage(damage)

        def use_holy_shield(self):
            self.defense = int(self.defense * 1.5)
            self.skill_timer = pygame.time.get_ticks()

        def is_alive(self):
            return self.health > 0

        def reset(self):
            self.health = self.max_health

        def draw(self, screen):
            screen.blit(self.image, (self.x, self.y))
            health_bar_width = 100
            health_ratio = self.health / self.max_health
            pygame.draw.rect(screen, RED, (self.x, self.y - 20, health_bar_width, 10))
            pygame.draw.rect(screen, GREEN, (self.x, self.y - 20, health_bar_width * health_ratio, 10))
            name_text = font.render(self.name, True, GOLD)
            screen.blit(name_text, (self.x, self.y + 110))

        def draw_skill_effect(self, screen):
            if self.skill_timer:
                elapsed_time = pygame.time.get_ticks() - self.skill_timer
                if elapsed_time < 1000 and self.skill_image:
                    screen.blit(self.skill_image, (self.x + 50, self.y - 50))
                else:
                    self.skill_timer = None

            if self.darksight_timer:
                elapsed_time = pygame.time.get_ticks() - self.darksight_timer
                if elapsed_time < 1000 and self.darksight_image:
                    screen.blit(self.darksight_image, (self.x + 50, self.y - 50))
                else:
                    self.darksight_timer = None

    def animate_attack(attacker, defender):
        original_x = attacker.x
        attack_step = 20
        attack_range = 50

        while abs(attacker.x - defender.x) > attack_range:
            attacker.x += attack_step if attacker.x < defender.x else -attack_step
            redraw_screen(attacker, defender)
            pygame.time.delay(10)

        while abs(attacker.x - original_x) > 0:
            attacker.x -= attack_step if attacker.x > original_x else -attack_step
            redraw_screen(attacker, defender)
            pygame.time.delay(10)

        attacker.x = original_x

    def animate_hit(defender, is_avoided):
        original_x = defender.x
        hit_offset = 15
        scratch_image = pygame.image.load("scratch.png")
        scratch_image = pygame.transform.scale(scratch_image, (50, 50))

        if not is_avoided:
            scratch_sound.play()
            for _ in range(5):
                screen.blit(scratch_image, (defender.x + 20, defender.y - 30))
                pygame.display.flip()
                pygame.time.delay(10)
                defender.x += hit_offset
                redraw_screen(None, defender)
                pygame.time.delay(10)
                defender.x -= hit_offset
                redraw_screen(None, defender)
                pygame.time.delay(10)
        defender.x = original_x

    def redraw_screen(attacker, defender):
        screen.blit(arena_background, (0, 0))
        paladin.draw(screen)
        thiefmaster.draw(screen)
        paladin.draw_skill_effect(screen)
        thiefmaster.draw_skill_effect(screen)
        if attacker:
            attacker.draw(screen)
        if defender:
            defender.draw(screen)
        pygame.display.flip()

    arena_background = pygame.image.load('arena_background.png')
    arena_background = pygame.transform.scale(arena_background, (screen_width, screen_height))

    paladin = Unit("팔라딘", 120, 15, 10, 5, "paladin.png", 300, 300, skill_image="shield.png")
    thiefmaster = Unit("시프마스터", 80, 20, 5, 10, "thiefmaster.png", 600, 300, skill_image="blow.png", darksight_image="darksight.png")

    def battle():
        if paladin.speed > thiefmaster.speed:
            attacker, defender = paladin, thiefmaster
        else:
            attacker, defender = thiefmaster, paladin

        while paladin.is_alive() and thiefmaster.is_alive():
            if attacker.name == "팔라딘" and random.random() < 0.3:
                attacker.use_holy_shield()
                holyshield_sound.play()
                redraw_screen(attacker, defender)
                pygame.time.delay(100)
            elif attacker.name == "시프마스터" and random.random() < 0.4:
                attacker.use_savage_blow(defender)
                redraw_screen(attacker, defender)
                pygame.time.delay(100)
            else:
                animate_attack(attacker, defender)
                damage = attacker.attack + random.randint(-5, 5)
                is_avoided = defender.take_damage(damage)
                animate_hit(defender, is_avoided)

            yield attacker, defender

            if defender.is_alive():
                attacker, defender = defender, attacker

        yield None, paladin if paladin.is_alive() else thiefmaster

    running_arena = True
    winner_message = ""
    betting_phase = True
    selected_character = None
    battle_generator = None
    battle_message = ""
    show_winner = False

    while running_arena and money >= bet_amount:
        if money >= target:
            pygame.mixer.music.stop()  # 배경 음악 중지 
            game_ending_text = font.render("돈을 다 모았습니다!!!", True, WHITE)
            screen.blit(game_ending_text, (screen_width // 2 - game_ending_text.get_width() // 2, screen_height // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            happy_ending()
            return
        
        screen.blit(arena_background, (0, 0))
        paladin.draw(screen)
        thiefmaster.draw(screen)
        paladin.draw_skill_effect(screen)
        thiefmaster.draw_skill_effect(screen)

        balance_text = font.render(f"현재 잔액: ${money}", True, WHITE)
        screen.blit(balance_text, (10, 10))

        if betting_phase:
            instruction_text = font.render("1번: 팔라딘 | 2번: 시프마스터", True, GREEN)
            screen.blit(instruction_text, (100, 100))
        elif show_winner:
            winner_text = font.render(winner_message, True, DARK_BLUE)
            screen.blit(winner_text, (screen_width // 2 - winner_text.get_width() // 2, 50))
            restart_text = font.render("다시 베팅하려면 SPACE를 누르세요", True,GOLD)
            screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, 100))
        
        else:
            battle_text = font.render(battle_message, True, WHITE)
            screen.blit(battle_text, (screen_width // 2 - battle_text.get_width() // 2, 50))
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            elif event.type == pygame.KEYDOWN:
                if betting_phase:
                    if event.key == pygame.K_1:
                        selected_character = "팔라딘"
                        betting_phase = False
                        battle_generator = battle()
                    elif event.key == pygame.K_2:
                        selected_character = "시프마스터"
                        betting_phase = False
                        battle_generator = battle()
                elif event.key == pygame.K_SPACE and show_winner:
                    paladin.reset()
                    thiefmaster.reset()
                    betting_phase = True
                    show_winner = False
                    winner_message = ""
                    battle_message = ""
                elif event.key == pygame.K_ESCAPE:
                    if not arena_game:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('main_menu_music.mp3')
                        pygame.mixer.music.play(-1)
                    running_arena = False  # 투기장 루프 종료
                    return  # 함수 종료로 메인 메뉴로 복귀


        if not betting_phase and not show_winner and battle_generator:
            try:
                attacker, defender = next(battle_generator)
                if attacker and defender:
                    battle_message = f"{attacker.name}이 {defender.name}을 공격합니다!"
            except StopIteration:
                show_winner = True
                winner = paladin if paladin.is_alive() else thiefmaster
                if winner.name == selected_character:
                    money += bet_amount
                    winner_message = f"{winner.name} 승리! (+${bet_amount})"
                else:
                    money -= bet_amount
                    winner_message = f"{winner.name} 승리! (-${bet_amount})"

        pygame.display.flip()

    if money < bet_amount:
        pygame.mixer.music.stop()  # 배경 음악 중지
        game_over_text = font.render("게임 오버! 잔액이 부족합니다.", True, WHITE)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        sad_ending()
        return


def intro_story():
    intro_background_image = pygame.image.load('intro_background.png')
    intro_background_image = pygame.transform.scale(intro_background_image, (screen_width, screen_height))

    story_pages = [
        "어느 날, 평범했던 일상이 한 통의 전화로 뒤바뀌었다.",
        '"당신의 가족이 우리 손에 있다. 몸값으로 10만달러를 준비해라."',
        "믿기 힘든 내용이 전화기 너머로 들려왔다.",
        "나는 가족을 구하기 위해 무엇이든 해야 했다.",
        "선택의 여지가 없었다.",
        "돈을 마련할 수 있는 유일한 방법은 카지노였다."
    ]

    current_page = 0
    current_text = ""
    char_index = 0
    text_speed = 50 
    last_update_time = pygame.time.get_ticks()

    running_intro = True

    pygame.mixer.music.load('call.mp3')#https://pgtd.tistory.com/280
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()

    

    while running_intro:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if current_page < len(story_pages) - 1:
                        current_page += 1
                        current_text = ""
                        char_index = 0
                    else:
                        return main_menu

        # 배경 이미지
        screen.blit(intro_background_image, (0, 0))


        # 텍스트 애니메이션 
        now = pygame.time.get_ticks()
        if now - last_update_time > text_speed and char_index < len(story_pages[current_page]):
            current_text += story_pages[current_page][char_index]
            char_index += 1
            last_update_time = now

        # 텍스트 렌더링 및 표시
        rendered_text = font.render(current_text, True, WHITE)
        text_rect = rendered_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(rendered_text, text_rect)

        pygame.display.flip()

def main_menu():
    # 메뉴 배경 이미지 로드 및 크기 조정
    menu_background_image = pygame.image.load('main_background.png')
    menu_background_image = pygame.transform.scale(menu_background_image, (screen_width, screen_height))
    # 메인 메뉴 루프
    running_menu = True
    while running_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if enter_button.collidepoint(mouse_pos):
                    # 입장하기 버튼 클릭 시 실행할 코드
                    print("게임에 입장합니다!")
                    running_menu = False

        # 메뉴 배경 이미지 그리기
        screen.blit(menu_background_image, (0, 0))
        # 메인 메뉴 화면 그리기

        enter_text = font.render("입장하기", True, WHITE)
        
        # "입장하기" 버튼 생성
        enter_button = pygame.Rect(screen_width // 2 - 75, screen_height // 1.5 - 25, 150, 50)
        pygame.draw.rect(screen, GOLD, enter_button, border_radius=10)
        screen.blit(enter_text, (enter_button.x + (enter_button.width - enter_text.get_width()) // 2, enter_button.y + (enter_button.height - enter_text.get_height()) // 2))

        pygame.display.flip()


def start_pygame():
    global screen

    # 배경 이미지 로드 및 크기 조정
    background_image = pygame.image.load('main.png')
    background_image = pygame.transform.scale(background_image, (1700, 1400))

    # 카메라 오프셋 초기화
    camera_x, camera_y = 0, 0

    # 게임 루프 초기화
    running = True

    pygame.mixer.music.load('main_menu_music.mp3')#Music by <a href="https://pixabay.com/ko/users/backgroundmusicforvideos-46459014/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=263181">Maksym Malko</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=263181">Pixabay</a>
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 게임 루프 내의 이벤트 처리 부분
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # 마우스 좌표를 카메라 오프셋을 적용하여 실제 좌표로 변환
                actual_mouse_pos = (mouse_pos[0] + camera_x, mouse_pos[1] + camera_y)
                # NPC 클릭 시 블랙잭 실행
                if blackjack_npc.rect.collidepoint(actual_mouse_pos):
                    play_blackjack()
                # 다른 NPC 클릭 시 슬롯머신 실행
                elif roulette_npc.rect.collidepoint(actual_mouse_pos):
                    play_slot_machine()
                elif roulette_npc1.rect.collidepoint(actual_mouse_pos):
                    play_slot_machine()
                elif roulette_npc2.rect.collidepoint(actual_mouse_pos):
                    play_slot_machine()
                elif dice_npc.rect.collidepoint(actual_mouse_pos):  # 홀짝 다이스 게임 실행
                    play_odd_even()
                elif arena_npc.rect.collidepoint(actual_mouse_pos):
                    arena_game()   

        # 애니메이션 상태에 따라 플레이어 그리기
        player_image = player_images[current_player_state]
        player_width, player_height = player_rect.width, player_rect.height
        player_frame_width = player_width // player_animation_frames

        source_rect = pygame.Rect(player_frame_index * player_frame_width, 0, player_frame_width, player_height)
        screen.blit(player_image, (player_rect.x - camera_x, player_rect.y - camera_y), source_rect)

        # 키 입력 처리
        keys = pygame.key.get_pressed()  # 여기서 keys 변수를 먼저 정의
        update_player_animation(keys)    # 애니메이션 업데이트
        
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed
        
        if keys[pygame.K_UP]:
            player_rect.y -= player_speed
        
        if keys[pygame.K_DOWN]:
            player_rect.y += player_speed

# 플레이어가 배경 밖으로 나가지 않도록 제한
        player_rect.x = max(0, min(player_rect.x, background_image.get_width() - player_rect.width))
        player_rect.y = max(0, min(player_rect.y, background_image.get_height() - player_rect.height))

# 카메라 오프셋 업데이트: 플레이어를 중심으로 카메라 위치 조정
        camera_x = max(0, min(player_rect.x - screen_width // 2 + player_rect.width // 2, background_image.get_width() - screen_width))
        camera_y = max(0, min(player_rect.y - screen_height // 2 + player_rect.height // 2, background_image.get_height() - screen_height))


        # 화면 그리기
        screen.blit(background_image, (-camera_x, -camera_y))  # 카메라 오프셋 적용된 배경
        # 플레이어 그리기 (카메라 오프셋 적용)
        screen.blit(player_image, (player_rect.x - camera_x, player_rect.y - camera_y))
        
        # NPC 그리기 (카메라 오프셋 적용)
        roulette_npc.draw(screen, camera_x, camera_y)
        roulette_npc1.draw(screen, camera_x, camera_y)
        roulette_npc2.draw(screen, camera_x, camera_y)
        blackjack_npc.draw(screen, camera_x, camera_y)
        dice_npc.draw(screen, camera_x, camera_y)
        arena_npc.draw(screen, camera_x, camera_y)

        # 화면 업데이트 
        pygame.display.flip()

def sad_ending():
    sad_background = pygame.image.load('sad_ending_background.png')  # 또는 새로운 엔딩용 배경
    sad_background = pygame.transform.scale(sad_background, (screen_width, screen_height))
    
    ending_texts = [
        "결국 돈을 모으는데 실패했다...",
        "더 이상 희망이 없었다.",
        "가족을 구하지 못한 나는...",
        "계속 살아갈 수 있을까...."
    ]
    
    running_ending = True
    current_text = ""
    current_page = 0
    char_index = 0
    text_speed = 50
    last_update_time = pygame.time.get_ticks()
    
    while running_ending:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if current_page < len(ending_texts) - 1:
                        current_page += 1
                        current_text = ""
                        char_index = 0
                    else:
                        pygame.quit()
                        sys.exit()
        
        screen.blit(sad_background, (0, 0))

        keys = pygame.key.get_pressed()
        update_player_animation(keys)

        
        now = pygame.time.get_ticks()
        if now - last_update_time > text_speed and char_index < len(ending_texts[current_page]):
            current_text += ending_texts[current_page][char_index]
            char_index += 1
            last_update_time = now
            
        rendered_text = font.render(current_text, True, RED)
        text_rect = rendered_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(rendered_text, text_rect)
        
        pygame.display.flip()

def happy_ending():
    happy_background = pygame.image.load('happy_ending_background.png')  # 또는 새로운 엔딩용 배경
    happy_background = pygame.transform.scale(happy_background, (screen_width, screen_height))
    
    ending_texts = [
        "마침내 돈을 다 모았다...",
        "이제 가족을 구할 수 있어.",
        "기다려, 곧 데리러 갈게...",
        "우리 다시 함께할 수 있어!"
    ]
    
    running_ending = True
    current_text = ""
    current_page = 0
    char_index = 0
    text_speed = 50
    last_update_time = pygame.time.get_ticks()
    
    while running_ending:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if current_page < len(ending_texts) - 1:
                        current_page += 1
                        current_text = ""
                        char_index = 0
                    else:
                        pygame.quit()
                        sys.exit()
        
        screen.blit(happy_background, (0, 0))
        
        now = pygame.time.get_ticks()
        if now - last_update_time > text_speed and char_index < len(ending_texts[current_page]):
            current_text += ending_texts[current_page][char_index]
            char_index += 1
            last_update_time = now
            
        rendered_text = font.render(current_text, True, RED)
        text_rect = rendered_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(rendered_text, text_rect)
        
        pygame.display.flip()


intro_story()
main_menu()
start_pygame()
