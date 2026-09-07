# Spotify Analytics Studio – Dashboard Phân Tích Dữ Liệu Âm Nhạc

Dự án cuối khóa phân tích dữ liệu Spotify: một trang **dashboard trực quan** giúp xem, tìm kiếm, lọc và thống kê hàng loạt khía cạnh của một bộ dữ liệu bài hát (thể loại, nghệ sĩ, quốc gia, hãng đĩa, lượt nghe, độ phổ biến...), kèm theo một **máy chủ web (backend)** cung cấp dữ liệu cho dashboard.



## 1. Dự án này dùng để làm gì?

Dự án gồm 2 phần:

1. **Xử lý dữ liệu (backend – viết bằng Python):** đọc file dữ liệu bài hát Spotify (định dạng CSV - đã upload lên git hub), sau đó tính toán, lọc, sắp xếp theo nhiều tiêu chí khác nhau.
2. **Giao diện (dashboard – file `dashboard.html`):** hiển thị các con số đó dưới dạng biểu đồ, bản đồ thế giới, bảng số liệu... để người dùng xem và hiểu được dữ liệu một cách trực quan.



## 2. Các tính năng chính

Dashboard được chia thành nhiều khu vực chức năng:

- **Tổng quan** – Thống kê sơ bộ, giúp user tiếp xúc với các dữ liệu tổng quát nhất.
- **Tìm kiếm** – tìm theo mã bài hát (track ID) hoặc theo tên bài hát.
- **Lọc dữ liệu** – lọc kết hợp theo thể loại, nghệ sĩ, năm phát hành, hãng đĩa, quốc gia, độ ồn (loudness) — có thể chọn nhiều tiêu chí cùng lúc.
- **Quản lý bài hát** – thêm bài hát mới vào hệ thống hoặc xóa bài hát đã có (mã bài hát được tự sinh tự động).
- **Xếp hạng & thống kê:**
  - Top bài hát có lượt nghe (stream) cao nhất / thấp nhất.
  - Top bài hát phổ biến nhất.
  - Tổng lượt nghe theo từng thể loại nhạc, xếp hạng.
  - Tổng lượt nghe theo từng năm.
  - Độ phổ biến trung bình theo thể loại, tự động phân loại thành "Rất phổ biến / Phổ biến / Ít phổ biến".
  - Số lượng bài hát phát hành theo từng quý trong năm.
- **Phân tích chuyên sâu Hãng đĩa (Label)** – số bài hát, tổng lượt nghe, và số nghệ sĩ ký hợp đồng với mỗi hãng đĩa (dùng để đánh giá độ uy tín của hãng).
- **Phân tích Bản đồ Quốc gia** – thống kê số bài hát và lượt nghe theo từng quốc gia, hiển thị trực quan trên bản đồ thế giới.



## 3. Cấu trúc các file trong dự án

| File | Vai trò |
|---|---|
| `main.py` | "Trung tâm điều phối" – khởi chạy máy chủ web, tiếp nhận mọi yêu cầu từ dashboard và gọi đúng chức năng xử lý tương ứng. |
| `data_processing.py` | Xử lý các thao tác **tìm kiếm & lọc** dữ liệu (theo thể loại, nghệ sĩ, năm, hãng đĩa, quốc gia, độ ồn, mã bài hát, tên bài hát). |
| `data_handle.py` | Xử lý các thao tác **thêm/xóa bài hát** và các **thống kê, xếp hạng** (top lượt nghe, độ phổ biến, theo quý, theo quốc gia...). |
| `data_ultilize.py` | Xử lý các **phân tích chuyên sâu về hãng đĩa** (số bài hát, tổng lượt nghe, số nghệ sĩ theo từng hãng). |
| `dashboard.html` | Giao diện dashboard hiển thị toàn bộ biểu đồ, bảng số liệu, bản đồ mà người dùng nhìn thấy và thao tác. |

> Có thể hình dung: `dashboard.html` là "mặt tiền cửa hàng", còn 3 file Python còn lại (`data_processing.py`, `data_handle.py`, `data_ultilize.py`) là "kho hàng phía sau", và `main.py` là "nhân viên thu ngân" đứng giữa, nhận yêu cầu từ khách rồi lấy đúng hàng từ đúng kho.



## 4. Dữ liệu đầu vào

Dự án sử dụng một file dữ liệu bài hát Spotify ở định dạng **CSV** (`spotify_data_processed.csv`), với các thông tin cho mỗi bài hát như: mã bài hát, tên bài hát, nghệ sĩ, thể loại, quốc gia, hãng đĩa, ngày phát hành, độ ồn, độ phổ biến, số lượt nghe (stream count)...

