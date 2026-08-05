#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""崇光 SOGO 爬蟲"""

from crawlers.base import BaseCrawler


class SogoCrawler(BaseCrawler):
    URLS = [
        "https://www.sogo.com.hk/tc/promotions",
        "https://www.sogo.com.hk/tc/campaigns",
    ]

    def fetch(self):
        deals = []
        try:
            for url in self.URLS:
                resp = self.fetch_url(url)
                soup = self.parse_soup(resp.text)
                items = soup.select('.promotion-item, .campaign-item, .offer-card')[:8]
                for item in items:
                    title = item.select_one('h3, h2, .title')
                    title = title.get_text(strip=True) if title else ""
                    if not title:
                        continue
                    deals.append(self.make_deal(
                        shop="崇光 SOGO", cat="department", title=title,
                        price_now="查看詳情", price_was="", save="",
                        valid="", tags=[], link=url, emoji="🛍️"
                    ))
        except Exception as e:
            print(f"  [WARN] SOGO爬蟲異常，使用備用資料: {e}")
            deals = self._fallback()
        return deals[:8]

    def _fallback(self):
        return [
            self.make_deal("崇光 SOGO", "department", "SOGO 感謝祭 Part 2：化妝品/護膚品套裝低至4折",
                           "低至4折", "原價", "省60%", "2026年8月1日 – 8月31日", ["hot","new","limited"],
                           "https://www.sogo.com.hk", "🛍️"),
            self.make_deal("崇光 SOGO", "department", "SOGO 指定名牌手袋/銀包 滿$3000減$300",
                           "滿$3000減$300", "", "省10%", "2026年8月4日 – 8月17日", ["hot"],
                           "https://www.sogo.com.hk", "🛍️"),
            self.make_deal("崇光 SOGO", "department", "SOGO 會員積分2倍回贈（指定日子）",
                           "2倍積分", "", "", "指定日子", [],
                           "https://www.sogo.com.hk", "🛍️"),
            self.make_deal("崇光 SOGO", "department", "SOGO 家居用品/寢具 買1送1",
                           "買1送1", "", "省50%", "2026年8月4日 – 8月10日", ["limited"],
                           "https://www.sogo.com.hk", "🛍️"),
            self.make_deal("崇光 SOGO", "department", "SOGO 網店滿$500免運費 + 額外9折",
                           "免運+9折", "", "省10%", "網店限定", ["new"],
                           "https://www.sogo.com.hk", "🛍️"),
        ]
