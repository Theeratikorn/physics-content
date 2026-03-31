#!/usr/bin/env python3
"""
Physics JSON → Word Generator (พร้อมเนื้อหา + คำถาม + เฉลย)
"""

import json
import os
import sys
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# ========== เนื้อหาฟิสิกส์ตามบท ==========
PHYSICS_CONTENT = {
    # Part 1: กลศาสตร์ + คลื่น
    "บทนำ": """## บทนำ: หน่วย มาตรฐาน และเลขนัยสำคัญ

### 1. หน่วยในระบบ SI
ระบบหน่วยสากล (International System of Units) มี 7 หน่วยฐาน:

| หน่วยฐาน | สัญลักษณ์ | ปริมาณ |
|-----------|-----------|--------|
| เมตร | m | ความยาว |
| กิโลกรัม | kg | มวล |
| วินาที | s | เวลา |
| แอมแปร์ | A | กระแสไฟฟ้า |
| เคลวิน | K | อุณหภูมิ |
| โมล | mol | ปริมาณสาร |
| แคนเดลา | cd | ความเข้มการส่องสว่าง |

### 2. คำอุปสรรค
| คำอุปสรรค | สัญลักษณ์ | ค่า |
|-----------|-----------|-----|
| เซนติ | c | 10⁻² |
| มิลลิ | m | 10⁻³ |
| ไมโคร | μ | 10⁻⁶ |
| นาโน | n | 10⁻⁹ |
| กิโล | k | 10³ |
| เมกะ | M | 10⁶ |
| กิกะ | G | 10⁹ |

### 3. เลขนัยสำคัญ
- ตัวเลขที่ไม่ใช่ศูนย์ = นัยสำคัญ
- ศูนย์ระหว่างตัวเลข = นัยสำคัญ
- ศูนย์หน้าจุดทศนิยม = ไม่นับ (ยกเว้นมีขีดเส้นใต้)
- จุดทศนิยม = นับ

### 4. การบวก ลบ คูณ หาร
- บวก ลบ: ใช้ทศนิยมน้อยที่สุด
- คูณ หาร: ใช้นัยสำคัญน้อยที่สุด""",

    "การเคลื่อนที่": """## การเคลื่อนที่แนวตรง

### 1. ปริมาณพื้นฐาน
- **ระยะทาง (s)** คือ ความยาวที่วัดได้ตามเส้นทางที่เดิน (scalar)
- **การกระจัด (Δx)** คือ เส้นตรงจากจุดเริ่มถึงจุดสุดท้าย (vector)
- **ความเร็ว (v)** คือ อัตราการเปลี่ยนตำแหน่ง
- **ความเร่ง (a)** คือ อัตราการเปลี่ยนความเร็ว

### 2. สมการการเคลื่อนที่แนวตรงด้วยความเร่งคงที่
- v = v₀ + at
- s = v₀t + ½at²
- v² = v₀² + 2as
- s = ½(v₀ + v)t

### 3. กราฟการเคลื่อนที่
- กราฟ s-t: ความชัน = ความเร็ว
- กราฟ v-t: ความชัน = ความเร่ง, พื้นที่ใต้กราฟ = การกระจัด""",

    "แรง": """## แรงและการเคลื่อนที่

### 1. กฎการเคลื่อนที่ของนิวตัน
- **กฎข้อ 1**: วัตถุจะรักษาสภาพหยุดนิ่งหรือเคลื่อนที่เส้นตรงสม่ำเสมอ ถ้าไม่มีแรงภายนอกมากระทำ
- **กฎข้อ 2**: F = ma (แรง = มวล × ความเร่ง)
- **กฎข้อ 3**: แรงกิริยา = แรงปฏิกิริยา (ทิศตรงข้าม ขนาดเท่ากัน)

### 2. แรงพื้นฐาน
- น้ำหนัก: W = mg (g = 9.8 m/s²)
- แรงเสียดทาน: f = μN
- แรงตึงเชือก: T
- แรงสปริง: F = kx

### 3. แผนภาพวัตถุอิสระ (Free Body Diagram)
- วาดวัตถุเป็นจุด
- ลากเส้นแทนแรงที่กระทำ (ใช้ลูกศร ยาวตามขนาด)
- แยกแรงตามแกน x, y""",

    "งานพลังงาน": """## งานและพลังงาน

### 1. งาน (Work)
- W = Fs cos θ
- หน่วย: จูล (J) = นิวตัน·เมตร
- งานเป็นบวกเมื่อแรงและการกระจัดไปทางเดียวกัน
- งานเป็นศูนย์เมื่อ cos θ = 0 (แรงตั้งฉาก)

### 2. พลังงานจลน์ (Kinetic Energy)
- KE = ½mv²
- พลังงานของวัตถุที่กำลังเคลื่อนที่

### 3. พลังงานศักย์โน้มถ่วง (Gravitational PE)
- PE = mgh
- พลังงานจากความสูง

### 4. กฎอนุรักษ์พลังงาน
- พลังงานรวม = คงที่ (ถ้าไม่มีแรงภายนอกทำงาน)
- KE₁ + PE₁ = KE₂ + PE₂

### 5. กำลัง (Power)
- P = W/t = Fv (หน่วย: วัตต์ = J/s)""",

    "โมเมนตัม": """## โมเมนตัมและการชน

### 1. โมเมนตัม
- p = mv (หน่วย: kg·m/s)
- เป็นปริมาณเวกเตอร์

### 2. แรงและโมเมนตัม
- F = Δp/Δt
- แรง = อัตราการเปลี่ยนโมเมนตัม

### 3. การอนุรักษ์โมเมนตัม
- ถ้าไม่มีแรงภายนอก: p₁ + p₂ = p₁' + p₂'
- ก่อนชน = หลังชน

### 4. ชนิดการชน
- **ชนแบบยืดหยุ่น**: พลังงานจลน์คงที่, e = 1
- **ชนแบบไม่ยืดหยุ่น**: พลังงานจลน์ลดลง, e < 1
- **e** = ค่าสัมประสิทธิ์การฟื้นตัว""",

    "การเคลื่อนที่แนวโค้ง": """## การเคลื่อนที่แนวโค้ง

### 1. การเคลื่อนที่แบบโปรเจกไทล์
- แกน x: x = v₀ cosθ · t
- แกน y: y = v₀ sinθ · t - ½gt²
- vₓ = v₀ cosθ (คงที่)
- vᵧ = v₀ sinθ - gt

### 2. สมการพาราโบลา
- y = x tanθ - (g/2v₀²cos²θ)x²

### 3. ความเร็ว
- ความเร็วสูงสุด: ที่จุดต่ำสุด
- ความเร็วต่ำสุด: ที่จุดสูงสุด

### 4. การเคลื่อนที่แบบวงกลม
- v = ωr
- a = v²/r = ω²r
- F = mv²/r""",

    "คลื่น": """## คลื่น

### 1. ประเภทคลื่น
- **คลื่นกล**: ต้องใช้ตัวกลาง (เสียง, คลื่นน้ำ)
- **คลื่นแม่เหล็กไฟฟ้า**: ไม่ต้องตัวกลาง (แสง)

### 2. ปริมาณคลื่น
- λ = ความยาวคลื่น (m)
- f = ความถี่ (Hz)
- T = คาบ (s), T = 1/f
- v = fλ

### 3. ชนิดคลื่นตามแนวการสั่น
- คลื่นขวาง: สั่นตั้งฉากทิศเคลื่อนที่ (เชือก, แสง)
- คลื่นตามยาว: สั่นขนานทิศเคลื่อนที่ (เสียง)

### 4. สมบัติคลื่น
- การสะท้อน
- การหักเห
- การแทรกสอด
- การเลี้ยวเบน""",

    "เสียง": """## เสียง

### 1. ธรรมชาติของเสียง
- เป็นคลื่นตามยาว
- ต้องใช้ตัวกลาง
- ความเร็วเสียงในอากาศ ≈ 340 m/s (ที่ 25°C)

### 2. ความถี่เสียง
- เสียงต่ำ (Infrasound): f < 20 Hz
- ช่วงหูคนได้ยิน: 20 Hz - 20 kHz
- เสียงสูง (Ultrasound): f > 20 kHz

### 3. ความเข้มเสียง
- I = P/A
- ระดับความเข้มเสียง: β = 10 log(I/I₀) dB

### 4. ปรากฏการณ์เสียง
- บีตส์: f = |f₁ - f₂|
- ปรากฏการณ์ดอปเปลอร์: f' = f(v ± vₒ)/(v ∓ vₛ)""",

    "แสง": """## แสง

### 1. ธรรมชาติของแสง
- เป็นคลื่นแม่เหล็กไฟฟ้า
- เดินทางด้วยความเร็ว c = 3×10⁸ m/s
- ไม่ต้องใช้ตัวกลาง

### 2. การสะท้อนแสง
- มุมตก = มุมสะท้อน
- กระจกราบ: ภาพหัวกลับด้าน
- กระจกเว้า: ภาพจริง/ภาพเสมือน
- กระจกนูน: ภาพเสมือน ย่อ

### 3. การหักเหของแสง
- n = c/v = sinθ₁/sinθ₂
- กฎสเนลล์: n₁sinθ₁ = n₂sinθ₂

### 4. กระจกและเลนส์
- กระจกเว้า: 1/f = 1/u + 1/v
- เลนส์บาง: 1/f = (n-1)(1/R₁ - 1/R₂)""",

    "เลเซอร์": """## เลเซอร์

### 1. ธรรมชาติของเลเซอร์
- Light Amplification by Stimulated Emission of Radiation
- เป็นคลื่นแม่เหล็กไฟฟ้าความถี่เดียว
- มีความเป็นระเบียบสูง (Coherent)

### 2. คุณสมบัติ
- เป็นระเบียบสูง (Coherent)
- มีทิศทางเดียว (Directional)
- มีความเข้มสูง (Intense)
- เป็นขั้วเดียว (Monochromatic)

### 3. การเกิดเลเซอร์
- การดูดกลืน (Absorption)
- การส่องสว่างเอง (Spontaneous Emission)
- การส่องสว่างแบบกระตุ้น (Stimulated Emission)

### 4. การประยุกต์
- ศัลยกรรมตา (LASIK)
- เครื่องเล่นแผ่น (CD/DVD)
- การสำรวจระยะไกล
- อุตสาหกรรม""",
}

