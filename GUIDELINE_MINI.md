# Mini guideline — bài làm cá nhân

Học viên: Hoàng Quốc Mạnh (03219, K5-L2A). Schema cố định theo `data.yaml`: `0 car`, `1 truck`, `2 bus`, `3 van`.

## Định nghĩa lớp

| Lớp | Định nghĩa của bạn | Ví dụ/điểm phân biệt |
| --- | --- | --- |
| `car` | Xe ô tô con chở người: sedan, hatchback, SUV, crossover, taxi, xe cảnh sát loại sedan/SUV. SUV 7 chỗ vẫn là `car`. Xe bán tải (pickup) là `car` theo schema README. | Thân thấp hoặc vừa, có nắp capo rõ, 4–5 cửa. Pickup có thùng hở nhỏ vẫn là `car`, không phải `truck`. |
| `truck` | Xe chở hàng: xe tải thùng, container, đầu kéo, xe ben, xe bồn, xe chuyên dụng (cứu hộ, xe cẩu, xe rác). | Có cabin tách khỏi thùng hàng hoặc có thiết bị chuyên dụng phía sau. Xe cứu hộ cảnh sát (drive_019, 038) là `truck`. |
| `bus` | Xe chở khách cỡ lớn: xe buýt thành phố, xe buýt nối toa, xe khách, xe đưa đón khoảng 25 chỗ trở lên. | Thân dài, liền khối, nhiều cửa sổ chạy dọc thân, cửa lên xuống lớn. |
| `van` | Xe hộp cỡ trung liền khối: minivan, xe 9–16 chỗ, van chở hàng thùng kín. | Đầu ngắn hoặc gần như không có capo, thân cao dạng hộp, thường có cửa trượt. Ngắn hơn hẳn `bus`, cao và vuông hơn `car`. |

## Quy tắc chung

- Box bám sát vật thể nghĩa là: 4 cạnh chạm đúng phần thân xe nhìn thấy (kể cả gương, cản), không lấy thêm bóng, mặt đường, trời hay xe bên cạnh. Mỗi xe một box riêng, không gộp hai xe vào một box.
- Vật thể bị che khuất: vẫn gán nếu phần nhìn thấy đủ để nhận ra lớp; box chỉ bao phần nhìn thấy, không đoán phần bị che. Hai xe chồng nhau thì vẽ hai box riêng.
- Vật thể bị cắt bởi rìa ảnh: box chạm đúng rìa ảnh, không đoán phần nằm ngoài khung.
- Vật thể rất nhỏ/mơ hồ: nếu không xác định chắc được lớp thì không gán và không tự đoán; ghi tên ảnh và hỏi giảng viên.
- Không gán: người đi bộ, xe máy/mô tô, xe đạp, biển báo, đèn giao thông, xe trong phản chiếu kính/gương, hình xe trên bảng quảng cáo.
- Xe đang đỗ vẫn gán theo loại xe (GUIDE.md mục 1).
- **Ngưỡng xe quá nhỏ (quyết định sau gold QC, chưa áp dụng vào bộ nhãn đã nộp):** ảnh 640×640, không gán xe có chiều cao box dưới 20 px. Căn cứ: gold chỉ có 3/653 box cao dưới 20 px, còn bộ nhãn của tôi có 31 box thừa dưới mức này. Phân tích cũng cho thấy phần lớn box thừa so với gold **không** do kích thước mà do vị trí (xe ở vùng xa phía trên ảnh, xe đỗ ngoài lòng đường), nên quy tắc cho hai nhóm này cần giảng viên xác nhận (ca 2 và 3 bên dưới).

## Ghi lại quyết định cho ít nhất ba ca mơ hồ

| Ảnh | Tình huống | Quyết định cuối | Lý do theo schema |
| --- | --- | --- | --- |
| `drive_026` (cũng gặp ở `drive_019`, `drive_041`) | Xe MPV/minivan thân cao, nằm giữa `car` và `van` | Gán `van` khi thân dạng hộp, đầu ngắn; gán `car` khi có capo rõ như SUV. **Cần hỏi giảng viên** | GUIDE.md: van/minivan mơ hồ với `car` thì không tự chọn, ghi case ID và hỏi. Gold QC có 17 box tôi gán `van` nhưng gold gán `car` |
| `drive_002`, `drive_003` | Nhiều xe nhỏ, dày đặc ở vùng xa phía trên ảnh, vẫn nhận ra được là ô tô | Bản đã nộp: có gán. Sau gold QC: chỉ gán khi xác định được lớp và box cao ≥ 20 px. **Cần hỏi giảng viên** về vùng xa | Schema yêu cầu gán xe nhận diện được, nhưng gold không gán vùng này (176 box thừa nằm phía trên vùng gold có gán) |
| `drive_050` (cũng gặp ở `drive_028`) | Xe đỗ ven đường, trên vỉa hè, ngoài làn chính | Gán theo loại xe (thường là `car`). **Cần hỏi giảng viên** vì gold không gán | GUIDE.md: "Xe đang đỗ: vẫn gán lớp theo loại xe" |
| `drive_009`, `drive_019` | Xe buýt thành phố cỡ lớn; gold và nhãn eval ghi ID 3 cho các xe này | Giữ `bus` (ID 2) theo `data.yaml`. Đã báo giảng viên | `data.yaml`/README: `2 bus`, `3 van`. Gold có vẻ dùng thứ tự ID khác (bus=3, van=1, truck=2) |
| `drive_019`, `drive_038` | Xe cứu hộ cảnh sát có cẩu phía sau | `truck` | Xe chuyên dụng, cabin tách khỏi phần chở/thiết bị, không chở khách |
