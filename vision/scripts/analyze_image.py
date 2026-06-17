#!/usr/bin/env python3
"""
图片分析脚本 —— 调用阿里云百炼（通义千问 VL）多模态模型识别图片内容。
支持从剪贴板读取截图或指定本地图片路径。
"""
import base64
import json
import os
import subprocess
import sys
import tempfile
import urllib.request
import urllib.error
from pathlib import Path


API_KEY = os.environ.get("DASHSCOPE_API_KEY")
if not API_KEY:
    print("错误：环境变量 DASHSCOPE_API_KEY 未设置", file=sys.stderr)
    print("请在 .env 文件中设置 DASHSCOPE_API_KEY=你的密钥，或通过 export 设置", file=sys.stderr)
    sys.exit(1)

MODEL = os.environ.get("DASHSCOPE_MODEL", "qwen3-vl-flash")
API_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"


def get_clipboard_image():
    """从 Windows 剪贴板读取图片，保存到临时文件返回路径。没有图片返回 None。"""
    ps_script = """
Add-Type -AssemblyName System.Windows.Forms
$img = [System.Windows.Forms.Clipboard]::GetImage()
if ($img) {
    $path = [System.IO.Path]::GetTempFileName() + ".png"
    $img.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
    Write-Output $path
} else {
    Write-Output "NO_IMAGE"
}"""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            capture_output=True, text=True, timeout=15
        )
        path = result.stdout.strip()
        if path == "NO_IMAGE" or not path:
            return None
        if os.path.exists(path):
            return path
        return None
    except Exception as e:
        print(f"读取剪贴板失败: {e}", file=sys.stderr)
        return None


def image_to_base64(file_path):
    """读取图片文件并返回 base64 编码和 MIME 类型。"""
    ext = Path(file_path).suffix.lower()
    mime_map = {
        ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".gif": "image/gif", ".webp": "image/webp", ".bmp": "image/bmp",
    }
    mime = mime_map.get(ext, "image/png")

    stat = os.stat(file_path)
    if stat.st_size > 50 * 1024 * 1024:
        print(f"错误：图片超过 50MB 限制 ({(stat.st_size / 1024 / 1024):.1f}MB)", file=sys.stderr)
        sys.exit(1)

    with open(file_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return b64, mime


def call_dashscope(image_path, prompt):
    """调用百炼 API 分析图片，返回分析结果文本。"""
    b64, mime = image_to_base64(image_path)

    payload = {
        "model": MODEL,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                {"type": "text", "text": prompt},
            ],
        }],
        "max_completion_tokens": 2048,
    }

    req = urllib.request.Request(
        f"{API_BASE}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_text = e.read().decode("utf-8", errors="replace")[:500]
        print(f"API 请求失败 (HTTP {e.code}): {err_text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"API 请求失败: {e}", file=sys.stderr)
        sys.exit(1)

    text = result.get("choices", [{}])[0].get("message", {}).get("content", "")
    if not text:
        print("API 返回为空", file=sys.stderr)
        sys.exit(1)

    usage = result.get("usage", {})
    if usage:
        parts = [f"{k}: {v}" for k, v in usage.items() if v]
        if parts:
            text += f"\n\n---\nToken 用量: {' | '.join(parts)}"

    return text


def main():
    import argparse

    parser = argparse.ArgumentParser(description="分析图片内容（百炼视觉模型）")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--file", "-f", help="本地图片路径")
    group.add_argument("--clipboard", "-c", action="store_true",
                       help="从剪贴板读取图片（默认行为：未指定 --file 时自动尝试剪贴板）")
    parser.add_argument("--prompt", "-p",
                        default="请详细描述这张图片中的内容，包括所有文字信息",
                        help="分析提示词（默认：详细描述图片内容）")

    args = parser.parse_args()

    # 确定图片来源
    img_path = None
    is_clipboard = False

    if args.file:
        img_path = args.file
        if not os.path.exists(img_path):
            print(f"错误：文件不存在 {img_path}", file=sys.stderr)
            sys.exit(1)
    else:
        # 默认尝试剪贴板
        img_path = get_clipboard_image()
        if img_path:
            is_clipboard = True
        else:
            print("错误：未提供图片路径（--file），且剪贴板中没有图片", file=sys.stderr)
            sys.exit(1)

    try:
        result = call_dashscope(img_path, args.prompt)
        print(result)
    finally:
        # 清理临时文件
        if is_clipboard and img_path:
            try:
                os.remove(img_path)
            except OSError:
                pass


if __name__ == "__main__":
    main()
