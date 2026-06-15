# Báo cáo Benchmark - Smart Meeting

- Thời gian chạy: 2026-06-15 17:35:26
- Audio: 3p_meeting_demo.wav (thời lượng: 243.6s)
- Điều kiện audio: Phòng yên tĩnh (1.1, < 22%)
- Số lượt nói (hệ thống / tham chiếu): 7 / 7
- Số từ khoá kiểm tra (1.5): 0
- Có dữ liệu tóm tắt (4.5): Không

## Tổng quan

- **Đạt**: 14
- **Không đạt**: 4
- **N/A / Thủ công**: 5

## Nhóm 1 - Nhận dạng giọng nói

| ID | Tiêu chí | Ngưỡng | Giá trị đo | Kết quả | Ưu tiên | Cách đo |
| --- | --- | --- | --- | --- | --- | --- |
| 1.1 | WER - phòng yên tĩnh | < 22% | 21.7% | Đạt | Cao | jiwer.wer(ref,hyp) sau chuẩn hoá; audio sạch |
| 1.3 | CER - tiếng Việt có dấu | < 13% | 17.1% | Không đạt | Cao | jiwer.cer(ref,hyp) |
| 1.4 | RTF lane STT (realtime) | < 1.0 | 0.03 | Đạt | Rất cao | thời gian xử lý STT / thời lượng audio |
| 1.5 | Nhận dạng thuật ngữ / tên riêng | > 80% | N/A | N/A | TB | Danh sách 50-100 từ họp thường gặp soạn trước |

## Nhóm 2 - Phân tách người nói 

| ID | Tiêu chí | Ngưỡng | Giá trị đo | Kết quả | Ưu tiên | Cách đo |
| --- | --- | --- | --- | --- | --- | --- |
| 2.1 | DER tổng | < 22% | 9.9% | Đạt | Rất cao | pyannote.metrics DiarizationErrorRate(ref_rttm, hyp_rttm) |
| 2.2 | Speaker confusion | < 12% | 5.9% | Đạt | Rất cao | Thành phần confusion của DER |
| 2.3 | Sai số số người nói | \|Δ\| ≤ 1 | 0.00 | Đạt | Cao | \|num_detected - num_true\| |
| 2.4 | P/R biên giới lượt (±0.5s) | P > 0.80 / R > 0.75 | P=16.7% / R=16.7% | Không đạt | Cao | So hyp_rttm với ref_rttm, dung sai 0.5s |
| 2.5 | RTF diarization (CPU) | < 1.5 | 0.17 | Đạt | Cao | thời gian xử lý diart / thời lượng audio |
| 2.6 | So sánh preset (A/B) | chọn min DER | N/A | Thủ công / định tính | TB | Lặp DIART_PRESET ∈ {ami, voxconverse, dihard}; cần chạy nhiều lần |

## Nhóm 3 - Gán người nói theo overlap

| ID | Tiêu chí | Ngưỡng | Giá trị đo | Kết quả | Ưu tiên | Cách đo |
| --- | --- | --- | --- | --- | --- | --- |
| 3.1 | TER - tỉ lệ lượt gán sai người | < 15% | 0.0% | Đạt | Rất cao | Khớp lượt hyp↔ref theo thời gian, đếm % sai nhãn speaker |
| 3.2 | Độ chính xác biên lượt STT | < 0.5s lệch TB | 2.65s | Không đạt | TB | So start/end lượt STT với mốc tiếng nói thật |
| 3.3 | Nhất quán đánh số người nói | 100% | 92.5% | Không đạt | Cao | Cùng 1 người → cùng 'Người nói N' suốt phiên (first-appearance) |

## Nhóm 4 - Hệ thống đầu cuối (end-to-end)

