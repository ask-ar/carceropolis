var map = null
var statesLayerGroup = null


function displayShortInfo(unidade) {
  $('#unidade-short-info').text(unidade.nome_unidade)
}

function stripDiacritics(str) {
  // TODO: polyfill normalize? ignore?
  return str.normalize("NFKD").replace(/[\u0300-\u036F]/g, '').toLowerCase()
}

// Compares strings converting them to "canonical" form (replace dicritics)
function unidadeMatchesFilter(unidade, filter) {
  // TODO: add cidade and estado to filter check
  let content = unidade.nome_unidade + " " + unidade.uf + " ";
  content += unidade.municipio + " " + unidade.nome_logradouro + " ";
  content = stripDiacritics(content)
  if (content.indexOf(stripDiacritics(filter)) > -1) return true
  else return false
}

$(window).ready(function(){

  const delimiters = ['[[', ']]']

  Vue.component('perc-bar', {
    delimiters: delimiters,
    template: '#perc-bar-template',
    props: {
      // Percentual value
      'value': Number,
      // Label text
      'label': [String, Number],
      // Bar color
      'color': String,
      // If label should be positioned inside or outside the bar
      // Should be "inside", "outside" or a number
      // if a number, will position label inside if value > number
      // this is usefull for auto position based on bar size
      'labelPosition': {
        type: [String, Number],
        default: 30,
      }
    },
    computed: {
      labelInside: function () {
        if (this.labelPosition === 'inside') return true
        if (this.labelPosition === 'outside') return false
        if (this.value > this.labelPosition) return true
        return false
      }
    }
  })

  Vue.component('age-pyramid', {
    delimiters: delimiters,
    template: '#age-pyramid-template',
    props: ['data'],
  })

  Vue.component('detailed-info', {
    delimiters: delimiters,
    template: '#detailed-info-template',
    props: ['unidade'],
  })

  new Vue({
    delimiters: delimiters,
    el: '#map-vue-app',
    data: {
      // string used in map filtering
      filterStr: '',
      // selected unidade
      unidade: null,
      // if should show complete info about selected unidade
      showCompleteInfo: false,
    },
    methods: {
      createMap: function () {
        map = L.map('map').setView([-15, -50], 4)
          L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', {
          maxZoom: 18,
          attribution: 'Map tiles by <a href="https://carto.com">Carto</a>, ' +
            'under <a href="https://creativecommons.org/licenses/by/3.0/">CC BY 3.0</a>. ' +
            'Data by <a href="https://openstreetmap.org">OpenStreetMap</a>, under ODbL. ' +
            'Icon by <a href="http://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">Flaticon</a> under <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a>.'
        }).addTo(map)

        statesLayerGroup = L.featureGroup().addTo(map).on('click', (marker) => this.unidade = marker.layer.unidade)

        this.plotMap()
      },
      plotMap: function () {
        var filter = this.filterStr
        var multiplier = 0.5;
        var customIcon = L.icon({
          iconUrl: '/static/images/map/marker-icon.png',
          // shadowUrl: '/static/images/map/marker-shadow.png',
          iconSize: [32, 30],
          iconAnchor: [16, 15],
          // popupAnchor: [1, -34],
          // tooltipAnchor: [16, -28],
          // shadowSize: [68, 32]
        })

        statesLayerGroup.clearLayers()
        $.each(states, function (uf, unidades) {
          var stateLayer = L.markerClusterGroup({
            showCoverageOnHover: false,
            // polygonOptions: {
            //   fillColor: 'grey',
            //   color: '#1b2557',
            //   weight: 0.0,
            //   opacity: 0,
            //   fillOpacity: 0.5
            // }
          })
          var i = 0
          var markers = []
          for (let unidade of unidades) {
            if (filter && !unidadeMatchesFilter(unidade, filter)) continue
            var marker = L.marker([unidade.lat, unidade.lon], {icon: customIcon})
            marker.unidade = unidade
            markers.push(marker)
          }
          stateLayer.addLayers(markers)
          statesLayerGroup.addLayer(stateLayer)
        })
      },
      // Format used by mailto links
      formatMailto: function (email) {
        return 'mailto:' + email
      },
      // Format phone numbers with DDD
      formatFone: function (fone, ddd) {
        var foneStr = fone.toString()
        return '(' + ddd + ') ' + foneStr.slice(0,4) + ' ' + foneStr.slice(4)
      },
      formatAddress: function (unidade) {
        return unidade.tipo_logradouro +
          ' ' + unidade.nome_logradouro +
          (unidade.numero ? ', ' + unidade.numero : '') +
          (unidade.complemento ? ', ' + unidade.complemento : '') +
          ' - CEP: ' + unidade.cep.slice(0,-3) + '-' + unidade.cep.slice(-3) +
          ' - ' + unidade.municipio +
          ' - ' + unidade.uf
      },
      formatBool: value => value ? '✓' : '✘'
    },
    watch: {
      filterStr: function (a, b) {
        this.plotMap()
      }
    },
    mounted: function () {
      this.createMap()
    }
  })
})
