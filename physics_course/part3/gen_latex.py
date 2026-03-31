#!/usr/bin/env python3
import json
import os

def escape_latex(text):
    """Escape special LaTeX characters."""
    if not isinstance(text, str):
        text = str(text)
    # Order matters - backslash first
    s = text.replace('\\', r'\textbackslash{}')
    s = s.replace('&', r'\&')
    s = s.replace('%', r'\%')
    s = s.replace('$', r'\$')
    s = s.replace('#', r'\#')
    s = s.replace('_', r'\_')
    s = s.replace('{', r'\{')
    s = s.replace('}', r'\}')
    s = s.replace('~', r'\textasciitilde{}')
    s = s.replace('^', r'\textasciicircum{}')
    return s

def generate_latex(lesson_num, is_extra=False):
    """Generate LaTeX file for a lesson."""
    suffix = f'_extra' if is_extra else ''
    json_file = f'lesson{lesson_num}{suffix}.json'
    tex_file = f'lesson{lesson_num}{suffix}.tex'

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    lesson_title = data['lesson']['title']
    questions = data['questions']

    lines = []
    lines.append(r'\documentclass[12pt]{article}')
    lines.append(r'\usepackage[UTF8]{inputenc}')
    lines.append(r'\usepackage{xeCJK}')
    lines.append(r'\setCJKmainfont{Sarabun}')
    lines.append(r'\usepackage{enumitem}')
    lines.append(r'\usepackage{geometry}')
    lines.append(r'\geometry{a4paper, margin=2.5cm}')
    lines.append(r'\usepackage{setspace}')
    lines.append(r'\onehalfspacing')
    lines.append('')
    lines.append(r'\begin{document}')
    lines.append('')
    lines.append(r'\begin{center}')
    lines.append(r'{\Large\textbf{' + escape_latex(lesson_title) + r'}}\\[6pt]')
    if is_extra:
        lines.append(r'{\normalsize แบบฝึกหัดเพิ่มเติม}\\[6pt]')
    lines.append(r'{\normalsize วิชาฟิสิกส์ ม.ปลาย บทที่ ' + str(lesson_num) + r'}\\[4pt]')
    lines.append(r'{\footnotesize ทั้งหมด ' + str(len(questions)) + r' ข้อ}')
    lines.append(r'\end{center}')
    lines.append(r'\hrule')
    lines.append(r'\bigskip')
    lines.append('')

    section_title = 'แบบฝึกหัดเพิ่มเติม' if is_extra else r'คำถาม in class'
    lines.append(r'\section*{' + escape_latex(section_title) + r'}')
    lines.append(r'\begin{enumerate}[label=\arabic*., itemsep=0.5\baselineskip, topsep=0.5\baselineskip, leftmargin=*]')

    for idx, q in enumerate(questions, 1):
        question_text = q['question']
        lines.append(r'\item ' + escape_latex(question_text))
        lines.append(r'\begin{enumerate}[label=\alph*)., itemsep=0.3\baselineskip, topsep=0.3\baselineskip]')

        options = q.get('options', {})
        for opt_key in sorted(options.keys()):
            opt_val = options[opt_key]
            lines.append(r'\item ' + escape_latex(opt_key) + r'\ ')
            lines.append(r'\begin{minipage}[t]{0.9\linewidth}')
            lines.append(r'\raggedright ' + escape_latex(opt_val))
            lines.append(r'\end{minipage}')

        lines.append(r'\end{enumerate}')

        answer = q.get('answer', '')
        if answer:
            lines.append(r'\vspace{-0.3\baselineskip}')
            lines.append(r'\begin{small}')
            lines.append(r'\textit{คำตอบ: ' + escape_latex(answer) + r'}')
            lines.append(r'\end{small}')

        lines.append('')

    lines.append(r'\end{enumerate}')
    lines.append(r'\end{document}')

    latex_content = '\n'.join(lines)

    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(latex_content)

    print(f'Generated: {tex_file} ({len(questions)} questions)')

def main():
    os.chdir('/home/pi4eiei/tutoring-company/physics_course/part3')

    for i in range(21, 31):
        generate_latex(i, is_extra=False)
        generate_latex(i, is_extra=True)

    print('\nAll done!')

if __name__ == '__main__':
    main()
