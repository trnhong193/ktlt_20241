import cv2
import mediapipe as mp
import pygame
import random
import time

# Khởi tạo MediaPipe và Pygame
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Hand Rehabilitation Game')
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Mở webcam
cap = cv2.VideoCapture(0)

score = 0
game_over = False

while not game_over:
    target_number = random.randint(0, 5)
    start_time = time.time()
    timer = 10  # 3 giây cho mỗi lượt

    correct = False

    while time.time() - start_time < timer and not correct:
        # Xử lý sự kiện Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Đọc hình ảnh từ webcam
        success, img = cap.read()
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = img.shape
                lm_list.append((int(lm.x * w), int(lm.y * h)))

            # Đếm số ngón tay
            fingers = []
            tip_ids = [4, 8, 12, 16, 20]
            
            # Ngón cái
            if lm_list[tip_ids[0]][0] > lm_list[tip_ids[0] - 1][0]:
                fingers.append(1)
            else:
                fingers.append(0)
            # 4 ngón còn lại
            for id in range(1, 5):
                if lm_list[tip_ids[id]][1] < lm_list[tip_ids[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            total_fingers = fingers.count(1)

            if total_fingers == target_number:
                correct = True
                score += 1
        flipped_frame = cv2.flip(img, 1)
        cv2.imshow("cam", flipped_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # running = False
            break

        # Hiển thị giao diện
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