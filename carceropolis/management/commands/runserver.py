import sys

from mezzanine.core.management.commands.runserver import Command as BaseRunserverCommand

from carceropolis import dashboard


class Command(BaseRunserverCommand):

    def run(self, **options):
        try:
            super(Command, self).run(**options)
        except (KeyboardInterrupt, SystemExit):
            dashboard.stop_server()
            sys.exit(3)
        # TODO: This is run multiple times before and after the dashboard
        # started.
        dashboard.stop_server()

    def inner_run(self, **options):
        dashboard.start_server()
        super(Command, self).inner_run(**options)
