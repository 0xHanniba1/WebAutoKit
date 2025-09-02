#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def setup_driver():
    """WebDriver配置fixture"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)  # 全局隐式等待：默认给每次查找元素多一点时间

    yield driver

    driver.quit()
