# Báo cáo tổng hợp Benchmark - Smart Meeting (đầy đủ 5 nhóm tiêu chí)

- Thời gian chạy: 2026-06-15 17:35:29
- Số phiên đánh giá: 8
- Lưu ý: `toadam5_doingoaivn` và `toadam6_kinhte` dùng `groundtruth_local.json` (nhãn người nói theo tên thật, ví dụ `Le_Hai_Binh`, `Pham_Minh_Chinh`) thay vì `transcript_*_groundtruth.json` (nhãn `Người nói N`) như các phiên khác - xem ghi chú trong mục Nhận xét & Kết luận.

## Tổng quan theo phiên

| Phiên | Audio (s) | Lượt (hyp/ref) | Đạt | Không đạt | N/A/Thủ công |
| --- | --- | --- | --- | --- | --- |
| 3p_meeting_demo | 243.6 | 7/7 | 14 | 4 | 5 |
| toadam1_bhyt | 2542.8 | 73/113 | 10 | 8 | 5 |
| toadam2_gdpt | 2339.7 | 75/87 | 12 | 6 | 5 |
| toadam3_quanlyvonmoi | 2692.8 | 73/73 | 14 | 4 | 5 |
| toadam4_nongsanxuatkhau | 2364.1 | 67/70 | 9 | 10 | 4 |
| toadam5_doingoaivn | 2773.7 | 78/67 | 14 | 4 | 5 |
| toadam6_kinhte | 2562.8 | 86/80 | 10 | 8 | 5 |
| toadam7_nongdocon | 2432.8 | 68/74 | 7 | 11 | 5 |

## Chi tiết theo tiêu chí

