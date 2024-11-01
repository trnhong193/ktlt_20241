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
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

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

        # Lật hình ảnh
        img = cv2.flip(img, 1)

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

                # Điều chỉnh nhãn tay sau khi lật hình ảnh
                if handedness_label == 'left':
                    displayed_hand = 'Left'  # Tay trái trở thành tay phải sau khi lật
                else:
                    displayed_hand = 'Right'   # Tay phải trở thành tay trái sau khi lật

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
            score += 1

        # Hiển thị hình ảnh
        cv2.imshow("Hand Counting Game", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            game_over = True
            break

        # Hiển thị giao diện Pygame
        screen.fill((255, 255, 255))
        number_text = font.render(str(target_number), True, (0, 0, 0))
        screen.blit(number_text, (400 - number_text.get_width() // 2, 200))
        time_left = int(timer - (time.time() - start_time))
        timer_text = small_font.render(f'Time: {time_left}', True, (0, 0, 0))
        screen.blit(timer_text, (10, 10))
        score_text = small_font.render(f'Score: {score}', True, (0, 0, 0))
        screen.blit(score_text, (700, 10))
        pygame.display.flip()

    if not correct:
        game_over = True

# Hiển thị Game Over
screen.fill((255, 255, 255))
game_over_text = font.render('Game Over', True, (255, 0, 0))
screen.blit(game_over_text, (400 - game_over_text.get_width() // 2, 300))
pygame.display.flip()
pygame.time.wait(3000)

# Giải phóng tài nguyên
cap.release()
pygame.quit()
cv2.destroyAllWindows()
