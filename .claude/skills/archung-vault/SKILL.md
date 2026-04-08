---
name: archung-vault
description: 阿忠（ArChung）的 Obsidian vault 記錄器。當使用者輸入以 /project、/daily、/kid 開頭的指令，或是提到要更新專案（王品、凱基、Uber Eats、Appier 等客戶）、寫日記、紀錄家裡兩個小孩（子誼、子寬）的事情時觸發。會自動偵測 vault 路徑（本機桌機 C:\Users\User\Desktop\阿忠vault 或 Dispatch clone 出來的 vault-dashboard repo），更新對應 markdown 檔案，並 commit + push 到 GitHub。
---

# archung-vault

阿忠的 vault 記錄器。負責把口語化的輸入整理成結構化的 markdown，寫進對應位置，並自動推到 GitHub。

## 觸發關鍵字

| 指令 | 用途 | 詳細規則 |
|------|------|---------|
| `/project` | 更新工作專案（Projects/、Brand/） | [references/PROJECT_RULES.md](references/PROJECT_RULES.md) |
| `/daily` | 寫每日日記（Daily/YYYY-MM-DD.md） | [references/DAILY_RULES.md](references/DAILY_RULES.md) |
| `/kid` | 紀錄子誼或子寬的日常與金句（Kids/） | [references/KID_RULES.md](references/KID_RULES.md) |

即使沒有明確使用斜線指令，只要語意上是在更新這些內容，也該載入此 skill。

## Step 1：偵測 vault 路徑（每次執行必做）

執行順序：

1. **檢查本機桌機路徑**：如果 `C:\Users\User\Desktop\阿忠vault\CLAUDE.md` 存在 → `VAULT=C:\Users\User\Desktop\阿忠vault`
2. **檢查當前 cwd**：跑 `git rev-parse --show-toplevel`，拿到 repo root 後跑 `git remote get-url origin`。如果 origin URL 含有 `vault-dashboard` 或 `阿忠vault` → 把 repo root 設為 `VAULT`
3. **往上找**：如果 cwd 不是 git repo，往上兩層找含 `CLAUDE.md` 且同時有 `Projects/`、`Daily/` 資料夾的目錄
4. **找不到** → 停下來跟使用者說「偵測不到 vault，請確認目前環境」，不要亂寫檔案

找到後，把路徑記在腦中（後面所有檔案操作都用絕對路徑），並短短告知使用者「vault: <path>」讓他確認。

## Step 2：取得現在時間

用 `date` 或 bash 取得：
- 日期：`YYYY-MM-DD`（檔名用）
- 時間：`HH:MM`（內容裡的時間戳用）

系統 context 裡的 `# currentDate` 可以當備援，但以 `date` 實際值為主。

## Step 3：執行對應指令邏輯

讀對應的 `references/<指令>_RULES.md`，按照裡面的格式處理。

## Step 4：Commit + Push（**強制**）

每次改完一定做：

```bash
cd "$VAULT"
git add <改動的檔案>
git commit -m "<簡短描述>"
git push
```

commit 訊息用中文，格式：`<類別>：<一句話摘要>`
範例：
- `王品：4/9 客戶確認打包檔格式`
- `Daily：記錄 4/9 的會議與待辦`
- `子誼：新增金句「我要當太空人」`

**絕對不要**忘記 push。阿忠主要從 index.html（GitHub Pages）看進度，沒 push = 等於沒做。

## Step 5：簡短回報

回報內容：
- 改了哪個檔案
- commit hash（短版即可）
- 有待辦事項的話提醒一下

避免長篇大論。阿忠可能在手機或 Dispatch 上看，越短越好。

## 一般原則

- **不要問確認**：阿忠希望直接做。判斷不了時才問。
- **中文、口語**：他用中文跟你講話，你也中文回。
- **metadata 欄位有才寫**：空的欄位不要寫「—」，直接省略那一行。
- **同時牽涉多處**：一句話如果牽涉多個檔案（例如 /project 講王品同時提到要加日期），更新所有相關檔案後一起 commit。
- **日期提醒**：使用者提到未來日期時，問一句「要不要加到 Google 日曆？」（如果有 gcal MCP 就直接建）。
