import shelve

import geocoder
import pandas as pd

api_name = 'osm'
api = getattr(geocoder, api_name)
df = pd.read_excel('BD_UNIDADES_FINAL_checado.xlsx', sheetname='tratamento')
df = df.fillna('')

markers = {}

with shelve.open('cache', writeback=True) as db:
    for row in df.itertuples():

        location_attrs = (str(attr) for attr in (
            # # row.tipo_logradouro + ' ' + row.nome_logradouro,
            # row.nome_logradouro,
            # row.numero if isinstance(row.numero, int) else '',
            # row.complemento,
            row.municipio,
            row.uf,
            'Brazil'
        ) if attr)
        location_str = ', '.join(location_attrs)
        print(location_str)

        cache_location = db.get(location_str, {})
        if cache_location.get(api_name) is None:
            # query API
            response = api(location_str)
            print(response.latlng)

            if response.latlng:
                stored_data = response.latlng
            else:
                stored_data = False

            cache_location[api_name] = stored_data
            db[location_str] = cache_location
            db.sync()
        else:
            print('on cache')

        try:
            lat, lon = cache_location.get(api_name)
            state = markers.get(row.uf, [])
            markers[row.uf] = state
            state.append({
                'lat': lat,
                'lon': lon,
                'nome_unidade': row.nome_unidade,
            })
        except TypeError:
            pass

import json
with open('unidades.json', 'w') as f:
    json.dump(markers, f)
