#!/usr/bin/env python3
"""ดูสรุปรายรับ-รายจ่าย"""
import csv
import json
from datetime import datetime
from collections import defaultdict

def load_transactions():
    transactions = []
    with open('transactions.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['date']:  # skip empty rows
                transactions.append(row)
    return transactions

def load_categories():
    with open('categories.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def print_summary(month=None, year=None):
    transactions = load_transactions()
    categories = load_categories()
    
    total_income = 0
    total_expense = 0
    by_category = defaultdict(lambda: {'income': 0, 'expense': 0})
    
    for t in transactions:
        t_date = datetime.strptime(t['date'], '%Y-%m-%d')
        if month and t_date.month != month:
            continue
        if year and t_date.year != year:
            continue
            
        amount = float(t['amount'])
        if t['type'] == 'income':
            total_income += amount
            by_category[t['category']]['income'] += amount
        else:
            total_expense += amount
            by_category[t['category']]['expense'] += amount
    
    print("=" * 50)
    print("📊 สรุปบัญชีรายรับ-รายจ่าย")
    if month and year:
        print(f"   เดือน {month}/{year}")
    else:
        print(f"   ทั้งหมด")
    print("=" * 50)
    print(f"💰 รายรับ: {total_income:,.2f} บาท")
    print(f"💸 รายจ่าย: {total_expense:,.2f} บาท")
    print(f"📈 คงเหลือ: {total_income - total_expense:,.2f} บาท")
    print()
    print("--- รายจ่ายตามหมวด ---")
    for cat, vals in sorted(by_category.items(), key=lambda x: x[1]['expense'], reverse=True):
        if vals['expense'] > 0:
            print(f"  {cat}: {vals['expense']:,.2f} บาท")

if __name__ == '__main__':
    import sys
    month = int(sys.argv[1]) if len(sys.argv) > 1 else None
    year = int(sys.argv[2]) if len(sys.argv) > 2 else None
    print_summary(month, year)
