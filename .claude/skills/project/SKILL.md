---
name: project
description: 阿忠（ArChung）更新工作專案到 Obsidian vault 的 Projects/ 或 Brand/ 資料夾。當使用者輸入 /project 開頭的指令，或提到要更新王品、凱基、Uber Eats、Appier、挖礦、業配、強強滾一家、夏日只想躺在家等專案的進度、報價、發票、待辦時觸發。會自動偵測 vault 路徑、判斷檔案歸屬、更新 metadata 與進度紀錄、commit + push 到 GitHub。
---

# /project

更新工作專案檔案。

## 執行流程

1. **載入規則**：讀 `C:\Users\User\.claude\skills\archung-vault\SKILL.md` 跟 `references\PROJECT_RULES.md`，按裡面的全部規則執行
   - 在 vault repo 環境（Dispatch）可改讀 `.claude/skills/archung-vault/SKILL.md`
2. **偵測 vault 路徑**（照 archung-vault SKILL.md Step 1）
3. **依歸檔表判斷檔案**（客戶名 → Projects/客戶.md；業配 → Brand/業配-合作清單.md 等）
4. **更新檔案**：metadata、最新結論、進度紀錄、待辦
5. **commit + push**

詳細歸檔表、metadata 格式、結案流程都在 `archung-vault/references/PROJECT_RULES.md`。