| ID | Tiêu chí | Ngưỡng | Giá trị đo | Kết quả | Ưu tiên | Cách đo |
| --- | --- | --- | --- | --- | --- | --- |
| 4.1 | WER toàn phiên (nội dung DOCX) | < 27% | 21.7% | Đạt | Rất cao | So bản ghi tay toàn phiên với text trong DOCX |
| 4.2 | TER trong DOCX | < 15% | 0.0% | Đạt | Rất cao | Đối chiếu nhãn người nói trong DOCX với nhãn chuẩn |
| 4.3 | RTF end-to-end (warm) | < 1.5 | 0.19 | Đạt | Rất cao | Từ bắt đầu xử lý đến xuất DOCX / thời lượng audio |
| 4.4 | Ổn định phiên dài > 2h | Không crash, RAM ổn định | N/A | Thủ công / định tính | Rất cao | 5 file x 30 phút cùng 1 session; theo dõi RAM |
| 4.5 | Chất lượng tóm tắt (Qwen) | Đạt theo rubric / ROUGE-L cao | N/A | N/A | TB | Chấm người hoặc ROUGE-L với bản tóm tắt mẫu |

## Nhóm 5 - Hiệu năng & độ trễ

| ID | Tiêu chí | Ngưỡng | Giá trị đo | Kết quả | Ưu tiên | Cách đo |
| --- | --- | --- | --- | --- | --- | --- |
| 5.1 | RTF STT (lane 1) | < 1.0 | 0.03 | Đạt | Rất cao | time.perf_counter quanh vòng decode |
| 5.2 | RTF diart (lane 2) | < 1.5 | 0.17 | Đạt | Cao | Đo riêng thread feeder; theo dõi backlog drain |
| 5.3 | Thời gian hoàn thiện | < 0.3x audio | 0.00 | Đạt | Cao | drain + gán overlap + khôi phục dấu câu |
| 5.4 | Thời gian tóm tắt (Qwen NPU) | < 60s / phiên | N/A | N/A | TB | Đo wall-clock gọi Nexa |
| 5.5 | Xuất DOCX | < 5s | 0.08s | Đạt | TB | Đo wall-clock export |

## Giá trị đo thô (raw metrics)

```json
{
  "wer": 0.2168141592920354,
  "cer": 0.17099236641221374,
  "keyword_recognition": null,
  "der": 0.09940298507462696,
  "speaker_confusion": 0.05889125799573559,
  "missed_detection": 0.02558635394456301,
  "false_alarm": 0.014925373134328358,
  "ref_speaker_count": 3,
  "hyp_speaker_count": 3,
  "speaker_count_diff": 0,
  "boundary_precision": 0.16666666666666666,
  "boundary_recall": 0.16666666666666666,
  "ter": 0.0,
  "turn_boundary_deviation": 2.6514285714285726,
  "speaker_numbering_consistency": 0.9253879310344828,
  "rtf_stt": 0.026565270935960592,
  "rtf_diarization": 0.1661642036124795,
  "rtf_e2e": 0.19472454844006568,
  "finalize_ratio": 0.0016728243021346468,
  "summary_time": null,
  "docx_export_time": 0.0785,
  "rouge_l": null
}
```

## Transcript đã dùng

### Hệ thống (Hypothesis)

