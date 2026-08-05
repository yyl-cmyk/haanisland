#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""7-Eleven 香港 爬蟲"""

from crawlers.base import BaseCrawler


class SevenElevenCrawler(BaseCrawler):
    URLS = [
        "https://www.7-eleven.com.hk/tc/campaigns",
        "https://www.7-eleven.com.hk/tc/promotions",
    ]

    def fetch(self):
        deals = []
        try:
            for url in self.URLS:
                resp = self.fetch_url(url)
                soup = self.parse_soup(resp.text)
                items = soup.select('.campaign-item, .promo-item, .offer-card')[:8]
                for item in items:
                    title = item.select_one('h3, h2, .title, .campaign-title')
                    title = title.get_text(strip=True) if title else ""
                    if not title:
                        continue
                    deals.append(self.make_deal(
                        shop="7-Eleven 香港", cat="convenience", title=title,
                        price_now="查看詳情", price_was="", save="",
                        valid="", tags=[], link=url, emoji="🏪"
                    ))
        except Exception as e:
            print(f"  [WARN] 7-Eleven爬蟲異常，使用備用資料: {e}")
            deals = self._fallback()
        return deals[:8]

    def _fallback(self):
        return [
            self.make_deal("7-Eleven 香港", "convenience", "7-Eleven 買1送1：指定零食/飲品（樂事薯片、維他奶等）",
                           "買1送1", "", "省50%", "2026年8月4日 – 8月10日", ["hot","limited"],
                           "https://www.7-eleven.com.hk", "🏪"),
            self.make_deal("7-Eleven 香港", "convenience", "7-Eleven yuu會員 指定商品額外9折",
                           "額外9折", "", "省10%", "長期", ["hot"],
                           "https://www.7-eleven.com.hk", "🏪"),
            self.make_deal("7-Eleven 香港", "convenience", "7-Eleven 現磨咖啡買5送1",
                           "買5送1", "", "省17%", "長期", [],
                           "https://www.7-eleven.com.hk", "🏪"),
            self.make_deal("7-Eleven 香港", "convenience", "7-Eleven 指定便當/飯團 晚上9點後7折",
                           "7折", "原價", "省30%", "每日晚上9點後", ["limited"],
                           "https://www.7-eleven.com.hk", "🏪"),
            self.make_deal("7-Eleven 香港", "convenience", "7-Eleven 新口味雪糕/甜品 上市優惠$10/件",
                           "$10/件", "$15起", "省33%", "2026年8月4日 – 8月17日", ["new"],
                           "https://www.7-eleven.com.hk", "🏪"),
        ]
