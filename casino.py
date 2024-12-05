import pygame
import random
import sys


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

# 글꼴 설정
try:
    font = pygame.font.SysFont("Apple SD Gothic Neo", 36, bold=True) 
except:
    font = pygame.font.SysFont(None, 36, bold=True) 

# 카드 이미지 경로
CARD_FOLDER = "card"

money= 1000

# 색상 정의
black = (0, 0, 0)

# 플레이어 이미지 로드 및 초기 설정
player_image = pygame.image.load("player1.png")
# 이미지 크기 조정
player_image = pygame.transform.scale(player_image, (player_image.get_width() // 10, player_image.get_height() // 10))
player_rect = player_image.get_rect()
player_rect.center = (screen_width // 2, screen_height // 2)

# 플레이어 이동 속도
player_speed = 5

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
roulette_npc = NPC("roulette.png", 200, 150)
blackjack_npc = NPC("blackjack_dealer.png", 700, 300)

def play_blackjack():
    global money  # 전역 변수로 돈 관리
    bet_amount = 100  # 기본 배팅 금액
    
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
    background_image = pygame.image.load('inside.png')
    
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
        screen.blit(bet_text, (screen_width - 250, 30))
        screen.blit(money_text, (screen_width - 250, 70))

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_blackjack = False
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

# 슬롯머신 실행 함수
def play_slot_machine():
    image_filenames = ['lemon.png', 'seven.png', 'apple.png', 'cherry.png']
    jackpot_image = pygame.image.load('jackpot.png')
    background_image = pygame.image.load('inside.png')
# 배경 이미지
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    reel_positions = [screen_width // 4, screen_width // 2, screen_width // 4 * 3] 
    reel_y = screen_height // 2 - 100
    images = [pygame.image.load(img) for img in image_filenames]

    # 슬롯머신 상태 
    reels_spinning = [False, False, False]
    current_images = [None, None, None]
    spin_sequence = [None, None, None]
    jackpot_triggered = False
    
    # 슬롯 머신 릴 이미지 크기 조정 (예: 크기를 100x100으로 조정)
    image_size = (100, 100)  # 원하는 크기 설정
    images = [pygame.transform.scale(pygame.image.load(img), image_size) for img in image_filenames]


    # 릴 회전 
    def spin_reels():
        nonlocal spin_sequence
        spin_sequence = [random.choice(images) for _ in range(3)]

    # 잭팟 확인 
    def check_jackpot():
        return spin_sequence[0] == spin_sequence[1] == spin_sequence[2]

    # 슬롯머신 화면 그리기 
    def draw_slot_machine():
        screen.fill(BLACK)
    
    # 슬롯머신 화면 그리기 
    def draw_slot_machine():
        # 배경 이미지 그리기
        screen.blit(background_image, (0, 0))

        # 제목 및 안내 텍스트 표시
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
            screen.blit(jackpot_image, (screen_width // 2 - jackpot_image.get_width() // 2, screen_height // 3 ))

    # 슬롯머신 게임 루프 변수 초기화
    running_slots = True
    reel_index_to_stop = 0

    while running_slots:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    running_slots = False

                elif event.key == pygame.K_SPACE:  
                    if not any(reels_spinning):  
                        reels_spinning = [True, True, True]
                        spin_reels()
                        current_images = [random.choice(images) for _ in range(3)]
                    else:
                        if reel_index_to_stop < len(reels_spinning):
                            reels_spinning[reel_index_to_stop] = False
                            current_images[reel_index_to_stop] = spin_sequence[reel_index_to_stop]
                            reel_index_to_stop += 1

                        # 모든 릴 멈춤 -> 잭팟 확인 및 결과 표시
                        if all(not spinning for spinning in reels_spinning):
                            jackpot_triggered = check_jackpot()
                            reel_index_to_stop = 0

        # 릴이 회전 중일 때 랜덤 이미지 표시
        for i in range(3):
            if reels_spinning[i]:
                current_images[i] = random.choice(images)

        draw_slot_machine()
        pygame.display.flip()

def intro_story():
    intro_background_image = pygame.image.load('intro_background.png')
    intro_background_image = pygame.transform.scale(intro_background_image, (screen_width, screen_height))

    story_pages = [
        "어느 날, 평범했던 일상이 한 통의 전화로 뒤바뀌었다.",
        '"당신의 가족이 우리 손에 있다. 몸값으로 1억원을 준비해라."',
        "믿기 힘든 내용이 전화기 너머로 들려왔다.",
        "나는 가족을 구하기 위해 무엇이든 해야 했다.",
        "선택의 여지가 없었다. 돈을 마련할 수 있는 유일한 방법은 카지노였다."
    ]

    current_page = 0
    current_text = ""
    char_index = 0
    text_speed = 50 
    last_update_time = pygame.time.get_ticks()

    running_intro = True

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
    menu_background_image = pygame.image.load('casino_main_background.png')
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

        # 메인 메뉴 화면 그리기
        # 메뉴 배경 이미지 그리기
        screen.blit(menu_background_image, (0, 0))
        title_text = font.render("카지노", True, BLACK)
        enter_text = font.render("입장하기", True, RED)

        # 제목과 버튼을 화면 중앙에 배치
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4))
        
        # "입장하기" 버튼 생성
        enter_button = pygame.Rect(screen_width // 2 - 75, screen_height // 2 - 25, 150, 50)
        pygame.draw.rect(screen, BLACK, enter_button)
        screen.blit(enter_text, (enter_button.x + (enter_button.width - enter_text.get_width()) // 2, enter_button.y + (enter_button.height - enter_text.get_height()) // 2))

        pygame.display.flip()


def start_pygame():
    global screen

    # 배경 이미지 로드 및 크기 조정
    background_image = pygame.image.load('casino_up.png')
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # 카메라 오프셋 초기화
    camera_x, camera_y = 0, 0

    # 게임 루프 초기화
    running = True
    
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

        # 키 입력 처리
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed
        
        if keys[pygame.K_UP]:
            player_rect.y -= player_speed
        
        if keys[pygame.K_DOWN]:
            player_rect.y += player_speed

        # 카메라 오프셋 업데이트: 플레이어를 중심으로 카메라 위치 조정
        camera_x = player_rect.x - screen_width // 2 + player_rect.width // 2
        camera_y = player_rect.y - screen_height // 2 + player_rect.height // 2


        # 화면 그리기
        screen.blit(background_image, (0, 0))  # 배경 이미지 그리기
        # 플레이어 그리기 (카메라 오프셋 적용)
        screen.blit(player_image, (player_rect.x - camera_x, player_rect.y - camera_y))
        
        # NPC 그리기 (카메라 오프셋 적용)
        roulette_npc.draw(screen, camera_x, camera_y)
        blackjack_npc.draw(screen, camera_x, camera_y)

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
