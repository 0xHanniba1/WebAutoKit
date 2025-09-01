#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from loguru import logger


@allure.title("测试iframe切换功能")
def test_frame_switch(setup_driver):
    """测试iframe切换功能"""
    driver = setup_driver
    page = BasePage(driver)

    # 导航到测试页面
    page.navigate_to("https://demoqa.com/frames")

    # 1. 切换到iframe
    assert page.switch_to_frame((By.ID, "frame1")), "切换到iframe失败"

    # 2. 验证：能访问iframe内的元素
    frame_text = page.get_text((By.ID, "sampleHeading"))
    logger.info(f"切换成功，frame 内文本: {frame_text}")
    assert "This is a sample page" in frame_text

    # 3. 切回主页面
    assert page.switch_to_default_content(), "切换回主页面失败"

    # 4. 验证：能访问主页面元素
    main_text = page.get_text((By.XPATH, "//h1[contains(text(), 'Frames')]"))
    logger.info(f"切回主页面成功，找到元素: {main_text}")
    assert "Frames" in main_text