| ID | Tiêu chí | Ngưỡng | 3p_meeting_demo | toadam1_bhyt | toadam2_gdpt | toadam3_quanlyvonmoi | toadam4_nongsanxuatkhau | toadam5_doingoaivn | toadam6_kinhte | toadam7_nongdocon |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.1 | WER - phòng yên tĩnh | < 22% | 21.7% (Đạt) | 7.4% (Đạt) | 14.7% (Đạt) | 9.9% (Đạt) | 37.9% (Không đạt) | 19.8% (Đạt) | 33.3% (Không đạt) | 34.6% (Không đạt) |
| 1.3 | CER - tiếng Việt có dấu | < 13% | 17.1% (Không đạt) | 6.5% (Đạt) | 13.8% (Không đạt) | 8.7% (Đạt) | 37.0% (Không đạt) | 14.0% (Không đạt) | 28.3% (Không đạt) | 33.7% (Không đạt) |
| 1.4 | RTF lane STT (realtime) | < 1.0 | 0.03 (Đạt) | 0.02 (Đạt) | 0.03 (Đạt) | 0.02 (Đạt) | 0.02 (Đạt) | 0.02 (Đạt) | 0.02 (Đạt) | 0.03 (Đạt) |
| 1.5 | Nhận dạng thuật ngữ / tên riêng | > 80% | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| 2.1 | DER tổng | < 22% | 9.9% (Đạt) | 26.3% (Không đạt) | 9.2% (Đạt) | 12.1% (Đạt) | 12.7% (Đạt) | 8.7% (Đạt) | 23.6% (Không đạt) | 28.1% (Không đạt) |
| 2.2 | Speaker confusion | < 12% | 5.9% (Đạt) | 18.2% (Không đạt) | 5.8% (Đạt) | 8.2% (Đạt) | 9.6% (Đạt) | 5.5% (Đạt) | 3.9% (Đạt) | 20.9% (Không đạt) |
| 2.3 | Sai số số người nói | \|Δ\| ≤ 1 | 0.00 (Đạt) | 6.00 (Không đạt) | 0.00 (Đạt) | 2.00 (Không đạt) | 4.00 (Không đạt) | 1.00 (Đạt) | 3.00 (Không đạt) | 5.00 (Không đạt) |
| 2.4 | P/R biên giới lượt (±0.5s) | P > 0.80 / R > 0.75 | P=16.7% / R=16.7% (Không đạt) | P=29.2% / R=18.8% (Không đạt) | P=45.9% / R=39.5% (Không đạt) | P=18.1% / R=18.1% (Không đạt) | P=24.2% / R=23.2% (Không đạt) | P=23.4% / R=27.3% (Không đạt) | P=42.4% / R=45.6% (Không đạt) | P=43.3% / R=39.7% (Không đạt) |
| 2.5 | RTF diarization (CPU) | < 1.5 | 0.17 (Đạt) | 0.16 (Đạt) | 0.18 (Đạt) | 0.16 (Đạt) | 0.16 (Đạt) | 0.16 (Đạt) | 0.16 (Đạt) | 0.16 (Đạt) |
| 2.6 | So sánh preset (A/B) | chọn min DER | Thủ công / định tính | Thủ công / định tính | Thủ công / định tính | Thủ công / định tính | Thủ công / định tính | Thủ công / định tính | Thủ công / định tính | Thủ công / định tính |
| 3.1 | TER - tỉ lệ lượt gán sai người | < 15% | 0.0% (Đạt) | 18.6% (Không đạt) | 19.5% (Không đạt) | 9.6% (Đạt) | 18.6% (Không đạt) | 10.4% (Đạt) | 8.8% (Đạt) | 31.1% (Không đạt) |
| 3.2 | Độ chính xác biên lượt STT | < 0.5s lệch TB | 2.65s (Không đạt) | 18.35s (Không đạt) | 7.72s (Không đạt) | 1.12s (Không đạt) | 2.07s (Không đạt) | 2.68s (Không đạt) | 4.12s (Không đạt) | 7.62s (Không đạt) |
| 3.3 | Nhất quán đánh số người nói | 100% | 92.5% (Không đạt) | 83.1% (Không đạt) | 94.1% (Không đạt) | 95.5% (Không đạt) | 95.3% (Không đạt) | 95.3% (Không đạt) | 94.6% (Không đạt) | 76.6% (Không đạt) |
| 4.1 | WER toàn phiên (nội dung DOCX) | < 27% | 21.7% (Đạt) | 7.4% (Đạt) | 14.7% (Đạt) | 9.9% (Đạt) | 37.9% (Không đạt) | 19.8% (Đạt) | 33.3% (Không đạt) | 34.6% (Không đạt) |
| 4.2 | TER trong DOCX | < 15% | 0.0% (Đạt) | 18.6% (Không đạt) | 19.5% (Không đạt) | 9.6% (Đạt) | 18.6% (Không đạt) | 10.4% (Đạt) | 8.8% (Đạt) | 31.1% (Không đạt) |
| 4.3 | RTF end-to-end (warm) | < 1.5 | 0.19 (Đạt) | 0.18 (Đạt) | 0.21 (Đạt) | 0.18 (Đạt) | 0.42 (Đạt) | 0.18 (Đạt) | 0.18 (Đạt) | 0.19 (Đạt) |
| 4.4 | Ổn định phiên dài > 2h | Không crash, RAM ổn định | Thủ công / định tính | Thủ công / định tính | Thủ công / định tính | Thủ công / định tính | Thủ công / định tính | Thủ công / định tính | Thủ công / định tính | Thủ công / định tính |
| 4.5 | Chất lượng tóm tắt (Qwen) | Đạt theo rubric / ROUGE-L cao | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| 5.1 | RTF STT (lane 1) | < 1.0 | 0.03 (Đạt) | 0.02 (Đạt) | 0.03 (Đạt) | 0.02 (Đạt) | 0.02 (Đạt) | 0.02 (Đạt) | 0.02 (Đạt) | 0.03 (Đạt) |
| 5.2 | RTF diart (lane 2) | < 1.5 | 0.17 (Đạt) | 0.16 (Đạt) | 0.18 (Đạt) | 0.16 (Đạt) | 0.16 (Đạt) | 0.16 (Đạt) | 0.16 (Đạt) | 0.16 (Đạt) |
| 5.3 | Thời gian hoàn thiện | < 0.3x audio | 0.00 (Đạt) | 0.00 (Đạt) | 0.00 (Đạt) | 0.00 (Đạt) | 0.00 (Đạt) | 0.00 (Đạt) | 0.00 (Đạt) | 0.00 (Đạt) |
| 5.4 | Thời gian tóm tắt (Qwen NPU) | < 60s / phiên | N/A | N/A | N/A | N/A | 560.17s (Không đạt) | N/A | N/A | N/A |
| 5.5 | Xuất DOCX | < 5s | 0.08s (Đạt) | 0.14s (Đạt) | 0.16s (Đạt) | 0.15s (Đạt) | 0.11s (Đạt) | 0.15s (Đạt) | 0.16s (Đạt) | 0.14s (Đạt) |

