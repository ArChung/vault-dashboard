---
name: kid
description: 阿忠（ArChung）紀錄家裡兩個小孩（子誼、子寬）的日常與金句到 Obsidian vault 的 Kids/ 資料夾。當使用者輸入 /kid 開頭的指令，或提到要記錄子誼、子寬、姊姊、弟弟相關的事情時觸發。會自動偵測 vault 路徑、寫入對應檔案、抽取金句、commit + push 到 GitHub。
---

# /kid

紀錄子誼或子寬的日常與金句。

## 執行流程

1. **載入規則**：讀 `C:\Users\User\.claude\skills\archung-vault\SKILL.md` 跟 `references\KID_RULES.md`，按裡面的全部規則執行
   - 在 vault repo 環境（Dispatch）可改讀 `.claude/skills/archung-vault/SKILL.md`
2. **偵測 vault 路徑**（照 archung-vault SKILL.md Step 1）
3. **判斷對象**（子誼/子寬/兩個都）
4. **寫入 Kids/XXX.md**（首次建檔或追加，金句倒序、日常倒序）
5. **commit + push**

詳細格式、金句抽取規則、雙更新邏輯都在 `archung-vault/references/KID_RULES.md`。
