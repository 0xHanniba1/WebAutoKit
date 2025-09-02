#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from loguru import logger


class BasePage:
    """基础页面类"""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def _wait(self, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout)

    def find_element(self, locator, timeout=None):
        """查找单个元素"""
        try:
            return self._wait(timeout).until(EC.presence_of_element_located(locator))
        except TimeoutException:
            logger.error(f"Element not found: 「{locator}」")
            raise NoSuchElementException(f"Element not found: 「{locator}」")

    def find_elements(self, locator, timeout=None):
        """查找多个元素"""
        try:
            return self._wait(timeout).until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            logger.error(f"Elements not found: 「{locator}」")
            return []

    def click(self, locator, timeout=None):
        """点击元素"""
        element = self._wait(timeout).until(EC.element_to_be_clickable(locator))
        element.click()
        logger.info(f"Clicked element: 「{locator}」")

    def input_text(self, locator, text):
        """输入文本"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        logger.info(f"Input text '「{text}」' to element: 「{locator}」")

    def get_text(self, locator):
        """获取元素文本"""
        element = self.find_element(locator)
        text = element.text
        logger.info(f"Got text '「{text}」' from element: 「{locator}」")
        return text

    def get_attribute(self, locator, attribute):
        """获取元素属性"""
        element = self.find_element(locator)
        value = element.get_attribute(attribute)
        logger.info(f"Got attribute '「{attribute}」' value '「{value}」' from element: 「{locator}」")
        return value

    def is_element_visible(self, locator, timeout=None):
        """检察元素是否可见"""
        try:
            self._wait(timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator):
        """检察元素是否存在"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def wait_for_element_visible(self, locator, timeout=None):
        """等待元素可见"""
        return self._wait(timeout).until(EC.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, locator, timeout=None):
        """等待元素可点击"""
        return self._wait(timeout).until(EC.element_to_be_clickable(locator))

    def scroll_to_element(self, locator):
        """滚动到元素"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(ture);", element)
        logger.info(f"Scrolled to element: 「{locator}」")

    def hover_over_element(self, locator):
        """鼠标悬停"""
        element = self.find_element(locator)
        ActionChains(self.driver).move_to_element(element).perform()
        logger.info(f"Hovered over element: 「{locator}」")

    def move_to_element(self, locator):
        """移动鼠标到元素"""
        element = self.find_element(locator)
        ActionChains(self.driver).move_to_element(element).perform()
        logger.info(f"Moved mouse to element: 「{locator}」")

    def select_dropdown_by_text(self, locator, text):
        """通过文本选择下拉选项"""
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_visible_text(text)
        logger.info(f"Selected dropdown option '「{text}」' for element: 「{locator}」")

    def select_dropdown_by_value(self, locator, value):
        """通过值选择下拉选项"""
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_value(value)
        logger.info(f"Selected dropdown value '「{value}」' for element: 「{locator}」")

    def navigate_to(self, url):
        """导航到页面"""
        self.driver.get(url)
        self.wait_for_page_load()
        logger.info(f"Navigated to: 「{url}」")

    def wait_for_page_load(self, timeout=30):
        """等待页面加载完成"""

        def _is_page_complete(driver_instance):
            return driver_instance.execute_script("return document.readyState") == "complete"

        self._wait(timeout).until(_is_page_complete)
        logger.info("Page loaded completely")

    def wait_for_url(self, url_fragment, timeout=None):
        try:
            self._wait(timeout).until(EC.url_contains(url_fragment))
            return True
        except TimeoutException:
            return False

    def get_current_url(self):
        """获取当前URL"""
        url = self.driver.current_url
        logger.info(f"Current URL: 「{url}」")
        return url

    def get_page_title(self):
        """获取页面标题"""
        title = self.driver.title
        logger.info(f"Page title: 「{title}」")
        return title

    def refresh_page(self):
        """刷新页面"""
        self.driver.refresh()
        logger.info("Page refreshed")

    def go_back(self):
        """返回上一页"""
        self.driver.back()
        logger.info("Navigated back")

    def go_forward(self):
        """前进到下一页"""
        self.driver.forward()
        logger.info("Navigated froward")

    def take_screenshot(self, file_path):
        """截图"""
        self.driver.save_screenshot(file_path)
        logger.info(f"Screenshot saved: 「{file_path}」")

    def execute_script(self, script, *args):
        """执行JavaScript"""
        result = self.driver.execute_script(script, *args)
        logger.info(f"Executed script: 「{script}」")
        return result

    def switch_to_frame(self, locator, timeout=None):
        """切换到iframe"""
        try:
            self._wait(timeout).until(EC.frame_to_be_available_and_switch_to_it(locator))
            logger.info(f"Switched to frame: 「{locator}」")
            return True
        except TimeoutException:
            logger.error(f"Failed to switch to frame: 「{locator}」")
            return False

    def switch_to_default_content(self):
        """切换回主页面"""
        try:
            self.driver.switch_to.default_content()
            logger.info("Switched back to default content")
            return True
        except Exception as e:
            logger.error(f"Failed to switch to default content: {e}")
            return False

    def switch_to_parent_frame(self):
        """切换到父级frame"""
        try:
            self.driver.switch_to.parent_frame()
            logger.info("Switched to parent frame")
            return True
        except Exception as e:
            logger.error(f"Failed to switch to parent frame: {e}")
            return False
