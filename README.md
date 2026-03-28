# 📚 Physics Content Repository

ระบบจัดการคอนเทนต์ฟิสิกส์สำหรับ TikTok/YouTube

## 📁 โครงสร้าง

```
physics-content/
├── 📁 scripts/
│   ├── 📁 videos/
│   │   ├── 📁 short/          # คลิปสั้น 1 นาที
│   │   │   ├── newton-*.md
│   │   │   ├── work-*.md
│   │   │   └── doppler-*.md
│   │   ├── 01-newton-laws.md       # คลิปรวม 3 กฎนิวตัน
│   │   ├── 02-work-power.md        # คลิปรวม งาน-กำลัง
│   │   └── 03-doppler-effect.md    # คลิปรวม Doppler
│   │   └── script_*.md            # สคริปต์เวอร์ชันยาว
├── 📁 content-sheets/
│   └── physics_content_plan.csv    # แผนคอนเทนต์ 68 หัวข้อ
├── 📁 research/
│   └── physics_sheets/             # ชีทเนื้อหาฟิสิกส์
└── 📄 README.md
```

## 🎬 สคริปต์ที่มี

### คลิปสั้น 1 นาที (แยกเรื่อง)
| หัวข้อ | เทคนิค | จุดพลาด | ทดลอง | ชีวิตจริง |
|---------|:------:|:-------:|:------:|:---------:|
| 3 กฎนิวตัน | ✅ | ✅ | ✅ | ✅ |
| งาน-พลังงาน | ✅ | ✅ | ✅ | ✅ |
| Doppler | ✅ | ✅ | ✅ | ✅ |

### คลิปยาว 5-10 นาที
- 01-newton-laws.md
- 02-work-power.md
- 03-doppler-effect.md

## 📋 สถานะการทำ

- ✅ ทำแล้ว: 15 สคริปต์
- ⬜ ยังไม่ทำ: 53 สคริปต์ (จาก 68 หัวข้อ)

## 🚀 วิธีใช้

1. Clone repo:
```bash
git clone https://github.com/Theeratikorn/physics-content.git
```

2. เลือกสคริปต์ที่จะใช้

3. อัดคลิปตามสคริปต์

## 📝 เพิ่มสคริปต์ใหม่

```bash
# สร้างไฟล์ใหม่
touch scripts/videos/short/[topic]-[focus].md

# Commit
git add .
git commit -m "เพิ่มสคริปต์ [หัวข้อ]"
git push
```

## 👥 ทีม

- ผู้สร้าง: กุ้ง (AI Assistant)
- ผู้ดูแล: เก็ต

## 📅 อัปเดตล่าสุด

2026-03-28
