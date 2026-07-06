#!/usr/bin/env python3
import sys
import os

def audit_file(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} does not exist.")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    total_lines = len(lines)
    total_chars = sum(len(line) for line in lines)
    
    empty_lines = 0
    comment_lines = 0
    code_lines = 0

    for line in lines:
        stripped = line.strip()
        if not stripped:
            empty_lines += 1
        elif stripped.startswith('#') or stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
            comment_lines += 1
        else:
            code_lines += 1

    code_ratio = (code_lines / total_lines * 100) if total_lines > 0 else 0
    comment_ratio = (comment_lines / total_lines * 100) if total_lines > 0 else 0
    empty_ratio = (empty_lines / total_lines * 100) if total_lines > 0 else 0

    print("==================================================")
    print(f" TOKEN DENSITY AUDIT FOR: {os.path.basename(filepath)}")
    print("==================================================")
    print(f"Total Lines:          {total_lines}")
    print(f"Total Characters:     {total_chars}")
    print(f"Code Lines:           {code_lines} ({code_ratio:.1f}%)")
    print(f"Comment/Doc Lines:    {comment_lines} ({comment_ratio:.1f}%)")
    print(f"Whitespace Lines:     {empty_lines} ({empty_ratio:.1f}%)")
    
    # Calculate Signal-to-Noise Ratio (SNR)
    # High empty line and comment ratios reduce token density in pure execution context
    snr = (code_lines / (comment_lines + empty_lines + 1))
    print(f"Signal-to-Noise Ratio:{snr:.2f}")
    
    print("--------------------------------------------------")
    if snr < 1.0:
        print("💡 Recommendation: Context is highly verbose. Consider stripping redundant docstrings and excessive blank lines before feeding to low-latency models.")
    else:
        print("💡 Recommendation: Excellent token density. The code has a strong signal-to-noise ratio.")
    print("==================================================")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 audit_tokens.py <filepath>")
        sys.exit(1)
    audit_file(sys.argv[1])
