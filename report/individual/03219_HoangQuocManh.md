# Báo cáo cá nhân — Ngày 2 Object Detection

## 1. Thông tin học viên

- Họ tên: Hoàng Quốc Mạnh
- MSSV: 03219
- Email: hoangquocmanh2004@gmail.com
- Lớp: K5-L2A
- Link repo bài làm: https://github.com/quocmanh0502/K5-L2A-DAY02-HoangQuocManh-03219-ObjectDetection
- Link Colab: https://colab.research.google.com/drive/10WIycuS0-VulBIY8zeJuI22PpjT5fuNE (TODO – chưa chạy xong; lần thử ngày 09/11/2026 gặp lỗi "Không gán được phần phụ trợ", xem mục 6). Kết quả ở mục 5 hiện là bản chạy local trên máy cá nhân (GPU RTX 3050 Laptop). Bằng chứng chạy local: notebook đã thực thi kèm toàn bộ output [assets/day2_annotation_to_yolo_executed_local.ipynb](assets/day2_annotation_to_yolo_executed_local.ipynb) (cell đầu in commit `fc41e9a` được clone từ repo trên GitHub), log train và ảnh chỉ số trong [assets/yolo26_runs/](assets/yolo26_runs/).

## 2. Schema và mini guideline

Schema cố định theo `data.yaml`: `0 car`, `1 truck`, `2 bus`, `3 van`. Chi tiết ở [GUIDELINE_MINI.md](../../GUIDELINE_MINI.md).

Định nghĩa lớp: `car` = xe con chở người (kể cả SUV 7 chỗ, pickup theo README); `truck` = xe chở hàng và xe chuyên dụng; `bus` = xe chở khách cỡ lớn, thân dài nhiều cửa sổ; `van` = xe hộp cỡ trung liền khối (minivan, 9–16 chỗ, van hàng kín).

Ca mơ hồ chính (đầy đủ trong guideline):

| Ảnh | Tình huống | Quyết định | Lý do |
|---|---|---|---|
| `drive_026` | MPV/minivan nằm giữa `car` và `van` | `van` nếu thân hộp, đầu ngắn; cần hỏi giảng viên | GUIDE.md: van mơ hồ với car thì ghi case và hỏi |
| `drive_002`, `drive_003` | Xe nhỏ ở vùng xa phía trên ảnh | Bản nộp có gán; sau QC chỉ gán khi rõ lớp và cao ≥ 20 px | Gold không gán vùng này |
| `drive_050` | Xe đỗ trên vỉa hè/ven đường | Gán theo loại xe; cần hỏi giảng viên | GUIDE.md: xe đỗ vẫn gán |
| `drive_009`, `drive_019` | Xe buýt lớn, gold ghi ID 3 | Giữ `bus` (ID 2) theo `data.yaml` | Schema cố định |

Phần cần giảng viên làm rõ:

1. **Thứ tự class ID của gold và eval khác `data.yaml`.** Khi so từng box trùng vị trí (IoU ≥ 0.5) và xem ảnh crop, gold train và nhãn eval dùng `1 = van`, `2 = truck`, `3 = bus`; còn schema bài (`data.yaml`, README) là `1 truck`, `2 bus`, `3 van`. Ví dụ: xe buýt ở `drive_002`, `drive_008`, `drive_009` được gold gán ID 3; xe van ở `drive_002`, `drive_008`, `drive_040` được gold gán ID 1; xe tải/xe cứu hộ ở `drive_005`, `drive_008`, `drive_009` được gold gán ID 2. Nhãn eval có cùng hiện tượng (`drive_052`, `drive_053`: xe buýt gán ID 3).
2. **Xe đỗ ven đường và xe ở xa.** Gold không gán xe đỗ ven đường và xe nhỏ ở xa phía trên khung hình (ví dụ `drive_028`, `drive_002`), trong khi CP1 ghi "xe đỗ, bị che hoặc bị cắt khung vẫn cần xử lý theo guideline". Cần quy tắc rõ ràng cho hai trường hợp này.

## 3. Annotation và self-QC

- Số file nhãn train: 50 (`drive_001.txt` … `drive_050.txt`), tổng 1003 box (car 804, truck 26, bus 92, van 81). Công cụ: CVAT (export YOLO 1.1). Ảnh `drive_032`–`drive_050` được pre-label bằng YOLO11m pretrained COCO (script `prelabel.py` do Claude viết, chỉ ánh xạ car/truck/bus; COCO không có van) rồi sửa tay toàn bộ trong CVAT; ảnh `drive_001`–`drive_031` gán tay từ đầu.
- Kết quả checker: `python tools/check_yolo_labels.py` → `ĐẠT cấu trúc: 50/50 file nhãn hợp lệ`. Không có lỗi cấu trúc cần sửa.
- Danh sách ít nhất 10 ảnh đã rà bằng mắt:

  `drive_032` đến `drive_050` (19 ảnh): rà và sửa tay từng box trong CVAT sau khi pre-label. Ảnh `drive_001`–`drive_031` được gán tay trực tiếp nên đã xem từng ảnh khi gán.

