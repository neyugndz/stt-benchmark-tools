# Báo cáo Benchmark - Smart Meeting

- Thời gian chạy: 2026-06-10 14:55:52
- Audio: 3p_meeting_demo.wav (thời lượng: 243.6s)
- Điều kiện audio: Phòng yên tĩnh (1.1, < 22%)
- Số lượt nói (hệ thống / tham chiếu): 7 / 7
- Số từ khoá kiểm tra (1.5): 0
- Có dữ liệu tóm tắt (4.5): Không

## Tổng quan

- **Đạt**: 8
- **Không đạt**: 11
- **N/A / Thủ công**: 4

## Nhóm 1 - Nhận dạng giọng nói (Zipformer-streaming, CPU)

| ID | Tiêu chí | Ngưỡng | Giá trị đo | Kết quả | Ưu tiên | Cách đo |
| --- | --- | --- | --- | --- | --- | --- |
| 1.1 | WER - phòng yên tĩnh | < 22% | 32.0% | Không đạt | Cao | jiwer.wer(ref,hyp) sau chuẩn hoá; audio sạch |
| 1.3 | CER - tiếng Việt có dấu | < 13% | 23.7% | Không đạt | Cao | jiwer.cer(ref,hyp) |
| 1.4 | RTF lane STT (realtime) | < 1.0 | 0.19 | Đạt | Rất cao | thời gian xử lý STT / thời lượng audio |
| 1.5 | Nhận dạng thuật ngữ / tên riêng | > 80% | N/A | N/A | TB | Danh sách 50-100 từ họp thường gặp soạn trước |

## Nhóm 2 - Phân tách người nói (diart online, CPU)

| ID | Tiêu chí | Ngưỡng | Giá trị đo | Kết quả | Ưu tiên | Cách đo |
| --- | --- | --- | --- | --- | --- | --- |
| 2.1 | DER tổng | < 22% | 70.9% | Không đạt | Rất cao | pyannote.metrics DiarizationErrorRate(ref_rttm, hyp_rttm) |
| 2.2 | Speaker confusion | < 12% | 37.0% | Không đạt | Rất cao | Thành phần confusion của DER |
| 2.3 | Sai số số người nói | \|Δ\| ≤ 1 | 0.00 | Đạt | Cao | \|num_detected - num_true\| |
| 2.4 | P/R biên giới lượt (±0.5s) | P > 0.80 / R > 0.75 | P=0.0% / R=0.0% | Không đạt | Cao | So hyp_rttm với ref_rttm, dung sai 0.5s |
| 2.5 | RTF diarization (CPU) | < 1.5 | 0.14 | Đạt | Cao | thời gian xử lý diart / thời lượng audio |
| 2.6 | So sánh preset (A/B) | chọn min DER | N/A | Thủ công / định tính | TB | Lặp DIART_PRESET ∈ {ami, voxconverse, dihard}; cần chạy nhiều lần |

## Nhóm 3 - Gán người nói theo overlap

| ID | Tiêu chí | Ngưỡng | Giá trị đo | Kết quả | Ưu tiên | Cách đo |
| --- | --- | --- | --- | --- | --- | --- |
| 3.1 | TER - tỉ lệ lượt gán sai người | < 15% | 71.4% | Không đạt | Rất cao | Khớp lượt hyp↔ref theo thời gian, đếm % sai nhãn speaker |
| 3.2 | Độ chính xác biên lượt STT | < 0.5s lệch TB | 17.09s | Không đạt | TB | So start/end lượt STT với mốc tiếng nói thật |
| 3.3 | Nhất quán đánh số người nói | 100% | 54.7% | Không đạt | Cao | Cùng 1 người → cùng 'Người nói N' suốt phiên (first-appearance) |

## Nhóm 4 - Hệ thống đầu cuối (end-to-end)

