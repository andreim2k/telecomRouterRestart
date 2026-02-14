# Router Restart Automation

Automatically restart a ZTE F6605R router every night at 3 AM using Selenium and Google Chrome.

**Status:** ✅ **FULLY WORKING** - Router restarts daily at 3:00 AM

## Quick Start

### Prerequisites
- Linux machine with Python 3.7+
- Google Chrome (automatically installed)
- Network access to router at 92.82.75.79

### Installation (Complete Setup)

```bash
cd telecomRouterRestart
chmod +x setup.sh
./setup.sh
chmod +x install_cron.sh
./install_cron.sh
```

Done! Your router will restart automatically **every day at 3:00 AM**.

### Verify Installation

```bash
# Check cron is scheduled
crontab -l

# View execution logs
tail -f ~/router_restart.log

# Check for successful restarts
grep "Router restart initiated" ~/router_restart.log
```

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

### Router Not Restarting?

1. **Check cron job exists:**
   ```bash
   crontab -l
   ```
   Should show: `0 3 * * * /path/to/router_restart_cron.sh`

2. **Verify Google Chrome is installed:**
   ```bash
   which google-chrome
   google-chrome --version
   ```

3. **Check execution logs:**
   ```bash
   tail -50 ~/router_restart.log
   ```

4. **Verify router is accessible:**
   ```bash
   ping 92.82.75.79
   ```

5. **Check credentials:**
   - Router URL: https://92.82.75.79
   - Username: admin
   - Password: Debianhusk2 (edit `router_restart.py` if changed)

---

## Project Files

| File | Purpose |
|------|---------|
| `router_restart.py` | Main production script - restarts router |
| `router_restart_test.py` | Safe test version (verifies setup without restarting) |
| `router_restart_cron.sh` | Cron wrapper - activates venv and runs script |
| `setup.sh` | Auto-install Python dependencies |
| `install_cron.sh` | Auto-schedule cron job for 3 AM daily |
| `requirements.txt` | Python package dependencies (13 packages) |
| `SYSTEM_REQUIREMENTS.md` | Complete system/browser requirements |
| `CRON_SETUP_STATUS.md` | Detailed cron setup and troubleshooting |

## Important Notes

- **Browser:** Google Chrome (installed automatically via `setup.sh`)
- **Schedule:** Daily at 3:00 AM (0 3 * * *)
- **Downtime:** ~5 minutes during restart
- **Logging:** `~/router_restart.log` (created automatically)
- **Manual trigger:** `/home/andrei/telecomRouterRestart/router_restart_cron.sh`
- **Tested and verified:** Working end-to-end ✅

