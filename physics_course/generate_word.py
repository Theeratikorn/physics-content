#!/usr/bin/env python3
"""
Physics JSON → Word Generator
ใช้ง่าย: python generate_word.py [ไฟล์.json] [โฟลเดอร์เอาท์พุต]

ตัวอย่าง:
  python generate_word.py lesson01.json
  python generate_word.py lesson01.json output/
  python generate_word.py part1/
"""

import json
import os
import sys
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def convert_to_word(json_path, output_dir=".", create_answer=True):
    """แปลง JSON → Word document"""
    
    # อ่าน JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    lesson_name = data.get('lesson', {}).get('name', 'Unknown')
    lesson_title = data.get('lesson', {}).get('title', 'ไม่ระบุ')
    questions = data.get('questions', [])
    
    base_name = os.path.splitext(os.path.basename(json_path))[0]
    
    # ========== สร้างเอกสารคำถาม ==========
    doc = Document()
    doc.core_properties.title = lesson_title
    
    doc.add_heading(lesson_title, 0)
    doc.add_paragraph(f"บทที่ {lesson_name}")
    doc.add_paragraph()
    
    # คำถาม - ข้อ 1-25 ต่อบท, ช้อย 1-4
    for i, q in enumerate(questions, 1):
        q_text = q.get('question', '')
        
        # คำถาม
        p = doc.add_paragraph()
        run = p.add_run(f"{i}. {q_text}")
        run.font.size = Pt(12)
        
        # ตัวเลือก 1-4
        options = q.get('options') or []
        for j, opt in enumerate(options, 1):
            p = doc.add_paragraph(f"    {j}. {opt}")
            p.paragraph_format.left_indent = Inches(0.5)
        
        doc.add_paragraph()
    
    docx_path = os.path.join(output_dir, f"{base_name}.docx")
    doc.save(docx_path)
    print(f"✅ คำถาม: {docx_path}")
    
    # ========== สร้างเอกสารเฉลย ==========
    if create_answer:
        doc_ans = Document()
        doc_ans.core_properties.title = f"เฉลย {lesson_title}"
        doc_ans.add_heading(f"เฉลย {lesson_title}", 0)
        doc_ans.add_paragraph()
        
        for i, q in enumerate(questions, 1):
            answer = q.get('answer', '')
            solution = q.get('solution', '')
            
            # แปลง A=1, B=2, C=3, D=4
            if isinstance(answer, str) and len(answer) == 1 and answer.upper() in 'ABCD':
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
        
        ans_path = os.path.join(output_dir, f"{base_name}_เฉลย.docx")
        doc_ans.save(ans_path)
        print(f"✅ เฉลย: {ans_path}")
    
    return docx_path

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("=" * 50)
        print("ตัวอย่าง:")
        print("  python generate_word.py lesson01.json")
        print("  python generate_word.py lesson01.json output/")
        print("  python generate_word.py part1/")
        return
    
    arg = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    os.makedirs(output_dir, exist_ok=True)
    
    if os.path.isdir(arg):
        # ถ้าเป็นโฟลเดอร์ หาไฟล์ .json
        json_files = sorted([f for f in os.listdir(arg) if f.endswith('.json') and 'extra' not in f])
        print(f"พบ {len(json_files)} ไฟล์ใน {arg}")
        
        for f in json_files:
            print(f"\n📄 {f}")
            try:
                convert_to_word(os.path.join(arg, f), output_dir)
            except Exception as e:
                print(f"❌ ผิดพลาด: {e}")
        
        print(f"\n✅ เสร็จสมบูรณ์! ไฟล์อยู่ที่: {output_dir}")
    
    elif os.path.isfile(arg):
        # ถ้าเป็นไฟล์เดียว
        convert_to_word(arg, output_dir)
    
    else:
        print(f"❌ ไม่พบ: {arg}")

if __name__ == "__main__":
    main()
