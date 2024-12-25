# Hand Counting Game

## Mô tả

**Hand Counting Game** là một trò chơi đơn giản được xây dựng bằng Python, nơi người chơi cần đếm số ngón tay mà họ giơ lên và so sánh với số mục tiêu hiển thị trên màn hình trong một khoảng thời gian giới hạn. Trò chơi sử dụng thư viện OpenCV để nhận diện ngón tay và Pygame để xây dựng giao diện người dùng. Đây là một trò chơi giúp rèn luyện phản xạ và khả năng đếm nhanh.

## Cách chơi
Cách chơi

    Khởi động trò chơi:
        Sau khi chạy chương trình, màn hình sẽ hiển thị giao diện của trò chơi với camera bật lên và các thông tin như:
            Số mục tiêu: Số cần đạt được (hiển thị ở giữa trên màn hình).
            Thời gian: Đếm ngược thời gian còn lại để hoàn thành.
            Điểm số: Điểm bạn đạt được khi trả lời đúng.

    Nhiệm vụ của bạn:
        Giơ tay trước camera và thể hiện số ngón tay giơ lên tương ứng với số mục tiêu.
            Ví dụ: Nếu số mục tiêu là 3, bạn cần giơ 3 ngón tay.

    Luật chơi:
        Trò chơi hỗ trợ nhận diện cả hai tay.
        Bạn có 10 giây để giơ số ngón tay khớp với số mục tiêu.
        Nếu bạn đoán đúng, điểm số sẽ tăng lên, và trò chơi sẽ chuyển sang số mục tiêu mới.
        Nếu hết thời gian mà bạn chưa đoán đúng, trò chơi sẽ kết thúc.

    Kết thúc trò chơi:
        Khi hết giờ hoặc khi bạn không giơ đúng số ngón tay trong thời gian quy định, trò chơi kết thúc.
        Màn hình sẽ hiển thị thông báo Game Over và điểm số cuối cùng của bạn.
## Yêu cầu

Để chạy được dự án này, bạn cần cài đặt các thư viện Python sau:

- Python 3.x
- OpenCV
- MediaPipe
- Pygame
- NumPy

Bạn có thể cài đặt tất cả các thư viện cần thiết bằng cách chạy lệnh sau trong terminal:

```bash
pip install opencv-python mediapipe pygame numpy


