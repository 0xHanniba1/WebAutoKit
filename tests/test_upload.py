#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from loguru import logger


@allure.title("测试文件上传功能")
def test_upload_file(setup_driver):
    """测试文件上传功能"""
    driver = setup_driver
    page = BasePage(driver)

    # 导航到测试页面
    page.navigate_to("https://the-internet.herokuapp.com/upload")

    # 1. 创建测试文件
    test_file_path = "/tmp/test_upload.txt"
    with open(test_file_path, "w") as f:
        f.write("Test file for upload")

    try:
        # 2. 选择文件
        file_input = (By.ID, "file-upload")
        page.input_text(file_input, test_file_path)
        logger.info(f"选择了文件: {test_file_path}")

        # 3. 点击上传按钮
        upload_button = (By.ID, "file-submit")
        page.click(upload_button)

        # 4. 验证上传成功
        success_message = page.get_text((By.ID, "uploaded-files"))
        logger.info(f"上传结果: {success_message}")
        assert "test_upload.txt" in success_message

        # 5. 验证页面标题
        page_title = page.get_text((By.TAG_NAME, "h3"))
        assert "File Uploaded!" in page_title
        
        logger.info("文件上传功能验证成功")

    finally:
        # 清理测试文件
        if os.path.exists(test_file_path):
            os.remove(test_file_path)