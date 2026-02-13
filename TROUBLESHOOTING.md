# Troubleshooting Guide

## Issue: Script runs but doesn't find restart page

### Root Cause
Every router has a different web interface. The standard URLs may not work for your specific router model.

### Solution

1. **Manually access your router:**
   - Open a browser
   - Go to `http://192.168.1.1`
   - Log in with `admin` / `Debianhusk2`
   - Navigate to the restart/reboot page
   - Note the exact URL in the address bar

2. **Inspect the page:**
   - Right-click on the restart button → "Inspect"
   - Look for the button's HTML attributes (name, id, class, or text)
   - Check if it's a `<button>`, `<input>`, or `<a>` tag

3. **Update the script:**
   - Open `router_restart.py`
   - In `navigate_to_restart()`: Add your actual URL to the `restart_urls` list
   - In `click_restart_button()`: Update the XPath selectors if needed

### Example Modification

If your restart page is at `http://192.168.1.1/system/reboot` and the button has `id="rebootBtn"`:

```python
def navigate_to_restart(driver):
    driver.get("http://192.168.1.1/system/reboot")
    return True

def click_restart_button(driver):
    button = driver.find_element(By.ID, "rebootBtn")
    button.click()
    return True
```

## Issue: "No such file or directory" when running from cron

### Root Cause
Relative paths don't work in cron. The script must be referenced with an absolute path.

### Solution

In your crontab, use the full path:

```bash
0 3 * * * /home/username/Development/telecomRouterRestart/router_restart.py
```

Not:
```bash
0 3 * * * ./router_restart.py
```

## Issue: ChromeDriver version mismatch

### Root Cause
Chrome and ChromeDriver versions must match exactly.

### Solution

```bash
# Check Chrome version
google-chrome --version
# or
chromium-browser --version

# Check ChromeDriver version
chromedriver --version

# If they don't match, update ChromeDriver
sudo apt-get install --only-upgrade chromium-chromedriver
```

## Issue: "Permission denied" when accessing log file

### Root Cause
Log file permissions are restrictive.

### Solution

```bash
sudo chmod 666 /var/log/router_restart.log
# or run script with sudo in crontab:
0 3 * * * sudo /path/to/router_restart.py
```

## Issue: Cron job appears to run but nothing happens

### Solution

1. **Check if cron daemon is running:**
   ```bash
   ps aux | grep cron
   ```

2. **Verify cron job is installed:**
   ```bash
   crontab -l
   ```

3. **Check system logs:**
   ```bash
   grep CRON /var/log/syslog | tail -20
   ```

4. **Test script manually:**
   ```bash
   /path/to/router_restart.py
   ```

5. **Run with explicit Python:**
   ```bash
   # In crontab:
   0 3 * * * /usr/bin/python3 /path/to/router_restart.py
   ```

## Issue: Login fails

### Checklist

1. **Verify credentials:**
   - Try logging in manually
   - Check for typos

2. **Check router connectivity:**
   ```bash
   ping 192.168.1.1
   curl http://192.168.1.1
   ```

3. **Check login form fields:**
   - The script looks for `<input name="username">` and `<input name="password">`
   - If your router uses different field names, update the script:
   ```python
   username_field = driver.find_element(By.ID, "user")  # or other selector
   password_field = driver.find_element(By.ID, "pwd")
   ```

4. **Check button selector:**
   - The script looks for `<button type="submit">`
   - If your router uses a different button, update:
   ```python
   login_button = driver.find_element(By.ID, "loginBtn")  # or other selector
   ```

## Issue: "Element not clickable" errors

### Root Cause
Page content may be loading dynamically after initial page load.

### Solution

Increase the timeout in `router_restart.py`:

```python
TIMEOUT = 20  # Increase from 10 to 20 seconds
```

## Debugging Steps

To debug specific issues:

1. **Create a test script** that prints HTML content:
   ```python
   driver.get("http://192.168.1.1")
   print(driver.page_source)
   ```

2. **Take a screenshot:**
   ```python
   driver.save_screenshot("debug_screenshot.png")
   ```

3. **Print all buttons found:**
   ```python
   buttons = driver.find_elements(By.TAG_NAME, "button")
   for btn in buttons:
       print(btn.text, btn.get_attribute("onclick"), btn.get_attribute("id"))
   ```

4. **Check actual HTML elements:**
   ```bash
   curl -u admin:Debianhusk2 http://192.168.1.1/admin | grep -i "restart\|reboot"
   ```

## Getting Help

When reporting issues, include:

1. **Router model:** (e.g., TP-Link WR841, Netgear R7000)
2. **Last 20 lines of log file:**
   ```bash
   tail -20 /var/log/router_restart.log
   ```
3. **Output from manual test run**
4. **Actual URL of restart page in your router**
5. **HTML of the restart button** (right-click → Inspect)