```
[5.45 --> 41.01] Người nói 1: Đồng chí hôm nay chúng ta sẽ tổ chức cuộc họp khẩn Để triển khai ứng phó sự tấn công mạng hoàng dữ liệu tại trung tâm dữ liệu tỉnh a như các đồng chí đã biết sự cố Xảy ra vào ngày hai mươi sáu tháng năm hai không hai sáu vừa qua là sự cầu an ninh mạng Nghiêm trọng nhất trong hai năm qua của chúng ta toàn bộ dữ liệu trên năm máy chủ bao gồm Cơ sở dữ liệu hộ tịch đất đai đăng ký kinh doanh file server và backup nội bộ đã bị Hóa với dung lượng lên tới hai phẩy năm têp tôi yêu cầu các đồng chí tập trung Trên cao độ phối hợp chặt chẽ để ứng phó khắc phục sự cố trong thời gian sớm nhất Đảm bảo khôi phục các dịch vụ công trực tuyến trực tuyến phục vụ người dân và doanh nghiệp Đồng chí tuấn và có tình hình cụ thể
[41.49 --> 82.80] Người nói 2: Báo cáo phó cục trưởng có phân tích ban đầu chúng tôi phát hiện đối tượng đã khai thác Phối hợp cv hai nghìn không trăm hai sáu một hai ba bốn trên phần mềm quản lý Máy chủ do chưa được cập nhật sau khi xâm nhập đối tượng đã chiếm quyền atmin Và triển khai mã đọc biến thể dốc bít sử dụng Thuật toán as hai năm sáu kết hợp với r a về hướng xử lý tôi xin đề xuất bốn điểm. Đầu tiên tiến hành khôi phục dữ liệu bản backup offline ngày hai tư tháng năm Thứ sáu thứ hai thực hiện phân tích trên sông mã độc thứ ba truy vết nguồn tấn công thông qua nốt pvn tại nga ukraine và hà lan Rà soát toàn bộ một trăm năm mươi sáu máy chủ còn lại và cập nhật ngay bản thân
[82.80 --> 122.94] Người nói 3: Báo mật báo cáo lãnh đạo và trưởng phòng về chi tiết kỹ thuật tôi đã thực hiện cô lập toàn bộ cụ máy chủ bị ảnh hưởng và ngăn kết quả Nối mạng vật lý đồng thời tôi đã thu thập bảo quản mẫu mã độc và Dữ liệu nhật ký hệ thống để phục vụ công tác điều tra hiện tại cũng đã quét toàn bộ hệ thống mạng để Xác định phạm vi lây nhiễm tôi xin kiến nghị ba việc một là lập tức gửi mẫu mã độc cho đối tác quốc tế qua dự án no more ramson để tìm Công cụ giải mã hai là phân tích toàn bộ nhật ký fire Ids ips trong ba mươi ngày trước khi xảy ra sự cố ba là cần tăng tần suất backup lên hằng ngày và bổ sung ngay một bản backup offline lưu tại điểm
[123.40 --> 164.48] Người nói 1: Thứ ba nhất trí bây giờ tôi sẽ phân công nhiệm vụ cụ thể Đồng chí thượng tá hoàng anh tuấn nhận nhiệm vụ thứ nhất đồng chí chủ trì phối hợp với trung tâm dữ liệu tỉnh a Khẩn trương khôi phục dữ liệu từ bản viết các offline từ các dịch vụ công trở lại hoạt động Thời hạn hoàn thành là trước mười bảy giờ ngày ba mươi mốt tháng năm hai không hai sáu Thứ hai đồng chí triển khai tổ chức điều tra truy vết nguồn gốc tổng công Phối hợp với interpo và các đối tác quốc tế đồng chí bắt đầu triển khai từ ngày mai hai Năm hai không hai sáu và phải báo cáo tiến độ định kỳ và hoàn toàn cho tôi thứ ba rà soát toàn bộ hệ thống Nhật bản báo cho lỗ hổng cv hai không hai sáu một hai ba tư Báo cáo kết quả về văn phòng thời hạn hoàn thành là trước mười bảy giờ ngày ba mươi tháng năm hai không hai sáu
[164.60 --> 203.60] Người nói 2: Đồng chí có ý kiến gì không. Vâng. Thưa lãnh đạo tôi xin tiếp thu và thực hiện Theo đúng chỉ đạo trên cơ sở nhiệm vụ được giao tôi phân công đồng chí thiếu tá lê thị hồng phụ trách ba đầu việc cụ thể Một phân tích chuyên sâu ma độc xác định chủng loại ran sum vầy Và khả năng giải mã sau đó gửi mẫu cho đối tác hạ hoàn thành là một Mười bảy giờ ngày ba mốt tháng năm hai không hai sáu hai là Kiểm tra toàn bộ một trăm năm mươi sáu máy chủ còn lại trong mạng của tỉnh a Để đảm bảo không có bách đo tồn tại lập báo cáo chi tiết cho tôi trước mười bảy giờ ngày mùng hai tháng sáu Sáu năm hai không hai sáu ba là đồng chí phụ trách xây dựng quy trình Để ứng phó sự cố an ninh mạng qr bay chuẩn và trình
[203.60 --> 223.80] Người nói 3: Đã phê duyệt trước ngày mười lăm tháng sáu năm hai không hai sáu rõ báo cáo lãnh đạo và trưởng phòng tôi đã nắm chắc ba đầu việc được giao về phân tích mẫu Mã độc rà soát bác đo trên một trăm năm mươi sáu máy chủ của tỉnh a và xây dựng quy trình iap chuẩn Tôi xin cam kết sẽ hoàn thành nhiệm vụ toàn bộ nhiệm vụ nghiêm ngặt theo đúng các mốc thời hạn trước ngày ba mốt tháng năm ngày mùng hai tháng sáu và ngày mười lăm tháng sáu năm hai không
[223.80 --> 238.51] Người nói 1: Như chỉ đạo tốt cuộc họp hôm nay các ý kiến đã được thảo luận rất thành tâm và toàn diện Tôi yêu cầu đồng chí hoàng anh tuấn và đồng chí lê thị hồng nghiêm túc triển khai các nhiệm vụ được giao báo cáo kết quả đúng thời hạn Học kết thúc vào hồi mười bảy giờ ba mươi phút mời các đồng chí nghỉ ngơi
```

