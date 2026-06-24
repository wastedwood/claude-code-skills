---
name: patent-pdf-batch-download
description: Use Google Patents as the primary source to match Chinese patent application numbers to publication numbers, download full-text PDFs, rename them by the original patent/application number, and validate file count and PDF integrity; optionally use CNIPA only as a fallback. Use when the user supplies an Excel/CSV patent list and asks to 批量下载专利、只依赖谷歌专利、根据申请号找公开号、从 Google Patents 下载 PDF、按专利号命名，或定期整理专利文献。
---

# 专利 PDF 批量下载

将 Excel 中的中国专利申请号通过 Google Patents 转换为公开号，再用公开号定位全文，并交付数量、名称和内容均已校验的 PDF 文件夹。默认不要求用户打开国家知识产权局网页。

本技能遵循 Agent Skills 通用结构。不要假设宿主是 Codex、Claude Code 或某个固定浏览器插件；根据当前环境选择可用的表格读取、网页访问、浏览器控制和命令执行工具。

批量处理时默认由一个 agent 顺序执行。除非用户明确要求并行，否则不要拆给多个 agent 同时操作浏览器或下载队列，避免页面状态互相干扰、进度难以追踪和重复初始化环境。

## 固定成功标准

1. Excel 目标行数、非空申请号数和唯一申请号数一致。
2. 每个申请号恰好对应一个公开号；不得靠标题猜测。
3. Google Patents 页面标题、公开号和 PDF 链接中的公开号一致。
4. 输出 PDF 数量等于目标记录数。
5. 文件名集合与 Excel 中的“专利号”或用户指定命名字段完全一致。
6. 每个 PDF 可解析、页数大于 0、文件非空。

## 申请号规范化

Excel 常见格式为无前缀、无点号：`2019209220005`、`202021006427X`。

国家知识产权局网页常见格式为：`CN201920922000.5`、`CN202021006427.X`。

匹配键统一按以下规则生成：

1. 转为字符串并大写。
2. 去掉开头的 `CN`。
3. 去掉所有 `.`。
4. 保留末尾校验字符 `X`，不得改成数字或删除。
5. 不使用 Excel 数值类型读取申请号，防止精度丢失。

需要重新插入点号时，在最后一位校验字符前插入 `.`，再加 `CN` 前缀。

## 工作流

### 1. 读取并检查源表

使用当前环境可用的表格工具读取 `.xlsx`、`.xls` 或 `.csv`。可选方式包括专用 spreadsheet 技能、Office 工具、Python 库或安全的只读转换工具。

- 优先识别“专利号”“申请号”“公开号”“专利名称”等列。
- 用户说明“专利号列实际是申请号”时，以用户说明为准。
- 记录原始行顺序、命名字段、申请号和标题。
- 报告目标数量、空值和重复项。发现空值或重复时不能静默跳过。

### 2. 用完整申请号搜索 Google Patents

将源表申请号转换为带 `CN` 和点号的完整格式，例如：

- `2019209220005` → `CN201920922000.5`
- `202021006427X` → `CN202021006427.X`

使用当前环境可用的 web access、网页搜索、浏览器控制或 HTTP 获取能力，优先以完整申请号访问 Google Patents 搜索：

`https://patents.google.com/?q=<FULL_APPLICATION_NUMBER>`

从唯一结果中提取公开号和 PDF 链接，并核对：

- 结果显示的申请日与源表一致。
- 结果标题与源表专利名称一致或语义明确对应。
- 结果详情中的申请号经规范化后与源表完全一致。

不能使用无 `CN`、无点号的纯数字作为主要查询，因为它可能被当作普通数字或匹配到无关专利。

### 3. 申请号搜索无结果时补查

Google Patents 对部分申请号的搜索索引不完整。显示 `No results found` 时：

1. 优先使用中国专利公布公告系统 `http://epub.cnipa.gov.cn/`，用规范化后的纯申请号补查公告号/公开号。
2. CNIPA 页面通常需要浏览器执行 JavaScript，不要假设普通 HTTP GET 可以直接抓取结果；一次只查一个申请号，不做批量粘贴。
3. 从 CNIPA 结果逐行读取公开号、申请号、申请日、标题和申请人，并用规范化申请号精确匹配。
4. 如果 CNIPA 暂不可用或仍无法确认，再使用完整专利名称搜索 Google Patents。
5. Google Patents 结果过多时，增加申请人或申请年份缩小范围；使用申请人检索时不要附加 `language=CHINESE`，该参数可能导致本应存在的申请人结果被过滤为空。
6. 打开最强候选的专利详情页，核对申请号、申请日、标题和申请人。
7. 只有详情页申请号规范化后与源表完全一致，才接受该公开号。

严禁只凭标题接受候选，因为标题可能重复，例如“一种变频一体机”。标题只是寻找候选的手段，申请号才是最终匹配依据。

CNIPA 浏览器查询要点：