> **Điểm nổi bật về đường dẫn (Dynamic Path):** Hệ thống đã được nâng cấp sử dụng **đường dẫn động tự động** (`BASE_DIR = os.path.dirname(os.path.abspath(__file__))`). Dữ liệu được xác định tự động ngay trong thư mục dự án, cho phép bạn sao chép toàn bộ thư mục sang bất kỳ máy tính nào (ổ C, D, Linux hay macOS) là có thể chạy được ngay mà **không cần phải sửa lại đường dẫn thủ công**. Mọi thao tác thêm/xóa bài hát cũng tự động cập nhật đồng bộ vào đúng file này.



## 5. Yêu cầu để chạy được dự án

Máy tính cần cài sẵn:

- **Python** (ngôn ngữ lập trình dùng để chạy phần "bộ não xử lý dữ liệu").
- Các thư viện Python: `pandas`, `flask`, `flask-cors`, `flask-compress`.

Cài đặt nhanh bằng lệnh:

```bash
pip install pandas flask flask-cors flask-compress
```



## 6. Cách chạy dự án

1. Đặt file dữ liệu `spotify_data_processed.csv` chung thư mục với `main.py` (hệ thống tự nhận diện).
2. Mở terminal (cửa sổ dòng lệnh) tại thư mục dự án (hoặc mở trực tiếp bằng IDE như VS Code / Antigravity).
3. Chạy lệnh:

   ```bash
   python main.py
   ```
4. Khi thấy máy chủ khởi động thành công, mở trình duyệt web và truy cập:

   ```
   http://localhost:8888
   ```

5. Dashboard sẽ hiển thị trực quan, bạn có thể bắt đầu xem, tìm kiếm, lọc, phân tích nhãn đĩa, bản đồ thế giới và quản lý bài hát.

6. **Chia sẻ ra bên ngoài (Tùy chọn):** Để người khác từ xa có thể xem dashboard của bạn, có thể public qua công cụ tunnel như ngrok:

   ```bash
   ngrok http 8888
   ```

   
## 7. Danh sách các "cửa ngõ" dữ liệu (API) cho ai muốn tìm hiểu sâu hơn

Đây là các endpoint API mà dashboard gọi tới để lấy dữ liệu:

| Đường dẫn | Chức năng |
|---|---|
| `/api/all` | Lấy toàn bộ dữ liệu, có phân trang |
| `/api/summary` | Lấy danh sách bài hát rút gọn |
| `/api/filter` | Lọc theo nhiều tiêu chí (thể loại, nghệ sĩ, năm, hãng đĩa, quốc gia, độ ồn) |
| `/api/search` | Tìm theo mã bài hát hoặc tên bài hát |
| `/api/suggest` | Gợi ý bài hát tự động (Autocomplete) |
| `/api/new` | Thêm bài hát mới vào hệ thống |
| `/api/remove` | Xóa bài hát theo ID hoặc tên bài hát |
| `/api/streamcount` | Top bài hát có lượt nghe cao/thấp nhất |
| `/api/popular` | Top bài hát phổ biến nhất |
| `/api/genrecountcrank` | Xếp hạng tổng lượt nghe theo thể loại |
| `/api/yearcountrank` | Tổng lượt nghe theo năm phát hành |
| `/api/poprank` | Độ phổ biến trung bình theo thể loại + phân loại cấp bậc |
| `/api/quarterrank` | Số bài hát phát hành theo từng quý trong năm |
| `/api/label1`, `/api/label2`, `/api/label3` | Thống kê hãng đĩa: số bài hát / tổng lượt nghe / số nghệ sĩ |
| `/api/labeldetails` | **Hồ sơ chuyên sâu nhãn đĩa:** KPIs, top nghệ sĩ, thể loại, hit tracks, quốc gia và xu hướng phát hành |
| `/api/countrystats` | Thống kê số bài hát và lượt nghe tổng hợp theo quốc gia (cho bản đồ nhiệt) |
| `/api/countrydetails` | **Phân tích chuyên sâu quốc gia:** KPIs, top nghệ sĩ, album, thể loại và xu hướng năm |



## 8. Một số điểm cần lưu ý / hướng cải thiện trong tương lai

- **Đường dẫn động (Đã hoàn thành):** Đã chuẩn hóa toàn bộ đường dẫn thành động (`BASE_DIR` + `os.path.join`), đảm bảo tính linh hoạt 100% khi di chuyển mã nguồn giữa các môi trường khác nhau.
- **Lưu trữ dữ liệu:** Thao tác thêm/xóa bài hát hiện lưu trực tiếp vào file CSV gốc. Trong tương lai có thể nâng cấp sang cơ sở dữ liệu như SQLite hoặc PostgreSQL để tăng tốc độ truy vấn đồng thời.
- **Mở rộng tính năng:** Có thể bổ sung thêm các thuật toán gợi ý nhạc tương đồng (Content-Based Recommendation), phân tích âm hưởng nâng cao (Energy, Danceability, Valence).
