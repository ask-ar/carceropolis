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
  if (stripDiacritics(unidade.nome_unidade).indexOf(filter) > -1) return true
  else return false
}



$(window).ready(function(){

  var delimiters = ['[[', ']]']

  Vue.component('perc-bar', {
    delimiters: delimiters,
    template: '#perc-bar-template',
    props: {
      'value': Number,
      'label': [String, Number],
      'color': String,
      'labelPosition': {
        // "inside", "outside" or number
        // if is a number, will position label inside if value > number
        type: [String, Number],
        default: 20,
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
            'Data by <a href="https://openstreetmap.org">OpenStreetMap</a>, under ODbL.'
	      }).addTo(map)
        var self = this
        statesLayerGroup = L.featureGroup().addTo(map).on('click', function(marker) {
          self.unidade = marker.layer.unidade
        })

        this.plotMap()
      },
      plotMap: function () {
        var filter = this.filterStr
        statesLayerGroup.clearLayers()
        $.each(states, function (uf, unidades) {
          var stateLayer = L.markerClusterGroup()
          var i = 0
          var markers = []
          for (i = 0; i < unidades.length; ++i) {
            var unidade = unidades[i]
            if (filter && !unidadeMatchesFilter(unidade, filter)) continue
            var marker = L.marker([unidade.lat, unidade.lon])
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
      formatBool: function (value) {
        if (value) return '✓'
        else return '✘'
      }
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
