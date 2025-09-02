#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from loguru import logger


@allure.title("测试文件下载功能")
def test_download_file(setup_driver):
    """测试文件下载功能"""
    driver = setup_driver
    page = BasePage(driver)

    # 导航到测试页面
    page.navigate_to("https://the-internet.herokuapp.com/download")

    # 1. 获取默认下载目录
    download_dir = os.path.expanduser("~/Downloads")
    logger.info(f"下载目录: {download_dir}")

    # 2. 获取下载前文件列表
    files_before = set(os.listdir(download_dir)) if os.path.exists(download_dir) else set()

    # 3. 点击第一个下载链接
    first_download_link = (By.XPATH, "//a[contains(@href, '.txt')][1]")
    if page.is_element_present(first_download_link):
        file_name = page.get_attribute(first_download_link, "href").split("/")[-1]
        page.click(first_download_link)
        logger.info(f"点击下载文件: {file_name}")
        
        # 4. 等待下载完成
        download_file_path = os.path.join(download_dir, file_name)
        timeout = 10
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if os.path.exists(download_file_path):
                logger.info(f"文件下载成功: {download_file_path}")
                break
            time.sleep(1)
        else:
            # 如果通过文件路径找不到，检查下载目录是否有新文件
            files_after = set(os.listdir(download_dir)) if os.path.exists(download_dir) else set()
            new_files = files_after - files_before
            
            if new_files:
                downloaded_file = new_files.pop()
                logger.info(f"检测到新下载文件: {downloaded_file}")
                download_file_path = os.path.join(download_dir, downloaded_file)
            else:
                assert False, "文件下载失败，超时"

        # 5. 验证文件存在且不为空
        assert os.path.exists(download_file_path), f"下载文件不存在: {download_file_path}"
        assert os.path.getsize(download_file_path) > 0, "下载文件为空"
        
        logger.info("文件下载功能验证成功")
        
        # 6. 清理下载的文件
        try:
            os.remove(download_file_path)
            logger.info(f"清理下载文件: {download_file_path}")
        except Exception as e:
            logger.warning(f"清理下载文件失败: {e}")
    else:
        logger.warning("未找到可下载的文件链接")