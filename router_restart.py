#!/usr/bin/env python3
"""
Router Restart Automation Script
Logs into a router at 192.168.1.1, navigates to restart page, and confirms restart.
"""

import sys
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Configuration
ROUTER_URL = "https://192.168.1.1"
ROUTER_USERNAME = "admin"
ROUTER_PASSWORD = "Debianhusk2"
TIMEOUT = 10  # seconds

# Setup logging
import os
log_file = os.path.expanduser('~/router_restart.log')  # Home directory on all systems

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def setup_driver():
    """Initialize Chrome WebDriver in headless mode."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(TIMEOUT)
    return driver


def login(driver):
    """Log into the router."""
    try:
        logger.info(f"Accessing router at {ROUTER_URL}")
        driver.get(ROUTER_URL)

        # Wait for login form
        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.NAME, "Frm_Username"))
        )

        # Fill login credentials
        username_field = driver.find_element(By.NAME, "Frm_Username")
        password_field = driver.find_element(By.NAME, "Frm_Password")

        username_field.clear()
        username_field.send_keys(ROUTER_USERNAME)

        password_field.clear()
        password_field.send_keys(ROUTER_PASSWORD)

        # Submit login form
        login_button = driver.find_element(By.ID, "LoginId")
        login_button.click()

        logger.info("Login submitted, waiting for page load...")
        # Wait for successful login (page should redirect)
        WebDriverWait(driver, TIMEOUT).until(
            EC.url_changes(ROUTER_URL)
        )
        logger.info("Successfully logged in")
        return True

    except Exception as e:
        logger.error(f"Login failed: {e}")
        return False


def navigate_to_restart(driver):
    """Navigate to the restart/reboot page through menu system."""
    try:
        import time
        logger.info("Navigating to restart page...")

        # Menu structure: Management & Diagnostic → System Management → Device Management
        time.sleep(2)

        # Click Management & Diagnostic
        mgrlink = driver.find_element(By.ID, "mgrAndDiag")
        mgrlink.click()
        logger.info("Clicked Management & Diagnostic")
        time.sleep(2)

        # Click System Management (devMgr)
        devmgrlink = driver.find_element(By.ID, "devMgr")
        devmgrlink.click()
        logger.info("Clicked System Management")
        time.sleep(2)

        # Click Device Management (rebootAndReset)
        rebootlink = driver.find_element(By.ID, "rebootAndReset")
        rebootlink.click()
        logger.info("Clicked Device Management")
        time.sleep(2)

        return True

    except Exception as e:
        logger.error(f"Failed to navigate to restart page: {e}")
        return False


def click_restart_button(driver):
    """Find and click the restart button."""
    try:
        logger.info("Looking for restart button...")

        # Try multiple selectors to find the restart button
        button_selectors = [
            ("ID: Btn_restart", (By.ID, "Btn_restart")),
            ("XPath: Repornește text", (By.XPATH, "//button[contains(text(), 'Repornește')]")),
            ("XPath: Restart text", (By.XPATH, "//button[contains(text(), 'Restart')]")),
        ]

        for label, (selector_type, selector_value) in button_selectors:
            try:
                button = WebDriverWait(driver, TIMEOUT).until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                logger.info(f"Found restart button: {label}")
                button.click()
                logger.info("Clicked restart button")
                return True
            except:
                continue

        logger.error("Could not find restart button")
        return False

    except Exception as e:
        logger.error(f"Error clicking restart button: {e}")
        return False


def confirm_restart(driver):
    """Confirm the restart operation by clicking OK."""
    try:
        import time
        logger.info("Looking for confirmation dialog...")

        # Try to find OK button by ID first (most reliable)
        try:
            ok_button = WebDriverWait(driver, TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "confirmOK"))
            )
            logger.info("Found confirmation dialog OK button")
            ok_button.click()
            logger.info("Clicked OK button - restart initiated")
            return True
        except Exception as e1:
            # Try by text as fallback
            ok_button = WebDriverWait(driver, TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))
            )
            ok_button.click()
            logger.info("Clicked OK button - restart initiated")
            return True

    except Exception as e:
        logger.error(f"Failed to confirm restart: {e}")
        return False


def main():
    """Main execution function."""
    logger.info("=" * 50)
    logger.info("Router Restart Operation Started")
    logger.info("=" * 50)

    driver = None
    try:
        driver = setup_driver()

        if not login(driver):
            logger.error("Failed to login to router")
            return 1

        if not navigate_to_restart(driver):
            logger.warning("Could not navigate to standard restart URL, continuing...")

        if not click_restart_button(driver):
            logger.error("Failed to click restart button")
            return 1

        if not confirm_restart(driver):
            logger.error("Failed to confirm restart")
            return 1

        logger.info("=" * 50)
        logger.info("Router restart initiated successfully!")
        logger.info("=" * 50)
        return 0

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    sys.exit(main())
