---
name: vision
description: >-
  分析图片内容的技能——使用阿里云百炼视觉模型（通义千问 VL）识别图片中的文字、物体、场景等。
  当用户说"帮我看看这张图"、"分析这个图片"、"提取图中文字"、"这张图里有什么"、"看图"或类似意图时使用此技能。
  也适用于用户要求"OCR"、"识别图片"、"图片里写了什么"等场景。
  注意：即使用户只是发了一张截图没有明确说"分析"，只要上下文暗示需要理解图片内容，就应使用此技能。
---

# Vision —— 图片分析技能

用阿里云百炼视觉大模型分析图片内容。支持从剪贴板读取截图，也支持指定本地文件路径。

## 使用方式

技能提供了一个 Python 脚本 `scripts/analyze_image.py`，**直接运行即可**：

```bash
# 方式 1：分析剪贴板中的截图（最常用）
python ~/.claude/skills/vision/scripts/analyze_image.py --clipboard

# 方式 2：分析本地图片文件
python ~/.claude/skills/vision/scripts/analyze_image.py --file "C:/path/to/image.png"

# 方式 3：带自定义提示词
python ~/.claude/skills/vision/scripts/analyze_image.py --clipboard --prompt "提取图中所有文字"
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `--clipboard` / `-c` | 从 Windows 剪贴板读取图片 |
| `--file PATH` / `-f PATH` | 指定本地图片路径 |
| `--prompt TEXT` / `-p TEXT` | 自定义分析提示词（默认：详细描述图片内容） |

不传 `--file` 时自动尝试剪贴板。

## 环境变量

脚本需要 `DASHSCOPE_API_KEY` 环境变量。已配置在全局 `~/.claude/settings.json` 中，无需用户额外设置。

## 工作流程

当用户触发此技能时，按以下步骤操作：

1. **确定图片来源**：问用户是要分析剪贴板截图还是指定图片文件。如果用户没说，优先尝试剪贴板。
2. **运行脚本**：执行 `analyze_image.py` 并传入对应参数。
3. **呈现结果**：将模型返回的内容以清晰的结构化方式展示给用户。如果用户有后续追问（"再仔细看看左上角"），调整 prompt 重新运行。

## 注意事项

- 支持的图片格式：PNG、JPG、JPEG、GIF、WebP、BMP
- 图片最大 50MB
- 剪贴板图片用完后自动清理临时文件
- 如果报错"API_KEY 未设置"，请检查 `DASHSCOPE_API_KEY` 环境变量
