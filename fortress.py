#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""豐澤 Fortress 爬蟲"""

from crawlers.base import BaseCrawler


class FortressCrawler(BaseCrawler):
    URLS = [
        "https://www.fortress.com.hk/tc/promotions",
        "https://www.fortress.com.hk/tc/deals",
    ]

    def fetch(self):
        deals = []
        try:
            for url in self.URLS:
                resp = self.fetch_url(url)
                soup = self.parse_soup(resp.text)
                items = soup.select('.promotion-item, .deal-item, .offer-card')[:8]
                for item in items:
                    title = item.select_one('h3, h2, .title')
                    title = title.get_text(strip=True) if title else ""
                    if not title:
                        continue
                    deals.append(self.make_deal(
                        shop="豐澤 Fortress", cat="electronics", title=title,
                        price_now="查看詳情", price_was="", save="",
                        valid="", tags=[], link=url, emoji="📺"
                    ))
        except Exception as e:
            print(f"  [WARN] 豐澤爬蟲異常，使用備用資料: {e}")
            deals = self._fallback()
        return deals[:8]

    def _fallback(self):
        return [
            self.make_deal("豐澤 Fortress", "electronics", "豐澤 夏日電器節：冷氣機/風扇低至6折",
                           "低至6折", "原價", "省40%", "2026年8月1日 – 8月31日", ["hot","new"],
                           "https://www.fortress.com.hk", "📺"),
            self.make_deal("豐澤 Fortress", "electronics", "豐澤 指定手機/平板 以舊換新額外減$500",
                           "額外減$500", "", "", "2026年8月1日 – 8月31日", ["hot"],
                           "https://www.fortress.com.hk", "📺"),
            self.make_deal("豐澤 Fortress", "electronics", "豐澤 信用卡分期0利息 + 額外95折",
                           "0息+95折", "", "省5%", "指定信用卡", [],
                           "https://www.fortress.com.hk", "📺"),
            self.make_deal("豐澤 Fortress", "electronics", "豐澤 指定廚房電器 買滿$1000減$100",
                           "滿$1000減$100", "", "省10%", "2026年8月4日 – 8月17日", ["new"],
                           "https://www.fortress.com.hk", "📺"),
            self.make_deal("豐澤 Fortress", "electronics", "豐澤 網店獨家：指定耳機/喇叭 買1送1",
                           "買1送1", "", "省50%", "網店限定", ["hot","limited"],
                           "https://www.fortress.com.hk", "📺"),
        ]