| ID | Tiêu chí | Ngưỡng | Giá trị đo | Kết quả | Ưu tiên | Cách đo |
| --- | --- | --- | --- | --- | --- | --- |
| 4.1 | WER toàn phiên (nội dung DOCX) | < 27% | 32.0% | Không đạt | Rất cao | So bản ghi tay toàn phiên với text trong DOCX |
| 4.2 | TER trong DOCX | < 15% | 71.4% | Không đạt | Rất cao | Đối chiếu nhãn người nói trong DOCX với nhãn chuẩn |
| 4.3 | RTF end-to-end (warm) | < 1.5 | 0.58 | Đạt | Rất cao | Từ bắt đầu xử lý đến xuất DOCX / thời lượng audio |
| 4.4 | Ổn định phiên dài > 2h | Không crash, RAM ổn định | N/A | Thủ công / định tính | Rất cao | 5 file x 30 phút cùng 1 session; theo dõi RAM |
| 4.5 | Chất lượng tóm tắt (Qwen) | Đạt theo rubric / ROUGE-L cao | N/A | N/A | TB | Chấm người hoặc ROUGE-L với bản tóm tắt mẫu |

## Nhóm 5 - Hiệu năng & độ trễ

| ID | Tiêu chí | Ngưỡng | Giá trị đo | Kết quả | Ưu tiên | Cách đo |
| --- | --- | --- | --- | --- | --- | --- |
| 5.1 | RTF STT (lane 1) | < 1.0 | 0.19 | Đạt | Rất cao | time.perf_counter quanh vòng decode |
| 5.2 | RTF diart (lane 2) | < 1.5 | 0.14 | Đạt | Cao | Đo riêng thread feeder; theo dõi backlog drain |
| 5.3 | Thời gian hoàn thiện | < 0.3x audio | 0.00 | Đạt | Cao | drain + gán overlap + khôi phục dấu câu |
| 5.4 | Thời gian tóm tắt (Qwen NPU) | < 60s / phiên | 61.51s | Không đạt | TB | Đo wall-clock gọi Nexa |
| 5.5 | Xuất DOCX | < 5s | 0.10s | Đạt | TB | Đo wall-clock export |

## Giá trị đo thô (raw metrics)

```json
{
  "wer": 0.3196902654867257,
  "cer": 0.23721048612878595,
  "keyword_recognition": null,
  "der": 0.7088034188034189,
  "speaker_confusion": 0.36977207977207976,
  "missed_detection": 0.3390313390313391,
  "false_alarm": 0.0,
  "ref_speaker_count": 3,
  "hyp_speaker_count": 3,
  "speaker_count_diff": 0,
  "boundary_precision": 0.0,
  "boundary_recall": 0.0,
  "ter": 0.7142857142857143,
  "turn_boundary_deviation": 17.092000000000002,
  "speaker_numbering_consistency": 0.5467241379310345,
  "rtf_stt": 0.1884035303776683,
  "rtf_diarization": 0.13886453201970442,
  "rtf_e2e": 0.5805615763546798,
  "finalize_ratio": 0.0003899835796387521,
  "summary_time": 61.5075,
  "docx_export_time": 0.0998,
  "rouge_l": null
}
```

## Transcript đã dùng

### Hệ thống (Hypothesis)

