#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path

def uninstall_libraries():
    """卸载ap_ds音频库"""
    print("正在卸载ap_ds音频库...")
    
    # 1. 确定安装目录
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        target = Path(sys.prefix) / "Lib" / "site-packages" / "ap_ds"
    else:
        target = Path(sys.prefix) / "Lib" / "ap_ds"
    
    # 2. 检查是否存在
    if not target.exists():
        print(f"未找到安装目录: {target}")
        return
    
    # 3. 删除目录
    try:
        shutil.rmtree(target)
        print(f"已删除: {target}")
        print("卸载完成！")
    except Exception as e:
        print(f"卸载失败: {str(e)}")

if __name__ == "__main__":
    uninstall_libraries()
