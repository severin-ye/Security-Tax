#!/usr/bin/env python3
"""自动为韩文LaTeX文件中的韩文文本添加\ko{}包裹"""

import re

def is_korean_char(ch):
    """判断字符是否为韩文字符"""
    code = ord(ch)
    return (0xAC00 <= code <= 0xD7A3) or (0x1100 <= code <= 0x11FF) or (0x3130 <= code <= 0x318F)

def wrap_korean_text(text):
    """为韩文文本段落添加\ko{}包裹"""
    # 跳过已经被\ko{}包裹的内容
    if '\\ko{' in text:
        return text
    
    result = []
    i = 0
    while i < len(text):
        # 跳过LaTeX命令
        if text[i] == '\\':
            # 找到命令结束
            j = i + 1
            while j < len(text) and (text[j].isalpha() or text[j] in '\\{}[]'):
                j += 1
            result.append(text[i:j])
            i = j
            continue
        
        # 检查是否是韩文字符
        if is_korean_char(text[i]):
            # 收集连续的韩文和空格
            korean_text = []
            j = i
            while j < len(text):
                if is_korean_char(text[j]) or text[j] in ' \t':
                    korean_text.append(text[j])
                    j += 1
                elif text[j] in '(),.:;!?·':
                    korean_text.append(text[j])
                    j += 1
                else:
                    break
            
            # 去除尾部空格
            korean_str = ''.join(korean_text).rstrip()
            if korean_str:
                result.append(f'\\ko{{{korean_str}}}')
            i = j
        else:
            result.append(text[i])
            i += 1
    
    return ''.join(result)

def process_latex_file(input_file, output_file):
    """处理LaTeX文件"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 按行处理
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        # 跳过注释行
        if line.strip().startswith('%'):
            new_lines.append(line)
            continue
        
        # 跳过包含LaTeX命令定义的行
        if any(cmd in line for cmd in ['\\newcommand', '\\usepackage', '\\documentclass', '\\setCJKmainfont', '\\newCJKfontfamily']):
            new_lines.append(line)
            continue
        
        # 检查是否包含韩文
        has_korean = any(is_korean_char(ch) for ch in line)
        if has_korean and '\\ko{' not in line:
            new_line = wrap_korean_text(line)
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    
    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print(f"✅ 处理完成: {output_file}")

if __name__ == '__main__':
    process_latex_file('论文初稿_韩文.tex', '论文初稿_韩文_wrapped.tex')
