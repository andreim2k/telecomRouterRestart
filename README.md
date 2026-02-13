# Router Restart Automation

Automatically restart a ZTE F6605R router every night at 3 AM using Selenium.

## Quick Start

### Prerequisites
- Linux machine with Python 3.7+
- Network access to router at 192.168.1.1

### Installation

```bash
cd telecomRouterRestart
chmod +x setup.sh
./setup.sh
```

### Test It Works

```bash
source venv/bin/activate
python3 router_restart_test.py
```

Should output: `✓ TEST SUCCESSFUL - All steps verified!`

### Schedule to Run Daily

```bash
chmod +x install_cron.sh
./install_cron.sh
```

Done! Router will restart daily at **3:00 AM**.

---

## Manual Execution

```bash
source venv/bin/activate
python3 router_restart.py
```

⚠️ **WARNING**: This will actually restart the router (~5 minutes downtime)

---

## Verify It's Working

### Check Cron Job

```bash
crontab -l
```

### View Logs

```bash
tail -f ~/router_restart.log
```

---

## Configuration

Edit `router_restart.py` to modify:

- `ROUTER_URL`: Router IP/hostname
- `ROUTER_USERNAME`: Login username
- `ROUTER_PASSWORD`: Login password
- `TIMEOUT`: Selenium timeout in seconds

---

## Router Configuration

- **Model**: ZTE F6605R
- **Protocol**: HTTPS
- **Login Fields**: `Frm_Username` & `Frm_Password`
- **Restart Button**: "Repornește" (ID: `Btn_restart`)

---

## Troubleshooting

### Chrome/ChromeDriver Issues

```bash
which google-chrome  # or chromium-browser
which chromedriver

# Install if missing
sudo apt-get install chromium-browser chromium-chromedriver
```

### Permission Denied on /var/log

On macOS, logs are saved to `~/router_restart.log` instead.

### Script Fails to Run

1. Verify router is online: `ping 192.168.1.1`
2. Check credentials: admin / Debianhusk2
3. View logs: `tail ~/router_restart.log`

---

## Files

- `router_restart.py` - Main production script
- `router_restart_test.py` - Safe test version (doesn't restart)
- `setup.sh` - Auto-install dependencies
- `install_cron.sh` - Auto-schedule cron job
- `requirements.txt` - Python packages

---

## Notes

- Router restart takes ~5 minutes
- During restart, internet will be unavailable
- All actions are logged to `~/router_restart.log` (or `/var/log/router_restart.log` on Linux)
- Cron job runs with full paths, no manual activation needed