## Nhận xét & Kết luận

### 1. Tổng quan theo từng phiên

- **3p_meeting_demo**: 14/18 tiêu chí đạt (78%), 5 tiêu chí N/A hoặc thủ công. Vấn đề chính: không có vấn đề nổi bật ngoài nhóm 3 (xem mục 3).
- **toadam1_bhyt**: 10/18 tiêu chí đạt (56%), 5 tiêu chí N/A hoặc thủ công. Vấn đề chính: DER cao (26.3%); sai số người nói lớn (ref=14 vs hyp=20); TER cao (18.6%).
- **toadam2_gdpt**: 12/18 tiêu chí đạt (67%), 5 tiêu chí N/A hoặc thủ công. Vấn đề chính: TER cao (19.5%).
- **toadam3_quanlyvonmoi**: 14/18 tiêu chí đạt (78%), 5 tiêu chí N/A hoặc thủ công. Vấn đề chính: sai số người nói lớn (ref=20 vs hyp=22).
- **toadam4_nongsanxuatkhau**: 9/19 tiêu chí đạt (47%), 4 tiêu chí N/A hoặc thủ công. Vấn đề chính: WER cao (37.9%); sai số người nói lớn (ref=14 vs hyp=18); TER cao (18.6%); tóm tắt Qwen vượt ngưỡng (560s).
- **toadam5_doingoaivn**: 14/18 tiêu chí đạt (78%), 5 tiêu chí N/A hoặc thủ công. Vấn đề chính: không có vấn đề nổi bật ngoài nhóm 3 (xem mục 3).
- **toadam6_kinhte**: 10/18 tiêu chí đạt (56%), 5 tiêu chí N/A hoặc thủ công. Vấn đề chính: WER cao (33.3%); DER cao (23.6%); sai số người nói lớn (ref=31 vs hyp=34).
- **toadam7_nongdocon**: 7/18 tiêu chí đạt (39%), 5 tiêu chí N/A hoặc thủ công. Vấn đề chính: WER cao (34.6%); DER cao (28.1%); sai số người nói lớn (ref=21 vs hyp=16); TER cao (31.1%).

### 2. Theo từng nhóm tiêu chí

**Nhóm 1 - STT (WER/CER/RTF):**
- 1.1 (WER < 22%): đạt ở 5/8 phiên (`3p_meeting_demo`, `toadam1_bhyt`, `toadam2_gdpt`, `toadam3_quanlyvonmoi`, `toadam5_doingoaivn`). 1.3 (CER < 13%): đạt ở 2/8 phiên. Kết quả WER/CER có dạng hai cực: các phiên đạt 1.1 có WER 7-22% (audio rõ, ít overlap), trong khi `toadam4_nongsanxuatkhau`, `toadam6_kinhte`, `toadam7_nongdocon` có WER/CER ~33-38% (audio noisy/nhiều giọng đè nhau hoặc ground truth khó căn chỉnh).
- 1.4/5.1 (RTF lane STT < 1.0): đạt 8/8 phiên (RTF ~0.02-0.03, rất nhanh so với realtime) - không phải điểm nghẽn.
- 1.5 (nhận dạng thuật ngữ/tên riêng): N/A ở tất cả phiên - chưa có danh sách từ khoá để đo, cần bổ sung danh sách thuật ngữ riêng cho từng cuộc họp.

