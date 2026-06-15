# Báo cáo Tổng hợp Benchmark - Smart Meeting (8 phiên)

- Thời gian tổng hợp: 2026-06-15
- Script sinh số liệu: `scripts/batch_eval.py` → `report/batch_eval_results.csv`
- Ngưỡng đối chiếu: `benchmark/thresholds.py` (trích "Bộ tiêu chí đề xuất - Mục V" của Benchmarking_SmartMeeting.docx)

## 1. Phương pháp đánh giá

Mỗi phiên được đánh giá bằng cách so sánh transcript tham chiếu (groundtruth)
với transcript do hệ thống sinh ra (hypothesis), dùng các thư viện/độ đo
chuẩn của ngành:

| Nhóm độ đo | Công cụ | Ý nghĩa |
| --- | --- | --- |
| WER / CER | `jiwer.wer`, `jiwer.cer` (sau chuẩn hoá: hạ chữ thường, bỏ dấu câu) | Độ chính xác nhận dạng giọng nói |
| DER, Speaker confusion, Boundary P/R | `pyannote.metrics.DiarizationErrorRate` + segmentation P/R | Độ chính xác phân tách người nói (so theo timeline, không phụ thuộc nội dung văn bản) |
| TER, Nhất quán đánh số người nói | Khớp lượt hyp↔ref theo overlap thời gian (tool tự viết) | Gán đúng người nói cho từng lượt thoại |
| RTF (STT, diarization) | thời gian xử lý / thời lượng audio | Hiệu năng thời gian thực |

Cách làm này giống phương pháp các benchmark công bố cho PhoWhisper và
pyannote, nên số liệu có thể so sánh tương đối với SOTA công bố. Việc chạy
trên 8 phiên (~6.3 giờ audio gộp) thay vì 1 file giúp số liệu ít bị nhiễu bởi
đặc thù của một bản ghi đơn lẻ.

## 2. Dữ liệu đầu vào & lưu ý chất lượng

| Lưu ý | Ảnh hưởng | Xử lý trong báo cáo này |
| --- | --- | --- |
| `toadam4`: groundtruth gốc bị "trôi" số thứ tự người nói (Gemini đặt lại số khi 1 người quay lại sau khoảng lặng dài) | DER/TER/nhất quán đánh số bị tính sai cho ~1/3 phiên | Đã chạy `scripts/groundtruth_qa.py relabel` với RTTM thật để gán lại nhãn → dùng `transcript_toadam4_nongsanxuatkhau_groundtruth.fixed.json`. Kết quả DER 21.5%→**12.7%**, speaker confusion 18.3%→**9.6%**, TER 25.7%→**18.6%**, nhất quán đánh số 91.5%→**95.3%** |
| `toadam5`, `toadam6`: groundtruth là bản **tóm tắt/diễn giải**, không phải verbatim (kiểm bằng `groundtruth_qa.py wordrate`: 1.45 / 1.94 từ/giây so với mức bình thường 2.5-4.5) | WER/CER (178-224%) là nhiễu do groundtruth, **không phản ánh chất lượng STT thật** | **Loại WER/CER của 2 file này khỏi số tổng hợp** (đánh dấu "loại trừ"). DER/TER/RTF vẫn giữ vì các độ đo này chỉ phụ thuộc timeline + nhãn người nói, không phụ thuộc câu chữ |
| `toadam1`-`toadam7`: không có file `.wav` gốc | Thời lượng audio dùng để tính RTF là **ước lượng** (mốc kết thúc cuối cùng trong groundtruth), không phải đo trực tiếp | Cột `audio_dur_s`/RTF của các file này đánh dấu "ước lượng"; chỉ `3p_meeting_zipformer` có thời lượng đo thật từ `.wav` |
| Tiêu chí 1.5 (từ khoá/tên riêng), 2.6 (so sánh preset diarization), 4.4 (ổn định >2h), 4.5 (ROUGE-L tóm tắt), 4.3 & 5.3-5.5 (RTF end-to-end, finalize, tóm tắt, xuất DOCX) | Không có dữ liệu cho batch 8 file này (`timings.json` của batch không chứa `finalize_ratio`/`summary_time`/`docx_export_time`, chưa có bộ từ khoá/RTTM preset thử nghiệm) | Đánh dấu **N/A** trong bảng tổng hợp, không tính vào tỉ lệ Đạt/Không đạt |

## 3. Số liệu thô theo từng phiên

| File | Lượt ref/hyp | Thời lượng (s)* | WER% | CER% | DER% | Spk.conf% | Δspk | Bound P%/R% | TER% | Nhất quán số TT% | RTF STT | RTF Diar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| toadam1_bhyt | 113/73 | 2541.5* | 7.4 | 6.5 | 26.3 | 18.2 | 6 | 29.2/18.8 | 18.6 | 83.1 | 0.022 | 0.161 |
| toadam2_gdpt | 87/75 | 2339.0* | 14.7 | 13.8 | 9.2 | 5.8 | 0 | 45.9/39.5 | 19.5 | 94.1 | 0.025 | 0.181 |
| toadam3_quanlyvonmoi | 73/73 | 2685.0* | 9.9 | 8.7 | 12.1 | 8.2 | 2 | 18.1/18.1 | 9.6 | 95.5 | 0.022 | 0.156 |
| toadam4_nongsanxuatkhau (fixed) | 70/67 | 2355.0* | 37.9 | 37.0 | 12.7 | 9.6 | 4 | 24.2/23.2 | 18.6 | 95.3 | 0.023 | 0.156 |
| toadam5_doingoaivn | 67/78 | 2767.0* | ~~223.6~~ | ~~179.8~~ | 8.7 | 5.5 | 1 | 23.4/27.3 | 10.4 | 95.3 | 0.021 | 0.156 |
| toadam6_kinhte | 80/86 | 2553.0* | ~~178.8~~ | ~~135.7~~ | 25.3 | 5.6 | 5 | 42.4/45.6 | 11.2 | 94.6 | 0.024 | 0.158 |
| toadam7_nongdocon | 74/68 | 2553.0* | 34.6 | 33.7 | 28.1 | 20.9 | 5 | 43.3/39.7 | 31.1 | 76.6 | 0.024 | 0.152 |
| 3p_meeting_zipformer | 7/7 | 243.6 | 21.7 | 17.1 | 9.9 | 5.9 | 0 | 16.7/16.7 | 0.0 | 92.5 | 0.027 | 0.166 |