- Lỗi bỏ sót/box/class phát hiện khi rà và cách sửa:

  Với ảnh pre-label, COCO không có lớp `van` nên các xe van phải tự gán lại lớp; các box của model được kiểm tra, chỉnh cạnh, xóa box sai và thêm xe bị bỏ sót trong CVAT trước khi khóa nhãn.

- Commit khóa nhãn ban đầu: `3f7ad11` — "Initial annotations" (2026-11-09 21:28 +07:00), đã push lên GitHub.

## 4. Gold QC và rework

| Chỉ số | Trước sửa | Sau sửa nếu có |
|---|---:|---:|
| TP | 454 | — |
| FP | 549 | — |
| FN | 199 | — |
| Precision | 0.4526 | — |
| Recall | 0.6953 | — |
| F1 | 0.5483 | — |
| mean_iou_of_matches | 0.8397 | — |
| passed | false | — |

File kết quả: [`outputs/annotation_evaluation.json`](../../outputs/annotation_evaluation.json) (commit `fc41e9a`). Lệnh chạy:

```bash
python tools/evaluate_annotations.py --student-labels dataset/labels/train --gold-labels gold_train_labels
```

**Không có vòng rework.** Mean IoU đạt (0.84 ≥ 0.70), F1 chưa đạt (0.55 < 0.80). Theo thông tin trong buổi lab, cả lớp đều ra kết quả tương tự, nên chuyển sang bước train và ghi lại nguyên nhân để giảng viên xem xét. Không sửa gold, không chép nhãn gold sang nhãn của mình.

Phân tích lỗi (đối chiếu từng box, mở lại ảnh để xem, không chỉ suy từ FP/FN):

1. **Lệch thứ tự class ID** (xem mục 2): các box trùng vị trí với gold nhưng khác ID gồm gold "van" ↔ mình `bus` 50 box, gold "truck" ↔ mình `van` 37 box, gold "bus" ↔ mình `truck` 19 box. Lỗi xuất hiện cả ở ảnh gán tay (001–031) lẫn ảnh pre-label (032–050), nên không phải do pre-label. Nếu chỉ đổi ID trong bộ nhớ để kiểm tra (không sửa file), F1 tăng từ 0.548 lên 0.678, mean IoU 0.847.
2. **Box thừa so với gold** (442 box sau khi đã tính đến lệch ID, chủ yếu `car`): phần lớn là xe đỗ ven đường và xe ở xa phía trên ảnh mà gold không gán; 152 box có cạnh dài < 32 px. Ảnh có nhiều box thừa nhất: `drive_003` (+27), `drive_002` (+24), `drive_030` (+20), `drive_044` (+15), `drive_049` (+14), `drive_028` (+12).
3. **Bỏ sót**: 92 box gold không có box tương ứng, chủ yếu `car`; nhiều nhất ở `drive_041` (12), `drive_030` (5), `drive_009` (5), `drive_045` (4).
4. **Độ bám box** tốt: mean IoU 0.84 trên các cặp đã ghép.

## 5. Kết quả YOLO

- Runtime: chạy local (Jupyter `nbconvert --execute`), Windows 11, GPU NVIDIA GeForce RTX 3050 Laptop 4 GB, Python 3.12.8, Ultralytics 8.4.208, Torch 2.3.0+cu121.
- Tham số thay đổi so với notebook: giữ nguyên `yolo26n.pt`, `epochs=50`, `imgsz=640`, `batch=-1`, `seed=20260909`, `data.yaml` và split. Chỉ thay đổi: điền `REPO_URL` và bỏ dòng `%pip install -U ultralytics` (dùng bản Ultralytics đã cài sẵn trên máy). Thời gian train ≈ 100 giây. Ultralytics 8.4 lưu kết quả dưới `runs/detect/...` thay vì `outputs/`, nên file zip notebook tạo ra thiếu hai thư mục kết quả; hai thư mục đã được copy thủ công vào `assets/`, giữ nguyên cấu trúc, bỏ file `.pt`.
- Best checkpoint: `runs/detect/Day2-Lab/outputs/yolo26_runs/vehicle_annotation/weights/best.pt` (epoch 37 theo mAP50 trên eval; không commit `.pt`).

