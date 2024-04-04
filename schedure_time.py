from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# Hàm sẽ được chạy theo lịch trình
def job():
    print("Hello, world!")

# Khởi tạo scheduler
scheduler = BlockingScheduler()

# Thời gian bắt đầu lập lịch
start_time = datetime(2024, 4, 4, 17, 10, 0)  # Bắt đầu lập lịch vào ngày 6 tháng 4 năm 2024, lúc 12:00:00

# Thêm công việc vào lịch trình - chạy job() mỗi 5 giây, bắt đầu từ start_time
scheduler.add_job(job, 'interval', seconds=5, start_date=start_time)

# Bắt đầu lịch trình
try:
    scheduler.start()
except KeyboardInterrupt:
    pass
