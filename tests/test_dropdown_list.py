#!/usr/bin/env python
# -*- coding: utf-8 -*-

import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from loguru import logger


@allure.title("测试下拉框选择功能")
def test_dropdown_list(setup_driver):
    """测试下拉框选择功能"""
    driver = setup_driver
    page = BasePage(driver)

    # 导航到测试页面
    page.navigate_to("https://the-internet.herokuapp.com/dropdown")

    # 1. 通过文本选择下拉选项
    dropdown_locator = (By.ID, "dropdown")
    page.select_dropdown_by_text(dropdown_locator, "Option 1")

    # 2. 验证选择结果
    selected_text = page.get_text((By.XPATH, "//select[@id='dropdown']/option[@selected]"))
    logger.info(f"通过文本选择的选项: {selected_text}")
    assert "Option 1" in selected_text

    # 3. 通过值选择下拉选项
    page.select_dropdown_by_value(dropdown_locator, "2")

    # 4. 验证选择结果
    selected_text = page.get_text((By.XPATH, "//select[@id='dropdown']/option[@selected]"))
    logger.info(f"通过值选择的选项: {selected_text}")
    assert "Option 2" in selected_text

    logger.info("下拉框选择功能验证成功")
