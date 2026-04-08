# /daily 規則

寫每日日記到 `$VAULT/Daily/YYYY-MM-DD.md`。

## 檔案位置

`$VAULT/Daily/YYYY-MM-DD.md`（今天的日期）

## 檔案結構

初次建立時的模板：

```markdown
# YYYY-MM-DD（週X）

## HH:MM
<內容>
```

之後每次追加新內容，在檔案末尾加：

```markdown

## HH:MM
<內容>
```

每筆獨立的記錄都用 `## HH:MM` 當標題。

## 寫入流程

1. `date` 取得今天日期（YYYY-MM-DD）和現在時間（HH:MM）
2. 檢查 `$VAULT/Daily/YYYY-MM-DD.md` 是否存在：
   - **不存在** → 用上面的模板建立，加入第一筆
   - **存在** → Read 出內容，Edit 在最後加新的 `## HH:MM` 段落
3. commit + push

## 內容整理原則

- **不逐字記錄**：把阿忠說的話整理成通順的段落
- **保留口語感**：不要過度正式，用他平常講話的語氣
- **條列式優先**：如果是多件事，用 `- ` bullet list
- **不分類**：日記就是日記，不要硬分「工作」「生活」類別
- **時間敏感的提醒**：如果提到未來日期或 deadline，同時提醒阿忠是否要寫進對應專案或加到 Google 日曆

## 內容範例

輸入：「/daily 今天跟王品開會，他們 IT 很機車一堆安全規範。下午去剪頭髮。晚上 podcast 錄音。」

寫入（首次建檔）：

```markdown
# 2026-04-09（四）

## 14:30
- 跟王品開會，IT 安全規範超嚴格，很多東西不能本地測試
- 下午去剪頭髮
- 晚上 podcast 錄音
```

再追加一筆（同日）：

輸入：「/daily 剛錄完 podcast，來賓超有梗」

追加：

```markdown

## 22:15
剛錄完 podcast，來賓超有梗
```

## Commit 訊息

格式：`Daily：YYYY-MM-DD <短摘要>`

範例：
- `Daily：2026-04-09 王品會議與 podcast 錄音`
- `Daily：2026-04-09 追加 podcast 心得`