**Nhóm 2 - Diarization (DER/speaker confusion/số người nói/biên lượt):**
- 2.1 (DER < 22%): đạt 5/8 phiên; 2.2 (speaker confusion < 12%): đạt 6/8 phiên. Các phiên fail 2.1 là `toadam1_bhyt`, `toadam6_kinhte`, `toadam7_nongdocon`, đều có sai số số người nói (2.3) đáng kể (xem bên dưới).
- 2.3 (|Δ số người nói| ≤ 1): đạt 3/8 phiên (`3p_meeting_demo`, `toadam2_gdpt`, `toadam5_doingoaivn`); 5 phiên còn lại (`toadam1_bhyt`, `toadam3_quanlyvonmoi`, `toadam4_nongsanxuatkhau`, `toadam6_kinhte`, `toadam7_nongdocon`) lệch 2-6 người, đa số là **over-segmentation** (hệ thống tách 1 người thành nhiều speaker ID), riêng `toadam7_nongdocon` thì ngược lại (gộp nhiều người vào ít speaker ID hơn).
- 2.4 (P/R biên giới lượt ±0.5s, cần P>0.80/R>0.75): **FAIL ở cả 8/8 phiên** (P=16-46%, R=16-40%) - đây là vấn đề có tính hệ thống, xem mục 3.
- 2.5/5.2 (RTF diarization < 1.5): đạt 8/8 phiên (RTF ~0.16-0.18) - không phải điểm nghẽn.
- 2.6 (so sánh preset A/B): thủ công/định tính ở tất cả phiên - cần chạy thêm với preset diarization khác để có cơ sở so sánh.

**Nhóm 3 - Gán người nói theo lượt (turn-speaker assignment):**
- 3.1/4.2 (TER < 15%): đạt 4/8 phiên (`3p_meeting_demo`, `toadam3_quanlyvonmoi`, `toadam5_doingoaivn`, `toadam6_kinhte`).
- 3.2 (lệch biên lượt trung bình < 0.5s): **FAIL ở 8/8 phiên**, lệch dao động 1.1s - 18.4s, lớn hơn ngưỡng 2-37 lần. Đây là tiêu chí fail nặng nhất và đồng đều nhất trong toàn bộ bảng.
- 3.3 (nhất quán đánh số người nói = 100%): **FAIL ở 8/8 phiên** (76.6% - 95.5%, trung vị ~95%).

**Nhóm 4 - End-to-end:**
- 4.1 (WER toàn phiên < 27%) và 4.3 (RTF end-to-end < 1.5): 4.3 đạt 8/8 phiên (RTF 0.18-0.42, rất xa ngưỡng), nhưng 4.1/4.2 lặp lại kết quả của 1.1/3.1 (xem trên).
- 4.4 (ổn định phiên > 2h): thủ công - chưa được kiểm chứng với phiên dài thật.
- 4.5 (chất lượng tóm tắt Qwen, ROUGE-L): N/A - chưa có bản tóm tắt mẫu để so sánh, ngoại trừ kiểm tra thời gian chạy (xem 5.4).

**Nhóm 5 - Hiệu năng:**
- 5.3 (thời gian hoàn thiện < 0.3x audio) và 5.5 (xuất DOCX < 5s): đạt 8/8 phiên, không đáng lo.
- 5.4 (tóm tắt Qwen NPU < 60s/phiên): chỉ có dữ liệu cho `toadam4_nongsanxuatkhau` và **FAIL nghiêm trọng** (560s, gấp ~9.3x ngưỡng); 5 phiên còn lại không có `summary_time` trong `timings.json` nên hiển thị N/A. Cần đo lại thời gian tóm tắt cho tất cả phiên.

### 3. Vấn đề mang tính hệ thống (ưu tiên xử lý)

