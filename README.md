# Smart Meeting - Công cụ Benchmark

Công cụ Streamlit để đối chiếu output của hệ thống Smart Meeting (STT + diarization)
với dữ liệu tham chiếu (ground truth), tính các chỉ số trong
`Benchmarking_SmartMeeting.docx` (mục V - Bộ tiêu chí đề xuất) và hiển thị
kết quả Đạt / Không đạt theo từng nhóm tiêu chí.

## Cài đặt

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

## Chạy

```powershell
.venv\Scripts\python -m streamlit run app.py
```

Mở trình duyệt tại địa chỉ Streamlit hiển thị (mặc định http://localhost:8501).

## Định dạng input

### Transcript (hệ thống & tham chiếu)

Hỗ trợ 2 định dạng, mỗi dòng/segment gồm: **thời gian bắt đầu - thời gian kết
thúc - người nói - nội dung**.

**Văn bản thuần** (mỗi dòng một lượt nói):
```
[00:00:00.000 --> 00:00:04.200] Người nói 1: Xin chào mọi người...
[00:00:04.500 --> 00:00:09.000] Người nói 2: Vâng, tôi đã chuẩn bị báo cáo...
```

**Văn bản chỉ có 1 mốc thời gian** (thời điểm bắt đầu lượt nói) cũng được hỗ
trợ trực tiếp - thời gian kết thúc sẽ được suy ra từ mốc bắt đầu của lượt
tiếp theo:
```
[00:05] Người nói 1: Các đồng chí, hôm nay chúng ta sẽ tổ chức cuộc họp khẩn...
[00:41] Người nói 2: Cụ thể báo cáo phó cấp trưởng...
```

**JSON** (xem `sample_data/reference.json` và `sample_data/hypothesis.json`):
```json
[
  {"start": 0.0, "end": 4.2, "speaker": "Người nói 1", "text": "Xin chào..."},
  {"start": 4.5, "end": 9.0, "speaker": "Người nói 2", "text": "Vâng..."}
]
```

Transcript "tham chiếu" (reference) là bản ghi tay / ground truth dùng để so
sánh; transcript "hệ thống" (hypothesis) là output thực tế từ pipeline.

### Audio

Upload file WAV để tự động tính thời lượng (dùng cho RTF). Nếu không có file,
có thể nhập tay thời lượng (giây).

### Thời gian xử lý

Nhập thời gian đo thực tế (giây) cho từng giai đoạn (STT, diarization,
finalize, tóm tắt, xuất DOCX) để tính RTF tương ứng (Nhóm 1, 2, 4, 5).

### Từ khoá / thuật ngữ (1.5)

Danh sách 50-100 từ thường gặp trong cuộc họp, mỗi dòng một từ. Công cụ kiểm
tra các từ khoá xuất hiện trong transcript tham chiếu có còn xuất hiện trong
transcript hệ thống hay không.

### Tóm tắt (4.5, tuỳ chọn)

Dán bản tóm tắt mẫu và bản tóm tắt do hệ thống tạo ra để tính ROUGE-L.

## Các chỉ số được tự động tính

| Nhóm | Chỉ số | Công cụ |
|---|---|---|
| 1 | WER, CER | `jiwer` |
| 1 | Nhận dạng thuật ngữ/tên riêng | so khớp từ khoá |
| 1, 5 | RTF STT | thời gian STT / thời lượng audio |
| 2 | DER, speaker confusion, sai số số người nói, P/R biên giới lượt | `pyannote.metrics` |
| 2, 5 | RTF diarization | thời gian diarization / thời lượng audio |
| 3 | TER, độ lệch biên lượt, nhất quán đánh số người nói | so khớp lượt theo overlap |
| 4 | WER/TER toàn phiên, RTF end-to-end | dùng lại các phép đo trên |
| 4 | Chất lượng tóm tắt | ROUGE-L (`rouge_score`) |
| 5 | Thời gian hoàn thiện, tóm tắt, xuất DOCX | nhập tay, so với ngưỡng |

Các tiêu chí 2.6 (so sánh preset) và 4.4 (ổn định phiên dài) mang tính định
tính / cần nhiều lần chạy nên được đánh dấu "Thủ công / định tính".

## Cấu trúc project

```
benchmark/
  parsers.py     - đọc transcript (JSON/text) thành các Segment(start,end,speaker,text)
  metrics.py     - tính WER/CER/DER/TER/RTF/ROUGE-L...
  thresholds.py  - bảng tiêu chí + ngưỡng từ Benchmarking_SmartMeeting.docx
app.py           - giao diện Streamlit (đánh giá từng phiên, qua giao diện web)
scripts/
  batch_eval.py     - chạy metrics cho nhiều phiên cùng lúc, xuất report/batch_eval_results.csv
  groundtruth_qa.py - QA/sửa ground truth (kiểm tốc độ nói, gán lại nhãn người nói theo RTTM)
sample_data/     - file transcript mẫu để test nhanh
report/          - báo cáo Markdown/CSV sinh ra từ app.py và scripts/batch_eval.py
```

## Đánh giá theo lô (scripts/batch_eval.py)

Để chạy metrics cho nhiều phiên ghi âm cùng lúc và xuất một bảng tổng hợp,
dùng `scripts/batch_eval.py`. Script này yêu cầu các thư mục dữ liệu nằm
**ngang hàng** với `stt-benchmark-tools/` (cùng cấp), theo cấu trúc:

```
benchmark/                          <- thư mục gốc, KHÔNG phải repo này
  stt-benchmark-tools/              <- repo này
  data_groundtruth/
    transcript_<ten_phien>_groundtruth.json
    rttm/<ten_phien>.rttm           (tuỳ chọn, dùng cho groundtruth_qa.py relabel)
  data_hypothesis/
    <ten_phien>/
      transcript_<ten_phien>.txt    <- output của hệ thống
      timings.json                  <- {"stt": ..., "diarization": ...} (giây)
      <ten_phien>.wav                (tuỳ chọn, nếu có sẽ dùng để tính RTF chính xác)
```

Danh sách các phiên + đường dẫn tương ứng được khai báo trong `PAIRS` ở đầu
file `scripts/batch_eval.py` - chỉnh sửa danh sách này cho phù hợp với dữ
liệu trên máy của bạn.

Chạy:

```powershell
.venv\Scripts\python scripts\batch_eval.py
```

Kết quả in ra console và lưu vào `report/batch_eval_results.csv`.

## QA / sửa ground truth (scripts/groundtruth_qa.py)

Ground truth do LLM sinh ra có thể gặp 2 lỗi phổ biến:

1. **Tóm tắt/diễn giải thay vì transcribe verbatim** - kiểm bằng:
   ```powershell
   .venv\Scripts\python scripts\groundtruth_qa.py wordrate <groundtruth.json> [...]
   ```
   File có tốc độ < 2.2 từ/giây hoặc > 5.0 từ/giây sẽ bị cảnh báo.

2. **"Trôi" số thứ tự người nói** trên phiên dài (LLM gán nhầm số khi một
   người quay lại sau khoảng lặng dài) - nếu có file RTTM với nhãn người nói
   ổn định (ví dụ từ pyannote diarization), gán lại nhãn theo overlap thời
   gian:
   ```powershell
   .venv\Scripts\python scripts\groundtruth_qa.py diff <groundtruth.json> <rttm>
   .venv\Scripts\python scripts\groundtruth_qa.py relabel <groundtruth.json> <rttm> <out.json>
   ```
   `diff` chỉ in ra các đoạn bị lệch nhãn (để kiểm tra trước); `relabel` ghi
   ra file mới với nhãn "Người nói N" đã sửa.

## Báo cáo

- `report/benchmark_report_*.md` - báo cáo từng phiên, sinh từ `app.py`
  (Streamlit).
- `report/batch_eval_results.csv` - số liệu thô cho nhiều phiên, sinh từ
  `scripts/batch_eval.py`.
- `report/bao_cao_tong_hop.md` - báo cáo tổng hợp 8 phiên, đối chiếu với
  toàn bộ bảng tiêu chí trong `benchmark/thresholds.py`, kèm các lưu ý về
  chất lượng ground truth (xem mục "Dữ liệu đầu vào & lưu ý chất lượng"
  trong file đó trước khi trích số liệu sang báo cáo khác).
