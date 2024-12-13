import cv2
import mediapipe as mp
import pygame
import random
import time
import numpy as np

# Lớp HandDetector
class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=2)
        self.tip_ids = [4, 8, 12, 16, 20]

    def detect_hands(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        total_fingers = 0

        if results.multi_hand_landmarks:
            for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                lm_list = []
                for lm in hand_landmarks.landmark:
                    h, w, _ = img.shape
                    lm_list.append((int(lm.x * w), int(lm.y * h)))

                # Đếm ngón tay
                fingers = []
                if hand_handedness.classification[0].label.lower() == 'right':
                    if lm_list[self.tip_ids[0]][0] > lm_list[self.tip_ids[0] - 1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                else:  # Tay trái
                    if lm_list[self.tip_ids[0]][0] < lm_list[self.tip_ids[0] - 1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                for id in range(1, 5):
                    if lm_list[self.tip_ids[id]][1] < lm_list[self.tip_ids[id] - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                total_fingers += fingers.count(1)

        return total_fingers

# Lớp GameLogic
class GameLogic:
    def __init__(self):
        self.score = 0
        self.target_number = random.randint(0, 10)
        self.start_time = time.time()
        self.timer = 10
        self.correct = False

    def update_target(self):
        self.target_number = random.randint(0, 10)
        self.start_time = time.time()
        self.correct = False

    def check_answer(self, total_fingers):
        if total_fingers == self.target_number:
            self.correct = True
            self.score += 1

    def is_time_up(self):
        return time.time() - self.start_time >= self.timer

# Lớp UIRenderer
class UIRenderer:
    def __init__(self, screen, font, small_font):
        self.screen = screen
        self.font = font
        self.small_font = small_font

    def draw_gradient_background(self, color1, color2):
        for y in range(self.screen.get_height()):
            color = [
                color1[i] + (color2[i] - color1[i]) * y // self.screen.get_height()
                for i in range(3)
            ]
            pygame.draw.line(self.screen, color, (0, y), (self.screen.get_width(), y))

    def render_ui(self, frame_surface, game_logic):
        # Hiển thị nền gradient
        self.draw_gradient_background((30, 144, 255), (255, 182, 193))

        # Hiển thị camera (nền)
        self.screen.blit(frame_surface, (80, 100))

        # Vẽ hộp chứa target number
        pygame.draw.rect(self.screen, (255, 255, 255), (300, 30, 200, 80), border_radius=10)
        number_text = self.font.render(str(game_logic.target_number), True, (0, 0, 0))
        self.screen.blit(number_text, (400 - number_text.get_width() // 2, 40))

        # Hiển thị thời gian còn lại
        pygame.draw.rect(self.screen, (255, 255, 255), (30, 30, 180, 50), border_radius=10)
        time_left = int(game_logic.timer - (time.time() - game_logic.start_time))
        timer_text = self.small_font.render(f'Time: {time_left}', True, (0, 0, 0))
        self.screen.blit(timer_text, (40, 40))

        # Hiển thị điểm số
        pygame.draw.rect(self.screen, (255, 255, 255), (550, 30, 180, 50), border_radius=10)
        score_text = self.small_font.render(f'Score: {game_logic.score}', True, (0, 0, 0))
        self.screen.blit(score_text, (560, 40))

# Main Program
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Hand Counting Game')
font = pygame.font.SysFont('Comic Sans MS', 74)
small_font = pygame.font.SysFont('Comic Sans MS', 36)

hand_detector = HandDetector()
game_logic = GameLogic()
ui_renderer = UIRenderer(screen, font, small_font)

game_over = False

while not game_over:
    success, img = cap.read()
    if not success:
        continue

    total_fingers = hand_detector.detect_hands(img)
    game_logic.check_answer(total_fingers)

    if game_logic.correct:
        game_logic.update_target()

    if game_logic.is_time_up():
        game_over = True

    # Chuyển đổi hình ảnh từ OpenCV sang Pygame Surface
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frame = np.rot90(img_rgb)
    frame_surface = pygame.surfarray.make_surface(frame)

    # Hiển thị giao diện
    ui_renderer.render_ui(frame_surface, game_logic)
    pygame.display.flip()

# Hiển thị Game Over
screen.fill((255, 255, 255))
game_over_text = font.render('Game Over', True, (255, 0, 0))
screen.blit(game_over_text, (400 - game_over_text.get_width() // 2, 200))
final_score_text = small_font.render(f'Final Score: {game_logic.score}', True, (0, 0, 0))
screen.blit(final_score_text, (400 - final_score_text.get_width() // 2, 300))
pygame.display.flip()
pygame.time.wait(3000)

cap.release()
pygame.quit()
cv2.destroyAllWindows()
