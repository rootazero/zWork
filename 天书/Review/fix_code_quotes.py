#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将Markdown技术内容中的中文全角引号 "" 改回半角引号 "
包括：HTML标签属性、代码块、内联代码等
"""

import os
import re
from pathlib import Path

def fix_code_quotes(text):
    """
    将技术内容中的中文全角引号替换为半角引号

    处理范围：
    1. HTML标签属性：<tag attr="value">
    2. 代码块：```...```
    3. 内联代码：`...`
    4. Markdown链接：[text](url)
    """
    result = []
    i = 0

    while i < len(text):
        # 检查是否在代码块中（```开始）
        if i < len(text) - 2 and text[i:i+3] == '```':
            # 找到代码块结束
            result.append('```')
            i += 3

            # 处理代码块内容
            code_block = []
            while i < len(text):
                if i < len(text) - 2 and text[i:i+3] == '```':
                    # 代码块结束，替换其中的中文引号
                    code_content = ''.join(code_block)
                    code_content = code_content.replace('"', '"').replace('"', '"')
                    result.append(code_content)
                    result.append('```')
                    i += 3
                    break
                else:
                    code_block.append(text[i])
                    i += 1
            continue

        # 检查是否在内联代码中（`开始）
        if text[i] == '`':
            result.append('`')
            i += 1

            # 处理内联代码内容
            inline_code = []
            while i < len(text) and text[i] != '`':
                inline_code.append(text[i])
                i += 1

            # 替换内联代码中的中文引号
            code_content = ''.join(inline_code)
            code_content = code_content.replace('"', '"').replace('"', '"')
            result.append(code_content)

            if i < len(text):
                result.append('`')
                i += 1
            continue

        # 检查是否在HTML标签中（<开始）
        if text[i] == '<':
            # 找到标签结束
            tag_start = i
            tag_content = []
            tag_content.append('<')
            i += 1

            while i < len(text) and text[i] != '>':
                tag_content.append(text[i])
                i += 1

            if i < len(text):
                tag_content.append('>')
                i += 1

            # 替换标签中的中文引号
            tag_str = ''.join(tag_content)
            tag_str = tag_str.replace('"', '"').replace('"', '"')
            result.append(tag_str)
            continue

        # 检查Markdown链接 [text](url)
        if text[i] == '[':
            bracket_content = []
            bracket_content.append('[')
            i += 1

            # 读取到 ]
            while i < len(text) and text[i] != ']':
                bracket_content.append(text[i])
                i += 1

            if i < len(text):
                bracket_content.append(']')
                i += 1

                # 检查是否后面跟着 (
                if i < len(text) and text[i] == '(':
                    bracket_content.append('(')
                    i += 1

                    # 读取到 )
                    while i < len(text) and text[i] != ')':
                        bracket_content.append(text[i])
                        i += 1

                    if i < len(text):
                        bracket_content.append(')')
                        i += 1

                    # 替换链接中的中文引号（如果有）
                    link_str = ''.join(bracket_content)
                    link_str = link_str.replace('"', '"').replace('"', '"')
                    result.append(link_str)
                    continue

            result.extend(bracket_content)
            continue

        # 普通字符，保持不变
        result.append(text[i])
        i += 1

    return ''.join(result)

def process_file(file_path):
    """处理单个文件"""
    print(f"处理文件: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否包含需要修复的内容
        has_html = '<' in content and '>' in content
        has_code = '`' in content or '```' in content

        if not (has_html or has_code):
            print(f"  跳过（无需修复）")
            return False

        # 检查是否有中文引号在代码相关内容中
        # 简单检查：是否同时包含中文引号和HTML/代码标记
        has_chinese_quotes = '"' in content or '"' in content
        if not has_chinese_quotes:
            print(f"  跳过（无中文引号）")
            return False

        # 修复引号
        new_content = fix_code_quotes(content)

        # 如果内容没有变化，跳过
        if new_content == content:
            print(f"  跳过（无需修改）")
            return False

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
        '0.封面.md',
        '0.目录.md',
        'CLAUDE.md',
        'README.md',
    ]
    for file_name in other_files:
        file_path = base_dir / file_name
        if file_path.exists() and file_path not in files_to_process:
            files_to_process.append(file_path)

    # 3. 处理子目录
    for subdir in ['planning', 'review', 'skills']:
        subdir_path = base_dir / subdir
        if subdir_path.exists():
            for file in subdir_path.glob('*.md'):
                files_to_process.append(file)

    # 排序文件列表
    files_to_process = sorted(set(files_to_process))

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
