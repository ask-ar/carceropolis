import shelve
import geocoder
from django.core.management.base import BaseCommand
from carceropolis.models import UnidadePrisional
from cidades.models import STATE_CHOICES


API_NAME = 'osm'
api = getattr(geocoder, API_NAME)
uf_estado = dict(STATE_CHOICES)


class Command(BaseCommand):
    help = 'Geolocates UnidadePrisional table'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            help='Geolocates even already geolocated',
        )

    def handle(self, *args, **options):
        objs = UnidadePrisional.objects.select_related('municipio')
        iterator = objs.all() if options['all'] else objs.filter(lat=None)
        with shelve.open('geo.cache', writeback=True) as cache:
            for unidade in iterator:
                location_attrs = (str(attr) for attr in (
                    # # unidade.tipo_logradouro + ' ' + unidade.nome_logradouro,
                    # unidade.nome_logradouro,
                    # unidade.numero if isinstance(unidade.numero, int) else '',
                    # unidade.complemento,
                    unidade.municipio.nome,
                    uf_estado[unidade.uf],
                    'Brasil'
                ) if attr)
                location_str = ', '.join(location_attrs)
                self.stdout.write(location_str)

                # Cache can have:
                # None: didn't try to geolocate
                # False: tried but not found
                # [lat, lon]: found!

                cache_location = cache.get(location_str, {})
                cached_info = cache_location.get(API_NAME)
                if cached_info is None:
                    # query API
                    response = api(location_str)
                    print(response.latlng)
                    if response.latlng:
                        # Found address
                        cached_info = response.latlng
                    else:
                        # Not found
                        cached_info = False
                    cache_location[API_NAME] = cached_info
                    cache[location_str] = cache_location
                    cache.sync()
                else:
                    self.stdout.write('On cache. value: %s' % cached_info)

                if cached_info:
                    # Store only if found address
                    unidade.lat, unidade.lon = cached_info
                    unidade.save()
