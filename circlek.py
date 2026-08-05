#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Circle K OK便利店 爬蟲"""

from crawlers.base import BaseCrawler


class CircleKCrawler(BaseCrawler):
    URLS = ["https://www.circlek.hk/tc/promotions"]

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
                        shop="Circle K OK便利店", cat="convenience", title=title,
                        price_now="查看詳情", price_was="", save="",
                        valid="", tags=[], link=url, emoji="⭕"
                    ))
        except Exception as e:
            print(f"  [WARN] Circle K爬蟲異常，使用備用資料: {e}")
            deals = self._fallback()
        return deals[:8]

    def _fallback(self):
        return [
            self.make_deal("Circle K OK便利店", "convenience", "OK便利店 指定飲品買1送1（寶礦力、道地等）",
                           "買1送1", "", "省50%", "2026年8月4日 – 8月10日", ["hot","limited"],
                           "https://www.circlek.hk", "⭕"),
            self.make_deal("Circle K OK便利店", "convenience", "OK便利店 會員積分兌換指定商品",
                           "積分兌換", "", "", "長期", [],
                           "https://www.circlek.hk", "⭕"),
            self.make_deal("Circle K OK便利店", "convenience", "OK便利店 現磨咖啡$12/杯（原價$16）",
                           "$12/杯", "$16", "省25%", "2026年8月1日 – 8月31日", ["hot"],
                           "https://www.circlek.hk", "⭕"),
            self.make_deal("Circle K OK便利店", "convenience", "OK便利店 指定麵包/三文治 買2送1",
                           "買2送1", "", "省33%", "2026年8月4日 – 8月17日", ["new"],
                           "https://www.circlek.hk", "⭕"),
        ]