\* Thời lượng ước lượng (không có `.wav` gốc). WER/CER gạch ngang = loại khỏi
tổng hợp do groundtruth không verbatim (xem mục 2).

## 4. Đối chiếu với tiêu chí chấp nhận (Đạt / Không đạt)

| ID | Tiêu chí | Ngưỡng | Số phiên đạt | Tỉ lệ | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| 1.1 | WER - phòng yên tĩnh | < 22% | 4/6 | 67% | toadam4, toadam7 không đạt; toadam5/6 loại trừ |
| 1.3 | CER - tiếng Việt có dấu | < 13% | 2/6 | 33% | chỉ toadam1, toadam3 đạt |
| 1.4 / 5.1 | RTF lane STT | < 1.0 | 8/8 | 100% | toàn bộ rất nhanh (~0.02), nhưng RTF của toadam1-7 dựa trên thời lượng ước lượng |
| 2.1 | DER tổng | < 22% | 5/8 | 63% | toadam1, toadam6, toadam7 không đạt |
| 2.2 | Speaker confusion | < 12% | 6/8 | 75% | toadam1, toadam7 không đạt |
| 2.3 | Sai số số người nói \|Δ\|≤1 | ≤ 1 | 3/8 | 38% | hệ thống có xu hướng tách dư người nói (over-segmentation) |
| 2.4 | P/R biên giới lượt (±0.5s) | P>0.80 / R>0.75 | 0/8 | 0% | tất cả đều cách xa ngưỡng (P,R cao nhất ~46%) |
| 2.5 / 5.2 | RTF diarization | < 1.5 | 8/8 | 100% | |
| 3.1 / 4.2 | TER - tỉ lệ gán sai người nói | < 15% | 4/8 | 50% | toadam1, toadam2, toadam4, toadam7 không đạt |
| 3.3 | Nhất quán đánh số người nói | 100% | 0/8 | 0% | cao nhất 95.5%, chưa file nào tuyệt đối |
| 4.1 | WER toàn phiên (DOCX) | < 27% | 4/6 | 67% | giống 1.1, ngưỡng rộng hơn |
| 1.5, 2.6, 4.3, 4.4, 4.5, 5.3-5.5 | (xem mục 2) | — | N/A | — | chưa có dữ liệu trong batch này |

## 5. Nhận xét

- **Nhận dạng giọng nói (Nhóm 1)** đạt yêu cầu ở các phiên hội thảo/tọa đàm
  nói chuẩn, tốc độ vừa (toadam1-3): WER 7-15%. Hai phiên có WER cao
  (toadam4 ~38%, toadam7 ~35%) cần nghe lại để xác định nguyên nhân (giọng
  địa phương, chồng tiếng, nhiễu nền).
- **Phân tách người nói (Nhóm 2)** là điểm yếu rõ nhất: tiêu chí 2.4
  (boundary P/R) không đạt ở tất cả 8 phiên và 2.3 (số người nói) chỉ đạt
  3/8 — hệ thống có xu hướng **tách quá nhiều người nói** (Δspk dương ở hầu
  hết các file). DER tổng thể (5/8 đạt) khá hơn nhờ phần lớn audio vẫn được
  gán nhãn đúng về tổng thời gian, nhưng biên các lượt nói lệch nhiều.
- **Gán người nói theo lượt (Nhóm 3)**: TER đạt 4/8, nhưng tiêu chí 3.3
  (nhất quán đánh số 100%) không file nào đạt — đây là giới hạn cố hữu của
  cách đánh số "Người nói N" theo thứ tự xuất hiện khi có >5-10 người nói
  trong phiên dài.
- Hiệu năng (RTF STT và diarization) **vượt xa ngưỡng** ở tất cả các phiên
  (RTF ~0.02-0.18 << 1.0/1.5), cho thấy hệ thống chạy rất nhanh so với thời
  gian thực — đây là điểm mạnh rõ rệt.

## 6. Việc còn thiếu để báo cáo đầy đủ

1. Re-transcribe verbatim cho `toadam5`, `toadam6` để có WER/CER thật (hiện
   đang loại khỏi tổng hợp).
2. Đo thời lượng `.wav` thật cho `toadam1`-`toadam7` để RTF chính xác hơn.
3. Bổ sung danh sách 50-100 từ khoá/tên riêng cho tiêu chí 1.5.
4. Bổ sung `finalize_ratio`, `summary_time`, `docx_export_time` vào
   `timings.json` của batch để tính được 4.3 và Nhóm 5 còn lại.
5. Chạy thử nghiệm 2.6 (so sánh `DIART_PRESET` ∈ {ami, voxconverse, dihard})
   và 4.4 (ổn định phiên dài, theo dõi RAM).
