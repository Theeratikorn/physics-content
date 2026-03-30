#!/usr/bin/env python3
"""
Physics Course Generator
Generates LaTeX documents from JSON question database
"""

import json
import os
import argparse
from datetime import datetime

# TikZ templates for diagrams
TIKZ_TEMPLATES = {
    "units": r"""
\begin{tikzpicture}[scale=0.6, every node/.style={scale=0.8}]
    % Unit conversion diagram
    \draw[thick,->] (0,0) -- (4,0) node[midway,above] {$10^{3}$};
    \draw[thick,->] (4,0) -- (8,0) node[midway,above] {$10^{3}$};
    \draw[thick,->] (8,0) -- (12,0) node[midway,above] {$10^{3}$};
    \node at (0,-0.5) {k};
    \node at (4,-0.5) {h};
    \node at (8,-0.5) {da};
    \node at (12,-0.5) {base};
\end{tikzpicture}""",
    
    "measurement": r"""
\begin{tikzpicture}[scale=0.8]
    % Measurement scale
    \draw[thick] (0,0) -- (10,0);
    \foreach \x/\label in {0/0, 2/2, 4/4, 6/6, 8/8, 10/10}
        \draw (\x,0) -- (\x,-0.2) node[below] {\label};
    \draw[red, thick, <->] (3,0.5) -- (7,0.5) node[midway,above] {$L$};
    \fill (3,0) circle[radius=2pt] node[above] {$A$};
    \fill (7,0) circle[radius=2pt] node[above] {$B$};
\end{tikzpicture}""",
    
    "vector": r"""
\begin{tikzpicture}[scale=0.8,>=stealth]
    \draw[->, thick] (0,0) -- (3,0) node[midway,below] {$\vec{F}_1$};
    \draw[->, thick] (0,0) -- (0,2.5) node[midway,left] {$\vec{F}_2$};
    \draw[->, thick, dashed] (0,0) -- (3,2.5) node[midway,above right] {$\vec{R}$};
    \draw (0.5,0) arc (0:90:0.5);
    \node at (0.3,0.25) {$\theta$};
\end{tikzpicture}"""
}

class PhysicsCourseGenerator:
    def __init__(self, base_path="."):
        self.base_path = base_path
        
    def load_json(self, filepath):
        """Load JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_question(self, q, number):
        """Generate LaTeX for a single question"""
        if q['type'] == 'choice':
            return self._generate_choice_question(q, number)
        else:
            return self._generate_calculation_question(q, number)
    
    def _generate_choice_question(self, q, number):
        """Generate choice question with options A-D"""
        latex = f"\\item[{number}] {q['question']}\n"
        latex += "\\begin{enumerate}\n"
        for opt_key, opt_val in q['options'].items():
            latex += f"\\item {opt_val}\n"
        latex += "\\end{enumerate}\n"
        latex += f"\\textbf{{คำตอบ: }} {q['answer']}\n"
        latex += f"\\textit{{เฉลย: }} {q['solution']}\n"
        latex += "\\HRule\n"
        return latex
    
    def _generate_calculation_question(self, q, number):
        """Generate calculation question with detailed solution"""
        latex = f"\\item[{number}] {q['question']}\n"
        latex += f"\\textbf{{คำตอบ: }} {q['answer']}\n"
        latex += f"\\textit{{วิธีทำ: }} {q['solution']}\n"
        latex += "\\HRule\n"
        return latex
    
    def generate_tikz(self, topic):
        """Generate TikZ diagram based on topic"""
        for key, template in TIKZ_TEMPLATES.items():
            if key in topic.lower():
                return template
        return ""
    
    def generate_lesson_latex(self, lesson_json, extra_json=None):
        """Generate complete LaTeX document for a lesson"""
        lesson = lesson_json['lesson']
        
        latex = self._latex_header(lesson)
        latex += "\n\\begin{document}\n"
        
        # Title
        latex += f"\\title{{\\textbf{{Part {lesson['part']}: ครั้งที่ {lesson['lesson_number']}}}}}\n"
        latex += f"\\subtitle{{{lesson['title']}}}\n"
        latex += f"\\date{{\\today}}\n"
        latex += "\\maketitle\n"
        
        # Topics
        latex += "\\section*{หัวข้อที่เรียน}\n"
        latex += "\\begin{itemize}\n"
        for topic in lesson['topics']:
            latex += f"\\item {topic}\n"
        latex += "\\end{itemize}\n"
        
        # Questions in class
        latex += f"\\newpage\n\\section*{{แบบฝึกหัดในคาบ ({lesson['in_class_questions']} ข้อ)}}\n"
        latex += "\\begin{enumerate}\n"
        for i, q in enumerate(lesson_json['questions'][:lesson['in_class_questions']], 1):
            # Add TikZ if applicable
            tikz = self.generate_tikz(q['topic'])
            if tikz:
                latex += f"\\begin{{center}}{tikz}\\end{{center}}\n"
            latex += self.generate_question(q, i)
        latex += "\\end{enumerate}\n"
        
        # Extra questions
        if extra_json:
            latex += f"\\newpage\n\\section*{{แบบฝึกเพิ่มเติม ({lesson['extra_questions']} ข้อ)}}\n"
            latex += "\\begin{enumerate}\n"
            for i, q in enumerate(extra_json['questions'][:lesson['extra_questions']], 1):
                tikz = self.generate_tikz(q['topic'])
                if tikz:
                    latex += f"\\begin{{center}}{tikz}\\end{{center}}\n"
                latex += self.generate_question(q, i)
            latex += "\\end{enumerate}\n"
        
        latex += "\\end{document}\n"
        
        return latex
    
    def _latex_header(self, lesson):
        """Generate LaTeX preamble"""
        return r"""\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{thaisup}
