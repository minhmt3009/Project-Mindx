# 🎧 Spotify Analytics Studio – Dashboard Phân Tích Dữ Liệu Âm Nhạc

Dự án cuối khóa phân tích dữ liệu Spotify: một trang **dashboard trực quan** giúp xem, tìm kiếm, lọc và thống kê hàng loạt khía cạnh của một bộ dữ liệu bài hát (thể loại, nghệ sĩ, quốc gia, hãng đĩa, lượt nghe, độ phổ biến...), kèm theo một **máy chủ web (backend)** cung cấp dữ liệu cho dashboard.

---

## 1. Dự án này dùng để làm gì?

Nói đơn giản, dự án gồm 2 phần:

1. **Bộ não xử lý dữ liệu (backend – viết bằng Python):** đọc file dữ liệu bài hát Spotify (định dạng CSV), sau đó tính toán, lọc, sắp xếp theo nhiều tiêu chí khác nhau.
2. **Giao diện xem trực quan (dashboard – file `dashboard.html`):** hiển thị các con số đó dưới dạng biểu đồ, bản đồ thế giới, bảng số liệu... để người dùng không cần biết code vẫn xem và hiểu được dữ liệu.

Nói cách khác: bạn mở dashboard lên trên trình duyệt, mọi thao tác tìm kiếm/lọc/thống kê bạn thấy trên màn hình đều được "hậu trường" xử lý bởi các file Python.

---

## 2. Các tính năng chính

Dashboard được chia thành nhiều khu vực chức năng:

- **📊 Tổng quan Thư viện Spotify** – xem toàn bộ danh sách bài hát, phân trang để không bị quá tải.
- **🔍 Tìm kiếm bài hát thông minh** – tìm theo mã bài hát (track ID) hoặc theo tên bài hát.
- **🎛️ Lọc dữ liệu đa tiêu chí thông minh** – lọc kết hợp theo thể loại, nghệ sĩ, năm phát hành, hãng đĩa, quốc gia, độ ồn (loudness) — có thể chọn nhiều tiêu chí cùng lúc.
- **⚙️ Quản lý kho dữ liệu bài hát** – thêm bài hát mới vào hệ thống hoặc xóa bài hát đã có (mã bài hát được tự sinh tự động).
- **📈 Xếp hạng & thống kê:**
  - Top bài hát có lượt nghe (stream) cao nhất / thấp nhất.
  - Top bài hát phổ biến nhất.
  - Tổng lượt nghe theo từng thể loại nhạc, xếp hạng.
  - Tổng lượt nghe theo từng năm.
  - Độ phổ biến trung bình theo thể loại, tự động phân loại thành "Rất phổ biến / Phổ biến / Ít phổ biến".
  - Số lượng bài hát phát hành theo từng quý trong năm.
- **🏷️ Phân tích chuyên sâu Hãng đĩa (Label)** – số bài hát, tổng lượt nghe, và số nghệ sĩ ký hợp đồng với mỗi hãng đĩa (dùng để đánh giá độ uy tín của hãng).
- **🌍 Phân tích Bản đồ Quốc gia** – thống kê số bài hát và lượt nghe theo từng quốc gia, hiển thị trực quan trên bản đồ thế giới.

---

## 3. Cấu trúc các file trong dự án

| File | Vai trò |
|---|---|
| `main.py` | "Trung tâm điều phối" – khởi chạy máy chủ web, tiếp nhận mọi yêu cầu từ dashboard và gọi đúng chức năng xử lý tương ứng. |
| `data_processing.py` | Xử lý các thao tác **tìm kiếm & lọc** dữ liệu (theo thể loại, nghệ sĩ, năm, hãng đĩa, quốc gia, độ ồn, mã bài hát, tên bài hát). |
| `data_handle.py` | Xử lý các thao tác **thêm/xóa bài hát** và các **thống kê, xếp hạng** (top lượt nghe, độ phổ biến, theo quý, theo quốc gia...). |
| `data_ultilize.py` | Xử lý các **phân tích chuyên sâu về hãng đĩa** (số bài hát, tổng lượt nghe, số nghệ sĩ theo từng hãng). |
| `dashboard.html` | Giao diện dashboard hiển thị toàn bộ biểu đồ, bảng số liệu, bản đồ mà người dùng nhìn thấy và thao tác. |

