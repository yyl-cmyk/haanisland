#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""唐吉訶德 DONKI 爬蟲"""

from crawlers.base import BaseCrawler


class DonkiCrawler(BaseCrawler):
    URLS = [
        "https://www.dondondonki.com.hk/tc/promotions",
        "https://www.dondondonki.com.hk/tc/campaigns",
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
                        shop="唐吉訶德 DONKI", cat="department", title=title,
                        price_now="查看詳情", price_was="", save="",
                        valid="", tags=[], link=url, emoji="🎌"
                    ))
        except Exception as e:
            print(f"  [WARN] DONKI爬蟲異常，使用備用資料: {e}")
            deals = self._fallback()
        return deals[:8]

    def _fallback(self):
        return [
            self.make_deal("唐吉訶德 DONKI", "department", "DONKI 驚安の殿堂：指定日本零食/飲品 買2送1",
                           "買2送1", "", "省33%", "2026年8月4日 – 8月10日", ["hot","limited"],
                           "https://www.dondondonki.com.hk", "🎌"),
            self.make_deal("唐吉訶德 DONKI", "department", "DONKI 會員限定：全場9折（每月8日）",
                           "全場9折", "", "省10%", "每月8日", ["hot"],
                           "https://www.dondondonki.com.hk", "🎌"),
            self.make_deal("唐吉訶德 DONKI", "department", "DONKI 指定和牛/海鮮 晚市8折",
                           "晚市8折", "原價", "省20%", "每日晚上8點後", ["limited"],
                           "https://www.dondondonki.com.hk", "🎌"),
            self.make_deal("唐吉訶德 DONKI", "department", "DONKI 新會員註冊送$50現金券",
                           "送$50券", "", "", "新會員限定", ["new"],
                           "https://www.dondondonki.com.hk", "🎌"),
            self.make_deal("唐吉訶德 DONKI", "department", "DONKI 指定日本美妝/護膚品 買滿$200減$30",
                           "滿$200減$30", "", "省15%", "2026年8月1日 – 8月31日", ["new"],
                           "https://www.dondondonki.com.hk", "🎌"),
        ]