| Chỉ số trên 10 ảnh eval | Giá trị |
|---|---:|
| Precision | 0.374 |
| Recall | 0.263 |
| mAP50 | 0.271 |
| mAP50–95 | 0.197 |

Theo từng lớp (113 box trên 10 ảnh eval):

| Lớp | Box | P | R | mAP50 | mAP50–95 |
|---|---:|---:|---:|---:|---:|
| car | 94 | 0.763 | 0.685 | 0.732 | 0.512 |
| truck | 5 | 0.500 | 0.200 | 0.233 | 0.201 |
| bus | 2 | 0.000 | 0.000 | 0.008 | 0.003 |
| van | 12 | 0.233 | 0.167 | 0.109 | 0.072 |

Kết quả: [metrics JSON](assets/model_eval_metrics.json), [ảnh dự đoán 10 ảnh eval](assets/eval_predictions/visuals/), [log train `results.csv`](assets/yolo26_runs/vehicle_annotation/results.csv), [đường cong train](assets/yolo26_runs/vehicle_annotation/results.png), [confusion matrix trên eval](assets/yolo26_runs/vehicle_eval/confusion_matrix.png).

Ví dụ cụ thể: ở [drive_053](assets/eval_predictions/visuals/drive_053.jpg), model đoán đúng hai xe buýt (xe buýt xanh lá phía dưới, `bus 0.85`; xe buýt đỏ trắng góc phải trên, `bus 0.84`), nhưng nhãn eval gán hai xe này ID 3 (`van` theo `data.yaml`), nên khi chấm cả hai bị tính sai. Confusion matrix trên eval cho thấy rõ: **11 box eval ID `van` được dự đoán là `bus`**, không box `van` nào được dự đoán đúng là `van`.

Trả lời bốn câu hỏi cuối notebook:

1. **Lớp nào recall thấp nhất? Ảnh nào minh họa?** `bus` (R = 0, chỉ 2 box eval), sau đó `van` (R = 0.167). Hai box eval ID `bus` nằm ở `drive_051` và `drive_058`; khi xem crop thì đó là xe tải thùng và xe cứu hộ, tức theo nghĩa `data.yaml` là `truck`. Model không đoán chúng là `bus` (confusion matrix: 1 thành `car`, 1 bị bỏ sót). Với `van`, ở [drive_053](assets/eval_predictions/visuals/drive_053.jpg) model đoán `bus` cho các xe buýt mà nhãn eval ghi ID `van`. Recall thấp của bus/van chủ yếu do lệch quy ước ID giữa nhãn train (theo `data.yaml`) và nhãn eval, cộng thêm số mẫu ít (eval chỉ có 2 bus, 5 truck).
2. **mAP50 cao nhưng mAP50–95 thấp → kiểm gì trên box?** Chênh lệch này cho biết box tìm đúng vật thể nhưng chưa sát ở ngưỡng IoU cao. Với `car`, mAP50 0.732 nhưng mAP50–95 0.512. Cần kiểm các cạnh box: box lỏng, lấn bóng hoặc nền, lệch ở xe nhỏ ở xa (vài pixel lệch đã làm IoU giảm mạnh), xe bị che chỉ bao phần nhìn thấy, và xem nhãn train có thống nhất cách vẽ box với nhãn eval không.
3. **Lỗi class nào liên quan guideline? Dữ kiện nào hỗ trợ?** (a) `bus`/`van`/`truck`: quy ước ID của nhãn eval và gold khác `data.yaml`. Dữ kiện: confusion matrix eval (11 eval-`van` → dự đoán `bus`), và so sánh nhãn train với gold (50 + 37 + 19 box cùng vị trí khác ID theo một quy luật hoán vị cố định). (b) Ranh giới `van`/`car` (minivan, MPV): 17 box gold gán `car` nhưng mình gán `van`, và 6 xe van (gold ID 1) mình gán `car`. Đây là ca mơ hồ GUIDE.md đã nêu ("Van/minivan mơ hồ với bus hoặc car"). (c) Xe đỗ và xe ở xa: confusion matrix eval có 825 dự đoán `car` rơi vào background, trùng với quy tắc gold/eval không gán xe đỗ và xe ở xa, trong khi nhãn train của mình có gán.
4. **Vì sao không dùng 10 ảnh eval để train?** Nếu train trên eval, model đã "nhìn thấy" chính các ảnh dùng để chấm, nên metrics sẽ cao giả và không phản ánh khả năng tổng quát. Trong notebook, `data.yaml` trỏ `val` tới 10 ảnh eval: chúng được dùng để tính metrics mỗi epoch và **chọn `best.pt`** (epoch 37). Vì đã dùng để chọn checkpoint nên tập này là validation, không phải test set độc lập; metrics trên nó vẫn hơi lạc quan.

