#!/usr/bin/env python3
# labs/03_clean_and_stats.py — 简单清洗与质量检测脚本
import sys
from collections import Counter

def load_sample(path):
    with open(path,'r',encoding='utf-8') as f:
        lines = [l.strip() for l in f if l.strip()]
    return lines

if __name__=='__main__':
    if len(sys.argv)<2:
        print('USAGE: python labs/03_clean_and_stats.py data/sample.txt')
        sys.exit(2)
    path = sys.argv[1]
    lines = load_sample(path)
    print('TOTAL', len(lines))
    uniq = list(dict.fromkeys(lines))
    print('UNIQ', len(uniq))
    lens = [len(l.split()) for l in uniq]
    print('AVG_LEN', sum(lens)/len(lens) if lens else 0)
    tokens = Counter()
    for l in uniq:
        tokens.update(l.split())
    print('TOP_20', tokens.most_common(20))
