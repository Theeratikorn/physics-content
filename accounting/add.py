#!/usr/bin/env python3
"""เพิ่มรายการรายรับ-รายจ่าย"""
import csv
import json
import sys
from datetime import datetime

def load_categories():
    with open('categories.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def add_transaction(date, type_, category, amount, description):
    with open('transactions.csv', 'a', encoding='utf-8') as f:
        f.write(f"{date},{type_},{category},{amount},{description}\n")
    print(f"✅ เพิ่มแล้ว: {date} | {type_} | {category} | {amount} บาท")

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("ใช้: add.py YYYY-MM-DD income/expense หมวด จำนวน [คำอธิบาย]")
        print("ตัวอย่าง: add.py 2026-04-09 expense ค่าเดินทาง 150 ค่าแท็กซี่")
        sys.exit(1)
    
    date = sys.argv[1]
    type_ = sys.argv[2]
    category = sys.argv[3]
    amount = sys.argv[4]
    description = sys.argv[5] if len(sys.argv) > 5 else ""
    
    add_transaction(date, type_, category, amount, description)
