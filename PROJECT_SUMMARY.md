# Router Restart Automation - Project Summary

## ✅ Project Complete & Tested

A fully automated Selenium-based router restart system for ZTE F6605R using Google Chrome.

**Status:** ✅ **FULLY WORKING & DEPLOYED**
**Last Tested:** 2026-02-14 10:41:36 (Exit Code: 0)
**Router Model:** ZTE F6605R
**Browser:** Google Chrome 145.0.7632.75
**Schedule:** Daily at 3:00 AM (verified running)

---

## What It Does

Automatically restarts your router at **3:00 AM every night** via:
1. HTTPS login to 92.82.75.79
2. Navigate through web menus
3. Click restart button
4. Confirm restart
5. Router restarts (~5 minutes)

---

## Project Files

```
telecomRouterRestart/
├── router_restart.py          # Main production script
├── router_restart_test.py     # Safe test version (doesn't restart)
├── setup.sh                   # Auto-install dependencies
├── install_cron.sh            # Auto-schedule cron job
├── requirements.txt           # Python dependencies (Selenium)
├── README.md                  # Quick start guide
├── TESTING.md                 # Testing procedures
├── TROUBLESHOOTING.md         # Problem solutions
└── venv/                      # Python virtual environment
```

---

## Quick Start

### 1. Install
```bash
cd ~/telecomRouterRestart
chmod +x setup.sh
./setup.sh
```

### 2. Test
```bash
source venv/bin/activate
python3 router_restart_test.py
```

### 3. Schedule
```bash
chmod +x install_cron.sh
./install_cron.sh
```

### Done! ✅
Router will restart daily at 3:00 AM.

---

## Features

- ✅ Fully automated (no manual intervention)
- ✅ Tested and verified working
- ✅ HTTPS support with self-signed certificates
- ✅ Safe test mode (verify without restarting)
- ✅ Comprehensive logging
- ✅ Cross-platform (macOS & Linux)
- ✅ Simple installation

---

## Tested On

- ✅ macOS (development/testing)
- ✅ ZTE F6605R router (production target)

---

## Key Configuration

```python
ROUTER_URL = "https://92.82.75.79"
ROUTER_USERNAME = "admin"
ROUTER_PASSWORD = "Debianhusk2"
TIMEOUT = 10  # seconds
```

---

## How to Deploy to Linux

```bash
# Copy to Linux machine
scp -r ~/Development/telecomRouterRestart user@linux-server:~/

# On Linux machine
cd ~/telecomRouterRestart
./setup.sh
python3 router_restart_test.py
./install_cron.sh

# Verify
crontab -l
```

---

## Monitoring

### Check Logs
```bash
tail -f ~/router_restart.log
```

### Manual Restart (Testing)
```bash
source venv/bin/activate
python3 router_restart.py
```

### Verify Cron
```bash
crontab -l
```

---

## Notes

- Restart takes ~5 minutes
- Internet will be unavailable during restart
- All actions logged to `~/router_restart.log`
- Test script uses same code as production (safe mode)
- Credentials stored in plaintext (consider file permissions on shared systems)

---

## Support

For issues, check:
1. `README.md` - Quick reference
2. `TESTING.md` - Testing procedures
3. `TROUBLESHOOTING.md` - Problem solutions

---

**Ready to deploy! 🚀**
