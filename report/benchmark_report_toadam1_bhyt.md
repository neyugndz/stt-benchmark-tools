# Báo cáo Benchmark - Smart Meeting

- Thời gian chạy: 2026-06-10 18:12:55
- Audio: toadam1_bhyt.wav (thời lượng: 2542.8s)
- Điều kiện audio: Phòng yên tĩnh (1.1, < 22%)
- Số lượt nói (hệ thống / tham chiếu): 74 / 113
- Số từ khoá kiểm tra (1.5): 0
- Có dữ liệu tóm tắt (4.5): Không

## Tổng quan

- **Đạt**: 7
- **Không đạt**: 12
- **N/A / Thủ công**: 4

## Nhóm 1 - Nhận dạng giọng nói

| ID | Tiêu chí | Ngưỡng | Giá trị đo | Kết quả | Ưu tiên | Cách đo |
| --- | --- | --- | --- | --- | --- | --- |
| 1.1 | WER - phòng yên tĩnh | < 22% | 66.9% | Không đạt | Cao | jiwer.wer(ref,hyp) sau chuẩn hoá; audio sạch |
| 1.3 | CER - tiếng Việt có dấu | < 13% | 54.9% | Không đạt | Cao | jiwer.cer(ref,hyp) |
| 1.4 | RTF lane STT (realtime) | < 1.0 | 0.18 | Đạt | Rất cao | thời gian xử lý STT / thời lượng audio |
| 1.5 | Nhận dạng thuật ngữ / tên riêng | > 80% | N/A | N/A | TB | Danh sách 50-100 từ họp thường gặp soạn trước |

## Nhóm 2 - Phân tách người nói 

| ID | Tiêu chí | Ngưỡng | Giá trị đo | Kết quả | Ưu tiên | Cách đo |
| --- | --- | --- | --- | --- | --- | --- |
| 2.1 | DER tổng | < 22% | 26.2% | Không đạt | Rất cao | pyannote.metrics DiarizationErrorRate(ref_rttm, hyp_rttm) |
| 2.2 | Speaker confusion | < 12% | 18.3% | Không đạt | Rất cao | Thành phần confusion của DER |
| 2.3 | Sai số số người nói | \|Δ\| ≤ 1 | 5.00 | Không đạt | Cao | \|num_detected - num_true\| |
| 2.4 | P/R biên giới lượt (±0.5s) | P > 0.80 / R > 0.75 | P=30.1% / R=19.6% | Không đạt | Cao | So hyp_rttm với ref_rttm, dung sai 0.5s |
| 2.5 | RTF diarization (CPU) | < 1.5 | 0.18 | Đạt | Cao | thời gian xử lý diart / thời lượng audio |
| 2.6 | So sánh preset (A/B) | chọn min DER | N/A | Thủ công / định tính | TB | Lặp DIART_PRESET ∈ {ami, voxconverse, dihard}; cần chạy nhiều lần |

## Nhóm 3 - Gán người nói theo overlap

| ID | Tiêu chí | Ngưỡng | Giá trị đo | Kết quả | Ưu tiên | Cách đo |
| --- | --- | --- | --- | --- | --- | --- |
| 3.1 | TER - tỉ lệ lượt gán sai người | < 15% | 18.6% | Không đạt | Rất cao | Khớp lượt hyp↔ref theo thời gian, đếm % sai nhãn speaker |
| 3.2 | Độ chính xác biên lượt STT | < 0.5s lệch TB | 18.19s | Không đạt | TB | So start/end lượt STT với mốc tiếng nói thật |
| 3.3 | Nhất quán đánh số người nói | 100% | 82.8% | Không đạt | Cao | Cùng 1 người → cùng 'Người nói N' suốt phiên (first-appearance) |

## Nhóm 4 - Hệ thống đầu cuối (end-to-end)

| ID | Tiêu chí | Ngưỡng | Giá trị đo | Kết quả | Ưu tiên | Cách đo |
| --- | --- | --- | --- | --- | --- | --- |
| 4.1 | WER toàn phiên (nội dung DOCX) | < 27% | 66.9% | Không đạt | Rất cao | So bản ghi tay toàn phiên với text trong DOCX |
| 4.2 | TER trong DOCX | < 15% | 18.6% | Không đạt | Rất cao | Đối chiếu nhãn người nói trong DOCX với nhãn chuẩn |
| 4.3 | RTF end-to-end (warm) | < 1.5 | 0.46 | Đạt | Rất cao | Từ bắt đầu xử lý đến xuất DOCX / thời lượng audio |
| 4.4 | Ổn định phiên dài > 2h | Không crash, RAM ổn định | N/A | Thủ công / định tính | Rất cao | 5 file x 30 phút cùng 1 session; theo dõi RAM |
| 4.5 | Chất lượng tóm tắt (Qwen) | Đạt theo rubric / ROUGE-L cao | N/A | N/A | TB | Chấm người hoặc ROUGE-L với bản tóm tắt mẫu |

## Nhóm 5 - Hiệu năng & độ trễ

| ID | Tiêu chí | Ngưỡng | Giá trị đo | Kết quả | Ưu tiên | Cách đo |
| --- | --- | --- | --- | --- | --- | --- |
| 5.1 | RTF STT (lane 1) | < 1.0 | 0.18 | Đạt | Rất cao | time.perf_counter quanh vòng decode |
| 5.2 | RTF diart (lane 2) | < 1.5 | 0.18 | Đạt | Cao | Đo riêng thread feeder; theo dõi backlog drain |
| 5.3 | Thời gian hoàn thiện | < 0.3x audio | 0.00 | Đạt | Cao | drain + gán overlap + khôi phục dấu câu |
| 5.4 | Thời gian tóm tắt (Qwen NPU) | < 60s / phiên | 271.08s | Không đạt | TB | Đo wall-clock gọi Nexa |
| 5.5 | Xuất DOCX | < 5s | 0.13s | Đạt | TB | Đo wall-clock export |

## Giá trị đo thô (raw metrics)

```json
{
  "wer": 0.6688318602917687,
  "cer": 0.5487820238305161,
  "keyword_recognition": null,
  "der": 0.26214249233912124,
  "speaker_confusion": 0.18260554988083097,
  "missed_detection": 0.020245999319032464,
  "false_alarm": 0.05929094313925784,
  "ref_speaker_count": 14,
  "hyp_speaker_count": 19,
  "speaker_count_diff": 5,
  "boundary_precision": 0.3013698630136986,
  "boundary_recall": 0.19642857142857142,
  "ter": 0.18584070796460178,
  "turn_boundary_deviation": 18.191017699115044,
  "speaker_numbering_consistency": 0.8284425766177593,
  "rtf_stt": 0.17641131814807376,
  "rtf_diarization": 0.17566256458566037,
  "rtf_e2e": 0.45910222475599655,
  "finalize_ratio": 0.0003715648751342876,
  "summary_time": 271.0758,
  "docx_export_time": 0.1267,
  "rouge_l": null
}
```

## Transcript đã dùng

### Hệ thống (Hypothesis)