\usepackage{graphicx}
\usepackage{tikz}
\usepackage{amsmath,amssymb}
\usepackage{geometry}
\geometry{margin=2.5cm}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{booktabs}
\usepackage{hyperref}

% Header/Footer
\pagestyle{fancy}
\fancyhf{}
\rhead{Part """ + str(lesson['part']) + r"""}
\lhead{ครั้งที่ """ + str(lesson['lesson_number']) + r"""}
\rfoot{หน้า \thepage}

% Question formatting
\setlist[enumerate]{fullwidth, itemindent=2em, label=\arabic*.}
\renewenvironment{enumerate}{\begin{trivlist}\item\薄}{\end{trivlist}}
\let\薄\item

% Line separator
\newcommand{\HRule}{\\ \hline \\}

% Answer box
\\newcounter{savedenum}
\usepackage{etoolbox}
\AtBeginEnvironment{enumerate}{\\stepcounter{savedenum}}

\begin{document}
"""
    
    def generate(self, lesson_path, extra_path=None, output_path=None):
        """Generate LaTeX from JSON files"""
        lesson_json = self.load_json(lesson_path)
        
        extra_json = None
        if extra_path and os.path.exists(extra_path):
            extra_json = self.load_json(extra_path)
        
        latex_content = self.generate_lesson_latex(lesson_json, extra_json)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            print(f"Generated: {output_path}")
        
        return latex_content

def main():
    parser = argparse.ArgumentParser(description='Physics Course Generator')
    parser.add_argument('lesson_json', help='Path to lesson JSON file')
    parser.add_argument('--extra', help='Path to extra questions JSON file')
    parser.add_argument('-o', '--output', help='Output LaTeX file path')
    parser.add_argument('--dir', help='Base directory for output')
    
    args = parser.parse_args()
    
    generator = PhysicsCourseGenerator()
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        lesson_name = os.path.splitext(os.path.basename(args.lesson_json))[0]
        output_path = f"{lesson_name}.tex"
    
    if args.dir:
        os.makedirs(args.dir, exist_ok=True)
        output_path = os.path.join(args.dir, os.path.basename(output_path))
    
    extra_path = args.extra if args.extra else None
    
    generator.generate(args.lesson_json, extra_path, output_path)
    print(f"\\nTo compile to PDF, run:")
    print(f"  pdflatex {output_path}")

if __name__ == "__main__":
    main()