### Tham chiếu (Reference)

```
[5.00 --> 41.50] Người nói 1: Chào các đồng chí. Hôm nay chúng ta sẽ tổ chức cuộc họp khẩn để triển khai ứng phó sự tấn công mã hóa dữ liệu tại Trung tâm dữ liệu tỉnh A. Như các đồng chí đã biết, sự cố xảy ra vào ngày 26 tháng 5 năm 2026 vừa qua là sự cố an ninh mạng nghiêm trọng nhất trong hai năm qua của chúng ta. Toàn bộ dữ liệu trên năm máy chủ bao gồm cơ sở dữ liệu hộ tịch, đất đai, đăng ký kinh doanh, file server và backup nội bộ đã bị mã hóa với dung lượng lên tới 2,5 TB. Tôi yêu cầu các đồng chí tập trung cao độ, phối hợp chặt chẽ để ứng phó, khắc phục sự cố trong thời gian sớm nhất nhằm đảm bảo khôi phục các dịch vụ công trực tuyến phục vụ người dân và doanh nghiệp. Đồng chí Tuấn báo cáo tình hình cụ thể.
[42.00 --> 84.50] Người nói 2: Báo cáo Phó cục trưởng, qua phân tích ban đầu chúng tôi phát hiện đối tượng đã khai thác lỗ hổng CVE-2026-1234 trên phần mềm quản lý máy chủ do chưa được cập nhật. Sau khi xâm nhập đối tượng đã chiếm quyền admin và triển khai mã độc biến thể LockBit sử dụng thuật toán AES-256 kết hợp với RSA. Về hướng xử lý, tôi xin đề xuất bốn điểm. Đầu tiên, tiến hành khôi phục dữ liệu bản backup offline ngày 24 tháng 5 năm 2026. Thứ hai, thực hiện phân tích chuyên sâu mã độc. Thứ ba, truy vết nguồn tấn công thông qua nút VPN tại Nga, Ukraine và Hà Lan. Thứ tư, rà soát toàn bộ 156 máy chủ còn lại và cập nhật ngay bản vá bảo mật.
[85.00 --> 125.00] Người nói 3: Báo cáo lãnh đạo và trưởng phòng, về chi tiết kỹ thuật, tôi đã thực hiện cô lập toàn bộ cụm máy chủ bị ảnh hưởng và ngắt kết nối mạng vật lý. Đồng thời tôi đã thu thập, bảo quản mẫu mã độc và dữ liệu nhật ký hệ thống để phục vụ công tác điều tra. Hiện tại cũng đã quét toàn bộ hệ thống mạng để xác định phạm vi lây nhiễm. Tôi xin kiến nghị ba việc. Một là lập tức gửi mẫu mã độc cho đối tác quốc tế qua dự án No More Ransom để tìm công cụ giải mã. Hai là phân tích toàn bộ nhật ký firewall, IDS, IPS trong 30 ngày trước khi xảy ra sự cố. Ba là cần tăng tần suất backup lên hằng ngày và bổ sung ngay một bản backup offline lưu tại địa điểm thứ ba.
[126.00 --> 170.50] Người nói 1: Nhất trí. Bây giờ tôi sẽ phân công nhiệm vụ cụ thể. Đồng chí Thượng tá Hoàng Anh Tuấn nhận nhiệm vụ. Thứ nhất, đồng chí chủ trì phối hợp với Trung tâm dữ liệu tỉnh A khẩn trương khôi phục dữ liệu từ bản backup offline, đưa các dịch vụ công trở lại hoạt động. Thời hạn hoàn thành là trước 17 giờ ngày 31 tháng 5 năm 2026. Thứ hai, đồng chí triển khai tổ chức điều tra, truy vết nguồn gốc tấn công, phối hợp với Interpol và các đối tác quốc tế. Đồng chí bắt đầu triển khai từ ngày mai 29 tháng 5 năm 2026 và phải báo cáo tiến độ định kỳ vào thứ sáu hằng tuần cho tôi. Thứ ba, rà soát toàn bộ hệ thống, cập nhật bản vá cho lỗ hổng CVE-2026-1234 và báo cáo kết quả về văn phòng. Thời hạn hoàn thành là trước 17 giờ ngày 30 tháng 5 năm 2026. Đồng chí có ý kiến gì không?
[171.00 --> 206.50] Người nói 2: Vâng, thưa lãnh đạo, tôi xin tiếp thu và thực hiện theo đúng chỉ đạo. Trên cơ sở nhiệm vụ được giao, tôi phân công đồng chí Thiếu tá Lê Thị Hồng phụ trách ba đầu việc cụ thể. Một, phân tích chuyên sâu mã độc, xác định chủng loại Ransomware và khả năng giải mã, sau đó gửi mẫu cho đối tác. Thời hạn hoàn thành là 17 giờ ngày 31 tháng 5 năm 2026. Hai là kiểm tra toàn bộ 156 máy chủ còn lại trong mạng của tỉnh A để đảm bảo không có backdoor tồn tại, lập báo cáo chi tiết cho tôi trước 17 giờ ngày 02 tháng 6 năm 2026. Ba là đồng chí phụ trách xây dựng quy trình ứng phó sự cố an ninh mạng IRP chuẩn và trình lãnh đạo phê duyệt trước ngày 15 tháng 6 năm 2026.
[207.00 --> 225.50] Người nói 3: Rõ. Báo cáo lãnh đạo và trưởng phòng, tôi đã nắm chắc ba đầu việc được giao về phân tích mẫu mã độc, rà soát backdoor trên 156 máy chủ của tỉnh A và xây dựng quy trình IRP chuẩn. Tôi xin cam kết sẽ hoàn thành toàn bộ nhiệm vụ nghiêm ngặt theo đúng các mốc thời hạn trước ngày 31 tháng 5, ngày 02 tháng 6 và ngày 15 tháng 6 năm 2026 như chỉ đạo.
[226.00 --> 243.00] Người nói 1: Tốt. Cuộc họp hôm nay các ý kiến đã được thảo luận rất thẳng thắn và toàn diện. Tôi yêu cầu đồng chí Hoàng Anh Tuấn và đồng chí Lê Thị Hồng nghiêm túc triển khai các nhiệm vụ đã được giao, báo cáo kết quả đúng thời hạn. Cuộc họp kết thúc vào hồi 17 giờ 30 phút. Mời các đồng chí nghỉ.
```
