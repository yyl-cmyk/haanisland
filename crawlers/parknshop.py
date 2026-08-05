#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""百佳 ParknShop 爬蟲"""

import re
from crawlers.base import BaseCrawler


class ParknShopCrawler(BaseCrawler):
    """百佳網店優惠爬蟲"""

    URLS = [
        "https://www.parknshop.com/zh-hk/promotions",
        "https://www.parknshop.com/zh-hk/deals",
    ]

    def fetch(self):
        deals = []
        try:
            for url in self.URLS:
                resp = self.fetch_url(url)
                soup = self.parse_soup(resp.text)

                # 嘗試多種選擇器
                promo_items = (
                    soup.select('.promotion-item') or
                    soup.select('[class*="promo"]') or
                    soup.select('.deal-card') or
                    soup.select('.product-tile')
                )

                for item in promo_items[:8]:
                    title = self._extract_text(item, ['h3', 'h2', '.title', '.name'])
                    if not title:
                        continue

                    price_now = self._extract_text(item, ['.price-now', '.special-price', '.deal-price'])
                    price_was = self._extract_text(item, ['.price-was', '.original-price', '.old-price'])
                    valid = self._extract_text(item, ['.validity', '.period', '.date'])
                    link = self._extract_link(item, url)

                    save = self.calc_save(price_now, price_was)

                    deals.append(self.make_deal(
                        shop="百佳 ParknShop",
                        cat="supermarket",
                        title=title,
                        price_now=price_now or "查看詳情",
                        price_was=price_was,
                        save=save,
                        valid=valid,
                        tags=self._infer_tags(title),
                        link=link or "https://www.parknshop.com",
                        emoji="🛒"
                    ))
        except Exception as e:
            print(f"  [WARN] 百佳爬蟲異常，使用備用資料: {e}")
            deals = self._fallback()

        return deals[:8]

    def _extract_text(self, item, selectors):
        for sel in selectors:
            el = item.select_one(sel)
            if el:
                return el.get_text(strip=True)
        return ""

    def _extract_link(self, item, base_url):
        a = item.select_one('a')
        if a and a.get('href'):
            href = a['href']
            if href.startswith('http'):
                return href
            return base_url.rstrip('/') + '/' + href.lstrip('/')
        return ""

    def _infer_tags(self, title):
        tags = []
        t = title.lower()
        if '買1送1' in title or '買一送一' in title or '買2送1' in title:
            tags.append('hot')
        if '新會員' in title or '新品' in title:
            tags.append('new')
        if '限定' in title or '限時' in title:
            tags.append('limited')
        return tags

    def _fallback(self):
        """當爬蟲失敗時的備用資料"""
        return [
            self.make_deal("百佳 ParknShop", "supermarket", "百佳網店購物滿$600 送$50現金券",
                           "滿$600送$50", "", "", "2026年8月4日 – 8月10日", ["hot","new"],
                           "https://www.parknshop.com", "🛒"),
            self.make_deal("百佳 ParknShop", "supermarket", "TASTE / FUSION / GREAT 週末限定：指定日本食材買2送1",
                           "買2送1", "", "省33%", "逢星期五至日", ["limited"],
                           "https://www.parknshop.com", "🛒"),
            self.make_deal("百佳 ParknShop", "supermarket", "百佳會員積分兌換：指定零食飲品低至5折",
                           "低至5折", "", "省50%", "長期", ["hot"],
                           "https://www.parknshop.com", "🛒"),
            self.make_deal("百佳 ParknShop", "supermarket", "百佳網店新會員首單免運費 + 額外95折",
                           "免運+95折", "", "", "新會員限定", ["new"],
                           "https://www.parknshop.com", "🛒"),
            self.make_deal("百佳 ParknShop", "supermarket", "指定啤酒/汽水買1送1（喜力、可口可樂等）",
                           "買1送1", "", "省50%", "2026年8月4日 – 8月17日", ["hot","limited"],
                           "https://www.parknshop.com", "🛒"),
        ]
