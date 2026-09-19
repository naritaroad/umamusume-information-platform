# 貢獻指南

語言：[繁體中文](CONTRIBUTING.md) · [English (UK)](docs/CONTRIBUTING.en-GB.md)

這是課程期末的賽馬娘輿情平台。歡迎修缺陷、補說明、整理結構；請先對齊現況再動手。

## 動工前

1. 讀 [`.cursorrules`](.cursorrules) 與 [`AGENTS.md`](AGENTS.md)。
2. 動到架構、流程、資料契約、路由時，打開對應的 [`SPEC/`](SPEC/INTENT_SPEC.md)。
3. 衝突時以**程式碼實作**為準，再回頭修正規格。

## 慣例

| 項目 | 約定 |
| --- | --- |
| 註解、維護者錯誤訊息 | 繁體中文；避免簡體與中國大陸用語（例如「視頻」「軟件」「網絡」） |
| 變數／函式 | `snake_case` |
| 類別 | `PascalCase` |
| 路由 path | kebab-case（`/crawler-admin/`，禁止底線） |
| 日期／時間 | `YYYY-MM-DD`、`HH:MM:SS`，台北時間 |
| 站內 URL | Template `{% url %}`；Python `reverse()` / `reverse_lazy()` |
| 寫入 AJAX | 必須 `X-CSRFToken`，並處理 `error` / `catch` |
| Model 變更 | 一定要附 migration |
| `data/raw`、`data/processed` | 核心欄位名稱與順序不得任意改 |

## 請不要

- 在程式碼硬寫金鑰、Token、密碼、絕對機器路徑
- 提交 `.env`、憑證、`db.sqlite3`、大型 `media/`
- 只改 Model 不產 migration
- 把 `app_*` 再平鋪回專案根目錄（對照表在 `website_configs/app_layout.py`）

不可逆動作（刪資料庫、`compose down -v`、強制推送、會產生費用的大量 LLM 呼叫）請先問。

## 改完必做

1. 契約或路由有變 → 同步 `SPEC/`
2. 把變更寫進 [`CHANGELOG.md`](CHANGELOG.md)：目的、影響範圍、驗收方式；**版本號不得重複**
3. 新增／修改 API：路由能解析、錯誤訊息可讀、主流程可重現
4. 改到畫面時，用瀏覽器把該流程點過一遍（不要只截一張靜態圖）

對外說明寫在 [`README.md`](README.md)（繁中）與 [`docs/README.en-GB.md`](docs/README.en-GB.md)（英式英文）。安裝與架構分檔在 `docs/`。