```
[19.39 --> 113.39] Người nói 1: Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Cả về độ bao phủ, quyền lợi người tham gia bảo hiểm y tế và chất lượng khám triệu bệnh Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Việc cơ bản đã đáp ứng được nhu cầu của nhân dân trong bảo vệ và chăm sóc sức khỏe. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Để chính sách bảo hiểm y tế ngày càng hoàn thiện, đáp ứng hơn nữa nhu cầu chăm sóc, bảo vệ sức khỏe nhân dân, bộ y tế đang chủ trì xây dựng luật bảo hiểm y tế sửa đổi. Cảm ơn các bạn đã theo dõi. 3 vị khách mời đến từ cơ quan xây dựng chính sách, cơ quan tổ chức thực hiện chính sách và cơ sở cung ứng dịch vụ khám chữa bệnh, bảo hiểm y tế Xin được trân trọng giới thiệu, bà trần thị trang, quyền vụ trưởng vụ bảo hiểm y tế, bộ y tế. Ông lê văn phúc, trưởng ban thực hiện chính sách bảo hiểm y tế, bảo hiểm xã hội việt nam Ông trịnh ngọc hải, phó giám đốc bệnh viện nhi trung ương.
[115.07 --> 118.38] Người nói 1: Xin trân trọng cảm ơn các vị khách mời đã nhận lời tham gia chương trình với chúng tôi
[120.61 --> 151.02] Người nói 1: Subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ
[156.87 --> 193.00] Người nói 2: Ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Cảm ơn các bạn đã theo dõi.
[195.73 --> 217.39] Người nói 3: Kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Thì có cả việc quản lý sức khỏe cá nhân sàng lọc trần đón sớm một số bệnh trong cộng đồng và thậm chí có những quốc gia Người ta còn chi trả cho một số dịch vụ y tế mang tính chức dự phòng cộng đồng nữa.
[218.46 --> 230.44] Người nói 4: Nếu mà chúng ta sàng lọc trong giai đoạn đầu, giai đoạn mới thì tốn rất ít tiền, nó để vừa lợi cho cả Liên quan đến đề xuất mua bảo
[231.85 --> 255.40] Người nói 2: Hiểm y tế bổ sung, Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Cảm ơn các bạn đã theo dõi.
[257.56 --> 284.77] Người nói 4: Là khi các cơ sở y tế người ta sử dụng Nó quá so với những năm trước, độ 5-7 tỷ. Chẳng hạn, độ 10-15% chẳng hạn. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn
[286.18 --> 314.28] Người nói 3: Các bạn hãy đăng ký kênh để ủng hộ kênh của chúng mình nhé. Cảm ơn các bạn đã theo dõi. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn
[315.79 --> 325.40] Người nói 2: Các chuyên gia nhấn mạnh, việc mở rộng quyền lợi bảo hiểm y tế là cần thiết, nhưng cần tính đến phạm vi, danh mục dịch vụ và khả năng chi trả của quỹ bảo hiểm y tế.
[328.42 --> 340.42] Người nói 1: Kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn
[341.15 --> 407.49] Người nói 5: Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Cảm ơn các bạn đã theo dõi. - Cái thứ ba là liên quan đến vấn đề khám trần đoán trước sinh, rồi là một số các dịch vụ khám bệnh chữa bệnh. Các bạn có thể nhớ like, share và đăng ký kênh để ủng hộ kênh của chúng mình nhé. Trong điều trị thì đấy là một số các phạm vi mà chúng tôi dự kiến đang thiết kế để đưa ra lấy ý kiến. Có hai loại
[407.72 --> 416.94] Người nói 1: Hình đó là bảo hiểm y tế và bảo hiểm y tế bổ sung Mới được đưa vào dự thảo luật sửa đổi. Vậy thì hai loại hình này sẽ được sắp xếp theo các nhóm đối tượng như thế?
[417.49 --> 512.99] Người nói 5: Nào? Bảo hiểm y tế mà chúng ta đang thực hiện theo quy định hiện hành. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Cảm ơn các bạn đã theo dõi. Bổ sung thì sẽ là một chính sách bảo hiểm y tế mà những người tham gia bảo hiểm y tế bắt buộc rồi thì sẽ tham gia bảo hiểm y tế bổ sung. Và cái thứ 2 nữa Vâng Ví dụ như là phần đồng chi trả mà người có thể bảo hiểm y tế phải đồng chi trả. Ví dụ như là những phạm vi quyền lợi mà nó ngoài mức hưởng của bảo hiểm Các bạn hãy đăng ký kênh để ủng hộ kênh của mình nhé. Cảm ơn các bạn đã theo dõi. Cảm ơn các bạn đã theo dõi và hẹn gặp lại. Cảm ơn các bạn đã theo dõi. Câu hỏi tiếp theo thì chúng
[513.14 --> 521.00] Người nói 1: Tôi muốn đặt ra cho ông phúc ạ. Liệu thì cái mức thu bảo hiểm y tế có được điều chỉnh mức đóng theo thu
[521.00 --> 571.00] Người nói 6: Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Chứ nhất là duy trì những quyền lợi người bệnh đã đang được hưởng. Tiếp theo là chúng ta sẽ xem xét để điều chỉnh mở rộng thêm một số những Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Chính sách chúng ta cũng phải đánh giá cái tác động của các dịch vụ, của các quyền lợi khi mà chúng ta bổ sung thêm để làm sao chúng ta có thể Cảm ơn các bạn đã theo dõi.
[571.00 --> 581.00] Người nói 1: Các dịch vụ có giá cao trong bảo hiểm y tế có được mở rộng hay giới hạn hay đồng chi trả như trước đây ạ?
[581.00 --> 625.87] Người nói 6: Thì có một số dịch vụ có chi phí lớn rồi một số thuốc có chi phí lớn thì đang được quy định Là đồng chi trả, có thể là chi trả quỹ bảo vệnh tế chi trả là 70% có thể là 50% và một số thuốc có thể chi trả là 30% thế tới đây, khi mà đánh giá Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Để tăng thêm cái mức độ chi trả để người dân, người tham gia vệnh y tế có thể tiếp cận tốt hơn đối với những cái dịch vụ y tế đó cũng như là đối với Các bạn hãy đăng ký kênh để ủng hộ kênh của chúng mình nhé.
[626.40 --> 636.40] Người nói 1: Vậy thì thưa ông phúc ạ, khi mở rộng quyền lợi của người tham gia vào hiểm y tế thì liệu có cần phải điều chỉnh mức thu để chúng ta có thể cân bằng nguồn quỹ hay không?
[636.40 --> 713.67] Người nói 6: Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Cái người đi khám triệu bệnh về nguyên tế cũng giả, tuy nhiên đến năm 2023 thì số lượt khám triệu bệnh trong 6 tháng đầu năm đã tăng lên cỡ khoảng Gần 40% so với năm 2022 và cái số chi cũng đã tăng trên 30% so với cùng kỳ của năm 2022 và nếu dự báo trong năm 2022 Thì số chi của chúng tôi cũng trong quỹ bảo vệnh y tế cỡ khoảng 120.000 tỷ và Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Cũng thấy rằng với cái mức độ khám chữa bệnh như hiện nay thì quỹ bản y tế cũng đã khó để cân đối trong năm do vậy khi chúng ta điều chỉnh Cái quyền lợi của người tham gia bởi hành y tế thì rõ ràng chúng ta phải xem xét đến việc điều chỉnh mức nóng bởi hành y tế
[714.09 --> 806.40] Người nói 5: Tôi xin phép được có thêm một ý kiến. Vâng Bên cạnh cái ý kiến của anh phúc, đấy là chúng ta cũng biết là cái không phải lúc nào mà chúng ta tăng quyền lợi là cũng nhất thiết phải tăng mức đóng. Bởi vì chúng ta thấy là nó phụ thuộc vào cái cân đối quỹ và cái phạm vi quyền lợi chúng ta mở rộng đấy nó tác động đến quỹ như thế nào. Ví dụ như tôi lấy ví dụ Chúng ta cho một số các dịch vụ sang lọc, trần đoán sớm một số bệnh để điều trị sớm thì chúng ta đánh giá tác động về chi phí hiệu quả đối với quỹ, chúng ta thấy rằng, mặc dù Chúng ta cho thêm một dịch vụ vào. Tuy nhiên thì chúng ta đánh giá tác động chung thì chúng ta thấy là. Ví dụ như tăng huyết áp. Chẳng hạn khi mà chúng ta đưa vào trần đoán sớm Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Mà ta cân đối được thì cũng không có nghĩa là ta bị mất cân đối quỹ vấn đề có tăng mức đóng hay không thì chúng ta thấy là trong suốt những năm qua quốc hội cho phép là chúng ta đến cái Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Vâng
[806.40 --> 846.40] Người nói 6: Một vấn đề nữa chúng tôi cũng rất muốn đề cập đến để cái giải pháp của chúng ta cũng đảm bảo được cái quân đối quỹ nó tốt hơn. Đó là Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Để giảm cái tình trạng người bệnh hiện nay đang phải đi lên tuyến trên rất nhiều nó vừa quá tải cho người bệnh vừa tăng cái chi phí lên chúng ta không biết là chỉ với Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn
[852.20 --> 867.41] Người nói 1: Hiện mức đóng bảo hiểm y tế tại nước ta được cho là thấp, nhưng mà quyền lợi được hưởng lại cao so với bảo hiểm y tế của một số quốc gia trong khu vực thực tế là có hàng trăm ngàn người Bệnh nhân này được chẩn đoán sốc
[869.89 --> 887.63] Người nói 7: Nhiễm khuẩn tổ chức Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Cảm ơn các bạn
[888.52 --> 892.20] Người nói 8: Đã theo dõi.
[892.20 --> 902.20] Người nói 9: Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn
[902.20 --> 905.61] Người nói 8: Hãy subscribe cho kênh ghiền mì
[906.58 --> 922.20] Người nói 7: Gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn
[923.22 --> 933.47] Người nói 10: Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Dù hiểu được lợi ích của
[934.22 --> 948.94] Người nói 7: Bảo hiểm y tế mang lại mỗi khi ốm đau, nhưng nhiều người trẻ lại chủ quan không quan tâm đến thẻ bảo hiểm y tế. Ví dụ như Bệnh nhân này bị tai nạn khi làm công nhân xây dựng dẫn đến đa chấn thương mới chỉ điều trị nội khoa
[949.13 --> 953.58] Người nói 8: Đã mất hơn 30 triệu. Nó thì ti phí không đủ. Vì không có thẻ bảo hiểm
[954.48 --> 977.16] Người nói 7: Y tế nên mọi chi phí phải tự lo. Các bác sĩ cho biết với những bệnh nhân có thẻ bảo hiểm y tế thì Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để
[978.19 --> 983.52] Người nói 8: Không bỏ lỡ những video hấp dẫn Cảm ơn các
[983.83 --> 991.06] Người nói 11: Bạn đã theo dõi và ủng hộ cho kênh lalaschool để không bỏ lỡ những video hấp dẫn
[992.20 --> 1002.20] Người nói 7: Với những bệnh nhân có thể bảo hiểm y tế, không chỉ có người bệnh yên tâm khi nằm viện mà bản thân các bác sĩ cũng phần nào yên tâm khi lựa chọn phương pháp và kỹ thuật điều trị cho người bệnh.
[1004.36 --> 1011.96] Người nói 1: Với mức đóng và mức hưởng hiện nay của người tham gia bảo hiểm y tế thì ông cho rằng nó đã phù hợp hay chưa ạ?
[1013.12 --> 1042.20] Người nói 12: Theo tình hình khám bệnh chữa bệnh tại bệnh vệnh y trung ương, chúng tôi cho rằng mức đóng bảo hiểm y tế và mức độ hưởng Cảm ơn các bạn đã theo dõi. Vâng
[1042.20 --> 1050.45] Người nói 1: Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video
[1050.94 --> 1192.20] Người nói 12: Hấp dẫn Cảm ơn các bạn đã theo dõi. Các bạn hãy đăng ký kênh để ủng hộ kênh của chúng mình nhé. Cảm ơn các bạn đã theo dõi và ủng hộ cho kênh lalaschool để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Mức nhu cầu hưởng và khả năng đóng của người bệnh để chúng ta đưa ra một con số hợp lý. Xong với đó để nâng cao chất lượng khám và điều trị cho Chúng tôi cũng mong là chúng ta sẽ sớm triển khai theo lộ trình tính đúng giá dịch vụ trong khám chữa bệnh. Nhưng mọi người biết là hiện nay với giá dịch vụ y tế mà đang thanh toán bảo hiểm y tế cho người bệnh thì chúng ta tính với tính 4 yếu tố trên tổng số chi Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Đó là cái chi phí về quản lý chi phí về gián tiếp rồi chi phí về đào tạo nghiên cứu khoa học, chuyển giao kỹ thuật nó cũng làm đến cái chất lượng và cái Cảm ơn các bạn đã theo dõi và hẹn gặp lại. Nó sẽ góp phần cho việc mà chúng ta đầu tư nâng cấp trang thiết bị, đào tạo can bộ, chuyển giao kỹ thuật. Theo đó thì chất lượng của dịch vụ khám bệnh cho bệnh nó sẽ tốt hơn. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Tạo ra một cái xã hội của chúng ta tốt đẹp hơn rất là nhiều. Dạ vâng, thưa bà trang có ý kiến cho rằng là chúng ta cũng cần phải cân nhắc việc mở rộng dịch vụ tri trạm bảo hiểm y tế đến mức hợp lý và phải có lụ trình
[1192.20 --> 1202.20] Người nói 1: Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn
[1203.47 --> 1315.61] Người nói 5: Tôi cho rằng là cái việc chúng ta tăng phạm vi quyền lợi thì chúng ta sẽ xem xét trong cái cân đối về mặt chi phí hiệu quả. Ví dụ như khi chúng ta tăng quyền lợi Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Chúng ta cũng thấy rằng là trong thời gian vừa qua, qua 14 năm thực hiện luật với cái mức đóng 4,5% như thế, chúng ta thấy là giá cả thì cũng đã có tăng. Cái thứ hai nữa là cái thu nhập của người dân cũng đã được cải thiện trong những năm vừa qua. Và cái thứ ba là chúng ta thấy rằng là để chăm sóc một cái dịch vụ Cảm ơn các bạn đã theo dõi và ủng hộ cho kênh lalaschool để không bỏ lỡ những video hấp dẫn Cảm ơn các bạn đã theo dõi. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Cảm ơn
[1315.70 --> 1342.20] Người nói 1: Các bạn đã theo dõi. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn
[1342.45 --> 1455.80] Người nói 6: Cảm ơn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Phương thức thanh toán. Một là thanh toán theo phí dịch vụ. Hai là thanh toán theo định xuất và ba là thanh toán theo chiều hợp bệnh. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Các nước đã không còn thực hiện nữa. Bởi vì phương thức thanh toán này thúc đẩy việc tăng cung các dịch vụ. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Tính minh mạch hơn, đó là thanh toán theo nhóm trần đoán đối với nội chú và chúng ta sẽ từng bước áp dụng cái thanh toán theo định xuất ở đây thì tại sao chúng ta Nói là thanh toán theo nhóm trần đoán tương đồng nó lại tạo nên cái minh bạch, bởi vì lúc đó cơ sở khám chứng bệnh cũng biết được rằng là đối với Những cái nhóm bệnh này, những cái trường hợp bệnh này thì được quỹ bảo hiểm y tế chi trả là bao nhiêu tiền. Và lúc đó các cơ sở khám chức bệnh sẽ phải tiết kiệm sẽ phải sử dụng hiệu Quả nhất cái nguồn mình có tôi nói. Ví dụ chẳng hạn để một cái trường hợp vào viện Thì cần làm những cái xét nghiệm gì rồi cần cái ngày điều trị của cái bệnh nhân đó như thế nào để mà hiệu quả nhất. Cơ sở khám chữa bệnh cũng nâng cao hơn Chất lượng điều trị, cái chất lượng trần đoán và điều trị lên. Và nếu tiết kiệm được trong cái số tiền mà mình được khoán thì rõ ràng là cơ sở khán chữa bệnh sẽ được lợi vào việc đó. Với cái
[1455.80 --> 1545.80] Người nói 5: Cảm ơn các bạn đã theo dõi. Cảm ơn các bạn đã theo dõi. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Cảm ơn các bạn đã theo dõi. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Cảm ơn các bạn đã theo dõi. Các vấn đề về quy trình chuyên môn về vấn đề là ban hành các quy định rồi vấn đề giám định để làm sao cho dù chúng ta áp dụng phương thức chẩn đoán nào Các bạn hãy đăng ký kênh để ủng hộ kênh của chúng mình nhé. Cả nhân công cả quản lý bên cạnh cái dịch vụ kỹ thuật và thuốc, nhưng đồng thời nữa là phải cân đối được quỹ bảo hiểm y tế thì đấy là một cái bài toán. Dạ. Vâng, còn Về phía biển nhiệt vụ
[1545.80 --> 1665.00] Người nói 12: Hãy subscribe Cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Cảm ơn các bạn đã theo dõi. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Các kỹ thuật cao trong trận đoán và điều trị đưa ra những các pháp đồ điều trị tiên tiến và phù hợp với lại sự phát triển chung của y học. Nước nhà và y học thế giới. Thế thì nó sẽ có những cái mà chúng ta cũng cần phải cân nhắc như chị trang nói là với các cơ sở y tế nếu mà chúng ta thanh toán chi phí khám giá bệnh theo cái Các cơ sở bệnh cũng sẽ bắt buộc xem xét chi phí và dễ dàng Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Các đơn vị cũng rất phải cân nhắc Cảm ơn các bạn đã theo dõi và ủng hộ cho kênh lalaschool để không bỏ lỡ những video hấp dẫn Cảm ơn các bạn đã theo dõi. Phát đổ tiên tiến các kỹ thuật mới, các vật tư, trang thiết bị mới, thuốc mới để vào phục vụ cho nâng cao sức khỏe của người dân. Thì có lẽ theo Vâng dùng làm sao cho phù
[1663.42 --> 1665.80] Người nói 8: Hợp
[1671.00 --> 1703.79] Người nói 1: Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp
[1706.02 --> 1726.87] Người nói 2: Hơn 2.000 giấy nghỉ hốm đã được trạm trường trạm y tế phương đông văn thị xã duy tiên, hà nam cấp cho công nhân tại một số khu công nghiệp của đông văn. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Đây là xin giấy ốm, mình cần gì
[1727.89 --> 1747.63] Người nói 8: Ốm đâu? Ở đây là mình cứ xin để hưởng bảo hiểm Thôi, mình cần gì ốm, tự lĩnh đồng mình, đừng có bệnh ốm. 4 hôm thì nó xin cho 4 ngày Người đến mua giấy nghỉ ốm phải mang
[1748.79 --> 1768.31] Người nói 2: Theo thẻ bảo hiểm y tế, mục đích để lập khống bệnh án, thanh toán tiền khả Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hà nam dưng thanh toán là 167 triệu đồng.
[1769.64 --> 1801.35] Người nói 13: Đối với trạm y tế phường đồng văn, cơ quan bảo hiểm xã hội tỉnh cũng đã tạm dừng thanh toán các trường hợp tỉnh, Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho
[1801.98 --> 1829.40] Người nói 2: Kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn
[1829.40 --> 1853.93] Người nói 14: Rất nhiều trường hợp mà chúng tôi đã phát hiện ra là mượn thẻ của người đã chết đi khám chữa bệnh hoặc là mượn thẻ rồi chết khi đi khám chữa bệnh rồi chết. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Đại diện trung tâm giám định bảo hiểm y tế
[1854.87 --> 1885.55] Người nói 2: Và thanh toán đa tuyến đề xuất để tránh tiền Nếu không hiệu quả thì không ký hợp đồng Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ
[1889.40 --> 1900.79] Người nói 1: Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe
[1901.22 --> 1970.66] Người nói 5: Cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Cảm ơn các bạn đã theo dõi và ủng hộ cho kênh lalaschool để không bỏ lỡ những video hấp dẫn Cảm ơn các bạn đã theo dõi. Các bạn hãy đăng ký kênh để ủng hộ kênh của chúng mình nhé. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Các bạn
[1970.83 --> 1989.40] Người nói 1: Hãy đăng ký kênh để ủng hộ kênh của chúng mình nhé. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn
[1989.40 --> 2049.40] Người nói 6: Cảm ơn các bạn đã theo dõi. Cảm ơn các bạn đã theo dõi và ủng hộ cho kênh lalaschool để không bỏ lỡ những video hấp dẫn Các bạn hãy đăng ký kênh để ủng hộ kênh của chúng mình nhé. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn
[2049.40 --> 2069.32] Người nói 1: Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Cho rằng là lạm dụng tương đối khó để có thể phát hiện ra. Đặc biệt là đối với những bệnh nhân nặng hoặc là cần có thêm xét nghiệm để chẩn đoán đúng bệnh. Vậy ý kiến của ông như thế nào?
[2069.40 --> 2149.09] Người nói 12: Tại bệnh viện y trung gương chúng tôi nói riêng và các bệnh viện chuyên khoa đầu ngành tuyến cuối thì hầu hết các bệnh nhân mà khi mà đến với các bệnh viện tuyến cuối Đầu ngành là những bệnh nhân nặng những bệnh nhân rất là hiểu, có nhiều cái căn bệnh hiểm nghèo, cần phải được quan tâm đặc biệt trong trường hợp cái bệnh nhân nặng thì các bác sĩ Các thầy thuốc sẽ cân nhắc để đưa ra những phát đồ, những chỉ định phù hợp. Bổ chức bình đơn, bình đơn, bình bệnh án để phát hiện ra và để phát hiện ra. Thống nhất phát đồ điều trị làm nào cho hạn chế sử dụng tức là làm nào chi phí ở mức độ rất là tiết kiệm, nhưng hiệu quả khám bệnh cho bệnh Điều trị thì lại là đạo. Hiện nay cơ quan mở hiểm xã hội triển khai cái quản lý bằng công nghệ thông tin. Các cái cổng thông tuyến với Cảm ơn các bạn đã theo dõi. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Các bạn hãy đăng ký kênh để ủng hộ kênh của chúng mình nhé.
[2156.98 --> 2167.61] Người nói 15: Mất tiền lại đều phát thuốc về uống. Đây là những lợi ích mà đồng bào người dân tục giao và tẩy tại xã quang minh và tây. Hãy subscribe cho kênh ghiền
[2168.30 --> 2179.39] Người nói 8: Mì gõ để không bỏ lỡ những video hấp dẫn Hiện tỷ lệ tham gia bảo hiểm y tế
[2179.83 --> 2194.41] Người nói 15: Tại xã quang minh mới đạt khoảng 85%. Trước đây có một cái thói quen là ưu Tiên để cấp
[2194.60 --> 2204.60] Người nói 16: Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn
[2204.60 --> 2224.60] Người nói 17: Các ban ngành đoàn thể cũng như là ban chỉ đạo của xã cũng cùng với phối hợp với trạm y tế là tuyên truyền để cho người dân bắt buộc là Người dân tại xã xuất lễ, cao lộc,
[2224.60 --> 2238.20] Người nói 15: Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Nếu mua bảo hiểm y tế cho cả gia đình cũng là một khoản
[2239.30 --> 2256.21] Người nói 18: Không nhỏ. Của vợ chồng là hết 1 triệu 300 mấy nghìn. Nếu mà nhà có mấy đứa con Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Mấy năm gần đây thì
[2256.21 --> 2267.77] Người nói 19: Mức độ thu nhập của bà con cũng giảm, cho nên là trong công tác Để giúp người dân có thể tham gia bảo hiểm y
[2268.33 --> 2292.09] Người nói 15: Tế, người dân khi mua bảo hiểm theo hộ gia đình có thể đặt Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Mua thẻ bảo hiểm y tế, đồng thời thường xuyên đến tận nhà, vận động, tuyên truyền cho người dân về những lợi ích khi tham gia bảo hiểm y tế
[2294.06 --> 2303.60] Người nói 1: Vâng, thưa ông phúc, hiện nay tỷ lệ người dân tham gia bảo hình y tế của chúng ta tương đối cao, tới 92%. Tuy nhiên thì vẫn còn khoảng 8% dân số chưa tham gia bảo hình y tế. Vậy thì
[2303.60 --> 2410.19] Người nói 6: Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Nhóm người thứ nhất là người tham gia bản nguy tế theo hộ nông lâm ngư diêm nghiệp có một sống trung bình thì cái tỷ lệ tham gia còn thấp hơn so với cái nhóm đối tượng khác Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Cái nhóm thứ hai đó là người tham gia bản y tế tại các hộ kinh doanh cá thể. Hiện nay thì cũng theo cái báo cáo thì có đến 5%. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Cái nhóm thứ 3 đó là tham gia, bởi vì theo hộ gia đình chúng ta cũng biết là hiện tại thì trong những cái năm gần đây thì thấy Người tham gia theo hộ gia đình đã tăng rất nhiều. Tuy nhiên thì vẫn còn một bộ phận là chưa tham gia. Tỷ lệ tham gia bởi một tế học sinh hiện nay, học sinh viên hiện nay cũng chưa đạt Được 100% và trong đó thì chúng tôi xác định được là có nhiều sinh viên từ năm thứ 2 trở đi năm thứ 2, năm thứ 3 không tham gia bệnh vi tuế Thì đó là những nhóm đối tượng mà cũng cần phải tập trung để mà chúng ta có những giải pháp kết hợp để tăng độ bao phủ mệnh vi tế đảm bảo được. Lộ trình tham gia bệnh viện y tế đến năm 2025 là khoảng 95%. Thưa bà trang, mục
[2410.27 --> 2420.73] Người nói 1: Tiêu của chúng ta cũng tương đối rõ ra Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ
[2421.12 --> 2499.34] Người nói 5: Những video hấp dẫn Cảm ơn các bạn đã theo dõi. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Cảm ơn các bạn đã theo dõi. Cảm Ơn các bạn đã theo dõi. Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không
[2499.83 --> 2536.57] Người nói 1: Bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Hãy subscribe cho kênh ghiền mì gõ để không bỏ lỡ những video hấp dẫn Cảm ơn quý vị Cảm ơn các
```

