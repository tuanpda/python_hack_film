# libraries
import pyodbc
import json
import datetime
from tqdm import tqdm

# zuiphim_phimmoi
# zuiphim_phimle
# zuiphim_phimvothuat
# zuiphim_phimanime
# zuiphim_phimkinhdi


def push_data_to_database(category, jsonfile, checkDelete):
    # info connect db
    server = "125.212.224.205"
    database = "tuanphan_phimhay"
    username = "tuanphan_phimhay"
    password = "qv3eL3^16"

    # Establishing a connection to the SQL Server
    cnxn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};\
                        SERVER="
        + server
        + ";\
                        DATABASE="
        + database
        + ";\
                        UID="
        + username
        + ";\
                        PWD="
        + password
    )

    # khởi tạo cursor
    cursor = cnxn.cursor()

    # Biến chuyển từ file khác có gọi đến hàm này
    name_jsonfile = jsonfile.strip()
    name_category = category.strip()

    # Đọc dữ liệu từ file JSON
    with open(f"{name_jsonfile}", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Tính tổng số lượng mục trong danh sách dữ liệu
    total_items = len(data)

    # Sử dụng tqdm để tạo thanh progress bar
    with tqdm(total=total_items, desc="Start push DB") as pbar:
        # Xóa toàn bộ dữ liệu của category trước khi chèn dữ liệu mới
        # NẾU NHƯ checkDelete = 0. TỨC LÀ CHỈ XÓA KHI ĐẨY PHIM TỪ SERVER ZUIPHIM
        # SERVER XEMPHIMNGAY HOẶC CÁC SV SAU SẼ KHÔNG XÓA
        if checkDelete == 0:
            cursor.execute("DELETE movies")

        # Lặp qua từng mục trong danh sách dữ liệu và chèn chúng vào bảng
        for item in data:
            if not item["image"].startswith("http"):
                item["image"] = "https://zuiphim.org/" + item["image"]

            # Kiểm tra xem tiêu đề đã tồn tại trong bảng chưa
            cursor.execute("SELECT * FROM movies WHERE title = ?", (item["title"],))
            existing_entry = cursor.fetchone()

            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # streams_url_str = ""
            # if item["server"] == "https://zuiphim.org/":
            #     streams_url_str = ",".join(item["streamsUrl"])
            # else:
            #     streams_url_str = item["streamsUrl"]
            # Nếu tiêu đề chưa tồn tại, thực hiện chèn dữ liệu mới
            if not existing_entry:
                cursor.execute(
                    """
                    INSERT INTO movies (title, country, year, content, category, category_name, link, image, actor, streamsUrl, server, createdAt, createdBy)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
                """,
                    (
                        item["title"],
                        item["country"],
                        item["year"],
                        item["content"],
                        item["category"],
                        item["category_name"],
                        item["link"],
                        item["image"],
                        item["actor"],
                        item["streamsUrl"],
                        item["server"],
                        current_datetime,
                        "commitByBot",
                    ),
                )

            # Cập nhật thanh progress bar
            pbar.update(1)
    print("# Pushed to DB !")
    # Hoàn tất ghi dữ liệu và đóng kết nối
    cnxn.commit()
    # đóng kết nối
    cnxn.close()
    
    

