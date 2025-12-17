#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将Markdown文件中的半角引号 " 替换为中文全角引号 “”
正确区分左引号“和右引号”
"""

import os
import re
from pathlib import Path

def replace_quotes(text):
    """
    将文本中的半角引号替换为中文全角引号
    策略：遇到半角引号 " 时，根据其前后的字符判断是左引号还是右引号
    - 左引号“：出现在行首、空格后、标点后、左括号后
    - 右引号”：出现在字母/数字/中文/标点前、行尾、空格前、右括号前
    """
    result = []
    i = 0
    quote_open = False  # 追踪引号状态

    while i < len(text):
        if text[i] == '"':
            # 获取前后字符
            prev_char = text[i-1] if i > 0 else '\n'
            next_char = text[i+1] if i < len(text) - 1 else '\n'

            # 判断是左引号还是右引号
            # 左引号的情况：
            # 1. 引号未开启状态（quote_open == False）
            # 2. 前面是空白、换行、左括号、左方括号、破折号
            is_left = False

            if not quote_open:
                # 如果引号未开启，这应该是左引号
                is_left = True
            else:
                # 如果引号已开启，检查是否是嵌套的左引号
                # 嵌套左引号前通常有：逗号、冒号、空格等
                if prev_char in [' ', '（', '【', '，', '：', '、', '\n', '\t']:
                    is_left = True

            if is_left:
                result.append('“')
                quote_open = True
            else:
                result.append('”')
                quote_open = False
        else:
            result.append(text[i])

        i += 1

    return ''.join(result)

def process_file(file_path):
    """处理单个文件"""
    print(f"处理文件: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否包含半角引号
        if '"' not in content:
            print(f"  跳过（无半角引号）")
            return False

        # 统计半角引号数量
        quote_count = content.count('"')
        print(f"  发现 {quote_count} 个半角引号")

        # 替换引号
        new_content = replace_quotes(content)

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  ✓ 完成")
        return True

    except Exception as e:
        print(f"  ✗ 错误: {e}")
        return False

def main():
    """主函数"""
    base_dir = Path(__file__).parent

    # 需要处理的文件列表
    files_to_process = []

    # 1. 处理根目录下的所有数字开头的.md文件
    for file in base_dir.glob('[0-9]*.md'):
        files_to_process.append(file)

    # 2. 处理其他重要文件
    other_files = [
        'CLAUDE.md',
        'README.md',
    ]
    for file_name in other_files:
        file_path = base_dir / file_name
        if file_path.exists():
            files_to_process.append(file_path)

    # 3. 处理子目录
    for subdir in ['planning', 'review', 'skills']:
        subdir_path = base_dir / subdir
        if subdir_path.exists():
            for file in subdir_path.glob('*.md'):
                files_to_process.append(file)

    # 排序文件列表
    files_to_process = sorted(files_to_process)

    print(f"共找到 {len(files_to_process)} 个文件需要检查\n")
    print("=" * 60)

    processed_count = 0
    for file_path in files_to_process:
        if process_file(file_path):
            processed_count += 1
        print()

    print("=" * 60)
    print(f"\n总计处理了 {processed_count} 个文件")

if __name__ == '__main__':
    main()
