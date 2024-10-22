# Hệ Thống Bầu Cử Realtime

## Giới thiệu
Kho lưu trữ này chứa mã cho hệ thống bỏ phiếu bầu cử theo thời gian thực. Hệ thống được xây dựng bằng **Python**, **Kafka**, **Spark Streaming**, **Postgres** và **Streamlit**. Hệ thống được xây dựng bằng **Docker Compose** để dễ dàng tạo các dịch vụ cần thiết trong các container Docker.

## Kiến trúc
![image](https://github.com/user-attachments/assets/d34bdd1a-eea5-4d11-b819-914a10e8d1ad)

## Ảnh chụp màn hình (nếu có)
![Stock Alert Dashboard](images/dashboard.png)

## Cài đặt

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