### Tham chiếu (Reference)

```
[
  {
    "start": 18.5,
    "end": 24.3,
    "speaker": "Người nói 1",
    "text": "Xin kính chào và cảm ơn quý vị đang theo dõi chương trình tọa đàm Mở rộng quyền lợi của người tham gia bảo hiểm y tế."
  },
  {
    "start": 25,
    "end": 43.6,
    "speaker": "Người nói 1",
    "text": "Bảo hiểm xã hội và bảo hiểm y tế là hai chính sách xã hội quan trọng, là trụ cột chính của hệ thống an sinh xã hội, góp phần thực hiện tiến bộ và công bằng xã hội, đảm bảo ổn định chính trị xã hội và phát triển kinh tế xã hội. Việc thực hiện đã đạt được nhiều kết quả tích cực cả về độ bao phủ, quyền lợi người tham gia bảo hiểm y tế và chất lượng khám chữa bệnh."
  },
  {
    "start": 44.2,
    "end": 58.7,
    "speaker": "Người nói 1",
    "text": "Tỷ lệ bao phủ bảo hiểm y tế đã ở mức cao. Hiện nay đã có trên 92% dân số tham gia bảo hiểm y tế. Các quy định về phạm vi quyền lợi, mức hưởng bảo hiểm y tế về cơ bản đã đáp ứng được nhu cầu của nhân dân trong bảo vệ và chăm sóc sức khỏe."
  },
  {
    "start": 59.4,
    "end": 81.3,
    "speaker": "Người nói 1",
    "text": "Tuy nhiên, Luật Bảo hiểm y tế vẫn còn những hạn chế nhất định như chưa đáp ứng hết nhu cầu của nhân dân trong chăm sóc sức khỏe, phạm vi quyền lợi đối với một số lĩnh vực còn hạn chế. Để chính sách bảo hiểm y tế ngày càng hoàn thiện, đáp ứng hơn nữa nhu cầu chăm sóc, bảo vệ sức khỏe nhân dân, Bộ Y tế đang chủ trì xây dựng Luật Bảo hiểm y tế sửa đổi."
  },
  {
    "start": 82.2,
    "end": 100.8,
    "speaker": "Người nói 1",
    "text": "Vậy thì việc sửa đổi này sẽ làm thay đổi phạm vi quyền lợi của người tham gia bảo hiểm y tế như thế nào? Và đây sẽ là chủ đề của chương trình tọa đàm của chúng tôi với ba vị khách mời đến từ cơ quan xây dựng chính sách, cơ quan tổ chức thực hiện chính sách và cơ sở cung ứng dịch vụ khám chữa bệnh bảo hiểm y tế."
  },
  {
    "start": 101.4,
    "end": 114.7,
    "speaker": "Người nói 1",
    "text": "Xin được trân trọng giới thiệu: Bà Trần Thị Trang, Quyền Vụ trưởng Vụ Bảo hiểm y tế, Bộ Y tế; Ông Lê Văn Phúc, Trưởng ban Thực hiện chính sách bảo hiểm y tế, Bảo hiểm xã hội Việt Nam; Ông Trịnh Ngọc Hải, Phó Giám đốc Bệnh viện Nhi Trung ương."
  },
  {
    "start": 115.5,
    "end": 118.9,
    "speaker": "Người nói 1",
    "text": "Vâng, xin được trân trọng cảm ơn các vị khách mời đã nhận lời tham gia chương trình với chúng tôi."
  },
  {
    "start": 120.3,
    "end": 150.8,
    "speaker": "Người nói 1",
    "text": "Thưa quý vị, sau 13 năm thực hiện Luật Bảo hiểm y tế đầu tiên và sau 8 năm triển khai thực hiện Luật Bảo hiểm y tế sửa đổi thì nhiều quy định của Luật đã không còn phù hợp với sự phát triển kinh tế xã hội, nhiều vấn đề mới phát sinh trong thực tiễn. Vì vậy, nếu không bổ sung sửa đổi toàn diện đạo luật quan trọng này thì sẽ không khắc phục được những hạn chế rồi khó khăn và đáp ứng được nhu cầu thực tiễn trong thực hiện chính sách bảo hiểm y tế. Luật Bảo hiểm y tế được dự kiến sửa đổi bổ sung năm nhóm chính sách lớn. Từ năm 2018 thì đã có nhiều ý kiến đóng góp vào dự thảo Luật Bảo hiểm y tế sửa đổi."
  },
  {
    "start": 154.1,
    "end": 178.5,
    "speaker": "Người nói 2",
    "text": "Luật Bảo hiểm y tế sửa đổi dự kiến điều chỉnh năm nhóm chính sách lớn, đó là mở rộng đối tượng tham gia, mở rộng phạm vi quyền lợi, đa dạng loại hình cơ sở cung ứng dịch vụ y tế, tăng cường chăm sóc sức khỏe ban đầu tại tuyến cơ sở; đảm bảo tính minh bạch, công khai, hiệu quả và trách nhiệm giải trình của cơ quan cung ứng dịch vụ và cơ quan bảo hiểm xã hội trong hoạt động giám định bảo hiểm y tế, nâng cao hiệu quả quản lý và sử dụng quỹ."
  },
  {
    "start": 181.2,
    "end": 196.8,
    "speaker": "Người nói 2",
    "text": "Một số ý kiến cho rằng việc chi trả bảo hiểm y tế cho dự phòng, sàng lọc phát hiện sớm các bệnh mãn tính là điều hết sức cần thiết. Điều này sẽ giảm nhẹ gánh nặng chi tiêu từ tiền túi của người dân cũng như quỹ bảo hiểm y tế."
  },
  {
    "start": 197.3,
    "end": 218.4,
    "speaker": "Người nói 3",
    "text": "Kinh nghiệm của nhiều nước trên thế giới thì người ta đã mở rộng cái quyền lợi bảo hiểm y tế bên cạnh việc khám bệnh, chữa bệnh thì có cả việc quản lý sức khỏe cá nhân, sàng lọc chẩn đoán sớm một số bệnh trong cộng đồng và thậm chí có những quốc gia người ta còn chi trả cho một số dịch vụ y tế mang tính chất dự phòng cộng đồng nữa."
  },
  {
    "start": 218.8,
    "end": 233.5,
    "speaker": "Người nói 4",
    "text": "Nếu mà chúng ta sàng lọc trong cái giai đoạn đầu, giai đoạn mới thì tốn rất ít tiền, nó lại vừa lợi cho cả người dân, lợi cho cả quỹ bảo hiểm và cái quan trọng nhất tính nhân văn đó là giữ được tính mạng con người."
  },
  {
    "start": 234.1,
    "end": 253.3,
    "speaker": "Người nói 2",
    "text": "Liên quan đến đề xuất mua bảo hiểm y tế bổ sung, một số ý kiến cho rằng điều này là cần thiết, tuy nhiên phải xây dựng gói quyền lợi, danh mục và mức độ thanh toán rõ ràng. Cũng có quan điểm cho rằng bảo hiểm y tế là bảo hiểm y tế xã hội nên mức đóng và hưởng giống nhau. Vấn đề cần làm rõ là thanh toán cho các cơ sở y tế đã ký hợp đồng với bảo hiểm xã hội."
  },
  {
    "start": 253.8,
    "end": 266,
    "speaker": "Người nói 4",
    "text": "Tôi lấy ví dụ như là khi các cơ sở y tế người ta sử dụng nó quá so với lại những cái năm trước độ 5, 7 tỉ chẳng hạn, hoặc độ 10, 15% chẳng hạn, thì trong Luật chúng ta cũng phải quy định rõ."
  },
  {
    "start": 266.3,
    "end": 284.9,
    "speaker": "Người nói 4",
    "text": "Là cái cơ quan quỹ bảo hiểm y tế ông phải ứng trước cho người ta bao nhiêu phần trăm cái số đó và sau bao lâu thì ông phải quyết toán dứt điểm, ông không thể để dây dưa từ giăm ba năm sau vẫn còn dây dưa, nhưng tôi nghĩ như thế là không hợp lý."
  },
  {
    "start": 285.5,
    "end": 313.2,
    "speaker": "Người nói 3",
    "text": "Khó khăn trong việc thanh quyết toán chi phí ảnh hưởng đến hoạt động của cơ sở khám bệnh chữa bệnh cũng như là phần nào ảnh hưởng đến quyền lợi của người tham gia bảo hiểm y tế và nó có thể ảnh hưởng đến cái việc phát triển cái lĩnh vực chăm sóc sức khỏe xét về cả mặt chuyên môn kỹ thuật cũng như là cái phạm vi quyền lợi của người tham gia bảo hiểm y tế."
  },
  {
    "start": 313.8,
    "end": 328.6,
    "speaker": "Người nói 2",
    "text": "Các chuyên gia nhấn mạnh việc mở rộng quyền lợi bảo hiểm y tế là cần thiết nhưng cần tính đến phạm vi, danh mục dịch vụ và khả năng chi trả của quỹ bảo hiểm y tế."
  },
  {
    "start": 329.1,
    "end": 342.3,
    "speaker": "Người nói 1",
    "text": "Vâng vấn đề đặt ra đầu tiên đó là xác định rõ phạm vi quyền lợi của người tham gia bảo hiểm y tế. À thưa bà Trang, vậy thì trong Luật sửa đổi lần này thì phạm vi và quyền lợi của người tham gia bảo hiểm y tế sẽ được mở rộng như thế nào ạ?"
  },
  {
    "start": 343.1,
    "end": 368.5,
    "speaker": "Người nói 5",
    "text": "Hiện nay thì chúng tôi đang thiết kế theo hướng là sẽ đề xuất mở rộng phạm vi quyền lợi được hưởng trong phạm vi mức hưởng và mức đóng của người tham gia bảo hiểm y tế đối với một số các cái dịch vụ. Ví dụ như là sàng lọc chẩn đoán sớm một số các bệnh, đặc biệt là những cái bệnh mà khi mà đưa vào bảo hiểm y tế thanh toán thì nó sẽ có cái hiệu quả rất là cao so với việc là khi phát hiện muộn rồi thì cái chi phí cho quỹ bảo hiểm y tế nó sẽ tăng cái gánh nặng cao hơn."
  },
  {
    "start": 369.2,
    "end": 381.1,
    "speaker": "Người nói 5",
    "text": "Cái thứ hai nữa là cho việc hỗ trợ một số các cái dụng cụ phục hồi chức năng cho cái người khuyết tật hoặc là người phục hồi chức năng."
  },
  {
    "start": 382.2,
    "end": 408.8,
    "speaker": "Người nói 5",
    "text": "Cái thứ ba là liên quan đến vấn đề khám chẩn đoán trước sinh rồi là một số các dịch vụ khám bệnh chữa bệnh tại nhà cho người khuyết tật nặng hoặc là cái người mà không thể đến cái cơ sở khám bệnh chữa bệnh và một số các cái dịch vụ khác và cái dinh dưỡng sử dụng trong điều trị. Thì đấy là một số các cái phạm vi mà chúng tôi dự kiến đang thiết kế để đưa ra lấy ý kiến."
  },
  {
    "start": 409.4,
    "end": 420.1,
    "speaker": "Người nói 1",
    "text": "Dạ vâng, có hai loại hình đó là bảo hiểm y tế và bảo hiểm y tế bổ sung mới được đưa vào dự thảo Luật sửa đổi. Vậy thì hai loại hình này sẽ được sắp xếp theo các nhóm đối tượng như thế nào ạ?"
  },
  {
    "start": 421.1,
    "end": 443.2,
    "speaker": "Người nói 5",
    "text": "Bảo hiểm y tế mà chúng ta đang thực hiện theo quy định hiện hành thì là bảo hiểm mang tính chất xã hội, chia sẻ rủi ro, phi lợi nhuận. Và trên cái nguyên tắc là thực hiện cái mục tiêu đó thì không phân biệt về cái mức đóng cũng như là cái phạm vi được hưởng mà mọi người thì đều có cái quyền được cái hưởng trong cái phạm vi quyền lợi và mức chi trả như nhau."
  },
  {
    "start": 444.4,
    "end": 469.7,
    "speaker": "Người nói 5",
    "text": "Tuy nhiên, đối với bảo hiểm y tế bổ sung thì sẽ là một cái chính sách bảo hiểm y tế mà những người tham gia bảo hiểm y tế bắt buộc rồi thì sẽ tham gia cái bảo hiểm y tế bổ sung. Và cái thứ hai nữa là đây là một cái hình thức tự nguyện. Vâng, thứ ba là bảo hiểm y tế bổ sung thì sẽ có những cái gói quyền lợi chi trả ngoài phạm vi của bảo hiểm y tế đang chi trả, ví dụ như là phần đồng chi trả mà người có thẻ bảo hiểm y tế phải đồng chi trả."
  },
  {
    "start": 470.8,
    "end": 514.8,
    "speaker": "Người nói 5",
    "text": "Ví dụ như là những cái phạm vi quyền lợi mà nó ngoài cái mức hưởng của bảo hiểm y tế, rồi một số những cái giá trị gia tăng cao hơn, ví dụ như là được lựa chọn cái cơ sở, lựa chọn các cái thầy thuốc hoặc là những cái thuốc mà có cái tỉ lệ chi trả nó cao hơn. Thì đấy là những cái đặc thù riêng của bảo hiểm y tế bổ sung. Và đây là một cái hình thức được thực hiện trên nền tảng là chúng ta phải có cái bảo hiểm y tế xã hội rồi, tức là bắt buộc rồi thì mới tham gia thêm cái bảo hiểm y tế bổ sung. Và cái nội dung của bảo hiểm y tế bổ sung là được thiết kế để bảo đảm rằng là những cái người mà có cái mức thu nhập trung bình trong xã hội cũng có thể có điều kiện để tham gia được bảo hiểm y tế bổ sung và cũng trên cái cơ sở là có sự chia sẻ rủi ro giữa những người tham gia bảo hiểm y tế bổ sung."
  },
  {
    "start": 515.5,
    "end": 524.1,
    "speaker": "Người nói 1",
    "text": "Dạ vâng, câu hỏi tiếp theo thì chúng tôi muốn đặt ra cho ông Phúc ạ. Liệu thì cái mức thu bảo hiểm y tế có được điều chỉnh mức đóng theo thu nhập và giới hạn dịch vụ hay không thưa ông?"
  },
  {
    "start": 525.1,
    "end": 538.2,
    "speaker": "Người nói 6",
    "text": "Chúng tôi thấy rằng trong cái lần sửa đổi Luật bảo hiểm y tế này thì chúng ta vẫn duy trì, trước hết là duy trì những cái quyền lợi đã người bệnh đã đang được hưởng."
  },
  {
    "start": 539.3,
    "end": 567.8,
    "speaker": "Người nói 6",
    "text": "Tiếp theo là chúng ta sẽ xem xét để điều chỉnh mở rộng thêm một số những quyền lợi như bà Trang cũng vừa trao đổi. Tất nhiên để mà đảm bảo được cái khả năng chi trả của quỹ bảo hiểm y tế, trước hết thì chúng ta khi mà xây dựng chính sách chúng ta cũng phải đánh giá cái tác động của các dịch vụ, của các quyền lợi khi mà chúng ta bổ sung thêm để làm sao chúng ta có thể căn cứ vào đó để có thể điều chỉnh cái mức đóng bảo hiểm y tế phù hợp khi mà chúng ta mở rộng cái quyền lợi bảo hiểm y tế."
  },
  {
    "start": 568.5,
    "end": 581.5,
    "speaker": "Người nói 1",
    "text": "Vâng, có một ý như thế này của khán giả gửi đến chương trình và cũng rất mong ông Phúc giải đáp giúp, đó là các dịch vụ có giá cao trong bảo hiểm y tế thì có được mở rộng hay là giới hạn hay là đồng chi trả như trước đây ạ?"
  },
  {
    "start": 582.5,
    "end": 599.4,
    "speaker": "Người nói 6",
    "text": "Hiện tại thì có một số dịch vụ cái chi phí lớn, rồi một số thuốc có chi phí lớn thì đang được quy định là đồng chi trả, có thể là chi trả quỹ bảo hiểm y tế chi trả là 70%, có thể là 50% và một số thuốc có thể chi trả là 30%."
  },
  {
    "start": 600,
    "end": 625.5,
    "speaker": "Người nói 6",
    "text": "Thế tới đây khi mà đánh giá lại toàn bộ và nếu quỹ bảo hiểm y tế còn đủ khả năng để chi trả thì trong cái lần sửa đổi này chúng ta cũng sẽ có những cái điều chỉnh để tăng thêm cái mức độ chi trả để người dân người tham gia bảo hiểm y tế có thể tiếp cận tốt hơn đối với những cái dịch vụ y tế đó cũng như là đối với những cái thuốc mà hiện nay đang bị giới hạn cái phần đồng chi trả."
  },
  {
    "start": 626.5,
    "end": 636.5,
    "speaker": "Người nói 1",
    "text": "À vậy thì thưa ông Phúc ạ, vậy thì khi mà mở rộng quyền lợi của người tham gia bảo hiểm y tế thì liệu có cần phải điều chỉnh mức thu để chúng ta có thể cân bằng cái nguồn quỹ hay không?"
  },
  {
    "start": 637.3,
    "end": 651.8,
    "speaker": "Người nói 6",
    "text": "Trong năm 2021, 2020, 21, 22 thì quỹ bảo hiểm y tế tạm thời là cân đối được. Có nghĩa là phần thu trong năm và đủ để cho chi trong năm."
  },
  {
    "start": 652.5,
    "end": 673.2,
    "speaker": "Người nói 6",
    "text": "Tuy nhiên chúng ta cũng biết là những năm 20, 21, 22 thì chúng ta vướng vào dịch bệnh COVID, cái người đi khám chữa bệnh bảo hiểm y tế cũng giảm. Tuy nhiên đến năm 2023 thì số lượt khám chữa bệnh trong 6 tháng đầu năm đã tăng lên cỡ khoảng gần 40% so với năm 2022 và cái số chi cũng đã tăng trên 30% so với cùng kỳ của năm 22."
  },
  {
    "start": 674.3,
    "end": 689.5,
    "speaker": "Người nói 6",
    "text": "Và nếu dự báo trong năm 2023 thì số chi của chúng tôi cũng trong quỹ bảo hiểm y tế cỡ khoảng 120.000 tỉ. Và như vậy đối chiếu với cả cái dự kiến mà thu được thì đâu đó cũng sẽ bị bội chi một chút so với cái số thu được."
  },
  {
    "start": 690.3,
    "end": 713.8,
    "speaker": "Người nói 6",
    "text": "Như vậy chúng ta cũng thấy rằng với cái mức độ khám chữa bệnh như hiện nay thì quỹ bảo hiểm y tế cũng đã khó để cân đối trong năm. Do vậy khi chúng ta điều chỉnh cái quyền lợi của người tham gia bảo hiểm y tế thì rõ ràng chúng ta phải xem xét đến việc điều chỉnh mức đóng bảo hiểm y tế."
  },
  {
    "start": 714.6,
    "end": 733.3,
    "speaker": "Người nói 5",
    "text": "Tôi xin phép được có thêm một ý kiến bên cạnh cái ý kiến của anh Phúc. Đấy là chúng ta cũng biết là cái không phải lúc nào mà chúng ta tăng quyền lợi là cũng nhất thiết phải tăng mức đóng. Bởi vì chúng ta thấy là nó phụ thuộc vào cái cân đối quỹ và cái phạm vi quyền lợi chúng ta mở rộng đấy nó tác động đến quỹ như thế nào."
  },
  {
    "start": 734.5,
    "end": 750.8,
    "speaker": "Người nói 5",
    "text": "Ví dụ như tôi lấy ví dụ, nếu chúng ta cho một số các cái dịch vụ sàng lọc chẩn đoán sớm một số bệnh để điều trị sớm thì chúng ta đánh giá tác động về chi phí hiệu quả đối với quỹ chúng ta thấy rằng mặc dù chúng ta cho thêm một dịch vụ vào."
  },
  {
    "start": 751.2,
    "end": 773.5,
    "speaker": "Người nói 5",
    "text": "Tuy nhiên thì chúng ta đánh giá tác động chung thì chúng ta thấy là ví dụ như tăng huyết áp chẳng hạn, khi mà chúng ta đưa vào chẩn đoán sớm và có thể điều trị dự phòng sớm, chúng ta sẽ tiết kiệm được cái khoản chi phí tiền thuốc, tiền dịch vụ kỹ thuật, tiền giường, thậm chí là chi tiền túi của người dân do các bệnh ví dụ như tim mạch, đột quỵ mà hiện nay nó cũng làm gia tăng cái chi phí của cái quỹ bảo hiểm y tế đang chi cho các cái bệnh này."
  },
  {
    "start": 774.5,
    "end": 780.8,
    "speaker": "Người nói 5",
    "text": "Vậy thì nếu cho ta cho một cái dịch vụ chẩn đoán sớm vào mà ta cân đối được thì cũng không có nghĩa là ta bị mất cân đối quỹ."
  },
  {
    "start": 781.4,
    "end": 804.8,
    "speaker": "Người nói 5",
    "text": "Vấn đề có tăng mức đóng hay không thì chúng ta thấy là trong suốt những năm qua Quốc hội cho phép là chúng ta đến cái mức đóng tối đa là 6% mức lương, thế nhưng mà chúng ta mới đến cái dư địa là 4,5%. Như vậy chúng ta còn 1,5% nữa mà chúng ta còn chưa tăng. Cho nên chúng tôi nghĩ rằng vẫn có cái phạm vi để chúng ta có thể là bảo đảm là mở rộng được cái quyền lợi cho người tham gia bảo hiểm y tế."
  },
  {
    "start": 805.5,
    "end": 820.3,
    "speaker": "Người nói 6",
    "text": "Vâng chúng ta phải tính toán rất là kỹ. Vâng, một vấn đề nữa chúng tôi cũng rất muốn đề cập đến để cái giải pháp của chúng ta cũng đảm bảo được cái cân đối quỹ nó tốt hơn. Đó là chúng ta có thể tổ chức lại cái việc khám chữa bệnh bảo hiểm y tế."
  },
  {
    "start": 821.5,
    "end": 846.8,
    "speaker": "Người nói 6",
    "text": "Chúng ta sẽ tăng cường hơn nữa cái việc khám chữa bệnh tại y tế cơ sở. Tức là chúng ta chăm sóc người bệnh ngay từ tuyến y tế cơ sở để giảm cái tình trạng người bệnh hiện nay đang phải đi lên tuyến trên rất nhiều. Nó vừa quá tải cho người bệnh vừa tăng cái chi phí lên. Chúng ta cũng biết là chỉ với 3% cái số người khám chữa bệnh tại tuyến trên, tuyến Trung ương nhưng cái chi phí đã là chiếm hơn 20% tổng chi phí y tế hiện tại là quỹ bảo hiểm y tế đang chi trả."
  },
  {
    "start": 851.5,
    "end": 863.3,
    "speaker": "Người nói 2",
    "text": "Hiện mức đóng bảo hiểm y tế tại nước ta được cho là thấp nhưng quyền lợi được hưởng là cao so với bảo hiểm y tế của một số quốc gia trong khu vực. Thực tế là có hàng trăm ngàn người sẵn sàng đóng bảo hiểm y tế ở mức cao hơn để hưởng các dịch vụ kỹ thuật tốt hơn."
  },
  {
    "start": 868.5,
    "end": 888.5,
    "speaker": "Người nói 2",
    "text": "Bệnh nhân này được chẩn đoán sốc nhiễm khuẩn, tổn thương phổi, dẫn đến suy đa phủ tạng phải lọc máu, thở máy. Đồng thời phải sử dụng nhiều loại thuốc kháng sinh thế hệ mới. Theo tính toán, mỗi ngày bệnh nhân sẽ phải chi trả ít nhất 20 triệu đồng. Tuy nhiên các khoản chi phí này đã được bảo hiểm y tế thanh toán 80%."
  },
  {
    "start": 889.3,
    "end": 903.6,
    "speaker": "Người nói 7",
    "text": "Nhiều bệnh nhân là không có bảo hiểm, mà với chi phí cao thì người nhà là rất khó khăn trong cái việc mà chi trả. Mà nếu mà có bảo hiểm thì rất là thuận lợi vì chúng tôi cũng mạnh dạn hơn trong quá trình điều trị."
  },
  {
    "start": 906.5,
    "end": 922.8,
    "speaker": "Người nói 2",
    "text": "May mắn là điều mà bệnh nhân này nói về việc tham gia bảo hiểm y tế. Một năm trước, anh thấy sức khỏe yếu khi đi khám được chẩn đoán suy thận và phải chạy thận chu kỳ tuần 3 buổi. Vì mới tham gia bảo hiểm y tế nên tháng đầu anh đã phải chi trả 12 triệu đồng."
  },
  {
    "start": 923.3,
    "end": 933.2,
    "speaker": "Người nói 8",
    "text": "Nếu như mà không có bảo hiểm ấy thì với cái điều kiện của tôi là một nách hai con ấy thật sự nó là một gánh nặng. Với cái bệnh này sức khỏe đã không còn nữa."
  },
  {
    "start": 934.1,
    "end": 950.2,
    "speaker": "Người nói 2",
    "text": "Dù hiểu được lợi ích của bảo hiểm y tế mang lại mỗi khi ốm đau nhưng nhiều người trẻ lại chủ quan không quan tâm đến thẻ bảo hiểm y tế. Ví dụ như bệnh nhân này bị tai nạn khi làm công nhân xây dựng dẫn đến đa chấn thương mới chỉ điều trị nội khoa đã mất hơn 30 triệu."
  },
  {
    "start": 951,
    "end": 953.5,
    "speaker": "Người nói 9",
    "text": "Lo vì chi phí không đủ để làm phẫu thuật."
  },
  {
    "start": 954.2,
    "end": 958.8,
    "speaker": "Người nói 2",
    "text": "Vì không có thẻ bảo hiểm y tế nên mọi chi phí phải tự lo."
  },
  {
    "start": 959.3,
    "end": 977.8,
    "speaker": "Người nói 2",
    "text": "Các bác sĩ cho biết với những bệnh nhân có thẻ bảo hiểm y tế thì việc điều trị sẽ dễ dàng hơn vì hầu hết các chi phí đã được bảo hiểm thanh toán. Bác sĩ có thể chỉ định làm các xét nghiệm cận lâm sàng, xét nghiệm và sử dụng các loại thuốc tốt. Nhưng với những trường hợp không có thẻ bảo hiểm thì sẽ phải cân nhắc và dựa trên khả năng của gia đình."
  },
  {
    "start": 978.5,
    "end": 983.8,
    "speaker": "Người nói 7",
    "text": "Trên một bệnh nhân có bảo hiểm hay không bảo hiểm thì tất nhiên là trên một cái nữa thì bác sĩ cũng sẽ yên tâm hơn."
  },
  {
    "start": 984.3,
    "end": 993.2,
    "speaker": "Người nói 7",
    "text": "Với những bệnh nhân mà không được bảo hiểm y tế thanh toán cái điều trị đối với bệnh nhân cũng như là những cái gánh nặng về mặt kinh tế đối với người nhà bệnh nhân là rất lớn."
  },
  {
    "start": 993.8,
    "end": 1003.5,
    "speaker": "Người nói 2",
    "text": "Với những bệnh nhân có thẻ bảo hiểm y tế không chỉ có người bệnh yên tâm khi nằm viện mà bản thân các bác sĩ cũng phần nào yên tâm khi lựa chọn phương pháp và kỹ thuật điều trị cho người bệnh."
  },
  {
    "start": 1004.2,
    "end": 1012.3,
    "speaker": "Người nói 1",
    "text": "Vâng, thưa ông Hải, với mức đóng và mức hưởng hiện nay của người tham gia bảo hiểm y tế thì ông cho rằng là nó đã phù hợp hay chưa?"
  },
  {
    "start": 1013.3,
    "end": 1026.5,
    "speaker": "Người nói 10",
    "text": "Theo cái tình hình khám bệnh chữa bệnh tại Bệnh viện Nhi Trung ương chúng tôi thì chúng tôi cho rằng là cái mức đóng bảo hiểm y tế và cái mức độ hưởng về bảo hiểm y tế của bệnh nhân hiện nay là cơ bản là phù hợp."
  },
  {
    "start": 1027.3,
    "end": 1041.8,
    "speaker": "Người nói 10",
    "text": "Để đáp ứng được cái nhu cầu của người dân và các cái kỹ thuật mới và các cái phương án phác đồ điều trị mới thì có lẽ chúng ta cũng phải đến lúc cũng phải điều chỉnh lại cái mức đóng cho nó phù hợp với lại cái nhu cầu và cái thực tế chi trả bảo hiểm y tế của người dân hiện nay."
  },
  {
    "start": 1042.3,
    "end": 1050.8,
    "speaker": "Người nói 1",
    "text": "Vâng, vậy thì theo ông thì cái ông đề xuất là cái mức điều chỉnh cho việc đóng và hưởng quyền lợi của từng nhóm đối tượng tham gia bảo hiểm y tế sẽ là như thế nào?"
  },
  {
    "start": 1051.5,
    "end": 1079.8,
    "speaker": "Người nói 10",
    "text": "Với một cái sự phát triển như chúng tôi đã báo cáo về mặt kinh tế xã hội như hiện nay thì có lẽ chúng ta cũng sẽ chia ra những cái mức khác nhau. Đấy các cái mức giá về bảo hiểm khác nhau để cho nó phù hợp với lại cái nền kinh tế cũng như là những cái điều kiện kinh tế của từng các cái tầng lớp dân cư khác nhau. Tôi nói ví dụ như cái số đối tượng mà thuộc về ngân sách nhà nước đóng thì chúng ta vẫn đảm bảo. Đối với như Trung ương thì cái trẻ em dưới 6 tuổi hiện nay là đã được đang được ngân sách nhà nước đóng bảo hiểm y tế thông qua quỹ bảo hiểm y tế."
  },
  {
    "start": 1080.3,
    "end": 1109.8,
    "speaker": "Người nói 10",
    "text": "Và cái mức mà như bà Trang và ông Phúc vừa nêu thì chúng tôi thấy rằng là trong thời gian tới thì chúng ta cũng cần phải đưa vào các cái quy định để mà nâng cái mức đóng bảo hiểm trên cơ sở cái mức nhu cầu hưởng và cái khả năng đóng của người bệnh để chúng ta đưa ra một con số hợp lý. Song song với đó thì để nâng cao cái chất lượng khám và điều trị cho bệnh nhân thì chúng tôi cũng mong là chúng ta sẽ sớm triển khai theo cái lộ trình tính đúng, tính đủ cái giá dịch vụ vào trong khám chữa bệnh."
  },
  {
    "start": 1110.3,
    "end": 1137.5,
    "speaker": "Người nói 10",
    "text": "Thì như mọi người biết là hiện nay thì với cái giá dịch vụ y tế mà đang thanh toán bảo hiểm y tế cho người bệnh thì chúng ta tính mới tính bốn yếu tố trên tổng số chín yếu tố ban đầu. Đó là cái tiền thuốc, vật tư, hóa chất, xét nghiệm, rồi máu, dịch truyền, tiền điện, tiền nước, tiền khử khuẩn, tiền xử lý môi trường, rồi tiền sửa chữa trang thiết bị và yếu tố nữa là tiền lương của cán bộ công nhân viên."
  },
  {
    "start": 1138.8,
    "end": 1175.8,
    "speaker": "Người nói 10",
    "text": "Thế còn lại các yếu tố mà cấu thành nên cái giá dịch vụ y tế nữa đó là cái chi phí về quản lý, chi phí về gián tiếp, rồi chi phí về đào tạo nghiên cứu khoa học, chuyển giao kỹ thuật. Đấy, nó cũng làm nên cái chất lượng và cái cái cái dịch vụ y tế. Thế còn chi phí về khấu hao trang thiết bị, về khấu hao hạ tầng cũng là rất là quan trọng để nếu mà chúng ta được tính cái đó thì nó sẽ góp phần cho cái việc mà chúng ta đầu tư nâng cấp trang thiết bị, đào tạo cán bộ, chuyển giao kỹ thuật. Theo đó thì cái chất lượng của dịch vụ khám bệnh chữa bệnh nó sẽ tốt hơn và ai là người được hưởng chính người bệnh là người được hưởng và những người mà tham gia bảo hiểm y tế là những người được hưởng."
  },
  {
    "start": 1176.5,
    "end": 1184.2,
    "speaker": "Người nói 10",
    "text": "Theo đó thì cái gánh nặng từ xã hội và từ gia đình nó cũng sẽ bớt đi và tạo nên một cái xã hội của chúng ta tốt đẹp hơn rất là nhiều."
  },
  {
    "start": 1185.5,
    "end": 1202.8,
    "speaker": "Người nói 1",
    "text": "Dạ vâng, thưa bà Trang, có ý kiến cho rằng là chúng ta cũng cần phải cân nhắc việc mở rộng dịch vụ chi trả bảo hiểm y tế đến mức hợp lý và phải có lộ trình phù hợp, lộ trình tính đúng, tính đủ như ông Hải vừa có chia sẻ và lộ trình tăng mức đóng bảo hiểm y tế, rồi lộ trình tăng quyền lợi của người tham gia bảo hiểm y tế. Vậy thì quan điểm của Bộ Y tế là như thế nào?"
  },
  {
    "start": 1203.5,
    "end": 1229.8,
    "speaker": "Người nói 5",
    "text": "Chúng tôi cho rằng là cái việc chúng ta tăng phạm vi quyền lợi thì chúng ta sẽ xem xét trong cái cân đối về mặt chi phí hiệu quả. Ví dụ như khi chúng ta tăng quyền lợi lên thì chúng ta phải tính đến các giải pháp. Thứ nhất là chúng ta có các giải pháp để phòng ngừa lạm dụng, trục lợi, kê chỉ định quá mức các dịch vụ kỹ thuật hay là chúng ta cũng phải tính tới cái giải pháp làm sao tổ chức công tác khám bệnh chữa bệnh tốt hơn, rồi cái tuyên truyền phòng bệnh cho người dân."
  },
  {
    "start": 1230.5,
    "end": 1257.5,
    "speaker": "Người nói 5",
    "text": "Rồi kể cả các vấn đề liên quan đến hoàn thiện các cái quy trình chuyên môn và các cái biện pháp khác. Sau đó chúng ta thấy rằng là gì, với một cái phạm vi mở rộng quyền lợi là cần thiết thì chúng ta sẽ tính tới là cái lộ trình để tăng mức đóng sau khi chúng ta đã thực hiện tất cả các giải pháp để bảo đảm sử dụng hiệu quả nhất quỹ bảo hiểm y tế mà chúng ta thấy rằng là vẫn cần phải có cái bổ sung cái nguồn thu của bảo hiểm y tế thì chúng ta sẽ tính tới vấn đề tăng mức đóng."
  },
  {
    "start": 1258.5,
    "end": 1295.5,
    "speaker": "Người nói 5",
    "text": "Và rõ ràng là chúng ta cũng phải tăng theo lộ trình. Và ở đây chúng ta cũng thấy rằng là trong thời gian vừa qua qua 14 năm thực hiện Luật với cái mức đóng 4,5% như thế, chúng ta thấy là giá cả thì cũng đã có tăng. Cái thứ hai nữa là cái thu nhập của người dân cũng đã được cải thiện trong những năm vừa qua. Và cái thứ ba là chúng ta thấy rằng là để chăm sóc một cái dịch vụ y tế tốt nhất chăm sóc cho người dân thì cái tính đúng tính đủ giá dịch vụ là một cái điều kiện tiên quyết để bảo đảm cả quyền lợi của người bệnh lẫn cái sự cung cấp dịch vụ có chất lượng của cơ sở y tế. Thế do đó mà cái mức đóng chúng ta phải làm sao đảm bảo được các yếu tố giữa là cái phạm vi quyền lợi, giữa cái vấn đề tính đúng tính đủ giá dịch vụ y tế, rồi các vấn đề khác trong cái việc hoàn thiện các cái quy định về khám bệnh chữa bệnh nói chung thì chúng ta sẽ xác định một cái mức đóng nó hợp lý để bảo đảm cân đối quỹ, bảo đảm được cái quyền của người bệnh, bảo đảm được cái cung cấp dịch vụ có chất lượng của cơ sở y tế."
  },
  {
    "start": 1296.5,
    "end": 1323.5,
    "speaker": "Người nói 1",
    "text": "Thưa ông Phúc, lâu nay thì chúng ta vẫn chủ yếu áp dụng cái phương thức thanh toán chi phí bảo hiểm y tế là theo giá dịch vụ, trong khi trên thế giới hiện nay thì bảo hiểm y tế sử dụng phương thức thanh toán là theo định suất đúng không ạ? Rồi thanh toán theo nhóm chẩn đoán liên quan. Vậy thì Luật Bảo hiểm y tế sửa đổi thì sẽ áp dụng thanh toán như thế nào để có thể đảm bảo quyền lợi, theo ông để có thể đảm bảo quyền lợi của cả ba bên đó là người tham gia bảo hiểm y tế rồi cơ quan bảo hiểm xã hội và cả bệnh viện?"
  },
  {
    "start": 1324.5,
    "end": 1352.2,
    "speaker": "Người nói 6",
    "text": "Chúng ta cũng biết là hiện tại tại Việt Nam chủ yếu là thực hiện phương thức thanh toán theo giá dịch vụ mà ta vẫn gọi là phí dịch vụ. Có nghĩa là cung ứng dịch vụ nào thì chi trả theo cái số lượng cũng như là đơn giá của dịch vụ đó. Luật Bảo hiểm y tế cũng đã quy định rõ là chúng ta có ba phương thức thanh toán. Một là thanh toán theo phí dịch vụ, hai là thanh toán theo định suất và ba là thanh toán theo trường hợp bệnh hay là thanh toán theo nhóm chẩn đoán liên quan như chúng ta vẫn nói."
  },
  {
    "start": 1353.5,
    "end": 1387.5,
    "speaker": "Người nói 6",
    "text": "Thế tuy nhiên thì hiện tại chúng ta cũng chưa xây dựng được hai phương thức thanh toán kia. Và đối với thanh toán theo giá dịch vụ hiện nay, chúng ta cũng biết là các nước đã không còn thực hiện nữa. Bởi vì sao? Bởi vì là cái phương thức thanh toán này nó thúc đẩy cái việc tăng cung các dịch vụ y tế và trong đó kể cả những cái dịch vụ y tế không cần thiết. Thì rõ ràng là chúng ta phải thay đổi cái phương thức thanh toán nó hiện đại hơn, nó đảm bảo được cái tính minh bạch hơn, đó là thanh toán theo nhóm chẩn đoán đối với nội trú và chúng ta sẽ từng bước áp dụng cái thanh toán theo định suất."
  },
  {
    "start": 1388.5,
    "end": 1414.5,
    "speaker": "Người nói 6",
    "text": "Ở đây thì tại sao chúng ta lại nói là thanh toán theo cái nhóm chẩn đoán tương đồng nó lại tạo nên cái minh bạch? Bởi vì lúc đó cơ sở khám chữa bệnh cũng biết được rằng là đối với những cái nhóm bệnh này, những cái trường hợp bệnh này thì được quỹ bảo hiểm y tế chi trả là bao nhiêu tiền. Và lúc đó các cơ sở khám chữa bệnh sẽ phải tiết kiệm, sẽ phải sử dụng hiệu quả nhất cái nguồn mình có. Tôi nói ví dụ chẳng hạn, để một cái trường hợp vào viện thì cần làm những cái xét nghiệm gì, rồi cần cái ngày điều trị của cái bệnh nhân đó như thế nào để mà hiệu quả nhất. Thì cơ sở khám chữa bệnh cũng nâng cao hơn cái chất lượng điều trị, cái chất lượng chẩn đoán và điều trị lên. Và nếu tiết kiệm được trong cái số tiền mà mình được khoán thì rõ ràng là cơ sở khám chữa bệnh sẽ được lợi ở việc đó."
  },
  {
    "start": 1415.8,
    "end": 1459.2,
    "speaker": "Người nói 5",
    "text": "Với cái phương thức thanh toán theo nhóm chẩn đoán, ví dụ như là DRG chẳng hạn, thì nó lại có một cái xu hướng ngược lại. Là bởi vì ta đã xác định khống chế một cái cái mức rồi, mức phí rồi. Cho nên là cơ sở khám bệnh chữa bệnh cũng có thể tôi lấy giả định thôi là sẽ chỉ định ít hơn các dịch vụ kỹ thuật, sẽ cho nhập viện ngắn hơn, rồi giảm các cái chi phí khác để làm giảm cái tổng chi của cơ sở y tế. Và như thế thì mới có cái khoản mà được lợi thêm như anh Phúc nói đúng không ạ? Tức là nó luôn luôn có hai cái xu hướng trái ngược nhau giữa hai cái phương thức này. Vậy thì bài toán là chúng ta phải sử dụng cả hai cái phương thức đó. Ví dụ như là phí dịch vụ đối với ngoại trú, đối với nội trú thì là theo DRG."
  },
  {
    "start": 1460.5,
    "end": 1504.8,
    "speaker": "Người nói 5",
    "text": "Rồi chúng tôi cũng tính đến một số các cái phương thức khác nữa làm sao để nó hài hòa nhất. Và chúng ta tìm ra được những cái nhược điểm của mỗi một phương thức để chúng ta phòng ngừa và hạn chế những các cái nhược điểm đấy bằng các cái cách thức khác trong cái quản lý giá, cũng như là bằng các cái vấn đề về quy trình chuyên môn, về vấn đề là ban hành các cái quy định, rồi vấn đề giám định để làm sao cho dù chúng ta áp dụng cái phương thức chẩn đoán nào thì cái lợi nhất vẫn là lợi cho người bệnh. Cơ sở y tế thì cũng phải bảo đảm để cung cấp được các cái dịch vụ mà đủ để chi trả những các cái chi phí bao gồm cả nhân công cả quản lý bên cạnh cái dịch vụ kỹ thuật và thuốc. Nhưng đồng thời nữa là phải cân đối được quỹ bảo hiểm y tế. Thì đấy là một cái bài toán."
  },
  {
    "start": 1505.5,
    "end": 1544.8,
    "speaker": "Người nói 10",
    "text": "Vâng tôi cũng rất là đồng tình và ủng hộ ý kiến của chị Trang và những nội dung mà anh Phúc nêu thì trong tương lai cũng như các nước trên thế giới người ta cũng đã áp dụng. Tuy nhiên là về phía đơn vị cung cấp dịch vụ là cái đơn vị mà khám bệnh chữa bệnh thì chúng tôi thấy là bất cứ một cái phương thức nào như chị Trang nói cũng có những cái mặt ưu và nhược điểm và chúng ta cần phải có một cái lộ trình triển khai và có một cái thí điểm đánh giá sau đó thì mới triển khai rộng. Chúng ta làm như thế nào nhưng mà vẫn phải triển khai được các kỹ thuật mới, các kỹ thuật cao trong chẩn đoán và điều trị, đưa ra những các cái phác đồ điều trị tiên tiến và phù hợp với lại cái sự phát triển chung của y học nước nhà và y học thế giới."
  },
  {
    "start": 1551.5,
    "end": 1624.8,
    "speaker": "Người nói 10",
    "text": "Thế thì nó sẽ có những các cái mà chúng ta cũng cần phải cân nhắc như chị Trang nói là với các cơ sở y tế nếu mà chúng ta thanh toán chi phí khám chữa bệnh theo cái phân nhóm hoặc là theo định suất thì không nhiều thì ít chắc chắn các cơ sở khám bệnh chữa bệnh cũng sẽ bắt buộc cũng phải xem xét là chi phí là ra là bao nhiêu và thu về là bao nhiêu. Đấy để sau đó thì cân nhắc xem cái phần chênh lệch thu chi. Và hiện nay thì với cái xu thế xu hướng chung quản lý ngân sách cũng như là đối với cái tài chính công và đối với tài chính của các đơn vị sự nghiệp công lập thì hướng dẫn đến cái tự chủ và tự chủ hoàn toàn. Thì các đơn vị cũng rất phải cân nhắc cái việc cân đối thu chi, trong đó thì cái thanh toán cái bảo hiểm y tế là một trong những các cái rất là quan trọng đối với các cơ sở y tế."
  },
  {
    "start": 1626.3,
    "end": 1663.8,
    "speaker": "Người nói 10",
    "text": "Thì chúng ta cân nhắc làm nào đó mà đưa ra một cái cơ chế vừa thúc đẩy được cái sự phát triển của y học nước nhà và chúng ta tiếp cận được với lại y học thế giới cũng như chuyển giao được các phác đồ tiên tiến, các cái kỹ thuật mới, các cái vật tư, cái trang thiết bị mới, thuốc mới để vào phục vụ cho nâng cao cái sức khỏe của người dân. Thì có lẽ theo tôi cái việc mà chúng ta triển khai cái mới và theo xu thế của thế giới là phù hợp nhưng mà cũng xin cân nhắc thật là kỹ để có những các cái thí điểm và đánh giá cho nó phù hợp."
  },
  {
    "start": 1671.5,
    "end": 1704.8,
    "speaker": "Người nói 2",
    "text": "Một trong những yếu tố để đảm bảo quyền lợi cho người tham gia bảo hiểm y tế đó là phòng ngừa và xử lý nghiêm hành vi trục lợi bảo hiểm. Qua các vụ trục lợi bảo hiểm y tế được phát hiện trong thời gian gần đây cho thấy là hành vi này xuất phát từ cả ba phía, đó là người tham gia bảo hiểm y tế, cơ sở y tế và chính cán bộ, nhân viên giám định. Thực tế này cho thấy, dự thảo Luật sửa đổi cần có một chương quy định rõ về công tác giám định, trong đó làm rõ về quyền và trách nhiệm của cơ quan thực hiện, người bệnh, cơ sở y tế và biện pháp xử lý khi có tranh chấp."
  },
  {
    "start": 1706.3,
    "end": 1726.2,
    "speaker": "Người nói 2",
    "text": "Hơn 2000 giấy nghỉ ốm đã được trạm trưởng trạm y tế phường Đồng Văn, thị xã Duy Tiên, Hà Nam cấp cho công nhân tại một số khu công nghiệp của Đồng Văn trong 6 tháng qua. Những công nhân này chỉ đến mua giấy nghỉ ốm để hưởng bảo hiểm xã hội. Mỗi người sẽ được vị trạm trưởng này nghĩ ra một bệnh để nghỉ từ 3 đến 5 ngày."
  },
  {
    "start": 1728.5,
    "end": 1739.5,
    "speaker": "Người nói 11",
    "text": "Đây là xin giấy ốm thì mình cần gì ốm đau, đây là mình đi xin để để hưởng bảo hiểm thôi chứ còn mình cần gì phải ốm, nó tự nghĩ cho mình dùng cái bệnh ốm, nó cấp cho mình một cái giấy này này mình nộp cho công ty thôi. Đấy đây xin nghỉ 4 hôm thì nó ghi cho 4 ngày."
  },
  {
    "start": 1746.5,
    "end": 1748.8,
    "speaker": "Người nói 11",
    "text": "5 ngày 150 và 3 ngày là 100."
  },
  {
    "start": 1749.2,
    "end": 1756.8,
    "speaker": "Người nói 2",
    "text": "Người đến mua giấy nghỉ ốm phải mang theo thẻ bảo hiểm y tế, mục đích để lập khống bệnh án, thanh toán tiền khám và tiền thuốc. Công an tỉnh Hà Nam đã bắt trạm trưởng này và điều tra về hành vi trục lợi bảo hiểm y tế, bảo hiểm xã hội."
  },
  {
    "start": 1763.5,
    "end": 1768.8,
    "speaker": "Người nói 2",
    "text": "Số tiền mà bảo hiểm xã hội tỉnh Hà Nam dừng thanh toán là 167 triệu đồng."
  },
  {
    "start": 1769.3,
    "end": 1799.2,
    "speaker": "Người nói 12",
    "text": "Đối với trạm y tế phường Đồng Văn thì cơ quan bảo hiểm xã hội tỉnh cũng đã tạm dừng thanh toán các cái trường hợp mà có cái hồ sơ do trạm y tế phường Đồng Nguyên trạm trưởng trạm y tế phường Đồng Văn cấp giấy chứng nhận nghỉ hưởng bảo hiểm xã hội. chúng tôi cũng tạm dừng thanh quyết toán chi phí khám chữa bảo hiểm y tế năm 2023 đối với các cái trường hợp người bệnh do nguyên trạm trưởng trạm y tế phường Đồng Văn chỉ định."
  },
  {
    "start": 1802.1,
    "end": 1833.2,
    "speaker": "Người nói 2",
    "text": "Qua hệ thống giám định, Bảo hiểm xã hội Việt Nam đã phát hiện ra nhiều hình thức trục lợi bảo hiểm như mượn thẻ đi khám, mượn thông tin của bác sĩ để chỉ định, kéo dài thời gian nằm viện. Đặc biệt, có một trường hợp từ tháng 9 năm trước đến đầu tháng 8 năm nay, đi khám tới 249 lần tại 8 cơ sở, với 77 loại bệnh khác nhau và được cấp phát tới 155 loại thuốc uống với tổng cộng hơn 11.000 viên."
  },
  {
    "start": 1834.3,
    "end": 1853.5,
    "speaker": "Người nói 6",
    "text": "Rất nhiều trường hợp mà chúng tôi đã phát hiện ra là mượn thẻ của người đã chết đi khám chữa bệnh, hoặc là mượn thẻ rồi chết khi đi đi khám chữa bệnh rồi chết, hoặc là có những cái trường hợp mà đã phẫu thuật cắt toàn bộ tử cung nhưng một vài tháng sau 5 tháng sau lại sinh con, hoặc là đẻ thường 5 tháng sau lại tiếp tục đẻ thường. Đó là những cái bất hợp lý trong cái việc chỉ định điều trị mà chúng tôi có thể sử dụng dữ liệu để phát hiện ra."
  },
  {
    "start": 1854.2,
    "end": 1884.2,
    "speaker": "Người nói 2",
    "text": "Đại diện Trung tâm giám định bảo hiểm y tế và thanh toán đa tuyến đề xuất, để tránh tình trạng trục lợi bảo hiểm y tế, Bảo hiểm xã hội Việt Nam phải có quyền lựa chọn các dịch vụ hiệu quả để ký với các cơ sở y tế. Nếu không hiệu quả thì không ký hợp đồng và không đưa vào danh mục được chi trả bảo hiểm y tế. Đồng thời, trong Luật bảo hiểm y tế sửa đổi sẽ quy định cụ thể về thẩm quyền của bảo hiểm xã hội trong việc thanh kiểm tra và ký hợp đồng, chấm dứt hợp đồng với các cơ sở y tế nếu có hành vi trục lợi."
  },
  {
    "start": 1889.3,
    "end": 1900.5,
    "speaker": "Người nói 1",
    "text": "Thưa bà Trang ạ, hành vi trục lợi bảo hiểm y tế khiến cho dư luận rất là bức xúc. Vậy thì trong dự thảo Luật Bảo hiểm y tế sửa đổi lần này thì sẽ có những cái quy định như thế nào để chúng ta có thể ngăn chặn được cái tình trạng trục lợi bảo hiểm y tế?"
  },
  {
    "start": 1901.4,
    "end": 1929.5,
    "speaker": "Người nói 5",
    "text": "Hiện nay chúng tôi cũng dự thảo các cái nội dung. Thứ nhất là giải thích từ ngữ rất là rõ thế nào là hành vi trục lợi bảo hiểm y tế để bổ sung vào trong Luật. Cái thứ hai là cũng có quy định bên cạnh các cái nội dung liên quan đến tăng cường vấn đề chuyên môn, vấn đề ban hành các cái định mức kỹ thuật, các cái quy trình kỹ thuật chuẩn để làm cái cơ sở tính giá rồi làm cái cơ sở để có các cái chỉ định."
  },
  {
    "start": 1930.5,
    "end": 1970.2,
    "speaker": "Người nói 5",
    "text": "Thì chúng tôi cũng nghĩ rằng công tác giám định bảo hiểm y tế là một trong những cái nội dung rất là quan trọng và để mà phòng ngừa được các cái trục lợi bảo hiểm y tế. Về mặt chế tài thì theo cái quy định hiện hành chúng ta cũng đã có các cái chế tài về mặt hành chính, về mặt chế tài kỷ luật, xử lý kỷ luật, xử lý hành chính, rồi thậm chí là cũng có những cái nội dung mà trục lợi bảo hiểm y tế ở cái mức mà đến một cái số tiền nhất định thì cũng bị xử lý hình sự. Cho nên là những các cái quy định trong Luật Bảo hiểm tới đây thì chúng tôi cũng sẽ cố gắng thể chế đầy đủ các cái nội dung thứ nhất là các cái hành vi, thứ hai là các cái chế tài."
  },
  {
    "start": 1971.2,
    "end": 1985.5,
    "speaker": "Người nói 1",
    "text": "Thưa ông Phúc ạ, là cơ quan quản lý quỹ thì theo ông, cái dự thảo Luật lần này thì chúng ta cần có những quy định như thế nào để quan trọng là chúng ta có thể giám sát và quản lý chặt chẽ quỹ bảo hiểm y tế và tránh tình trạng như chúng ta đã nói và đã xem trong phóng sự rồi?"
  },
  {
    "start": 1986.3,
    "end": 2011.8,
    "speaker": "Người nói 6",
    "text": "Trong cái lần sửa đổi Luật lần này, chúng tôi cũng đã đề nghị kiến nghị với Bộ Y tế, với Chính phủ, Quốc hội là sẽ đưa một chương về công tác giám định vào trong Luật Bảo hiểm y tế. Và chúng ta cũng sẽ nói rõ được cái trách nhiệm của cơ quan bảo hiểm xã hội trong cái việc thực thi công tác giám định. Cái trách nhiệm đi đôi với cái quyền hạn."
  },
  {
    "start": 2012.2,
    "end": 2043.2,
    "speaker": "Người nói 6",
    "text": "Rồi vấn đề trách nhiệm giải trình, trách nhiệm của các cơ sở khám chữa bệnh. Trong Luật Bảo hiểm y tế hiện hành hiện tại thì trách nhiệm của bảo hiểm xã của của các cơ sở khám chữa bệnh trong cái việc quản lý sử dụng quỹ cũng khá là mờ nhạt, chưa ràng buộc được những cái trách nhiệm quản lý sử dụng. Bởi vì hiện tại thì chúng ta cũng biết là cơ quan bảo hiểm xã hội thì trong cái quy định thì chưa có quyền lựa chọn các cơ sở khám chữa bệnh để ký hợp đồng cũng như chưa có quyền để tạm dừng hay là dừng hợp đồng khám chữa bệnh khi phát hiện những cái sai phạm."
  },
  {
    "start": 2044.3,
    "end": 2057.2,
    "speaker": "Người nói 6",
    "text": "Và trong cái thời gian tới đây, chúng tôi nghĩ rằng là chúng ta sẽ mạnh mẽ hơn, mạnh tay hơn, có những cái chế tài mạnh hơn đối với cái việc những cái cơ sở khám chữa bệnh mà lạm dụng trục lợi quỹ bảo hiểm y tế."
  },
  {
    "start": 2058.5,
    "end": 2069.2,
    "speaker": "Người nói 1",
    "text": "Còn thưa ông Hải, một số quan điểm cho rằng là việc lạm dụng tương đối khó để có thể phát hiện ra, đặc biệt là đối với những cái bệnh nhân nặng hoặc là cần có thêm xét nghiệm để chẩn đoán đúng bệnh. Vậy ý kiến của ông như thế nào?"
  },
  {
    "start": 2070.1,
    "end": 2094.2,
    "speaker": "Người nói 10",
    "text": "Tại Bệnh viện Nhi Trung ương chúng tôi nói riêng và các bệnh viện chuyên khoa đầu ngành tuyến cuối thì hầu hết các cái bệnh nhân mà khi mà đến với các cái bệnh viện tuyến cuối đầu ngành là những bệnh nhân nặng, những bệnh nhân rất là hiểm có nhiều cái căn bệnh hiểm nghèo cần phải được quan tâm đặc biệt. Trong trường hợp các bệnh nhân nặng này thì các bác sĩ, các thầy thuốc sẽ cân nhắc để đưa ra những cái phác đồ, đưa ra những các cái chỉ định nó phù hợp."
  },
  {
    "start": 2095.2,
    "end": 2110.2,
    "speaker": "Người nói 10",
    "text": "Tổ chức bình đơn, bình đơn, bình bệnh án để phát hiện ra và để thống nhất cái phác đồ điều trị làm sao cho hạn chế sử dụng tức là làm sao chi phí ở mức mức độ rất là tiết kiệm nhưng hiệu quả khám bệnh chữa bệnh, điều trị thì lại là cao."
  },
  {
    "start": 2111.3,
    "end": 2154.5,
    "speaker": "Người nói 10",
    "text": "Hiện nay cơ quan bảo hiểm xã hội triển khai cái quản lý bằng công nghệ thông tin. Các cái cổng thông tuyến với với lại Trung tâm đa tuyến và với bảo hiểm xã hội và Bộ Y tế thì hiện nay đã làm rất là tốt và phát hiện ra những các cái nhầm lẫn sai sót hoặc là có cái ý mà như chúng ta đã nêu có thể có những trục lợi hoặc là lạm dụng thì chúng ta phát hiện ra và ngăn chặn được ngay. Cho nên là trong thời gian gần đây thì như chúng tôi cũng đã có trao đổi với anh Phúc ấy là nó giảm thiểu rất là nhiều về cái việc các cái bên chưa thống nhất, chưa đồng thuận về số liệu, chưa đồng thuận về những các cái nội dung liên quan đến khám bệnh chữa bệnh."
  },
  {
    "start": 2156.3,
    "end": 2179.5,
    "speaker": "Người nói 2",
    "text": "Đi khám bệnh không mất tiền lại được phát thuốc về uống. Đây là những lợi ích mà đồng bào người dân tộc Dao và Tày tại xã Quang Minh, Văn Yên, Yên Bái thấy được mỗi khi đi khám. Hiện tỉ lệ tham gia bảo hiểm y tế tại xã Quang Minh mới đạt khoảng 85%. Từ khi xã đạt chuẩn nông thôn mới, đồng bào dân tộc không được cấp thẻ miễn phí, một số gia đình không tự nguyện tham gia."
  },
  {
    "start": 2180.3,
    "end": 2200.2,
    "speaker": "Người nói 13",
    "text": "Khám ở đây thì cũng nếu mà không có nguy hiểm mấy đấy thì không phải mất tiền đâu có bảo hiểm các thứ không phải mất tiền. Trước đây có một cái thói quen là ưu tiên cấp miễn phí trong thôn thì vẫn còn một số chưa tự nguyện tham gia mua bảo hiểm. Có một số bảo là bản thân tôi chưa cần thiết."
  },
  {
    "start": 2205.2,
    "end": 2224.2,
    "speaker": "Người nói 2",
    "text": "Các ban ngành đoàn thể cũng như là ban chỉ đạo của xã cũng mới phối hợp với trạm y tế là tuyên truyền để cho người dân bắt buộc là tham gia bảo hiểm tự nguyện những cái gia đình mà người ta thu nhập còn thấp ấy thì mà mua cho cả nhà ấy thì đâm ra là cũng có khó khăn. Người dân tại xã Xuất Lễ, Cao Lộc, Lạng Sơn chủ yếu là đồng bào dân tộc Nùng, Dao và Tày, chỉ làm nông nghiệp không có nghề phụ, thu nhập trung bình chỉ từ 3 đến 5 triệu đồng. Vì vậy nếu mua bảo hiểm y tế cho cả gia đình cũng là một khoản không nhỏ."
  },
  {
    "start": 2239.5,
    "end": 2254.5,
    "speaker": "Người nói 14",
    "text": "Của vợ chồng là hết 1.300 mấy nghìn, nếu mà nhà có mấy đứa con liền thì mỗi đứa con cũng phải đóng trên 500 nghìn nên là với thu nhập của vợ chồng ấy thì rất là cao thôi. Mấy năm gần đây thì cái mức độ thu nhập của bà con thì cũng giảm, cho nên là trong công tác kinh phí để đóng bảo hiểm thì cũng gặp nhiều khó khăn đối với bà con."
  },
  {
    "start": 2268.3,
    "end": 2292.5,
    "speaker": "Người nói 2",
    "text": "Để giúp người dân có thể tham gia bảo hiểm y tế, người dân khi mua bảo hiểm theo hộ gia đình có thể đóng theo tháng, theo quý. Tại một số tỉnh đã có những chính sách hỗ trợ từ 20 đến 30% cho hộ cận nghèo, hộ gia đình nông lâm ngư diêm nghiệp mua thẻ bảo hiểm y tế. Đồng thời thường xuyên đến tận nhà vận động tuyên truyền cho người dân về những lợi ích khi tham gia bảo hiểm y tế mang lại."
  },
  {
    "start": 2293.3,
    "end": 2308.2,
    "speaker": "Người nói 1",
    "text": "Vâng thưa ông Phúc ạ, hiện nay thì tỉ lệ người dân tham gia bảo hiểm y tế của chúng ta tương đối cao, lên tới 92%. Tuy nhiên thì vẫn còn khoảng 8% dân số chưa tham gia bảo hiểm y tế. Vậy thì ông cho biết là đây là những đối tượng nào và tại sao họ lại không tham gia bảo hiểm y tế?"
  },
  {
    "start": 2309.3,
    "end": 2340.5,
    "speaker": "Người nói 6",
    "text": "Chúng tôi cũng đã thống kê từ các địa phương, đó là những cái nhóm người thứ nhất là người tham gia bảo hiểm y tế theo hộ nông lâm ngư diêm nghiệp có mức sống trung bình thì cái tỉ lệ tham gia còn thấp hơn so với các nhóm đối tượng khác. Chúng ta cũng biết là cái đối với những các cái hộ gia đình này thì sẽ được nhà nước hỗ trợ là 30% mức đóng bảo hiểm y tế. Tuy nhiên cái công tác bình bầu cũng còn hạn chế, chính vì vậy cũng chưa xác định được đầy đủ cái nhóm đối tượng mà được hỗ trợ tham gia bảo hiểm y tế theo hộ nông lâm ngư diêm nghiệp có mức sống trung bình."
  },
  {
    "start": 2341.3,
    "end": 2363.3,
    "speaker": "Người nói 6",
    "text": "Cái nhóm thứ hai đó là người tham gia bảo hiểm y tế tại các hộ kinh doanh cá thể. Hiện nay thì cũng theo cái báo cáo thì có đến 5 triệu hộ kinh doanh cá thể, nhưng trong số này thì những cái người trong cái hộ này thì cái tham gia bảo hiểm y tế cũng chưa chưa đầy đủ, vẫn còn thiếu hụt rất nhiều."
  },
  {
    "start": 2364.2,
    "end": 2384.8,
    "speaker": "Người nói 6",
    "text": "Cái nhóm thứ ba đó là tham gia bảo hiểm y tế theo hộ gia đình. Chúng ta cũng biết là hiện tại thì trong những năm gần đây thì thấy cái người tham gia theo hộ gia đình đã tăng rất nhiều. Tuy nhiên thì vẫn còn một cái bộ phận là chưa tham gia. Tỉ lệ tham gia bảo hiểm y tế học sinh hiện nay, học sinh sinh viên hiện nay cũng chưa đạt được 100%."
  },
  {
    "start": 2385.5,
    "end": 2410.8,
    "speaker": "Người nói 6",
    "text": "Và trong đó thì chúng tôi xác định được là có nhiều sinh viên từ năm thứ hai trở đi, năm thứ hai, năm thứ ba không tham gia bảo hiểm y tế. Thì đó là những cái nhóm đối tượng mà cũng cần phải tập trung để mà chúng ta có những các cái giải pháp kết hợp để tăng cái độ bao phủ bảo hiểm y tế, đảm bảo được cái lộ trình tham gia bảo hiểm y tế đến năm 2025 là 95%."
  },
  {
    "start": 2411.3,
    "end": 2420.3,
    "speaker": "Người nói 1",
    "text": "Vâng, thưa bà Trang ạ, mục tiêu của chúng ta cũng tương đối rõ ràng, bảo hiểm y tế toàn dân. Vậy thì làm thế nào để có thể bao phủ được bảo hiểm y tế toàn dân như cái mong muốn của chúng ta?"
  },
  {
    "start": 2421.3,
    "end": 2440.3,
    "speaker": "Người nói 5",
    "text": "Để mà đạt được cái mục tiêu bảo hiểm y tế toàn dân thì nó phụ thuộc vào rất là nhiều các cái yếu tố. Thứ nhất là chúng ta phải có được cái cơ chế để vận động được ngày càng nhiều các cái đối tượng nằm trong cái khoảng 8% tham gia vào bằng những các cái cơ chế hợp lý nhất."
  },
  {
    "start": 2441.5,
    "end": 2460.5,
    "speaker": "Người nói 5",
    "text": "Chúng ta cũng phải tổ chức tuyên truyền để người dân thấy được cái lợi ích của bảo hiểm y tế, đặc biệt là cái chia sẻ rủi ro của số đông cho số ít. Và chúng ta cũng ngày càng phải tăng cái chất lượng phục vụ đối với người bệnh bảo hiểm y tế thông qua nhiều cái hình thức. Thứ nhất là cái phạm vi quyền lợi của người ta được tăng cái phạm vi quyền lợi trong cái mức đóng và cái khả năng chi trả của quỹ bảo hiểm y tế."
  },
  {
    "start": 2461.3,
    "end": 2500.5,
    "speaker": "Người nói 5",
    "text": "Cái thứ hai là chúng ta cũng phải quan tâm tới các cái đối tượng mà hiện nay tham gia bảo hiểm y tế mà còn có những các cái khó khăn về vấn đề mức đóng để chúng ta duy trì ví dụ như là cái hộ cận nghèo để tiếp rồi học sinh sinh viên, rồi những cái người mà đóng bảo hiểm y tế theo hộ gia đình để khuyến khích các đối tượng đấy duy trì và tiếp tục tham gia bảo hiểm y tế thì mới đạt được cái mục tiêu là bao phủ bảo hiểm y tế toàn dân. Rất nhiều các cái biện pháp giải pháp về mặt cơ chế chính sách, về mặt truyền thông và về mặt nâng cao cái chất lượng khám bệnh chữa bệnh bảo hiểm y tế."
  },
  {
    "start": 2501.4,
    "end": 2541.5,
    "speaker": "Người nói 2",
    "text": "Luật Bảo hiểm y tế lần này sẽ sửa đổi toàn diện thay thế cho luật hiện hành nhằm thể chế quan điểm của Đảng tại Nghị quyết số 20 của Ban Chấp hành Trung ương Đảng khóa XII năm 2017 về tăng cường công tác bảo vệ, chăm sóc và nâng cao sức khỏe nhân dân trong tình hình mới. Luật này phải đồng bộ với các luật hiện hành, phù hợp với sự phát triển kinh tế xã hội, đồng thời sẽ từng bước đổi mới phương thức thanh toán chi phí khám chữa bệnh bảo hiểm y tế theo định suất và theo nhóm chẩn đoán liên quan. Trong kỳ họp Quốc hội tháng 10 tới đây, Bộ Y tế sẽ đề xuất đưa Luật bảo hiểm y tế sửa đổi vào chương trình xây dựng Luật, Pháp lệnh năm 2024. Cảm ơn quý vị và các bạn đã quan tâm theo dõi chương trình tọa đàm của Đài Truyền hình Việt Nam."
  }
]
```
