"""
Django Management Command: runnetwork
সার্ভার network এ চালানোর জন্য
"""

import socket
from django.core.management.commands.runserver import Command as RunserverCommand
from django.core.management.base import CommandError


class Command(RunserverCommand):
    """
    Usage:
        python manage.py runnetwork         # Auto port 7777
        python manage.py runnetwork 8000    # Custom port
    """

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            'port',
            nargs='?',
            default='7777',
            type=int,
            help='Port number (default: 7777)'
        )

    def get_local_ip(self):
        """Get local network IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def handle(self, *args, **options):
        local_ip = self.get_local_ip()
        port = options.get('port', 7777)

        print("\n" + "="*60)
        print("  🏥 Doctor Recommendation API Server")
        print("="*60)
        print(f"\n✓ Local Network IP: {local_ip}")
        print(f"✓ Port: {port}")
        print(f"\n📍 Access URLs:")
        print(f"   Network: http://{local_ip}:{port}")
        print(f"   Localhost: http://127.0.0.1:{port}")
        print(f"\n📚 API Endpoints:")
        print(f"   GET  /api/health")
        print(f"   GET  /api/options")
        print(f"   GET  /api/thanas/<district>")
        print(f"   POST /api/recommendations")
        print(f"\n🌐 Web UI: http://{local_ip}:{port}/")
        print(f"\n{'='*60}\n")

        # Set the address and port
        options['addrport'] = f'0.0.0.0:{port}'

        # Call parent's handle method
        super().handle(*args, **options)
