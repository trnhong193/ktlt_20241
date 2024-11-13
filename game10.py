import cv2
import mediapipe as mp
import pygame
import random
import time
import numpy as np

# Khởi tạo MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_draw = mp.solutions.drawing_utils

# Mở webcam và đặt kích thước khung hình
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

score = 0
game_over = False

# Khởi tạo Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Hand Counting Game')
font = pygame.font.SysFont('Comic Sans MS', 74)  # Font Comic Sans MS
small_font = pygame.font.SysFont('Comic Sans MS', 36)

# Gradient background function
def draw_gradient_background(surface, color1, color2):
    for y in range(surface.get_height()):
        color = [
            color1[i] + (color2[i] - color1[i]) * y // surface.get_height()
            for i in range(3)
        ]
        pygame.draw.line(surface, color, (0, y), (surface.get_width(), y))

while not game_over:
    target_number = random.randint(0, 10)  # Tổng số ngón tay có thể từ 0 đến 10
    start_time = time.time()
    timer = 10  # 10 giây cho mỗi lượt

    correct = False

    while time.time() - start_time < timer and not correct:
        # Xử lý sự kiện Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Đọc hình ảnh từ webcam
        success, img = cap.read()
        if not success:
            continue  # Nếu không lấy được khung hình, bỏ qua vòng lặp này

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        total_fingers = 0  # Tổng số ngón tay giơ lên

        if results.multi_hand_landmarks:
            for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                lm_list = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = img.shape
                    lm_list.append((int(lm.x * w), int(lm.y * h)))

                # Đếm số ngón tay
                fingers = []
                tip_ids = [4, 8, 12, 16, 20]
                handedness_label = hand_handedness.classification[0].label.lower()

                if handedness_label == 'left':
                    displayed_hand = 'Left'
                else:
                    displayed_hand = 'Right'

                # Ngón cái
                if displayed_hand.lower() == 'right':
                    if lm_list[tip_ids[0]][0] > lm_list[tip_ids[0] - 1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                else:  # Tay trái
                    if lm_list[tip_ids[0]][0] < lm_list[tip_ids[0] - 1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                # 4 ngón còn lại
                for id in range(1, 5):
                    if lm_list[tip_ids[id]][1] < lm_list[tip_ids[id] - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                finger_count = fingers.count(1)
                total_fingers += finger_count

                # Vẽ bàn tay và số ngón tay lên hình ảnh
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                cv2.putText(img, f'{displayed_hand} Hand: {finger_count}', (10, 30 if displayed_hand == 'Left' else 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        if total_fingers == target_number:
            correct = True
            score += 1  # Cập nhật điểm số
            print(f"Score updated: {score}")  # Debug giá trị score

        # Chuyển đổi hình ảnh từ OpenCV sang Pygame Surface
        frame = np.rot90(img_rgb)
        frame_surface = pygame.surfarray.make_surface(frame)

        # Hiển thị nền gradient
        draw_gradient_background(screen, (30, 144, 255), (255, 182, 193))

        # Hiển thị camera (nền)
        screen.blit(frame_surface, (80, 100))  

        # Vẽ hộp chứa target number
        pygame.draw.rect(screen, (255, 255, 255), (300, 30, 200, 80), border_radius=10)
        number_text = font.render(str(target_number), True, (0, 0, 0))
        screen.blit(number_text, (400 - number_text.get_width() // 2, 40))
        
        # Hiển thị thời gian còn lại
        pygame.draw.rect(screen, (255, 255, 255), (30, 30, 180, 50), border_radius=10)
        time_left = int(timer - (time.time() - start_time))
        timer_text = small_font.render(f'Time: {time_left}', True, (0, 0, 0))
        screen.blit(timer_text, (40, 40))

        # Hiển thị điểm số
        pygame.draw.rect(screen, (255, 255, 255), (550, 30, 180, 50), border_radius=10)
        score_text = small_font.render(f'Score: {int(score)}', True, (0, 0, 0))
        screen.blit(score_text, (560, 40))

        # Cập nhật màn hình Pygame
        pygame.display.flip()

    if not correct:
        game_over = True

# Hiển thị Game Over
screen.fill((255, 255, 255))
game_over_text = font.render('Game Over', True, (255, 0, 0))
screen.blit(game_over_text, (400 - game_over_text.get_width() // 2, 200))
final_score_text = small_font.render(f'Final Score: {score}', True, (0, 0, 0))
screen.blit(final_score_text, (400 - final_score_text.get_width() // 2, 300))
pygame.display.flip()
pygame.time.wait(3000)

# Giải phóng tài nguyên
cap.release()
pygame.quit()
cv2.destroyAllWindows()