1. **Lệch biên lượt nói (3.2) và P/R biên giới lượt (2.4) fail ở toàn bộ 8/8 phiên**, độc lập với chất lượng nội dung (kể cả phiên WER thấp nhất `toadam1_bhyt` (7.4%) cũng có lệch biên trung bình 18.35s). Đây là dấu hiệu diarization và STT đang cắt turn theo logic khác với cách ground truth phân đoạn (ví dụ: hệ thống tạo turn mới mỗi khi có khoảng lặng ngắn / mỗi câu, còn ground truth gộp theo lượt nói thực tế dài hơn). Nên kiểm tra logic merge segment liên tiếp cùng speaker trước khi tính 2.4/3.2.
2. **Over/under-segmentation số người nói (2.3, 3.3)** tương quan trực tiếp với DER/TER fail: `toadam1_bhyt` (+6 spk), `toadam3_quanlyvonmoi` (+2 spk), `toadam4_nongsanxuatkhau` (+4 spk), `toadam6_kinhte` (+3 spk) đều tách dư speaker ID (over-segmentation); `toadam7_nongdocon` (-5 spk) lại gộp nhiều người vào ít speaker ID hơn (under-segmentation). Cần tinh chỉnh ngưỡng clustering của diarization (có thể khác nhau giữa phòng yên tĩnh và phòng nhiều người/talkshow).
3. **WER/CER tăng vọt ở phiên nhiều người/audio khó** (`toadam4_nongsanxuatkhau`, `toadam6_kinhte`, `toadam7_nongdocon` ~33-38% so với ~7-22% ở các phiên khác) - cần kiểm tra chất lượng audio đầu vào và mức độ overlap giọng nói của các phiên này, có thể cần mô hình STT khác hoặc xử lý tách giọng (speech separation) trước khi STT.
4. **Thời gian tóm tắt Qwen (5.4) vượt ngưỡng gần 10 lần** ở phiên duy nhất có số liệu (`toadam4_nongsanxuatkhau`, 560s) - cần đo lại cho các phiên còn lại và tối ưu (batch size, độ dài input, NPU offload).
5. **Thiếu dữ liệu cho 1.5, 2.6, 4.4, 4.5** (N/A/thủ công ở tất cả phiên) - cần bổ sung: danh sách thuật ngữ/từ khoá theo từng cuộc họp (1.5), chạy lại với preset diarization khác để so sánh (2.6), test phiên dài liên tục >2h (4.4), và bản tóm tắt tham chiếu để tính ROUGE-L (4.5).
6. **Ground truth của `toadam5_doingoaivn` và `toadam6_kinhte` dùng `groundtruth_local.json`** với nhãn người nói là tên thật (vd. `Le_Hai_Binh`, `Pham_Minh_Chinh`, `Phong_vien_toadam6_3`...) thay vì `Người nói N` như các phiên còn lại. Số lượng nhãn (ref_speaker_count) vì vậy cao bất thường (toadam5: 13, toadam6: 31) vì mỗi nhân vật xuất hiện trong clip/trích dẫn (kể cả chỉ 1 lượt ngắn) cũng được tính là một người nói riêng. Các chỉ số 2.1/2.2/2.3/3.x cho hai phiên này nên được đọc với lưu ý đó - chúng phản ánh khả năng tách đúng *từng nhân vật được nêu tên*, khắt khe hơn cách đếm `Người nói N` thông thường. Dù vậy WER (1.1) của `toadam5_doingoaivn` vẫn đạt ngưỡng (19.8%), cho thấy nội dung STT chính xác tốt cho phiên talkshow này.

### 4. Khuyến nghị ưu tiên

