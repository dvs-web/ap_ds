# ap_ds - Python 音频播放库

基于 SDL2 的简单易用音频播放库，支持多种音频格式，专为 Python 开发者设计。

## 🌟 特性

- 🎵 **多格式支持**: MP3, WAV, OGG, FLAC, M4A, AAC 等主流音频格式
- 🚀 **简单易用**: 直观的 API 设计，几行代码即可播放音频
- 💾 **内存管理**: 智能缓存机制，高效内存使用
- ⏱️ **精确控制**: 播放、暂停、继续、停止、跳转、音量控制
- 📊 **时长获取**: 自动获取音频文件时长信息
- 🔧 **自动下载**: 自动下载所需的 DLL 依赖文件
- 🖥️ **跨平台**: 支持 Windows 系统

## 📦 安装

### 方法一：双击安装（最简单）
1. 下载本项目到本地
2. 双击运行 `install_apds.py`
3. 等待安装完成

### 方法二：命令行安装
```bash
# 克隆项目
git clone https://github.com/yourusername/ap_ds.git
cd ap_ds

# 运行安装脚本
python install_apds.py
```

### 方法三：手动安装
```bash
# 使用 pip 安装
pip install git+https://github.com/yourusername/ap_ds.git
```

## 🚀 快速开始

### 基础播放
```python
from ap_ds import AudioLibrary

# 创建音频库实例
lib = AudioLibrary()

# 播放音频文件
aid = lib.play_from_file("music.mp3")
print(f"开始播放，音频ID: {aid}")

# 等待播放完成（在实际应用中应该使用事件循环）
import time
time.sleep(10)

# 停止播放
lib.stop_audio(aid)
```

### 完整控制示例
```python
from ap_ds import AudioLibrary
import time

# 初始化音频库
lib = AudioLibrary()

try:
    # 播放音频
    audio_file = "sample.mp3"
    aid = lib.play_from_file(audio_file)
    print(f"开始播放: {audio_file}")
    
    # 获取音频时长
    duration = lib.get_audio_duration(audio_file, is_file=True)
    print(f"音频时长: {duration} 秒")
    
    # 播放3秒后暂停
    time.sleep(3)
    lib.pause_audio(aid)
    print("音频已暂停")
    
    # 2秒后继续播放
    time.sleep(2)
    lib.play_audio(aid)
    print("继续播放")
    
    # 设置音量（0-128）
    lib.set_volume(aid, 80)
    print("音量设置为80")
    
    # 等待播放结束
    remaining = duration - 5  # 减去已经播放的时间
    if remaining > 0:
        time.sleep(remaining)
    
    print("播放完成!")
    
finally:
    # 停止播放
    lib.stop_audio(aid)
```

## 📚 API 参考

### AudioLibrary 类

#### 初始化
```python
lib = AudioLibrary(frequency=44100, format=MIX_DEFAULT_FORMAT, channels=2, chunksize=2048)
```

#### 核心方法

| 方法 | 描述 | 参数 | 返回 |
|------|------|------|------|
| `play_from_file(file_path, loops=0, start_pos=0.0)` | 从文件播放 | `file_path`: 文件路径, `loops`: 循环次数, `start_pos`: 开始位置(秒) | 音频ID (aid) |
| `play_from_memory(file_path, loops=0, start_pos=0.0)` | 从内存缓存播放 | 同上 | 音频ID (aid) |
| `new_aid(file_path)` | 预加载音频到内存 | `file_path`: 文件路径 | 音频ID (aid) |
| `play_audio(aid)` | 播放/继续音频 | `aid`: 音频ID | None |
| `pause_audio(aid)` | 暂停音频 | `aid`: 音频ID | None |
| `stop_audio(aid)` | 停止音频 | `aid`: 音频ID | 已播放时长(秒) |
| `seek_audio(aid, position)` | 跳转到指定位置 | `aid`: 音频ID, `position`: 位置(秒) | None |
| `set_volume(aid, volume)` | 设置音量 | `aid`: 音频ID, `volume`: 音量(0-128) | bool |
| `get_volume(aid)` | 获取音量 | `aid`: 音频ID | 当前音量(0-128) |
| `get_audio_duration(source, is_file=False)` | 获取音频时长 | `source`: 文件路径或音频ID | 时长(秒)或(0, 错误信息) |

## 🎯 高级用法

### 预加载多个音频文件
```python
from ap_ds import AudioLibrary

lib = AudioLibrary()

# 预加载多个音频文件
audio_files = ["sound1.mp3", "sound2.wav", "music.ogg"]
aids = {}

for file in audio_files:
    try:
        aid = lib.new_aid(file)
        aids[file] = aid
        print(f"已加载: {file} -> AID: {aid}")
    except Exception as e:
        print(f"加载失败 {file}: {e}")

# 快速播放预加载的音频
lib.play_audio(aids["sound1.mp3"])
```

### 音频队列播放
```python
import time
from ap_ds import AudioLibrary

class AudioQueue:
    def __init__(self):
        self.lib = AudioLibrary()
        self.queue = []
        self.current_aid = None
        
    def add_to_queue(self, file_path):
        self.queue.append(file_path)
        
    def play_next(self):
        if self.queue:
            file_path = self.queue.pop(0)
            self.current_aid = self.lib.play_from_file(file_path)
            duration = self.lib.get_audio_duration(file_path, is_file=True)
            print(f"正在播放: {file_path} (时长: {duration}秒)")
            return duration
        return 0

# 使用示例
queue = AudioQueue()
queue.add_to_queue("song1.mp3")
queue.add_to_queue("song2.mp3")
queue.add_to_queue("song3.mp3")

while queue.queue:
    duration = queue.play_next()
    if duration > 0:
        time.sleep(duration + 1)  # 等待当前音频播放完成
```

## 🔧 故障排除

### 常见问题

**Q: 安装时出现 DLL 下载错误**
A: 检查网络连接，或手动下载 DLL 文件放置在同一目录下

**Q: 播放没有声音**
A: 检查系统音量，确认音频文件格式支持，检查文件路径是否正确

**Q: 出现 SDL 初始化错误**
A: 以管理员权限运行程序，或检查音频驱动是否正常

**Q: 如何卸载库？**
A: 双击运行 `uninstall_apds.py` 脚本

### 支持的音频格式
- ✅ MP3 (.mp3)
- ✅ WAV (.wav)
- ✅ OGG (.ogg)
- ✅ FLAC (.flac)

## 📁 项目结构
```
ap_ds/
├── README.md                 # 项目说明文档
├── requirements.txt         # 依赖说明
├── ap_ds/                  # 主包目录
│   ├── __init__.py
│   ├── player.py
│   ├── audio_parser.py
│   ├── install_apds.py
│   └── uninstall_apds.py
└── dist/                   # 发布文件（可选）
    ├── SDL2.dll
    ├── SDL2_mixer.dll
    └── audio_parser.dll
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 🙏 致谢

- [SDL2](https://www.libsdl.org/) - 底层音频库
- [SDL2_mixer](https://www.libsdl.org/projects/SDL_mixer/) - 音频混合库

## 📞 支持

- 📧 邮箱: me@dvsyun.top
- 🐛 [Issues](https://github.com/yourusername/ap_ds/issues)
- 🌐 [官方网站](https://www.dvsyun.top/ap_ds)

---

**开始使用**: 双击 `install_apds.py` 即可安装，然后参考示例代码开始使用！

**注意**: 首次运行会自动下载所需的 DLL 文件，请确保网络连接正常。
