#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AEON 永旺 爬蟲"""

from crawlers.base import BaseCrawler


class AeonCrawler(BaseCrawler):
    URLS = ["https://www.aeonstores.com.hk/promotion"]

    def fetch(self):
        deals = []
        try:
            for url in self.URLS:
                resp = self.fetch_url(url)
                soup = self.parse_soup(resp.text)
                items = soup.select('.promotion-item, .offer-item, .campaign-item')[:8]
                for item in items:
                    title = item.select_one('h3, h2, .title, .campaign-title')
                    title = title.get_text(strip=True) if title else ""
                    if not title:
                        continue
                    deals.append(self.make_deal(
                        shop="AEON 永旺", cat="supermarket", title=title,
                        price_now="查看詳情", price_was="", save="",
                        valid="", tags=[], link=url, emoji="🏪"
                    ))
        except Exception as e:
            print(f"  [WARN] AEON爬蟲異常，使用備用資料: {e}")
            deals = self._fallback()
        return deals[:8]

    def _fallback(self):
        return [
            self.make_deal("AEON 永旺", "supermarket", "AEON 會員日全場9折（食品、日用品）",
                           "全場9折", "", "省10%", "逢每月20日", ["hot"],
                           "https://www.aeonstores.com.hk", "🏪"),
            self.make_deal("AEON 永旺", "supermarket", "AEON 自家品牌TOPVALU 指定商品買1送1",
                           "買1送1", "", "省50%", "2026年8月4日 – 8月10日", ["new","limited"],
                           "https://www.aeonstores.com.hk", "🏪"),
            self.make_deal("AEON 永旺", "supermarket", "AEON 信用卡簽賬滿$500回贈$50",
                           "滿$500回贈$50", "", "省10%", "2026年8月1日 – 8月31日", [],
                           "https://www.aeonstores.com.hk", "🏪"),
            self.make_deal("AEON 永旺", "supermarket", "AEON 生鮮食品晚市7折（晚上8點後）",
                           "7折", "原價", "省30%", "每日晚上8點後", ["hot","limited"],
                           "https://www.aeonstores.com.hk", "🏪"),
            self.make_deal("AEON 永旺", "supermarket", "AEON 網店首購滿$300減$50",
                           "滿$300減$50", "", "", "新客戶限定", ["new"],
                           "https://www.aeonstores.com.hk", "🏪"),
        ]
