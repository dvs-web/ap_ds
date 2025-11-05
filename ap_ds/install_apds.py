#!/usr/bin/env python3
import os,sys
import urllib.request
import shutil
import platform
from pathlib import Path
def download_sdl_libraries():
    files = [
        {
            "url": "https://dvsyun.top/ap_ds/download/SDL2",
            "expected_name": "SDL2.dll",
            "alt_names": ["SDL2 (1).dll", "SDL2_64.dll", "SDL2_x64.dll"]
        },
        {
            "url": "https://dvsyun.top/ap_ds/download/SDL2_M",
            "expected_name": "SDL2_mixer.dll",
            "alt_names": ["SDL2_mixer (1).dll", "SDL2_mixer_64.dll", "SDL2_mixer_x64.dll"]
        },
        {
            "url": "https://dvsyun.top/ap_ds/download/AParser_DLL",
            "expected_name": "audio_parser.dll",
            "alt_names": ["audio_parser.dll (1).dll"]
        }
    ]
    
    for file_info in files:
        for alt_name in file_info["alt_names"]:
            if os.path.exists(alt_name):
                if alt_name != file_info["expected_name"]:
                    os.rename(alt_name, file_info["expected_name"])
                    print(f"正在将 '{alt_name}' 重命名为 '{file_info['expected_name']}'")
                break
        
        if not os.path.exists(file_info["expected_name"]):
            print(f"正在下载文件 {file_info['expected_name']}...")
            try:
                # Use built-in urllib.request to download files
                with urllib.request.urlopen(file_info["url"], timeout=10) as response:
                    with open(file_info["expected_name"], 'wb') as f:
                        f.write(response.read())
                
                print(f"该文件已下载成功：{file_info['expected_name']}")
            except Exception as e:
                raise RuntimeError(f"Failed to download {file_info['expected_name']}: {str(e)}")

download_sdl_libraries()

def get_apds_path():
    """获取ap_ds目录路径"""
    # 检查是否在虚拟环境中
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        target = Path(sys.prefix) / "Lib" / "site-packages" / "ap_ds"
    else:
        # 标准Python安装
        target = Path(sys.prefix) / "Lib" / "ap_ds"
    
    target.mkdir(parents=True, exist_ok=True)
    return target

def install_libraries():
    """安装SDL库和Python音频库"""
    print("正在安装ap_ds音频库...")
    
    # 1. 创建目标目录
    apds_path = get_apds_path()
    print(f"目标安装目录: {apds_path}")
    
    # 2. 复制当前目录的SDL库文件
    current_dir = Path(__file__).parent.resolve()
    
    # 需要复制的文件列表
    required_files = [
        "__init__.py",
        "SDL2.dll", 
        "SDL2_mixer.dll",
        "player.py",
        "audio_parser.dll",
        "audio_parser.py"
    ]
    
    # 3. 复制文件
    for file in required_files:
        src = current_dir / file
        if src.exists():
            shutil.copy2(src, apds_path)
            print(f"已复制: {file}")
        else:
            print(f"警告: 未找到 {file}")
    
    # 4. 创建__init__.py
    (apds_path / "__init__.py").touch()
    
    # 5. 添加到Python路径
    add_to_pythonpath(apds_path)
    
    print("\n安装成功！")
    print(f"音频库已安装到: {apds_path}")
    print("你可以通过 'import ap_ds' 来使用")

def add_to_pythonpath(path):
    """将路径添加到PYTHONPATH"""
    path = str(path)
    if path not in sys.path:
        sys.path.append(path)
        print(f"已将 {path} 添加到当前Python路径")

if __name__ == "__main__":
    install_libraries()
