---
name: podcast-ingest
description: 處理「夏日只想躺在家」Podcast 短影音的 ingest pipeline。掃描 I:\.shortcut-targets-by-id\17Jr3DtGAN59oLGep2Cdsp1WhGsaYVZqN\夏日只想躺在家(完稿)\ 找新檔 → Whisper 產逐字稿 → 套 podcast-copywriting skill 產 IG 文案 → 寫 draft 到 Brand/podcast-drafts/ → commit + push。當使用者說「跑 podcast-ingest」、「處理新的 podcast 短影音」、「看看有沒有新檔要產文案」時觸發。每日排程會自動呼叫。
---

# Podcast Ingest Pipeline

## 目的
把 Google Drive 同步進來的 Podcast 短影音，自動做成「逐字稿 + IG 文案 draft」，讓阿忠只需要進審核介面微調、打勾。

## 前置條件（不符合就停，回報阿忠）
- `transcribe.py` 在 vault 根（呼叫 OpenAI Whisper API）
- 環境變數 `OPENAI_API_KEY` 已設（`echo $OPENAI_API_KEY` 非空）
- `.claude/skills/podcast-copywriting/SKILL.md` 存在（tone 由它管）
- `Brand/podcast-drafts/` 目錄存在

## 路徑變數

為了讓 skill 好讀，下面用 `<DRIVE>` 代表：
```
I:\.shortcut-targets-by-id\17Jr3DtGAN59oLGep2Cdsp1WhGsaYVZqN\夏日只想躺在家(完稿)
```
這是 Google Drive 「與我共用」加捷徑後的本機串流路徑（不是本機實體資料夾）。

## 流程

### Step 1：找新檔
掃 `<DRIVE>\` 列出副檔名是 `.mp4 .mov .m4a .mp3 .wav` 的檔案。

比對 `Brand/podcast-drafts/*.md` 跟 `Brand/podcast-drafts/archive/*.md` 的 frontmatter `source_file` 欄位，過濾掉「已處理過」的檔名。

沒有新檔 → 結束，跟阿忠說「沒有新的」。

### Step 2：每個新檔跑一次

對每個新檔 `F`：

**2a. 產逐字稿（OpenAI Whisper API）**

執行：
```bash
python transcribe.py "<DRIVE>\F.mp4"
```
stdout 會印出純逐字稿文字，stderr 為錯誤。25MB 上限（短影音正常不會超過，超過就跳過該檔 + 回報）。

定價 ≈ $0.006/分鐘 → 2-3 分鐘短片約 $0.02。

**2b. 產生 slug 與 draft 檔名**

- slug：從檔名取 basename、去副檔名、用短 hash 防撞（例：`ep42-clip01-a1b2`）
- draft 檔名：`Brand/podcast-drafts/YYYY-MM-DD-<slug>.md`（YYYY-MM-DD 用今天）

**2c. 套 podcast-copywriting skill 產 IG 文案**

載入 `.claude/skills/podcast-copywriting/SKILL.md`，嚴格遵照其中定義的主持人、tone、風格、禁用詞。餵逐字稿，產出 **一份 IG caption**（含 hashtag，如 skill 有指定格式）。

**不要**：
- 用制式開頭（「嗨大家」「今天要跟大家分享」）
- 用 emoji 裝飾列表（除非 skill 明確說要）
- 條列式 bullet（IG 文案要自然段落）
- 「讓我們一起」「期待」這種 AI 感句

**2d. 寫 draft MD**

寫入檔案：
```markdown
---
source_file: I:\.shortcut-targets-by-id\17Jr3DtGAN59oLGep2Cdsp1WhGsaYVZqN\夏日只想躺在家(完稿)\<原始檔名>
slug: <slug>
created_at: <ISO 8601 帶時區>
status: pending
---

# <slug>

## IG 文案

<caption>

## 逐字稿

<transcript>
```

### Step 3：Commit + Push

處理完所有新檔後：
```bash
git add Brand/podcast-drafts/
git commit -m "podcast: ingest <N> new draft(s): <slug1>, <slug2>, ..."
git push
```

### Step 4：回報

告訴阿忠：
- 處理了幾個檔
- 每個的 slug
- 審核連結：`http://localhost:3001/`（提醒他如果 server 沒開要先開）

## 錯誤處理
- Whisper 失敗（影片檔損壞 / 太長）：跳過該檔、記錄到回報、繼續下一個
- 某支影片逐字稿全空（沒講話）：仍寫 draft，但 caption 段留空白 + 提示「逐字稿為空，請檢查影片」
- Git push 失敗：警告但不擋流程，draft 已寫到本地

## 不要做
- ❌ 直接刪 `I:\.shortcut-targets-by-id\17Jr3DtGAN59oLGep2Cdsp1WhGsaYVZqN\夏日只想躺在家(完稿)\` 的原檔（刪檔只在審核介面打勾後發生）
- ❌ 跳過 podcast-copywriting skill 自己編文案 tone
- ❌ 一次處理超過 5 個檔（超過就分批，避免 context 爆）