# Fallback content for unknown topics
DEFAULT_CONTENT = """## เนื้อหา

### หลักการ
ศึกษาหลักการพื้นฐานและนำไปประยุกต์ใช้

### สมการสำคัญ
- ทำความเข้าใจสมการและการใช้งาน

### การคำนวณ
- ฝึกทำโจทย์เพื่อเสริมความเข้าใจ"""

def get_content_for_topic(topic_text):
    """หาเนื้อหาจาก topic"""
    topic_lower = topic_text.lower()
    
    for key in PHYSICS_CONTENT:
        if key.lower() in topic_lower:
            return PHYSICS_CONTENT[key]
    
    return DEFAULT_CONTENT

def convert_to_word(json_path, output_dir=".", create_answer=True):
    """แปลง JSON → Word document (พร้อมเนื้อหา)"""
    
    # อ่าน JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    lesson = data.get('lesson', {})
    lesson_name = lesson.get('name', 'Unknown')
    lesson_title = lesson.get('title', 'ไม่ระบุ')
    topics = lesson.get('topics', [])
    questions = data.get('questions', [])
    
    base_name = os.path.splitext(os.path.basename(json_path))[0]
    
    # ========== สร้างเอกสาร ==========
    doc = Document()
    doc.core_properties.title = lesson_title
    
    # หัวข้อบท
    doc.add_heading(lesson_title, 0)
    
    # ========== ส่วนเนื้อหา ==========
    doc.add_heading("เนื้อหา", level=1)
    
    # ดึงเนื้อหาจาก topics
    topic_str = ', '.join(topics) if isinstance(topics, list) else str(topics)
    content = get_content_for_topic(topic_str)
    
    # แปลง markdown-like content เป็น Word
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            doc.add_paragraph()
        elif line.startswith('## '):
            doc.add_heading(line[3:], level=2)
        elif line.startswith('### '):
            doc.add_heading(line[4:], level=3)
        elif line.startswith('- '):
            doc.add_paragraph(line[2:], style='List Bullet')
        elif line.startswith('| '):
            # เป็นตาราง - ข้ามไปก่อน (Word ไม่รองรับ markdown table โดยตรง)
            pass
        else:
            doc.add_paragraph(line)
    
    doc.add_paragraph()
    
    # ========== ส่วนคำถาม ==========
    doc.add_heading("แบบฝึกหัด", level=1)
    
    for i, q in enumerate(questions, 1):
        q_text = q.get('question', '')
        
        # คำถาม
        p = doc.add_paragraph()
        run = p.add_run(f"{i}. {q_text}")
        run.font.size = Pt(12)
        
        # ตัวเลือก
        options = q.get('options') or []
        if isinstance(options, dict):
            options = list(options.values())
        
        for j, opt in enumerate(options, 1):
            p = doc.add_paragraph(f"    {j}. {opt}")
            p.paragraph_format.left_indent = Inches(0.5)
        
        doc.add_paragraph()
    
    docx_path = os.path.join(output_dir, f"{base_name}.docx")
    doc.save(docx_path)
    print(f"✅ {docx_path}")
    
    # ========== สร้างเฉลย ==========
    if create_answer:
        doc_ans = Document()
        doc_ans.core_properties.title = f"เฉลย {lesson_title}"
        doc_ans.add_heading(f"เฉลย {lesson_title}", 0)
        doc_ans.add_paragraph()
        
        for i, q in enumerate(questions, 1):
            answer = q.get('answer', '')
            solution = q.get('solution', '')
            
            # แปลง ก=1, ข=2, ค=3, ง=4
            if isinstance(answer, str) and len(answer) == 1 and answer in 'กขคง':
                answer = 'กขคง'.index(answer) + 1
            
            p = doc_ans.add_paragraph()
            run = p.add_run(f"ข้อ {i}: ")
            run.bold = True
            run.font.size = Pt(12)
            run2 = p.add_run(f"คำตอบ: {answer}")
            run2.font.size = Pt(12)
            
            if solution:
                p2 = doc_ans.add_paragraph(f"   วิธีทำ: {solution}")
                p2.paragraph_format.left_indent = Inches(0.3)
            
            doc_ans.add_paragraph()
        
        ans_path = os.path.join(output_dir, f"{base_name}_เฉลย.docx")
        doc_ans.save(ans_path)
        print(f"✅ เฉลย: {ans_path}")
    
    return docx_path

def main():
    if len(sys.argv) < 2:
        print("ใช้งาน:")
        print("  python generate_word.py lesson01.json")
        print("  python generate_word.py lesson01.json output/")
        print("  python generate_word.py part1/")
        print("  python generate_word.py part1/ output/")
        return
    
    arg = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    os.makedirs(output_dir, exist_ok=True)
    
    if os.path.isdir(arg):
        json_files = sorted([f for f in os.listdir(arg) if f.endswith('.json') and 'extra' not in f])
        print(f"พบ {len(json_files)} ไฟล์ใน {arg}")
        
        for f in json_files:
            print(f"\n📄 {f}")
            try:
                convert_to_word(os.path.join(arg, f), output_dir)
            except Exception as e:
                print(f"❌ ผิดพลาด: {e}")
        
        print(f"\n✅ เสร็จสมบูรณ์!")
    
    elif os.path.isfile(arg):
        convert_to_word(arg, output_dir)
    
    else:
        print(f"❌ ไม่พบ: {arg}")

if __name__ == "__main__":
    main()
