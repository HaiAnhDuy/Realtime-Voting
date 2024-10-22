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

## Thiết lập hệ thống
Tệp Docker Compose này cho phép bạn dễ dàng khởi chạy ứng dụng Zookkeeper, Kafka và Postgres trong các container Docker.

### Ảnh chụp

1. **Thông tin ứng cử viên và đảng phái**:
 
![image](https://github.com/user-attachments/assets/294bebc8-7616-4544-ac50-3f0dccf7c29e)

2. **Người bỏ phiếu**:

![image](https://github.com/user-attachments/assets/639ac5d7-baf5-4a5d-ae2b-cfec0f0cb2fd)

3. **Bỏ phiếu**

![image](https://github.com/user-attachments/assets/d49f3813-469a-4dd9-8e9b-ceb505a8a987)

4. **Dashboard**

![image](https://github.com/user-attachments/assets/568c67ab-dfc0-488e-a909-ac4881295493)


