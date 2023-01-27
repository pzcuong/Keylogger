# IE105.N14.CNCL.1 - Nhóm 1
#### [](https://github.com/pzcuong/QuanLyHocSinh/tree/master#ph%E1%BA%A7n-m%E1%BB%81m-qu%E1%BA%A3n-l%C3%BD-h%E1%BB%8Dc-sinh)*Script: Keylogger
[![Build Status](https://camo.githubusercontent.com/c29bc856325cd819f5a3bb6536b7982f04a161e656de066c4c970e0079c14ff5/68747470733a2f2f7472617669732d63692e6f72672f6a6f656d6363616e6e2f64696c6c696e6765722e7376673f6272616e63683d6d6173746572)](https://travis-ci.org/joemccann/dillinger)

## [](https://github.com/pzcuong/QuanLyHocSinh/tree/master#gi%E1%BB%9Bi-thi%E1%BB%87u)Giới thiệu

Keylogger hay "trình theo dõi thao tác bàn phím" theo cách dịch ra tiếng Việt là một chương trình máy tính ban đầu được viết nhằm mục đích theo dõi và ghi lại mọi thao tác thực hiện trên bàn phím vào một tập tin nhật ký (log) để cho người cài đặt nó sử dụng. Vì chức năng mang tính vi phạm vào riêng tư của người khác này nên các trình keylogger được xếp vào nhóm các phần mềm gián điệp.

Về sau, khi keylogger phát triển cao hơn nó không những ghi lại thao tác bàn phím mà còn ghi lại cả các hình ảnh hiển thị trên màn hình (screen) bằng cách chụp (screen-shot) hoặc quay phim (screen-capture) thậm chí còn ghi nhận cách con trỏ chuột trên máy tính di chuyển.

## [](https://github.com/pzcuong/QuanLyHocSinh/tree/master#t%C3%ADnh-n%C4%83ng)Tính năng

- [x] Hỗ trợ trên cả 2 nền tảng: macOS và Windows
- [x] Không bị các trình diệt virus phát hiện (ví dụ: Windows Security)
- [x] Theo dõi bàn phím
- [x] Theo dõi clipboard
- [x] Tự động gom từ khi có tín hiệu "enter"
- [x] Theo dõi chuột
- [x] Theo dõi màn hình
- [x] Gửi thông tin về server  
- [x] Tự động tải và cài đặt thư viện còn thiếu để chạy script
- [ ] Ẩn ứng dụng chạy ngầm

## [](https://github.com/pzcuong/QuanLyHocSinh/tree/master#c%C3%B4ng-ngh%E1%BB%87-s%E1%BB%AD-d%E1%BB%A5ng)Công nghệ sử dụng

-   [Python] - Xử lý API, Back-end, theo dõi
-   [Quarzt] - Thư viện hỗ trợ theo dõi thông tin trên macOS
-   [win32gui] - Thư viện hỗ trợ theo dõi thông tin trên Windows

## [](https://github.com/pzcuong/QuanLyHocSinh/tree/master#c%C3%A0i-%C4%91%E1%BA%B7t)Cài đặt

Yêu cầu:  

```
python keylogger.py
```

## [](https://github.com/pzcuong/QuanLyHocSinh/tree/master#license)License

MIT
