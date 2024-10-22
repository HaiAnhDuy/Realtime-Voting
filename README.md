# Hệ Thống Bầu Cử Realtime

## Giới thiệu
Kho lưu trữ này chứa mã cho hệ thống bỏ phiếu bầu cử theo thời gian thực. Hệ thống được xây dựng bằng **Python**, **Kafka**, **Spark Streaming**, **Postgres** và **Streamlit**. Môi trường được xây dựng bằng **Docker Compose** để dễ dàng tạo các dịch vụ cần thiết trong các container Docker.

## Kiến trúc
![image](https://github.com/user-attachments/assets/d34bdd1a-eea5-4d11-b819-914a10e8d1ad)

## Luồng hệ thống
![image](https://github.com/user-attachments/assets/3169a0c9-f546-4f84-8d0f-cdf796b7ec75)

## Thành phần
- **main.py**: Đây là tập lệnh Python chính tạo các bảng cần thiết trên postgres (**candidates**, **voters** và **votes**), nó cũng tạo chủ đề Kafka và tạo một bản sao của bảng **votes** trong chủ đề Kafka. Nó cũng chứa logic để sử dụng các phiếu bầu từ chủ đề Kafka và tạo dữ liệu trên **voters_topic** Kafka.
- **voting.py**: Đây là tập lệnh Python chứa logic để sử dụng các phiếu bầu từ chủ đề Kafka (**voters_topic**), tạo dữ liệu bỏ phiếu và xuất dữ liệu trên **votes_topicKafka**.
- **spark-streaming.py**: Đây là tập lệnh Python chứa logic để sử dụng các phiếu bầu từ chủ đề Kafka (**votes_topic**), làm giàu dữ liệu từ postgres và tổng hợp các phiếu bầu và tạo dữ liệu cho các chủ đề cụ thể trên Kafka.
- **streamlit-app.py**: Đây là tập lệnh Python chứa logic để sử dụng dữ liệu bỏ phiếu tổng hợp từ chủ đề Kafka cũng như postgres và hiển thị dữ liệu bỏ phiếu theo thời gian thực bằng **Streamlit**.

### Yêu cầu hệ thống
Để chạy dự án này, bạn cần cài đặt các phần mềm sau:
- **Python** 3.9+
- **Docker**
- **Apache Kafka**
- **Spark**

### Hướng dẫn cài đặt

1. **Clone repository** về máy:
   ```bash
   git clone https://github.com/username/stock-price-alert.git
   cd stock-price-alert
