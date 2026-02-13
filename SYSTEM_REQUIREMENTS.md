# System Requirements

Complete list of all dependencies required to run the Router Restart Automation.

## Python Version
- **Python 3.7+** (tested on 3.12.3)

## System Packages (Linux/Ubuntu)

### Browser and WebDriver
```bash
chromium-browser       # 2:1snap1-0ubuntu2 (Transitional package)
chromium-chromedriver  # 2:1snap1-0ubuntu2 (WebDriver for Chromium)
```

### Python Development Tools
```bash
python3-pip           # 24.0+dfsg-1ubuntu1.3 (Python package installer)
python3-dev           # 3.12.3-0ubuntu2.1 (Python header files and static library)
libpython3-dev        # 3.12.3-0ubuntu2.1 (Python headers - dependency of python3-dev)
```

### Build Dependencies (installed as part of python3-dev)
```bash
libexpat1-dev         # XML parser library
libpython3.12-dev     # Python 3.12 specific headers
python3.12-dev        # Python 3.12 development files
python3-wheel         # Python wheel package format
zlib1g-dev            # Compression library
```

### Additional System Dependencies
```bash
javascript-common     # Common JavaScript files
libjs-jquery          # jQuery JavaScript library
libjs-sphinxdoc       # Sphinx documentation JavaScript
libjs-underscore      # Underscore.js library
```

## Python Packages (pip)

All packages are listed in `requirements.txt`:

### Core
- **selenium==4.15.2** - Browser automation framework

### Selenium WebDriver Dependencies
- **attrs==25.4.0** - Python class decorator for attribute handling
- **certifi==2026.1.4** - SSL certificates for HTTPS
- **h11==0.16.0** - HTTP/1.1 protocol implementation
- **idna==3.11** - International domain names
- **outcome==1.3.0.post0** - Capture and re-raise exceptions
- **PySocks==1.7.1** - SOCKS proxy support
- **sniffio==1.3.1** - Async library detection
- **sortedcontainers==2.4.0** - Sorted container implementations
- **trio==0.32.0** - Async I/O library
- **trio-websocket==0.12.2** - WebSocket support for Trio
- **urllib3==2.6.3** - HTTP client library (SOCKS support)
- **wsproto==1.3.2** - WebSocket protocol parser

## Installation Commands

### Quick Installation (Automated)
```bash
cd telecomRouterRestart
chmod +x setup.sh
./setup.sh
```

### Manual Installation (Step-by-Step)

1. **Update package lists:**
   ```bash
   sudo apt-get update
   ```

2. **Install system packages:**
   ```bash
   sudo apt-get install -y \
     chromium-browser \
     chromium-chromedriver \
     python3-pip \
     python3-dev
   ```

3. **Create Python virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Python packages:**
   ```bash
   pip3 install -r requirements.txt
   ```

## Verification

### Check Python
```bash
python3 --version
pip3 --version
```

### Check Chromium
```bash
which chromium-browser
which chromedriver
```

### Check Virtual Environment
```bash
source venv/bin/activate
python3 -c "import selenium; print(selenium.__version__)"
```

Expected output: `4.15.2`

## Total Disk Space Required

- Chromium: ~300 MB
- ChromeDriver: ~2 MB
- Python dependencies: ~50 MB
- Virtual environment: ~100 MB
- **Total: ~450 MB**

## macOS Alternative

On macOS, use Homebrew:
```bash
brew install chromium chromedriver
brew install python3
pip3 install -r requirements.txt
```

## Notes

- All dependencies are pinned to specific versions for reproducibility
- The virtual environment (`venv/`) isolates dependencies from system Python
- ChromeDriver version must match Chromium browser version
- HTTPS support requires valid SSL certificates (handled by `certifi`)
