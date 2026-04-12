#!/usr/bin/env python
"""
Network API Server - Auto-detect and run on network
এই script network এ সব PC থেকে access করা যায়
"""

import os
import sys
import socket
import subprocess
from pathlib import Path

def get_local_ip():
    """Get local network IP address"""
    try:
        # Connect to a public DNS to find local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def main():
    # Get project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Get local IP
    local_ip = get_local_ip()
    port = 7777
    
    print("\n" + "="*50)
    print("  Doctor Recommendation API Server")
    print("="*50)
    print(f"\n✓ Local IP: {local_ip}")
    print(f"✓ Port: {port}")
    print(f"\n📍 Network URL:")
    print(f"   http://{local_ip}:{port}")
    print(f"\n💻 Localhost URL:")
    print(f"   http://127.0.0.1:{port}")
    print(f"\n📚 API Endpoints:")
    print(f"   GET  /api/health")
    print(f"   GET  /api/options")
    print(f"   GET  /api/thanas/<district>")
    print(f"   POST /api/recommendations")
    print(f"\n{'='*50}\n")
    
    # Activate venv and run Django
    if sys.platform == "win32":
        # Windows
        venv_python = project_root / ".venv" / "Scripts" / "python.exe"
        subprocess.run([
            str(venv_python),
            "manage.py",
            "runserver",
            f"0.0.0.0:{port}"
        ])
    else:
        # Linux/Mac
        venv_python = project_root / ".venv" / "bin" / "python"
        subprocess.run([
            str(venv_python),
            "manage.py",
            "runserver",
            f"0.0.0.0:{port}"
        ])

if __name__ == "__main__":
    main()
