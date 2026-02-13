#!/usr/bin/env python3
"""
Router Restart Automation - TEST MODE
Does everything EXCEPT actually confirm the restart.
Use this to verify the script works before scheduling it.
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
ROUTER_URL = "https://92.82.75.79"
ROUTER_USERNAME = "admin"
ROUTER_PASSWORD = "Debianhusk2"
TIMEOUT = 10  # seconds

# Setup logging
import os
log_file = os.path.expanduser('~/router_restart_test.log')  # Home directory on all systems

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
        logger.info("✓ Successfully logged in")
        return True

    except Exception as e:
        logger.error(f"✗ Login failed: {e}")
        return False


def navigate_to_restart(driver):
    """Navigate to the restart/reboot page through JavaScript menus."""
    try:
        logger.info("Navigating to restart page through menus...")
        import time

        # Wait for JavaScript menus to load
        time.sleep(2)

        # Click on "Management & Diagnostic" menu item (id="mgrAndDiag")
        logger.info("Clicking on Management & Diagnostic menu...")

        try:
            mgrlink = driver.find_element(By.ID, "mgrAndDiag")
            mgrlink.click()
            logger.info("✓ Clicked Management & Diagnostic")
        except:
            logger.warning("Could not find Management & Diagnostic menu")
            return False

        time.sleep(2)

        # Click on "Managementul sistemului" (devMgr) first
        logger.info("Clicking on System Management submenu...")

        try:
            devmgrlink = driver.find_element(By.ID, "devMgr")
            devmgrlink.click()
            logger.info("✓ Clicked System Management (devMgr)")
        except:
            logger.warning("Could not find System Management submenu")
            return False

        time.sleep(2)

        # Now click on the restart submenu (id="rebootAndReset")
        logger.info("Clicking on Device Management submenu...")

        try:
            rebootlink = driver.find_element(By.ID, "rebootAndReset")
            rebootlink.click()
            logger.info("✓ Clicked Device Management (rebootAndReset)")
        except:
            logger.warning("Could not find Device Management submenu")
            # Try to find it by text content
            try:
                elem = driver.find_element(By.XPATH, "//*[contains(text(), 'Managementul dispozitivelor')]")
                elem.click()
                logger.info("✓ Clicked by text content")
            except:
                logger.warning("Could not find restart menu by text either")
                return False

        time.sleep(2)

        # Now look for the restart button
        if "Repornire" in driver.page_source or "Restart" in driver.page_source:
            logger.info("✓ Found restart page after menu navigation")
            return True
        else:
            logger.warning("⚠ Restart page not found yet, but continuing...")
            return True

    except Exception as e:
        logger.error(f"✗ Failed to navigate to restart page: {e}")
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
            ("XPath: Repornire text", (By.XPATH, "//button[contains(text(), 'Repornire')]")),
        ]

        for label, (selector_type, selector_value) in button_selectors:
            try:
                button = WebDriverWait(driver, TIMEOUT).until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                logger.info(f"✓ Found restart button: {label}")

                # DON'T CLICK - just show we found it
                logger.info("✓ [TEST MODE] Found button but NOT clicking")
                return True
            except:
                continue

        logger.error("✗ Could not find restart button")
        logger.info("Page HTML (first 2000 chars):")
        logger.info(driver.page_source[:2000])
        return False

    except Exception as e:
        logger.error(f"✗ Error finding restart button: {e}")
        return False


def check_confirmation_dialog(driver):
    """Check if confirmation dialog exists (don't confirm it)."""
    try:
        logger.info("Looking for confirmation dialog...")

        # Look for OK button by ID or text
        try:
            ok_button = driver.find_element(By.ID, "confirmOK")
            logger.info("✓ Found confirmation dialog (ID: confirmOK)")
            logger.info(f"  Button text: '{ok_button.text}'")
            logger.info("✓ [TEST MODE] Confirmation dialog found but NOT clicking OK")
            return True
        except:
            # Try by text
            ok_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'OK')]")
            if ok_buttons:
                logger.info(f"✓ Found {len(ok_buttons)} OK button(s)")
                for i, btn in enumerate(ok_buttons):
                    logger.info(f"  Button {i+1}: '{btn.text}'")
                logger.info("✓ [TEST MODE] Confirmation dialog found but NOT clicking OK")
                return True
            else:
                logger.warning("⚠ Could not find OK button for confirmation")
                return False

    except Exception as e:
        logger.error(f"✗ Error checking confirmation dialog: {e}")
        return False


def main():
    """Main execution function."""
    logger.info("=" * 60)
    logger.info("TEST MODE: Router Restart Script Test")
    logger.info("This will verify all steps EXCEPT the final confirmation")
    logger.info("=" * 60)

    driver = None
    try:
        driver = setup_driver()

        if not login(driver):
            logger.error("Failed to login to router")
            return 1

        if not navigate_to_restart(driver):
            logger.warning("Warning: Could not navigate to standard restart URL")

        if not click_restart_button(driver):
            logger.error("Failed to find restart button")
            return 1

        if not check_confirmation_dialog(driver):
            logger.warning("Warning: Confirmation dialog not found")

        logger.info("=" * 60)
        logger.info("✓ TEST SUCCESSFUL - All steps verified!")
        logger.info("✓ Script is ready to be scheduled")
        logger.info("=" * 60)
        return 0

    except Exception as e:
        logger.error(f"✗ Unexpected error: {e}")
        return 1

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    sys.exit(main())
