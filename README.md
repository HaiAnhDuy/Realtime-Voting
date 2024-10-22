# Stock Price Alert System

## Giới thiệu
Hệ thống này cho phép người dùng thiết lập cảnh báo giá cổ phiếu dựa trên dữ liệu thời gian thực. Khi giá cổ phiếu đạt ngưỡng do người dùng thiết lập, hệ thống sẽ gửi email cảnh báo. Dự án sử dụng **Python**, **Kafka**, và **Spark** để xử lý dữ liệu và **Docker** để quản lý môi trường triển khai.

### Tính năng
- **Theo dõi cổ phiếu thời gian thực:** Xử lý dữ liệu streaming từ nguồn dữ liệu chứng khoán.
- **Thiết lập ngưỡng giá:** Người dùng có thể thiết lập ngưỡng giá cho từng mã cổ phiếu.
- **Cảnh báo qua email:** Gửi cảnh báo tự động khi cổ phiếu đạt giá yêu cầu.

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
