#!/usr/bin/env python
# -*- coding: utf-8 -*-

import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from loguru import logger


@allure.title("测试入口广告弹窗功能")
def test_entry_ad(setup_driver):
    """测试入口广告弹窗功能"""
    driver = setup_driver
    page = BasePage(driver)

    # 导航到测试页面
    page.navigate_to("https://the-internet.herokuapp.com/entry_ad")

    # 1. 等待并检查广告弹窗是否出现
    modal_locator = (By.CLASS_NAME, "modal")
    if page.is_element_visible(modal_locator, timeout=5):
        logger.info("检测到入口广告弹窗")
        
        # 2. 获取广告内容
        ad_title = page.get_text((By.XPATH, "//div[@class='modal']//h3"))
        logger.info(f"广告标题: {ad_title}")
        
        # 3. 点击关闭按钮
        close_button = (By.XPATH, "//div[@class='modal']//p[contains(text(), 'Close')]")
        page.click(close_button)
        logger.info("点击关闭广告弹窗")
        
        # 4. 验证弹窗已关闭
        assert not page.is_element_visible(modal_locator, timeout=3), "广告弹窗未正确关闭"
        logger.info("广告弹窗已成功关闭")
        
    else:
        logger.info("未检测到入口广告弹窗，可能是随机显示")

    # 5. 验证页面主内容可访问
    main_content = page.get_text((By.TAG_NAME, "h3"))
    assert "Entry Ad" in main_content
    logger.info(f"页面主内容: {main_content}")
    
    # 6. 测试重新触发广告（点击重新启用链接）
    restart_link = (By.ID, "restart-ad")
    if page.is_element_present(restart_link):
        page.click(restart_link)
        logger.info("点击重新启用广告链接")
        
        # 等待页面重新加载并检查广告是否再次出现
        page.wait_for_page_load()
        if page.is_element_visible(modal_locator, timeout=3):
            logger.info("广告弹窗重新出现")
            # 再次关闭
            close_button_again = (By.XPATH, "//div[@class='modal']//p[contains(text(), 'Close')]")
            page.click(close_button_again)
            logger.info("再次关闭广告弹窗")
        
    logger.info("入口广告功能验证完成")