- 使用首页检索框 `#searchStr` 输入规范化后的纯申请号，例如 `2021214578686`。
- 通过表单 `#indexForm` 提交查询；不要直接拼接一个未验证的结果 URL。
- 打开首页后先等待页面脚本和可能的 WAF 检查完成，再等待 `#searchStr` 可用。
- 提交后等待页面导航或网络空闲，再额外短暂等待结果区域稳定，避免读取到半渲染页面。
- 解析结果时保留原始候选文本；只有候选中的申请号规范化后与源表完全一致，才提取对应公告号/公开号。

如果当前环境可以运行 Playwright，可使用可选脚本辅助查询：

```text
python "<本技能目录>/scripts/cnipa_lookup_publication.py" 2021214578686
```

脚本必须只作为候选发现工具。它的标准输出包含固定前缀 `CNIPA_LOOKUP_JSON:`，后接 UTF-8 JSON 对象；调用方应读取 JSON 中的 `verified`、`publication_no`、`application_no`、`title` 和 `candidates` 字段，再按本技能的交叉核验规则继续处理。

CNIPA 只用于发现或核对公告号/公开号，不能代替最终下载入口。取得公开号后，仍应回到 Google Patents 公开号详情页获取 PDF 链接并完成 PDF 链接、公开号和标题的交叉核对。

网页访问工具只能提供候选和页面事实，不能降低核验标准。无论使用 Codex Chrome、Claude Code web access、Playwright、MCP 浏览器或普通 HTTP，请始终完成申请号、公开号、标题和 PDF 链接的交叉核对。

### 4. 使用公开号访问 Google Patents

获得公开号后，一律使用：

`https://patents.google.com/patent/<PUBLICATION_NUMBER>`

例如：`https://patents.google.com/patent/CN209676041U`

不要把申请号搜索结果页作为最终批量下载入口。

逐条核对：

- 页面标题包含目标公开号。
- 页面专利名称与源表一致或语义明确对应。
- PDF 链接文件名包含同一公开号。

### 5. 下载和命名

创建桌面输出文件夹前检查是否已存在同名目录。

- 不存在：创建。
- 已存在：不得删除或整体覆盖；使用带日期的新名称，或询问用户。

生成 UTF-8 JSON 清单：

```json
[
  {
    "patent_no": "2019209220005",
    "application_no": "2019209220005",
    "publication_no": "CN209676041U",
    "title": "机壳支撑结构以及电机壳组件",
    "pdf_url": "https://patentimages.storage.googleapis.com/.../CN209676041U.pdf"
  }
]
```

使用当前环境的 Python 3 运行。不要假设当前工作目录就是技能目录：

```text
Claude Code:
python "${CLAUDE_SKILL_DIR}/scripts/download_and_validate.py" manifest.json "<output-folder>"

其他 Agent:
python "<本技能目录>/scripts/download_and_validate.py" manifest.json "<output-folder>"
```

默认按 `patent_no` 命名为 `<patent_no>.pdf`。除非用户明确要求，否则文件名不加标题、公开号或序号。

### 6. 最终验收

- PDF 数量等于目标数量。
- 无缺失和多余文件名。
- 每个文件以 `%PDF-` 开头。
- 每个 PDF 页数大于 0。
- 如果当前环境能抽取 PDF 文本，优先核对首页或首页附近文本中的公开号、专利名称与清单一致。
- 报告总页数、最小和最大页数。

向用户只报告最终文件夹、数量和校验结果。不要把临时清单放入交付文件夹。

## 异常处理

- 当前环境没有网页访问能力：停止公开号发现步骤，说明需要启用 web access、浏览器或允许访问 Google Patents；不要猜测。
- 当前环境不能运行 Python：仍可下载，但必须用等价方法完成 PDF 文件头、数量、文件名和页数校验；不能省略验收。
- Google Patents 申请号搜索无结果：优先使用中国专利公布公告系统 `http://epub.cnipa.gov.cn/` 查询公告号/公开号；CNIPA 不可用时，再改用“专利名称 + 申请人或年份”寻找候选，并在详情页精确核对申请号。
- Google Patents 和 CNIPA 都无法验证：说明具体失败项，不猜测公开号；这通常意味着申请号、标题或申请人信息需要用户复核。
- 国家知识产权局备用页面登录失效：请用户重新登录，不绕过登录。
- 出现 CAPTCHA：按浏览器安全规则暂停并请用户处理或确认。
- 公开号直达页无结果：重新核对公开号，不通过扩大关键词搜索来猜测。
- PDF 链接与公开号不一致：停止该条下载并标记冲突。
- 下载失败：保留已成功文件，重试失败项；不得用 HTML 错误页冒充 PDF。
- 同名文件已存在：先比较文件完整性，不静默覆盖用户已有文件。

## 资源

- `scripts/cnipa_lookup_publication.py`：可选 Playwright 辅助脚本，按纯申请号查询 CNIPA 公布公告系统并输出固定 JSON 候选结果。
- `scripts/download_and_validate.py`：规范化申请号、校验清单、下载 PDF、按专利号命名并检查完整性。

脚本只依赖 Python 标准库完成清单校验和下载。页数校验优先使用 `pypdf`，不存在时尝试系统 `pdfinfo`；两者都不可用时明确报错，不自动安装全局依赖。