- **Ưu tiên 1**: Rà soát cách xác định ranh giới lượt nói (turn boundary) trong pipeline STT+diarization - nguyên nhân gốc của 2.4/3.2/3.3 fail toàn bộ và ảnh hưởng dây chuyền tới 3.1/4.2.
- **Ưu tiên 2**: Tinh chỉnh tham số diarization (clustering threshold, min/max speakers) để giảm sai số số người nói (2.3), đặc biệt cho `toadam1_bhyt`, `toadam3_quanlyvonmoi`, `toadam4_nongsanxuatkhau`, `toadam6_kinhte`, `toadam7_nongdocon`.
- **Ưu tiên 3**: Điều tra nguyên nhân WER/CER cao bất thường ở `toadam4_nongsanxuatkhau`, `toadam6_kinhte`, `toadam7_nongdocon` (audio quality, overlap, ground truth alignment).
- **Ưu tiên 4**: Tối ưu thời gian tóm tắt Qwen (5.4) và đo lại cho toàn bộ phiên; bổ sung dữ liệu còn thiếu cho 1.5, 2.6, 4.4, 4.5.

## Giá trị đo thô theo phiên (raw metrics)

```json
{
  "3p_meeting_demo": {
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
  },
  "toadam1_bhyt": {
    "wer": 0.07368757320839102,
    "cer": 0.06471521777464292,
    "keyword_recognition": null,
    "der": 0.2625766087844736,
    "speaker_confusion": 0.18189479060265587,
    "missed_detection": 0.02176540687776589,
    "false_alarm": 0.058916411304051855,
    "ref_speaker_count": 14,
    "hyp_speaker_count": 20,
    "speaker_count_diff": 6,
    "boundary_precision": 0.2916666666666667,
    "boundary_recall": 0.1875,
    "ter": 0.18584070796460178,
    "turn_boundary_deviation": 18.350669642857138,
    "speaker_numbering_consistency": 0.8312234036004912,
    "rtf_stt": 0.021907776510590234,
    "rtf_diarization": 0.16047925497860382,
    "rtf_e2e": 0.1838300702236672,
    "finalize_ratio": 0.0013868006130250193,
    "summary_time": null,
    "docx_export_time": 0.143,
    "rouge_l": null
  },
  "toadam2_gdpt": {
    "wer": 0.1474242972614308,
    "cer": 0.1377638177109164,
    "keyword_recognition": null,
    "der": 0.0924234234234233,
    "speaker_confusion": 0.058238738738738687,
    "missed_detection": 0.01121171171171179,
    "false_alarm": 0.022972972972972825,
    "ref_speaker_count": 21,
    "hyp_speaker_count": 21,
    "speaker_count_diff": 0,
    "boundary_precision": 0.4594594594594595,
    "boundary_recall": 0.3953488372093023,
    "ter": 0.19540229885057472,
    "turn_boundary_deviation": 7.716609195402299,
    "speaker_numbering_consistency": 0.9406574032438308,
    "rtf_stt": 0.02512548552984299,
    "rtf_diarization": 0.1806464641802068,
    "rtf_e2e": 0.20756075961485862,
    "finalize_ratio": 0.0017190577301821762,
    "summary_time": null,
    "docx_export_time": 0.1632,
    "rouge_l": null
  },
  "toadam3_quanlyvonmoi": {
    "wer": 0.09891808346213292,
    "cer": 0.08737798569565022,
    "keyword_recognition": null,
    "der": 0.1206824457593686,
    "speaker_confusion": 0.08201972386587798,
    "missed_detection": 0.010260355029585522,
    "false_alarm": 0.02840236686390509,
    "ref_speaker_count": 20,
    "hyp_speaker_count": 22,
    "speaker_count_diff": 2,
    "boundary_precision": 0.18055555555555555,
    "boundary_recall": 0.18055555555555555,
    "ter": 0.0958904109589041,
    "turn_boundary_deviation": 1.1170547945205462,
    "speaker_numbering_consistency": 0.9547731684353679,
    "rtf_stt": 0.02188215432206263,
    "rtf_diarization": 0.15603561491545004,
    "rtf_e2e": 0.179481207327929,
    "finalize_ratio": 0.0015093676424437511,
    "summary_time": null,
    "docx_export_time": 0.1456,
    "rouge_l": null
  },
  "toadam4_nongsanxuatkhau": {
    "wer": 0.3787112666925969,
    "cer": 0.36977298079532095,
    "keyword_recognition": null,
    "der": 0.12712791991101244,
    "speaker_confusion": 0.09551501668520566,
    "missed_detection": 0.009744160177975743,
    "false_alarm": 0.02186874304783104,
    "ref_speaker_count": 14,
    "hyp_speaker_count": 18,
    "speaker_count_diff": 4,
    "boundary_precision": 0.24242424242424243,
    "boundary_recall": 0.2318840579710145,
    "ter": 0.18571428571428572,
    "turn_boundary_deviation": 2.067285714285719,
    "speaker_numbering_consistency": 0.9531640839652705,
    "rtf_stt": 0.02336798114970982,
    "rtf_diarization": 0.1558809380276539,
    "rtf_e2e": 0.4181543782169795,
    "finalize_ratio": 0.0019112754810844772,
    "summary_time": 560.1704,
    "docx_export_time": 0.1142,
    "rouge_l": null
  },
  "toadam5_doingoaivn": {
    "wer": 0.19756261180679785,
    "cer": 0.13970889708897088,
    "keyword_recognition": null,
    "der": 0.08718986384266264,
    "speaker_confusion": 0.05467473524962168,
    "missed_detection": 0.012447049924356898,
    "false_alarm": 0.02006807866868406,
    "ref_speaker_count": 13,
    "hyp_speaker_count": 12,
    "speaker_count_diff": 1,
    "boundary_precision": 0.23376623376623376,
    "boundary_recall": 0.2727272727272727,
    "ter": 0.1044776119402985,
    "turn_boundary_deviation": 2.6823880597014913,
    "speaker_numbering_consistency": 0.953106994726273,
    "rtf_stt": 0.021297903945170088,
    "rtf_diarization": 0.1556709597664027,
    "rtf_e2e": 0.17823536471233264,
    "finalize_ratio": 0.0012122053900921958,
    "summary_time": null,
    "docx_export_time": 0.1506,
    "rouge_l": null
  },
  "toadam6_kinhte": {
    "wer": 0.3327937535707484,
    "cer": 0.2834943763343825,
    "keyword_recognition": null,
    "der": 0.23649116730169686,
    "speaker_confusion": 0.039186006234845694,
    "missed_detection": 0.18085555940422585,
    "false_alarm": 0.016449601662625307,
    "ref_speaker_count": 31,
    "hyp_speaker_count": 34,
    "speaker_count_diff": 3,
    "boundary_precision": 0.4235294117647059,
    "boundary_recall": 0.45569620253164556,
    "ter": 0.0875,
    "turn_boundary_deviation": 4.116582278481002,
    "speaker_numbering_consistency": 0.9460362466630192,
    "rtf_stt": 0.023973368170257664,
    "rtf_diarization": 0.15724813270495763,
    "rtf_e2e": 0.18264342332091724,
    "finalize_ratio": 0.0013609734360648012,
    "summary_time": null,
    "docx_export_time": 0.1562,
    "rouge_l": null
  },
  "toadam7_nongdocon": {
    "wer": 0.3460559796437659,
    "cer": 0.33690192968543486,
    "keyword_recognition": null,
    "der": 0.28105022831050214,
    "speaker_confusion": 0.2085429638854296,
    "missed_detection": 0.052984640929846324,
    "false_alarm": 0.019522623495226248,
    "ref_speaker_count": 21,
    "hyp_speaker_count": 16,
    "speaker_count_diff": 5,
    "boundary_precision": 0.43283582089552236,
    "boundary_recall": 0.3972602739726027,
    "ter": 0.3108108108108108,
    "turn_boundary_deviation": 7.622253521126763,
    "speaker_numbering_consistency": 0.7659455675380846,
    "rtf_stt": 0.025589059368116437,
    "rtf_diarization": 0.15957821677277872,
    "rtf_e2e": 0.18658997756155157,
    "finalize_ratio": 0.0013630984892198336,
    "summary_time": null,
    "docx_export_time": 0.145,
    "rouge_l": null
  }
}
```