> Có thể hình dung: `dashboard.html` là "mặt tiền cửa hàng", còn 3 file Python còn lại (`data_processing.py`, `data_handle.py`, `data_ultilize.py`) là "kho hàng phía sau", và `main.py` là "nhân viên thu ngân" đứng giữa, nhận yêu cầu từ khách rồi lấy đúng hàng từ đúng kho.

---

## 4. Dữ liệu đầu vào

Dự án sử dụng một file dữ liệu bài hát Spotify ở định dạng **CSV** (`spotify_data_processed.csv`), với các thông tin cho mỗi bài hát như: mã bài hát, tên bài hát, nghệ sĩ, thể loại, quốc gia, hãng đĩa, ngày phát hành, độ ồn, độ phổ biến, số lượt nghe (stream count)...

> ⚠️ **Lưu ý:** Hiện tại đường dẫn tới file dữ liệu đang được ghi cố định trong code (ví dụ: `D:\Data Science\Project cuối khóa 1 Mindx\spotify_data_processed.csv`). Nếu chạy trên máy khác, cần đổi đường dẫn này cho khớp với vị trí lưu file CSV trên máy đó.

---

## 5. Yêu cầu để chạy được dự án

Máy tính cần cài sẵn:

- **Python** (ngôn ngữ lập trình dùng để chạy phần "bộ não xử lý dữ liệu").
- Các thư viện Python: `pandas`, `flask`, `flask-cors`, `flask-compress`.

Cài đặt nhanh bằng lệnh:

```bash
pip install pandas flask flask-cors flask-compress
```

---

## 6. Cách chạy dự án

1. Đảm bảo file dữ liệu CSV đã có sẵn đúng đường dẫn được khai báo trong các file `.py`.
2. Mở terminal (cửa sổ dòng lệnh) tại thư mục chứa dự án.
3. Chạy lệnh:

   ```bash
   python main.py
   ```

4. Khi thấy máy chủ khởi động thành công, mở trình duyệt web và truy cập:

   ```
   http://localhost:8888
   ```

5. Dashboard sẽ hiện ra, có thể bắt đầu xem, tìm kiếm, lọc và thống kê dữ liệu.

---

## 7. Danh sách các "cửa ngõ" dữ liệu (API) cho ai muốn tìm hiểu sâu hơn

Đây là các đường dẫn mà dashboard gọi tới để lấy dữ liệu (không cần quan tâm nếu chỉ dùng dashboard):

| Đường dẫn | Chức năng |
|---|---|
| `/api/all` | Lấy toàn bộ dữ liệu, có phân trang |
| `/api/summary` | Lấy danh sách bài hát rút gọn |
| `/api/filter` | Lọc theo nhiều tiêu chí (thể loại, nghệ sĩ, năm, hãng, quốc gia, độ ồn) |
| `/api/search` | Tìm theo mã bài hát hoặc tên bài hát |
| `/api/new` | Thêm bài hát mới |
| `/api/remove` | Xóa bài hát |
| `/api/streamcount` | Top bài hát có lượt nghe cao/thấp nhất |
| `/api/popular` | Top bài hát phổ biến nhất |
| `/api/genrecountcrank` | Xếp hạng tổng lượt nghe theo thể loại |
| `/api/yearcountrank` | Tổng lượt nghe theo năm |
| `/api/poprank` | Độ phổ biến trung bình theo thể loại + phân loại |
| `/api/quarterrank` | Số bài hát phát hành theo quý |
| `/api/label1`, `/api/label2`, `/api/label3` | Số bài hát / tổng lượt nghe / số nghệ sĩ theo từng hãng đĩa |
| `/api/countrystats` | Thống kê số bài hát và lượt nghe theo quốc gia |

---

## 8. Một số điểm cần lưu ý / hướng cải thiện trong tương lai

- Đường dẫn tới file CSV hiện đang cố định (hardcode), nên cân nhắc chuyển thành đường dẫn tương đối hoặc đọc từ file cấu hình để dễ chia sẻ dự án cho người khác chạy.
- Dữ liệu bài hát mới thêm/xóa hiện chỉ lưu tạm trong bộ nhớ khi máy chủ đang chạy — khi tắt máy chủ, các thay đổi này có thể chưa được lưu lại vào file CSV gốc.
- Có thể mở rộng thêm các thống kê khác (ví dụ theo mùa phát hành nhạc, theo mối liên hệ giữa độ ồn và độ phổ biến...) trong tương lai.

---

*Dự án được thực hiện trong khuôn khổ Project cuối khóa Data Science.*
