---
name: archung-brand
description: 阿忠個人品牌的視覺設計系統。當使用者要產出「強強滾工作室 / 強強滾一家 / 夏日只想躺在家」的視覺物件（網頁、簡報、IG 貼文、Reels 封面、podcast cover、提案 PDF、Notion 頁面樣式）時觸發。自動套用對應品牌的色票、字型、卡片樣式，避免 AI 感的套版輸出。
---

# 阿忠個人品牌設計指南

## 設計哲學（全品牌共用）

做設計的時候要讓人「一看就知道是阿忠做的」，而不是 ChatGPT / Midjourney 感。三條金律：

1. **Bold outline + hard-edge shadow**：所有卡片 / 按鈕 / 輸入框都用 `2~3px solid` 黑色邊框 + `3~6px offset` 無模糊陰影（Brutalist / Maxima Therapy 血統），**絕不用** `box-shadow: 0 4px 12px rgba(0,0,0,0.1)` 這種軟糊陰影。
2. **Pill shape > rounded rectangle**：狀態標籤、按鈕、tag 全部用 `border-radius: 999px`（藥丸），資訊卡才用 `12~16px` 圓角。避免所有元件一律圓角的「Material 塑膠感」。
3. **Cream 底勝過純白**：預設底色 `#F5F1E4`（奶油），不要 `#FFFFFF`。純白會讓亮彩色看起來廉價。

## 品牌一：戰情表 / 強強滾工作室（Maxima 風格）

**用在**：index.html 戰情表、提案文件、工作室網站、B2B 合作簡報

### 色票（這份是 index.html 的真實 token，改版時以這為準）

| 角色 | 變數 | Hex |
|---|---|---|
| 底色 | `--cream` | `#F5F1E4` |
| 文字 / 邊框 | `--ink` | `#1a1a1a` |
| 主強調（按鈕、高亮） | `--orange` | `#E8441E` |
| 進行中 / 成功 | `--green` | `#1BB24B` |
| 連結 / 次要強調 | `--blue` | `#1F3FD4` |
| 品牌 / 重點事件 | `--pink` | `#E6298A` |
| 等待 / 警示 | `--yellow` | `#F7C93A` |
| 輔助灰 | `--gray` | `#9ca3af` |
| 淡灰底 | `--gray-soft` | `#e5e5e5` |

**配色原則**：一個畫面最多用 **2 個主色 + 黑 + 奶油**。不要 rainbow。

### 字型

```css
/* 標題 */
font-family: 'Anton', 'Noto Sans TC', sans-serif;   /* 英數粗大 + 中文黑體 */

/* 內文 / UI */
font-family: 'Noto Sans TC', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### 關鍵元件樣式

**卡片**
```css
background: #fff;
border: 2px solid var(--ink);
border-radius: 12px;
box-shadow: 4px 4px 0 var(--ink);    /* 重點：0 模糊 */
padding: 20px;
```

**按鈕（藥丸）**
```css
background: var(--orange);
color: #fff;
border: 2px solid var(--ink);
border-radius: 999px;
box-shadow: 3px 3px 0 var(--ink);
padding: 10px 20px;
font-weight: 700;

/* hover：陰影往內縮模擬按下 */
&:hover { box-shadow: 1px 1px 0 var(--ink); transform: translate(2px, 2px); }
```

**狀態 pill**
```css
border-radius: 999px;
padding: 4px 12px;
font-size: 0.78em;
border: 2px solid var(--ink);
/* active: green, waiting: yellow, done: gray-soft */
```

---

## 品牌二：強強滾一家（IG 內容品牌 ~173k）

**用在**：IG 貼文、Reels 封面、限動模板、公關品開箱影片 lower-third

### 色票（**TODO：阿忠確認**）

目前暫用下列作為 fallback，真實 IG 調性請阿忠確認：

| 角色 | Hex | 備註 |
|---|---|---|
| 主粉 | `#E6298A` | 跟戰情表 `--pink` 一致（這是目前唯一確定的） |
| 襯底 | `#F5F1E4` | 奶油（可能換米白 `#FFF8EC`） |
| 強調黃 | `#F7C93A` | 生活化暖感 |
| 文字 | `#1a1a1a` | ink |

**請阿忠補充**：
- IG 目前實際在用的主色（如果跟上面不同）
- 是否有另一個「弟弟色」/「姊姊色」區分子誼、子寬貼文
- Reels 封面的統一樣式（字體大小、標題位置）

### 字型（**TODO**）

中文推薦：思源黑體（Noto Sans TC）或**源樣明體**（有親子感）。等阿忠確認目前模板在用什麼。

### 視覺調性

- **親子日常 > 完美精修**：照片保留自然光、不濾鏡到失真
- **標題字要夠大**（手機縮圖一眼看懂，至少佔縮圖 30% 高）
- **人臉優先於商品**（業配也是）—— 強強滾一家賣的是家庭感不是商品

---

## 品牌三：夏日只想躺在家（Podcast）

**用在**：podcast cover art、單集封面、IG 宣傳圖、Spotify banner

### 色票（**TODO：阿忠確認**）

目前未知，暫用 placeholder：

| 角色 | Hex | 備註 |
|---|---|---|
| 主色 | `#?` | 阿忠補 |
| 襯底 | `#?` | 阿忠補 |

### 調性關鍵字（建議方向）

- 慵懶、夏天、軟墊、冷氣房、日光
- **不要**用 Canva 常見的 podcast 套版（那種麥克風 + 漸層）
- 參考方向：Apple Podcasts 精選類的極簡 + 插畫風，而不是 YouTuber 頻道 cover

---

## 使用規則（給 Claude）

當使用者要產出視覺物件時：

1. **先問品牌**：「這是要給哪個品牌用？戰情表 / 強強滾一家 / Podcast / 其他？」（如果上下文明確就跳過）
2. **讀對應色票 + 字型**：從上面表格取值，**不要自己編顏色**
3. **套三金律**：Bold outline、Pill shape、Cream 底
4. **自我檢查**：輸出前問自己三題：
   - 看起來像不像 Material Design 套版？ → 像就打掉重來
   - 陰影是不是模糊的？ → 模糊就改成 `Xpx Xpx 0 ink`
   - 整個畫面有超過 3 個主色嗎？ → 有就刪到 2 個

## 什麼不要做

- ❌ 模糊陰影（`rgba(0,0,0,0.1)` 那種）
- ❌ 漸層背景（除非阿忠明確說要）
- ❌ 純白背景（用 cream 代替）
- ❌ 通用 emoji / Lottie 動畫裝飾
- ❌ Poppins / Inter / Roboto（這是 Anthropic / SaaS 套版字）
- ❌ 一次用超過 3 種主色

## 維護

- 阿忠真實 index.html 改版後，請以 index.html 的 `:root { --xxx }` 為準回頭更新本檔
- 強強滾一家 / Podcast 的 TODO 區塊阿忠補齊後，刪掉「**TODO**」標記
- 如果某個品牌下有新子系列（例如夏躁有「來賓特輯」），在對應章節加子段落
