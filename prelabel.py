#!/usr/bin/env python3
"""
prelabel.py - Tu dong gan nhan nhap (pre-label) cho cac anh chua gan nhan,
roi gop voi nhan ban da lam trong CVAT thanh 1 file zip YOLO 1.1 de upload lai.

- Anh DA CO nhan trong file export CVAT  -> giu nguyen nhan cua ban.
- Anh CHUA CO nhan                       -> dung YOLO (COCO) du doan car/truck/bus.
  (COCO khong co lop "van" -> van se bi doan thanh car/truck, ban sua tay.)

Cach dung (chay o thu muc goc cua repo):
    pip install ultralytics
    python prelabel.py --existing cvat_export.zip
Ket qua: prelabels_yolo11.zip -> upload vao CVAT (Upload annotations, YOLO 1.1).
"""
import argparse
import zipfile
from pathlib import Path

CLASSES = ["car", "truck", "bus", "van"]          # thu tu dung voi lab: 0..3
COCO_TO_LAB = {2: 0, 7: 1, 5: 2}                  # COCO car->car, truck->truck, bus->bus


def read_existing(zip_path):
    """Doc cac file .txt tu file export YOLO 1.1 cua CVAT -> {stem: noi_dung}."""
    labels = {}
    if not zip_path:
        return labels
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            if name.endswith(".txt") and "obj_train_data/" in name:
                labels[Path(name).stem] = z.read(name).decode("utf-8").strip()
    return labels


def predict(model, img_path, conf, imgsz):
    r = model.predict(str(img_path), conf=conf, imgsz=imgsz, verbose=False)[0]
    lines = []
    for cls, xywhn in zip(r.boxes.cls.tolist(), r.boxes.xywhn.tolist()):
        cls = int(cls)
        if cls in COCO_TO_LAB:
            x, y, w, h = (min(max(v, 0.0), 1.0) for v in xywhn)
            lines.append(f"{COCO_TO_LAB[cls]} {x:.6f} {y:.6f} {w:.6f} {h:.6f}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--images", default="dataset/images/train", help="thu muc anh train")
    ap.add_argument("--existing", default=None, help="file zip export YOLO 1.1 tu CVAT")
    ap.add_argument("--out", default="prelabels_yolo11.zip")
    ap.add_argument("--model", default="yolo11m.pt", help="yolo11n/s/m/l/x.pt (lon hon = chinh xac hon, cham hon)")
    ap.add_argument("--conf", type=float, default=0.30, help="nguong tin cay")
    ap.add_argument("--imgsz", type=int, default=960, help="anh lon hon giup bat xe nho o xa")
    args = ap.parse_args()

    images = sorted(p for p in Path(args.images).iterdir()
                    if p.suffix.lower() in {".jpg", ".jpeg", ".png"})
    if not images:
        raise SystemExit(f"Khong tim thay anh trong {args.images}")

    existing = read_existing(args.existing)
    todo = [p for p in images if not existing.get(p.stem)]
    print(f"{len(images)} anh | giu nhan cu: {len(images) - len(todo)} | du doan moi: {len(todo)}")

    preds = {}
    if todo:
        from ultralytics import YOLO
        model = YOLO(args.model)
        for p in todo:
            preds[p.stem] = predict(model, p, args.conf, args.imgsz)
            print(f"  {p.name}: {len(preds[p.stem].splitlines()) if preds[p.stem] else 0} box")

    with zipfile.ZipFile(args.out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("obj.names", "\n".join(CLASSES) + "\n")
        z.writestr("obj.data", f"classes = {len(CLASSES)}\nnames = data/obj.names\n"
                               "train = data/train.txt\nbackup = backup/\n")
        z.writestr("train.txt", "".join(f"data/obj_train_data/{p.name}\n" for p in images))
        for p in images:
            txt = existing.get(p.stem) or preds.get(p.stem, "")
            z.writestr(f"obj_train_data/{p.stem}.txt", txt + ("\n" if txt else ""))
    print(f"Da tao {args.out} -> upload vao CVAT voi dinh dang YOLO 1.1")


if __name__ == "__main__":
    main()