## 6. Khó khăn và cách xử lý

| Bước/thời điểm | Lỗi quan sát | Cách đã thử | Kết quả/còn thiếu |
|---|---|---|---|
| CP5 — Gold QC | F1 = 0.548 < 0.80, truck/bus/van gần như không khớp gold | So từng box cùng vị trí, crop ảnh để xem; đổi ID trong bộ nhớ để đo ảnh hưởng | Phát hiện gold/eval dùng thứ tự ID khác `data.yaml`; F1 khi khớp ID là 0.678. Không rework, chờ giảng viên làm rõ |
| CP5 — Gold QC | 442 box thừa | Vẽ chồng box gold và box của mình | Gold không gán xe đỗ và xe ở xa; cần quy tắc trong guideline |
| CP4 — push | `git push` báo `Invalid username or token` | Đăng nhập lại bằng `gh auth login` + `gh auth setup-git` | Push thành công |
| CP6 — chạy notebook | Ultralytics 8.4 lưu kết quả vào `runs/detect/...`, zip thiếu `eval_predictions/` và `yolo26_runs/` | Copy thủ công hai thư mục vào `assets/`, bỏ `.pt` | Đủ ảnh và log |
| CP6 — Colab (09/11/2026) | Colab báo "Không gán được phần phụ trợ" (Failed to assign a backend), không có runtime GPU | Đợi rồi thử lại; đổi runtime sang CPU | TODO – chưa chạy xong trên Colab; tạm chạy local trên RTX 3050, có notebook đã thực thi làm bằng chứng |
| Pre-label | Ultralytics bản cũ không tải được `yolo11m.pt` | Nâng cấp Ultralytics, đổi sang model YOLO11 tải được | Pre-label chạy được cho `drive_032`–`drive_050` |

## 7. Tự đánh giá theo rubric

| Tiêu chí | Tình trạng |
|---|---|
| Hoàn thành và định dạng YOLO (10) | Đạt: 50/50 file, checker đạt |
| Đầy đủ vật thể (20) | Đã gán cả xe che, cắt khung, xe đỗ; so với gold còn thiếu 92 box và thừa box ở xe đỗ/ở xa (do khác quy tắc) |
| Độ bám sát box (20) | Mean IoU 0.84 trên các cặp đã ghép |
| Phân lớp nhất quán (15) | Lớp gán theo `data.yaml`; vẫn có nhầm ranh giới van/car (17 + 6 box) |
| Mini guideline (10) | Có định nghĩa 4 lớp, quy tắc box, ngưỡng xe nhỏ sau QC và 5 ca mơ hồ có tên ảnh thật |
| Gold-set QC (15) | Chưa đạt ngưỡng F1; không rework; đã phân tích nguyên nhân |
| Pipeline YOLO và phân tích (10) | Chạy đủ notebook, không dùng eval để train, có metrics, ảnh eval và phân tích; **không có link Colab** (chạy local) |

## 8. Công cụ AI và tài liệu tham khảo

- **Claude Code (Anthropic)**, dùng để: hướng dẫn quy trình làm lab; viết script `prelabel.py` để pre-label `drive_032`–`drive_050`; viết nháp mini guideline; giải nén export CVAT, chạy checker và evaluator; phân tích lỗi nhãn so với gold (phát hiện lệch ID, box thừa/thiếu; dùng script đọc file, không chép nhãn gold); chạy notebook local và gom kết quả vào `assets/`; soạn bản nháp báo cáo này từ số liệu đã chạy. Phần tôi tự làm và kiểm tra: gán tay `drive_001`–`drive_031`; rà và sửa tay toàn bộ box pre-label của `drive_032`–`drive_050` trong CVAT; quyết định lớp cho các ca mơ hồ; xem lại ảnh so sánh với gold để xác nhận các kết luận phân tích; duyệt nội dung báo cáo và guideline.
- **YOLO11m pretrained COCO (Ultralytics)**: pre-label ảnh `drive_032`–`drive_050` bằng `prelabel.py`, sau đó sửa tay toàn bộ trong CVAT. Script này lỡ được commit ở `f43c3b7` và đã gỡ khỏi repo ở commit sau (vẫn giữ trên máy).
- Công cụ gán nhãn: CVAT (chạy local).
- Không dùng nguồn nhãn ngoài repo. Không đưa gold train vào repo.
