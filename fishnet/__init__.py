"""
MIT License

Copyright (c) 2020-2022 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import argparse
import sys


def cli():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fishnet.core.settings')

    try:
        from django.core.management import call_command
        from django.core.wsgi import get_wsgi_application

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    description = "Powerful advanced web platform for collaboration and automated penetration testing."

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-a', '--address', dest='address', help='Deploy Fishnet on custom address.')
    parser.add_argument('-m', '--migrate', action='store_true', help='Set up Fishnet database.')

    parser.add_argument('--db-username', dest='db_username', help='MySQL database username.')
    parser.add_argument('--db-password', dest='db_password', help='MySQL database password.')
    parser.add_argument('--db-host', dest='db_host', help='MySQL database host.')
    parser.add_argument('--db-port', dest='db_port', type=int, help='MySQL database password.')
    parser.add_argument('--db-name', dest='db_name', help='MySQL database name.')

    args = parser.parse_args()
    db_args = [
        args.db_username,
        args.db_password,
        args.db_host,
        args.db_port,
        args.db_name
    ]

    if all(db_args):
        os.environ.setdefault('DB_USERNAME', args.db_username)
        os.environ.setdefault('DB_PASSWORD', args.db_password)
        os.environ.setdefault('DB_HOST', args.db_host)
        os.environ.setdefault('DB_PORT', str(args.db_port))
        os.environ.setdefault('DB_NAME', args.db_name)

        get_wsgi_application()

        if args.migrate:
            call_command('migrate')

        if args.address:
            call_command('runserver', args.address)
            sys.exit(0)

        call_command('runserver', '0.0.0.0:7777')
    else:
        parser.print_help()
        sys.exit(1)
