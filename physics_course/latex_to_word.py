"""
Physics Sheet to Word Converter
- อ่าน JSON → สร้าง Word
- เพิ่มรูปฟิสิกส์บางข้อ (matplotlib)
- แยกเฉลยไว้หน้าหลัง
"""

import json
import os
import random
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# ใช้ฟอนต์ที่รองรับภาษาไทย
plt.rcParams['font.family'] = 'FreeSerif'
plt.rcParams['axes.unicode_minus'] = False

# Physics image templates
def create_physics_image(question_type, output_path):
    """สร้างรูปฟิสิกส์ตามประเภทคำถาม"""
    fig, ax = plt.subplots(1, 1, figsize=(4, 3))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    if "กลศาสตร์" in question_type or "แรง" in question_type:
        # วาดลูกศรแรง
        ax.annotate('', xy=(8, 5), xytext=(2, 5),
                    arrowprops=dict(arrowstyle='->', lw=3, color='blue'))
        ax.text(5, 5.5, 'F', fontsize=14, ha='center', fontweight='bold')
        ax.add_patch(patches.Rectangle((1, 3), 3, 3, fill=True, color='gray', alpha=0.5))
        
    elif "คลื่น" in question_type or "เสียง" in question_type:
        # วาดคลื่น
        x = np.linspace(0, 4*np.pi, 100)
        ax.plot(x, np.sin(x), 'b-', linewidth=2)
        ax.set_title('คลื่น', fontsize=12)
        
    elif "แสง" in question_type or "กระจก" in question_type or "เลนส์" in question_type:
        # วาดกระจก/เลนส์
        ax.plot([2, 8], [5, 5], 'k-', linewidth=2)
        ax.plot([5, 5], [2, 8], 'k-', linewidth=2)
        ax.text(5, 9, 'เลนส์', fontsize=10, ha='center')
        
    elif "ไฟฟ้า" in question_type:
        # วา�ดวงจรไฟฟ้าง่ายๆ
        ax.add_patch(patches.Circle((3, 5), 0.8, fill=False, edgecolor='black', linewidth=2))
        ax.text(3, 5, 'R', fontsize=10, ha='center', va='center')
        ax.plot([3, 1], [5, 5], 'k-', linewidth=2)
        ax.plot([1, 1], [3, 7], 'k-', linewidth=2)
        
    elif "พลังงาน" in question_type or "งาน" in question_type:
        # วาดพลังงาน
        ax.text(5, 8, 'พลังงาน', fontsize=14, ha='center', fontweight='bold')
        ax.annotate('', xy=(5, 6), xytext=(5, 3),
                    arrowprops=dict(arrowstyle='->', lw=2, color='red'))
        ax.text(5.5, 4.5, 'h', fontsize=10)
        
    else:
        # วาดรูปทั่วไป
        ax.add_patch(patches.Circle((5, 5), 2, fill=False, edgecolor='black', linewidth=2))
        ax.text(5, 5, question_type[:3], fontsize=10, ha='center', va='center')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=100, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()

def add_question_with_image(doc, question_data, q_num, add_image=False):
    """เพิ่มคำถามพร้อมรูป (ถ้าต้องการ)"""
    q_text = question_data.get('question', '')
    q_type = question_data.get('topic', '')
    options = question_data.get('options', [])
    
    # หัวข้อคำถาม - เริ่มนับ 1 ใหม่
    p = doc.add_paragraph()
    run = p.add_run(f"{q_num}. {q_text}")
    run.font.size = Pt(12)
    
    # เพิ่มรูป (ถ้ามีและต้องการ)
    if add_image and random.random() < 0.3:  # 30% ของข้อจะมีรูป
        img_path = f"/tmp/physics_img_{q_num}.png"
        try:
            create_physics_image(q_type, img_path)
            if os.path.exists(img_path):
                doc.add_picture(img_path, width=Inches(2))
                doc.add_paragraph()  # บรรทัดว่าง
        except:
            pass
    
    # ตัวเลือก - เปลี่ยนจาก A B C D เป็น 1 2 3 4
    if options:
        for i, opt in enumerate(options, 1):
            p = doc.add_paragraph(f"    {i}. {opt}")
            p.paragraph_format.left_indent = Inches(0.5)
    
    doc.add_paragraph()  # บรรทัดว่าง