```
[5.45 --> 41.01] Người nói 1: Các đồng chí, hôm nay chúng ta sẽ tổ chức cuộc họp khẩn Để trực ra ứng phó sự tấn công mạng hòa dữ liệu tại trung tâm dữ liệu tỉnh a. Như các đồng chí đã biết, Xảy ra vào ngày 26 tháng 5, 2026, vừa qua là sự cố an ninh mạng Nghiêm trọng nhất trong hai năm qua của chúng ta và một dữ liệu trên 5 máy chủ bao gồm Cơ sở vữ liệu hộ tịch, đăng ký kinh doanh, file server và backup nợ bộ đã bị mạo hóa. Các bạn hãy đăng ký kênh để ủng hộ kênh của chúng mình nhé. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Đảm bảo phục các thực vụ công trực tuyến phục vụ người dân và doanh nghiệp. Đồng trí tuấn và các tinh hình
[41.49 --> 82.80] Người nói 2: Cụ thể báo cáo phó cấp trưởng qua phân tích ban đầu chúng tôi phát hiện đối tượng đã Cảm ơn các bạn đã theo dõi. Máy chủ do chưa được cập nhật. Sau khi xâm nhập, đối tượng đã chiếm quyền admin. Và triển khai mái đập biến thể dốc bit sử dụng Thuật toán aes 256 kết hợp với rsa. Về hướng xử lý, tôi xin lề xuất 4 điểm. Đầu tiên, tiến hành khôi phục dữ liệu bản backup offline ngày 24-5-2014. Thứ hai, thực hiện phân tích trên sơn mã độc. Thứ ba, tri vết nguồn tấn công thông qua nốt vpn tại nga, ukraine và hà lan. Thứ ba, thực hiện phân tích trên sơn mã độc. Thứ ba, tri vết nguồn tấn công thông qua nốt vpn tại nga, ukraine và hà lan. Thứ ba, thực hiện phân tích trên sơn mã độc. Thứ ba, tri vết nguồn tấn công thông qua nốt vpn tại nga, ukraine và hà lan. Thứ ba, thực hiện phân tích trên sơn mã độc. Thứ ba, tri vết nguồn tấn công thông qua nốt vpn tại nga, ukraine và hà lan. Thứ ba, thực hiện phân t Giả soát tầm bộ 156 máy chủ còn lại và cập nhật ngay bản
[82.80 --> 122.94] Người nói 3: Bảo mật báo cáo lãnh đạo và trưởng phòng về chi tiết kỹ thuật tôi đã thực hiện cô lập toàn bộ cụ máy chủ bị ảnh hưởng và Đối với mạng phần lý đồng thời tôi đã thu thập bảo quản mẫu mã độc Dữ liệu nhật ký hệ thống để phục vụ công tác điều tra hiện tại cũng đã qua toàn bộ hệ thống mạng Xác định phạm vi lây nhiễm tôi xin ký nghĩ 3 việc một là lập tức gửi mẫu mã độc cho đối tác quốc tế qua dự án no more ransom để Tìm công cụ giải mã hay là phân tích toàn bộ nhật ký file Ấn là ids/ips trong 30 ngày trước khi xảy ra sự cố. 3. Cần tăng tần suất backup lên hàng ngày và bổ sung ngay một bản backup offline
[123.40 --> 164.48] Người nói 1: Nhất trí, bây giờ tôi sẽ phân công nhiệm vụ cụ thể. Đồng chí thợ tá hoàng anh tuấn nhận nhiệm vụ. Thứ nhất, đồng chí chủ trì với hợp vật trung tâm dữ liệu thực nha. Khẩn trương khôi phục dữ liệu từ bàn backup offline, được các dịch vụ công trở lại hoạt động. Thời hạn hoàn thành là trước 17h ngày 31 tháng 5 năm 2026. Thứ hai, đồng chí triển khai tổ chức điều tra, truy vết nguồn gất tổng công. Phối hợp với interpol và các đầu tác quốc tế. Đồng chí bắt đầu trưởng khai từ ngày mai 29 tháng 5 Thông tin trong năm 2026 và phải bảo cao tiến độ định kỳ vào thời gian hoàn toàn cho tôi thứ ba là sót tầm hộ hệ thống Hồng nhật bản vá cho lỗ hồng cve 2026-1234 Và báo cáo kết quả về văn phòng. Thời hạn hoàn thành là trước 17h ngày 30 tháng 5 năm 2026.
[164.60 --> 203.60] Người nói 2: Đồng chí có ý kiến hay không? Vâng, các anh ạ, tôi xin tiếp thu và thực hiện Theo đúng chỉ đạo trên cơ sở nhà vụ lực giao tôi phân công đồng chí thiếu tá lê thị hồng phụ trách 3 đồ việc cụ thể 1. Phân tích chuyên sâu ma đọc, xác định chủng loại ransomware. Sau đó, cử mẫu cho đối tác hạ hoàn thành là 10. Ngày 31 tháng 5 năm 2026 hay là Kiểm tra toàn bộ 156 máy chủ còn lại trong mạng của tỉnh a. Để đảm bảo không có bách đo tồn tại. Lập báo cáo chính tiết cho tôi trước 17h ngày 2 tháng 6 3. Đồng chí phụ trách xây dựng quy trình Ứng phó sự cố đăng ninh mạng, irp chuẩn và trình bánh
[203.60 --> 223.80] Người nói 3: Lãnh đạo phê diệt trước ngày 15 tháng 6 năm 2016 rõ báo cáo lãnh đạo và trưởng phòng tôi đã nắm chắc 3 đồ việc được giao về phân Giá soát backdoor trên 156 máy chủ của tỉnh a và xây dựng quy trình irp chuẩn. Tôi xin cam kết sẽ hoàn thành nhập toàn bộ nhiệm vụ nghiêm lạc theo đúng các mốc thời hạn trước ngày 31 tháng 5, ngày 2 tháng 6 và ngày 15 tháng 6 năm 2020.
[223.80 --> 238.51] Người nói 1: Tốt, cuộc họp hôm nay các ý kế đã được thảo luận rất thẳng mất toàn điện. Tôi yêu cầu đồng chí hoàng anh tuấn và đồng chí lê thị hồng nghiêm túc chuyển khai các nhiệm vụ đưa đồ giao và có kết quả đúng thời hạn. Học kết thúc vào hồi 17h30. Mời các đồng chí nghỉ.
```

