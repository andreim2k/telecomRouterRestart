# Testing Guide

## Before Scheduling - IMPORTANT!

**DO NOT schedule the script to run at 3 AM until you've tested it thoroughly.**

Use `router_restart_test.py` to verify everything works without actually restarting the router.

## Step 1: Setup (Run on Linux Machine)

### 1.1 Install Dependencies

```bash
sudo apt-get update
sudo apt-get install -y python3 pip3 chromium-browser chromium-chromedriver
```

### 1.2 Create Virtual Environment

```bash
cd /path/to/telecomRouterRestart
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### 1.3 Make Scripts Executable

```bash
chmod +x router_restart.py
chmod +x router_restart_test.py
chmod +x setup.sh
chmod +x install_cron.sh
```

## Step 2: Test with Dry-Run Script

### Run the test script

This script goes through all steps EXCEPT confirming the restart:

```bash
python3 router_restart_test.py
```

### Expected Output

```
============================================================
TEST MODE: Router Restart Script Test
This will verify all steps EXCEPT the final confirmation
============================================================
[timestamp] - INFO - Accessing router at http://192.168.1.1
[timestamp] - INFO - Login submitted, waiting for page load...
[timestamp] - INFO - ✓ Successfully logged in
[timestamp] - INFO - Navigating to restart page...
[timestamp] - INFO -   Trying: http://192.168.1.1/admin/restart
[timestamp] - INFO - ✓ Found restart page at http://192.168.1.1/admin/restart
[timestamp] - INFO - Looking for restart button...
[timestamp] - INFO - ✓ Found restart button: XPath: Repornire text
[timestamp] - INFO -   Button text: Repornire
[timestamp] - INFO -   Button tag: button
[timestamp] - INFO - ✓ [TEST MODE] Found button but NOT clicking (test mode)
[timestamp] - INFO - Looking for confirmation dialog...
[timestamp] - INFO - ✓ Found 1 OK button(s)
[timestamp] - INFO -   Button 1: 'OK'
[timestamp] - INFO - ✓ [TEST MODE] Confirmation dialog found but NOT clicking OK
============================================================
[timestamp] - INFO - ✓ TEST SUCCESSFUL - All steps verified!
[timestamp] - INFO - ✓ Script is ready to be scheduled
============================================================
```

### If Test Fails

Check the troubleshooting section below for your specific error.

## Step 3: Real Test (Optional - Actually Restart)

Once test script passes, you can run the real script:

```bash
python3 router_restart.py
```

⚠️ **WARNING**: This will actually restart your router. The restart typically takes 5 minutes.

Expected behavior:
- Script logs indicate restart initiated
- Router becomes unavailable
- After ~5 minutes, router comes back online

## Step 4: Schedule with Cron

Once fully tested:

```bash
./install_cron.sh
```

Or manually:

```bash
crontab -e
# Add this line:
0 3 * * * /full/path/to/router_restart.py
```

Verify:
```bash
crontab -l
```

## Troubleshooting During Testing

### Issue: "ChromeDriver version mismatch"

```
Error: "ChromeDriver version must match Chrome version"
```

**Fix:**
```bash
google-chrome --version
chromedriver --version

# If versions don't match, update ChromeDriver
sudo apt-get install --only-upgrade chromium-chromedriver
```

### Issue: "Connection refused" or "Chrome failed to start"

```
Error: "Chrome process crashed or could not be started"
```

**Fix - Check Chrome installation:**
```bash
which google-chrome
# or
which chromium-browser

# Install if missing:
sudo apt-get install chromium-browser
```

### Issue: "Cannot connect to localhost:9515"

```
Error: "Cannot connect to localhost:9515"
```

**Fix - ChromeDriver missing or not in PATH:**
```bash
which chromedriver

# If not found, install:
sudo apt-get install chromium-chromedriver

# Or install manually:
sudo cp /usr/lib/chromium-browser/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

### Issue: "Login failed" - Login form not found

```
[timestamp] - ERROR - ✗ Login failed: no such element
```

**Cause**: Router login form has different field names.

**Fix**:
1. Open browser and go to `http://192.168.1.1`
2. Right-click on username field → Inspect
3. Look for the `name=` attribute (e.g., `user` instead of `username`)
4. Update `router_restart.py` line 65-67:
   ```python
   username_field = driver.find_element(By.NAME, "user")  # Change from "username"
   password_field = driver.find_element(By.NAME, "pwd")   # Change from "password"
   ```

### Issue: "Could not find restart button"

```
[timestamp] - ERROR - ✗ Could not find restart button
```

**Cause**: Restart page has different button text or structure.

**Fix**:
1. Go to your router manually
2. Navigate to the restart page
3. Right-click on restart button → Inspect
4. Note the exact text or attributes
5. If button shows `onclick="doRestart()"`, you might need:
   ```python
   button = driver.find_element(By.XPATH, "//*[@onclick='doRestart()']")
   button.click()
   ```

### Issue: "Could not find restart page"

```
[timestamp] - WARNING - ⚠ Could not find restart page at standard URLs
```

**Fix**:
1. Log into your router manually
2. Find the restart/reboot page
3. Note the URL (e.g., `http://192.168.1.1/system/settings/reboot`)
4. Update `router_restart.py` line 109:
   ```python
   restart_urls = [
       f"{ROUTER_URL}/system/settings/reboot",  # Add your actual URL
       # ... keep other URLs ...
   ]
   ```

### Issue: Timeout during login

```
Error: "TimeoutException: Message: Timeout waiting for element"
```

**Fix - Increase timeout**:

Edit `router_restart.py` line 20:
```python
TIMEOUT = 20  # Increase from 10
```

### Issue: Test script works but real script doesn't

**Cause**: Usually permissions or environment differences.

**Fix**:
1. Ensure you run real script with same user/permissions:
   ```bash
   python3 router_restart.py
   ```

2. If running from cron, ensure paths are absolute:
   ```bash
   0 3 * * * /usr/bin/python3 /full/path/to/router_restart.py
   ```

## Logging

### View Test Logs (console only)

Test script logs to console only. You'll see output directly.

### View Production Logs (once scheduled)

```bash
# Watch logs in real-time
tail -f /var/log/router_restart.log

# View last 50 lines
tail -50 /var/log/router_restart.log

# Search for errors
grep ERROR /var/log/router_restart.log
```

## Testing Checklist

- [ ] **Setup**: Dependencies installed, virtual environment created
- [ ] **Chrome**: `google-chrome --version` or `chromium-browser --version` works
- [ ] **ChromeDriver**: `chromedriver --version` works and matches Chrome version
- [ ] **Network**: `ping 192.168.1.1` succeeds
- [ ] **Credentials**: Can log in manually with admin/Debianhusk2
- [ ] **Test Script**: `python3 router_restart_test.py` completes successfully
- [ ] **Test Script Output**: Shows "✓ TEST SUCCESSFUL"
- [ ] **Real Script**: `python3 router_restart.py` successfully restarts router (optional)
- [ ] **Cron**: `crontab -l` shows the restart job
- [ ] **Logs**: `/var/log/router_restart.log` exists and is writable

## Next Steps

Once all tests pass:

1. **Real execution test** (optional):
   ```bash
   python3 router_restart.py
   ```
   Wait 5 minutes for router to come back online.

2. **Schedule with cron**:
   ```bash
   ./install_cron.sh
   ```

3. **Monitor first run**:
   Tomorrow at 3 AM, check:
   ```bash
   tail -f /var/log/router_restart.log
   ```

4. **Set phone reminder** (optional):
   Set a reminder for the next morning to verify router restarted successfully.
