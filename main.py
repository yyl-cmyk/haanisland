#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
慳島 Haanisland - 香港Jetso自動爬蟲系統
每日自動爬取10間零售商最新優惠
"""

import json
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path

from crawlers.parknshop import ParknShopCrawler
from crawlers.wellcome import WellcomeCrawler
from crawlers.aeon import AeonCrawler
from crawlers.seven_eleven import SevenElevenCrawler
from crawlers.circlek import CircleKCrawler
from crawlers.fortress import FortressCrawler
from crawlers.broadway import BroadwayCrawler
from crawlers.xiaomi import XiaomiCrawler
from crawlers.sogo import SogoCrawler
from crawlers.donki import DonkiCrawler

# 輸出路徑
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_JSON = DATA_DIR / "deals.json"
OUTPUT_JSON_MIN = DATA_DIR / "deals.min.json"

def run_all_crawlers():
    """執行所有爬蟲並合併結果"""
    all_deals = []
    errors = []

    crawlers = [
        ("百佳 ParknShop", ParknShopCrawler),
        ("惠康 Wellcome", WellcomeCrawler),
        ("AEON 永旺", AeonCrawler),
        ("7-Eleven", SevenElevenCrawler),
        ("Circle K", CircleKCrawler),
        ("豐澤 Fortress", FortressCrawler),
        ("百老匯 Broadway", BroadwayCrawler),
        ("小米 Xiaomi", XiaomiCrawler),
        ("崇光 SOGO", SogoCrawler),
        ("唐吉訶德 DONKI", DonkiCrawler),
    ]

    for name, CrawlerClass in crawlers:
        try:
            print(f"[INFO] 正在爬取: {name}...")
            crawler = CrawlerClass()
            deals = crawler.fetch()
            print(f"[OK] {name}: 找到 {len(deals)} 個優惠")
            all_deals.extend(deals)
        except Exception as e:
            err_msg = f"[ERROR] {name}: {str(e)}"
            print(err_msg)
            errors.append({"shop": name, "error": str(e), "trace": traceback.format_exc()})

    # 加入元數據
    result = {
        "meta": {
            "site_name": "慳島 Saan Dou",
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_deals": len(all_deals),
            "shops_crawled": len(crawlers) - len(errors),
            "shops_failed": len(errors),
            "errors": errors
        },
        "deals": all_deals
    }

    # 寫入 JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    with open(OUTPUT_JSON_MIN, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, separators=(',', ':'))

    print(f"\n[INFO] 總共爬取 {len(all_deals)} 個優惠")
    print(f"[INFO] 成功: {len(crawlers) - len(errors)} 間店")
    print(f"[INFO] 失敗: {len(errors)} 間店")
    print(f"[INFO] 結果已儲存至: {OUTPUT_JSON}")

    return result

if __name__ == "__main__":
    run_all_crawlers()
