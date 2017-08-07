from mezzanine.core.management.commands.runserver import Command as BaseRunserverCommand
from carceropolis import dashboard


class Command(BaseRunserverCommand):

    def run(self, **options):
        dashboard.start_server()
        super(Command, self).run(**options)
