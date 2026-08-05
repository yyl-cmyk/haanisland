#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""惠康 Wellcome 爬蟲"""

from crawlers.base import BaseCrawler


class WellcomeCrawler(BaseCrawler):
    URLS = [
        "https://www.wellcome.com.hk/zh-hk/promotions.html",
        "https://www.wellcome.com.hk/zh-hk/offers.html",
    ]

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
                        shop="惠康 Wellcome", cat="supermarket", title=title,
                        price_now="查看詳情", price_was="", save="",
                        valid="", tags=[], link=url, emoji="🥬"
                    ))
        except Exception as e:
            print(f"  [WARN] 惠康爬蟲異常，使用備用資料: {e}")
            deals = self._fallback()
        return deals[:8]

    def _fallback(self):
        return [
            self.make_deal("惠康 Wellcome", "supermarket", "惠康yuu會員週二額外95折",
                           "額外95折", "", "", "逢星期二", ["hot"],
                           "https://www.wellcome.com.hk", "🥬"),
            self.make_deal("惠康 Wellcome", "supermarket", "Market Place / 3hreesixty 有機食品滿$200減$30",
                           "滿$200減$30", "", "省15%", "2026年8月1日 – 8月31日", ["new"],
                           "https://www.wellcome.com.hk", "🥬"),
            self.make_deal("惠康 Wellcome", "supermarket", "Oliver's The Delicatessen 精選芝士/凍肉8折",
                           "8折", "原價", "省20%", "2026年8月4日 – 8月10日", ["limited"],
                           "https://www.wellcome.com.hk", "🥬"),
            self.make_deal("惠康 Wellcome", "supermarket", "惠康網店滿$350免運費 + 指定商品買1送1",
                           "免運+買1送1", "", "", "長期", [],
                           "https://www.wellcome.com.hk", "🥬"),
            self.make_deal("惠康 Wellcome", "supermarket", "指定品牌洗頭水/護髮素 第2件半價（潘婷、海倫仙度絲）",
                           "第2件半價", "", "省25%", "2026年8月4日 – 8月17日", ["hot"],
                           "https://www.wellcome.com.hk", "🥬"),
        ]
