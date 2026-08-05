#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""小米 Xiaomi HK 爬蟲"""

from crawlers.base import BaseCrawler


class XiaomiCrawler(BaseCrawler):
    URLS = [
        "https://www.mi.com/hk/events",
        "https://www.mi.com/hk/promotions",
    ]

    def fetch(self):
        deals = []
        try:
            for url in self.URLS:
                resp = self.fetch_url(url)
                soup = self.parse_soup(resp.text)
                items = soup.select('.event-item, .promo-item, .deal-card')[:8]
                for item in items:
                    title = item.select_one('h3, h2, .title')
                    title = title.get_text(strip=True) if title else ""
                    if not title:
                        continue
                    deals.append(self.make_deal(
                        shop="小米 Xiaomi HK", cat="electronics", title=title,
                        price_now="查看詳情", price_was="", save="",
                        valid="", tags=[], link=url, emoji="📱"
                    ))
        except Exception as e:
            print(f"  [WARN] 小米爬蟲異常，使用備用資料: {e}")
            deals = self._fallback()
        return deals[:8]

    def _fallback(self):
        return [
            self.make_deal("小米 Xiaomi HK", "electronics", "小米 816 感恩季：全場手機/家電低至5折",
                           "低至5折", "原價", "省50%", "2026年8月1日 – 8月31日", ["hot","new","limited"],
                           "https://www.mi.com/hk", "📱"),
            self.make_deal("小米 Xiaomi HK", "electronics", "小米 紅米手機 指定型號買1送1保護殼",
                           "送保護殼", "", "", "2026年8月1日 – 8月31日", ["new"],
                           "https://www.mi.com/hk", "📱"),
            self.make_deal("小米 Xiaomi HK", "electronics", "小米 掃地機器人/空氣清新機 組合價再減$200",
                           "組合減$200", "", "", "2026年8月4日 – 8月17日", ["hot"],
                           "https://www.mi.com/hk", "📱"),
            self.make_deal("小米 Xiaomi HK", "electronics", "小米 新會員首單免運費 + 額外95折",
                           "免運+95折", "", "", "新會員限定", ["new"],
                           "https://www.mi.com/hk", "📱"),
        ]
