import shelve
import geocoder
from django.core.management.base import BaseCommand
from carceropolis.models import UnidadePrisional
from cidades.models import STATE_CHOICES


# geolocating API usage order
APIS = ['osm', 'google']

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
                print('')

                location_attrs = [str(attr).strip() for attr in (
                    unidade.tipo_logradouro + ' ' + unidade.nome_logradouro,
                    # unidade.nome_logradouro,
                    unidade.numero if isinstance(unidade.numero, int) else '',
                    unidade.complemento,
                    unidade.municipio.nome,
                    uf_estado[unidade.uf],
                    'Brasil'
                ) if attr]
                location_str = ', '.join(location_attrs)

                # use all location attrs
                cached_info = self.get_location_any_api(cache, location_str)
                if not cached_info:
                    # use only city
                    location_str = ', '.join(location_attrs[-3:])
                    cached_info = self.get_location_any_api(
                        cache, location_str)

                if cached_info:
                    # Store only if found address
                    unidade.lat, unidade.lon = cached_info
                    unidade.save()

    def get_location_any_api(self, cache, location_str):
        '''Try multiple geocoding APIs'''
        for api_name in APIS:
            cached_info = self.get_location_single_api(
                cache, location_str, api_name)
            if cached_info:
                break
        return cached_info

    def get_location_single_api(self, cache, location_str, api_name):
        '''Get data about a location. Fisrt try the cache, then the api.'''
        # Cache can have:
        # None: didn't try to geolocate
        # False: tried but not found
        # [lat, lon]: found!
        self.stdout.write(location_str)
        cache_location = cache.get(location_str, {})
        cached_info = cache_location.get(api_name)
        if cached_info is None:
            # query API
            api = getattr(geocoder, api_name)
            response = api(location_str)
            print(api_name, '>', response.latlng)
            if response.latlng:
                # Found address
                cached_info = response.latlng
            else:
                # Not found
                cached_info = False
            cache_location[api_name] = cached_info
            cache[location_str] = cache_location
            cache.sync()
        else:
            self.stdout.write(api_name + '> On cache. value: %s' % cached_info)

        return cached_info
