---
name: daily
description: 阿忠（ArChung）寫每日日記到 Obsidian vault 的 Daily/ 資料夾。當使用者輸入 /daily 開頭的指令，或提到要記錄今天的事情、會議、心得、生活流水帳到日記時觸發。會自動偵測 vault 路徑、寫入 Daily/YYYY-MM-DD.md（首次建立或追加）、commit + push 到 GitHub。
---

# /daily

寫每日日記。

## 執行流程

1. **載入規則**：讀 `C:\Users\User\.claude\skills\archung-vault\SKILL.md` 跟 `references\DAILY_RULES.md`，按裡面的全部規則執行
   - 在 vault repo 環境（Dispatch）可改讀 `.claude/skills/archung-vault/SKILL.md`
2. **偵測 vault 路徑**（照 archung-vault SKILL.md Step 1）
3. **取得今天日期與時間**
4. **寫入 Daily/YYYY-MM-DD.md**（首次建檔或追加 `## HH:MM` 段落）
5. **commit + push**

詳細日記格式、追加邏輯、內容整理原則都在 `archung-vault/references/DAILY_RULES.md`。