### Tham chiếu (Reference)

```
[
  {
    "start": 0,
    "end": 42.2,
    "speaker": "Người nói 1",
    "text": "Chào các đồng chí. Hôm nay chúng ta sẽ tổ chức cuộc họp khẩn để triển khai ứng phó sự cố tấn công mã hóa dữ liệu tại trung tâm dữ liệu tỉnh A. Như các đồng chí đã biết, sự cố xảy ra vào ngày 26 tháng 5 2026 vừa qua là sự cố an ninh mạng nghiêm trọng nhất trong hai năm qua của chúng ta. Toàn bộ dữ liệu trên năm máy chủ bao gồm cơ sở dữ liệu hộ tịch, đất đai, đăng ký kinh doanh, file server và backup nội bộ đã bị mã hóa với dung lượng lên tới 2,5 TB. Tôi yêu cầu các đồng chí tập trung cao độ, phối hợp chặt chẽ để ứng phó, khắc phục sự cố trong thời gian sớm nhất nhằm đảm bảo khôi phục các dịch vụ công trực tuyến phục vụ người dân và doanh nghiệp. Đồng chí Tuấn báo cáo tình hình cụ thể."
  },
  {
    "start": 42.2,
    "end": 115.5,
    "speaker": "Người nói 2",
    "text": "Báo cáo Phó cục trưởng, qua phân tích ban đầu chúng tôi phát hiện đối tượng đã khai thác lỗ hổng CVE-2026-1234 trên phần mềm quản lý máy chủ do chưa được cập nhật. Sau khi xâm nhập, đối tượng đã chiếm quyền admin và triển khai mã độc biến thể LockBit sử dụng thuật toán AES-256 kết hợp với RSA. Về hướng xử lý, tôi xin đề xuất bốn điểm. Đầu tiên, tiến hành khôi phục dữ liệu bản backup offline ngày 24 tháng 5 2026. Thứ hai, thực hiện phân tích chuyên sâu mã độc. Thứ ba, truy vết nguồn tấn công thông qua nốt VPN tại Nga, Ukraine và Hà Lan. Thứ tư, rà soát toàn bộ 156 máy chủ còn lại và cập nhật ngay bản vá bảo mật."
  },
  {
    "start": 115.5,
    "end": 153.2,
    "speaker": "Người nói 3",
    "text": "Báo cáo lãnh đạo và trưởng phòng, về chi tiết kỹ thuật tôi đã thực hiện cô lập toàn bộ cụm máy chủ bị ảnh hưởng và ngắt kết nối mạng vật lý. Đồng thời tôi đã thu thập, bảo quản mẫu mã độc và dữ liệu nhật ký hệ thống để phục vụ công tác điều tra. Hiện tại cũng đã quét toàn bộ hệ thống mạng để xác định phạm vi lây nhiễm. Tôi xin kiến nghị ba việc: một là lập tức gửi mẫu mã độc cho đối tác quốc tế qua dự án No More Ransom để tìm công cụ giải mã; hai là phân tích toàn bộ nhật ký firewall, IDS, IPS trong 30 ngày trước khi xảy ra sự cố; ba là cần tăng tần suất backup lên hằng ngày và bổ sung ngay một bản backup offline lưu tại điểm thứ ba."
  },
  {
    "start": 153.2,
    "end": 230.5,
    "speaker": "Người nói 1",
    "text": "Nhất trí. Bây giờ tôi sẽ phân công nhiệm vụ cụ thể. Đồng chí Thượng tá Hoàng Anh Tuấn nhận nhiệm vụ. Thứ nhất, đồng chí chủ trì phối hợp với Trung tâm dữ liệu tỉnh A khẩn trương khôi phục dữ liệu từ bản backup offline, đưa các dịch vụ công trở lại hoạt động. Thời hạn hoàn thành là trước 17 giờ ngày 31 tháng 5 năm 2026. Thứ hai, đồng chí triển khai tổ chức điều tra, truy vết nguồn gốc tấn công, phối hợp với Interpol và các đối tác quốc tế. Đồng chí bắt đầu triển khai từ ngày mai 29 tháng 5 năm 2026 và phải báo cáo tiến độ định kỳ vào thứ Sáu hằng tuần cho tôi. Thứ ba, rà soát toàn bộ hệ thống, cập nhật bản vá cho lỗ hổng CVE-2026-1234 và báo cáo kết quả về văn phòng. Thời hạn hoàn thành là trước 17 giờ ngày 30 tháng 5 năm 2026. Đồng chí có ý kiến gì không?"
  },
  {
    "start": 230.5,
    "end": 305.2,
    "speaker": "Người nói 2",
    "text": "Vâng, thưa lãnh đạo, tôi xin tiếp thu và thực hiện theo đúng chỉ đạo. Trên cơ sở nhiệm vụ được giao, tôi phân công đồng chí Thiếu tá Lê Thị Hồng phụ trách ba đầu việc cụ thể. Một, phân tích chuyên sâu mã độc, xác định chủng loại ransomware và khả năng giải mã, sau đó gửi mẫu cho đối tác, thời hạn hoàn thành là 17 giờ ngày 31 tháng 5 năm 2026. Hai là kiểm tra toàn bộ 156 máy chủ còn lại trong mạng của tỉnh A để đảm bảo không có backdoor tồn tại, lập báo cáo chi tiết cho tôi trước 17 giờ ngày mùng 2 tháng 6 năm 2026. Ba là đồng chí phụ trách xây dựng quy trình ứng phó sự cố an ninh mạng IRP chuẩn và trình lãnh đạo phê duyệt trước ngày 15 tháng 6 năm 2026."
  },
  {
    "start": 305.2,
    "end": 332,
    "speaker": "Người nói 3",
    "text": "Rõ. Báo cáo lãnh đạo và trưởng phòng, tôi đã nắm chắc ba đầu việc được giao về phân tích mẫu mã độc, rà soát backdoor trên 156 máy chủ của tỉnh A và xây dựng quy trình IRP chuẩn. Tôi xin cam kết sẽ hoàn thành toàn bộ nhiệm vụ nghiêm ngặt theo đúng các mốc thời hạn trước ngày 31 tháng 5, ngày mùng 2 tháng 6 và ngày 15 tháng 6 năm 2026 như chỉ đạo."
  },
  {
    "start": 332,
    "end": 351,
    "speaker": "Người nói 1",
    "text": "Tốt. Cuộc họp hôm nay các ý kiến đã được thảo luận rất thẳng thắn và toàn diện. Tôi yêu cầu đồng chí Hoàng Anh Tuấn và đồng chí Lê Thị Hồng nghiêm túc triển khai các nhiệm vụ đã được giao, báo cáo kết quả đúng thời hạn. Cuộc họp kết thúc vào hồi 17 giờ 30 phút. Mời các đồng chí nghỉ."
  }
]
```