def convert_lesson_to_word(json_path, output_dir="/home/pi4eiei/tutoring-company/physics_course/word"):
    """แปลงไฟล์ JSON lesson → Word document"""
    os.makedirs(output_dir, exist_ok=True)
    
    # อ่าน JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    lesson_name = data.get('lesson', {}).get('name', 'Unknown')
    lesson_title = data.get('lesson', {}).get('title', 'ไม่ระบุ')
    questions = data.get('questions', [])
    
    # ชื่อไฟล์
    base_name = os.path.splitext(os.path.basename(json_path))[0]
    docx_path = os.path.join(output_dir, f"{base_name}.docx")
    answers_path = os.path.join(output_dir, f"{base_name}_เฉลย.docx")
    
    # ========== สร้างเอกสารคำถาม ==========
    doc = Document()
    doc.core_properties.title = lesson_title
    
    # หัวข้อ
    doc.add_heading(lesson_title, 0)
    doc.add_paragraph(f"บทที่ {lesson_name}")
    doc.add_paragraph()
    
    # คำถาม - เริ่มนับ 1 ใหม่ทุกบท
    for i, q in enumerate(questions, 1):
        add_question_with_image(doc, q, i, add_image=True)
    
    doc.save(docx_path)
    print(f"✅ สร้างเอกสาร: {docx_path}")
    
    # ========== สร้างเอกสารเฉลย ==========
    doc_ans = Document()
    doc_ans.core_properties.title = f"เฉลย {lesson_title}"
    doc_ans.add_heading(f"เฉลย {lesson_title}", 0)
    doc_ans.add_paragraph()
    
    for i, q in enumerate(questions, 1):
        answer = q.get('answer', '')
        solution = q.get('solution', '')
        
        # แปลงตัวอักษรเป็นตัวเลข
        if isinstance(answer, str) and len(answer) == 1:
            # A=1, B=2, C=3, D=4
            if answer.upper() in 'ABCD':
                answer = str(ord(answer.upper()) - ord('A') + 1)
        
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
    
    doc_ans.save(answers_path)
    print(f"✅ สร้างเฉลย: {answers_path}")
    
    return docx_path, answers_path

def convert_all_lessons(part_dir, output_dir):
    """แปลงทุกไฟล์ในโฟลเดอร์"""
    json_files = [f for f in os.listdir(part_dir) if f.endswith('.json') and 'extra' not in f]
    json_files.sort()
    
    print(f"พบ {len(json_files)} ไฟล์ใน {part_dir}")
    
    for f in json_files:
        json_path = os.path.join(part_dir, f)
        print(f"\n📄 กำลังแปลง: {f}")
        try:
            convert_lesson_to_word(json_path, output_dir)
        except Exception as e:
            print(f"❌ ผิดพลาด: {e}")

if __name__ == "__main__":
    import sys
    
    print("=" * 50)
    print("Physics Sheet → Word Converter")
    print("=" * 50)
    
    # แปลง part1 ก่อน (ทดสอบ)
    part1_dir = "/home/pi4eiei/tutoring-company/physics_course/part1"
    output_dir = "/home/pi4eiei/tutoring-company/physics_course/word"
    
    if len(sys.argv) > 1:
        # รับ argument
        part = sys.argv[1]
        part_dir = f"/home/pi4eiei/tutoring-company/physics_course/{part}"
        convert_all_lessons(part_dir, output_dir)
    else:
        # แปลงทุก part
        for part in ['part1', 'part2', 'part3']:
            print(f"\n{'='*50}")
            print(f"แปลง {part}")
            print(f"{'='*50}")
            part_dir = f"/home/pi4eiei/tutoring-company/physics_course/{part}"
            convert_all_lessons(part_dir, output_dir)
    
    print(f"\n✅ เสร็จสมบูรณ์! ไฟล์อยู่ที่: {output_dir}")
