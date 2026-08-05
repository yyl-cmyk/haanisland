#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""慳島 - 基礎爬蟲類"""

import re
import time
import random
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup


class BaseCrawler(ABC):
    """所有爬蟲的基礎類別"""

    # 請求設定
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-HK,zh-TW;q=0.9,zh;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    # 重試設定
    MAX_RETRIES = 3
    RETRY_DELAY = 2
    REQUEST_TIMEOUT = 15

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def fetch_url(self, url, retries=None):
        """帶重試機制的請求"""
        retries = retries or self.MAX_RETRIES
        for attempt in range(retries):
            try:
                # 隨機延遲避免被封
                if attempt > 0:
                    time.sleep(self.RETRY_DELAY + random.uniform(0, 1))

                resp = self.session.get(url, timeout=self.RETRY_TIMEOUT)
                resp.raise_for_status()
                resp.encoding = 'utf-8'
                return resp
            except Exception as e:
                print(f"  [WARN] 請求失敗 ({attempt+1}/{retries}): {url} - {e}")
                if attempt == retries - 1:
                    raise
        return None

    def parse_soup(self, html):
        """解析 HTML"""
        return BeautifulSoup(html, 'lxml')

    def make_deal(self, shop, cat, title, price_now, price_was="", save="", 
                  valid="", tags=None, link="", emoji=""):
        """建立標準化的優惠字典"""
        return {
            "shop": shop,
            "cat": cat,
            "emoji": emoji,
            "title": title.strip(),
            "priceNow": price_now,
            "priceWas": price_was,
            "save": save,
            "valid": valid or "請查看官網",
            "tags": tags or [],
            "link": link,
        }

    def calc_save(self, now, was):
        """計算折扣百分比"""
        try:
            now_f = float(re.sub(r'[^\d.]', '', str(now)))
            was_f = float(re.sub(r'[^\d.]', '', str(was)))
            if was_f > 0:
                pct = int((1 - now_f / was_f) * 100)
                return f"省{pct}%"
        except:
            pass
        return ""

    @abstractmethod
    def fetch(self):
        """子類必須實現此方法，回傳 deals list"""
        pass
