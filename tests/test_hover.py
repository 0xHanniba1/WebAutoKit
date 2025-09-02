#!/usr/bin/env python
# -*- coding: utf-8 -*-

import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from loguru import logger


@allure.title("测试鼠标悬浮功能")
def test_hover(setup_driver):
    """测试鼠标悬浮功能"""
    driver = setup_driver
    page = BasePage(driver)

    # 导航到测试页面
    page.navigate_to("https://the-internet.herokuapp.com/hovers")

    # 1. 悬浮到第一个图片
    first_avatar = (By.XPATH, "//div[@class='figure'][1]")
    page.hover_over_element(first_avatar)

    # 2. 验证悬浮后显示的用户信息
    user_info = page.get_text((By.XPATH, "//div[@class='figure'][1]//h5"))
    logger.info(f"悬浮显示用户信息: {user_info}")
    assert "user1" in user_info

    # 3. 验证查看资料链接可见
    profile_link = (By.XPATH, "//div[@class='figure'][1]//a[@href='/users/1']")
    assert page.is_element_visible(profile_link), "查看资料链接不可见"
    logger.info("悬浮效果验证成功")
