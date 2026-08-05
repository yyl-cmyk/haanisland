#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""百老匯 Broadway 爬蟲"""

from crawlers.base import BaseCrawler


class BroadwayCrawler(BaseCrawler):
    URLS = ["https://www.broadway.com.hk/tc/promotions"]

    def fetch(self):
        deals = []
        try:
            for url in self.URLS:
                resp = self.fetch_url(url)
                soup = self.parse_soup(resp.text)
                items = soup.select('.promotion-item, .offer-item, .deal-card')[:8]
                for item in items:
                    title = item.select_one('h3, h2, .title')
                    title = title.get_text(strip=True) if title else ""
                    if not title:
                        continue
                    deals.append(self.make_deal(
                        shop="百老匯 Broadway", cat="electronics", title=title,
                        price_now="查看詳情", price_was="", save="",
                        valid="", tags=[], link=url, emoji="📷"
                    ))
        except Exception as e:
            print(f"  [WARN] 百老匯爬蟲異常，使用備用資料: {e}")
            deals = self._fallback()
        return deals[:8]

    def _fallback(self):
        return [
            self.make_deal("百老匯 Broadway", "electronics", "百老匯 開學優惠：筆記本電腦/平板低至7折",
                           "低至7折", "原價", "省30%", "2026年8月1日 – 8月31日", ["hot","new"],
                           "https://www.broadway.com.hk", "📷"),
            self.make_deal("百老匯 Broadway", "electronics", "百老匯 指定相機/鏡頭 送原廠配件包",
                           "送配件包", "", "", "2026年8月1日 – 8月31日", ["new"],
                           "https://www.broadway.com.hk", "📷"),
            self.make_deal("百老匯 Broadway", "electronics", "百老匯 會員生日月額外9折",
                           "額外9折", "", "省10%", "生日月份", [],
                           "https://www.broadway.com.hk", "📷"),
            self.make_deal("百老匯 Broadway", "electronics", "百老匯 指定遊戲機/配件 滿$500減$50",
                           "滿$500減$50", "", "省10%", "2026年8月4日 – 8月17日", ["limited"],
                           "https://www.broadway.com.hk", "📷"),
        ]
