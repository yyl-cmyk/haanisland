# ⛰️ 慳島 HaanIsland

> 香港每日最新 Jetso 自動聚合網站

## 專案簡介

慳島是一個全自動化的香港優惠資訊聚合平台，每日自動爬取全港 10 間主要零售商的最新優惠，並以精美的網頁呈現。

## 技術架構

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  GitHub Actions │────▶│  Python 爬蟲    │────▶│  data/deals.json│
│  (每日 06:00)   │     │  (10間店)       │     │  (優惠資料)     │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                          │
┌─────────────────┐     ┌─────────────────┐              │
│  用戶瀏覽器      │◀────│  GitHub Pages   │◀─────────────┘
│  (index.html)   │     │  (免費部署)      │
└─────────────────┘     └─────────────────┘
```

## 目錄結構

```
saan-dou/
├── .github/
│   └── workflows/
│       └── crawl.yml          # GitHub Actions 定時爬蟲
├── crawlers/
│   ├── __init__.py
│   ├── base.py                # 基礎爬蟲類
│   ├── parknshop.py           # 百佳
│   ├── wellcome.py            # 惠康
│   ├── aeon.py                # AEON
│   ├── seven_eleven.py        # 7-Eleven
│   ├── circlek.py             # Circle K
│   ├── fortress.py            # 豐澤
│   ├── broadway.py            # 百老匯
│   ├── xiaomi.py              # 小米
│   ├── sogo.py                # SOGO
│   └── donki.py               # DONKI
├── data/
│   └── deals.json             # 爬蟲輸出 (自動生成)
├── index.html                 # 前端網站
├── main.py                    # 主爬蟲腳本
├── requirements.txt           # Python 依賴
└── README.md                  # 本文件
```

## 支援商戶

| 類別 | 商戶 |
|------|------|
| 🥬 超市 | 百佳 ParknShop、惠康 Wellcome、AEON 永旺 |
| 🏪 便利店 | 7-Eleven 香港、Circle K OK便利店 |
| 📱 電器 | 豐澤 Fortress、百老匯 Broadway、小米 Xiaomi HK |
| 🛍️ 百貨 | 崇光 SOGO、唐吉訶德 DONKI |

## 快速開始

### 1. Fork 此專案到自己的 GitHub

### 2. 啟用 GitHub Pages

前往 **Settings → Pages → Source**，選擇 `Deploy from a branch`，分支選 `main`，資料夾選 `/ (root)`。

### 3. 啟用 GitHub Actions

前往 **Actions** 分頁，點擊 **I understand my workflows, go ahead and enable them**。

### 4. 手動測試爬蟲

```bash
# 安裝依賴
pip install -r requirements.txt

# 執行爬蟲
python main.py

# 檢查輸出
cat data/deals.json
```

### 5. 自動運作

GitHub Actions 會每日香港時間早上 6 點自動：
1. 執行所有爬蟲
2. 更新 `data/deals.json`
3. 自動 commit
4. 重新部署 GitHub Pages

## 爬蟲備用機制

每個爬蟲都有**備用資料 (fallback)**。當網站反爬蟲或結構改變時，爬蟲會自動回退到預設的熱門優惠資料，確保網站永遠不會空白。

## 自定義

### 修改爬蟲選擇器

編輯 `crawlers/` 下的對應檔案，調整 `items = soup.select(...)` 中的 CSS 選擇器。

### 修改備用資料

編輯各爬蟲檔案中的 `_fallback()` 方法。

### 修改執行時間

編輯 `.github/workflows/crawl.yml` 中的 `cron` 設定：
```yaml
# 香港時間早上6點 = UTC 22:00
cron: '0 22 * * *'
```

### 新增商戶

1. 在 `crawlers/` 新增 `xxx.py`
2. 繼承 `BaseCrawler` 並實現 `fetch()`
3. 在 `main.py` 的 `crawlers` 列表中加入

## 注意事項

1. **反爬蟲**：部分網站可能有反爬蟲機制。如被封鎖，可考慮加入 `time.sleep()` 延遲或使用代理。
2. **網站改版**：當商戶網站改版時，需要更新對應的 CSS 選擇器。
3. **免費額度**：GitHub Actions 免費版每月 2,000 分鐘，足夠每日執行。

## License

MIT

---

Made with 🔥 in Hong Kong
