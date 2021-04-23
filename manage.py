#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    argv = sys.argv
    index = None
    for ind,arg in enumerate(argv):
        if '=' in arg:
            key,val = arg.replace('--','').split("=")
            if key=='env':
                index = ind
                os.environ['ENV'] = val

    if index !=None:
        sys.argv = sys.argv[:index]+sys.argv[index+1:]
    
    if os.environ.get('ENV') == 'local':
        print('Using local settings')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.local')
    elif os.environ.get('ENV') == 'dev' or os.environ.get('ENV')==None:
        print('Using dev settings')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')
    elif os.environ.get('ENV') == 'deploy':
        print('Using deploy settings')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.deploy')
    else:
        raise Exception("env keyword is wrong, please pass local, dev or deploy")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
