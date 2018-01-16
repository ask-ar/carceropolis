var map = null
var mapData = window.map_data
var statesLayerGroup = null

function createMap () {
  map = L.map('map').setView([-15, -50], 4)
	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
			'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="http://mapbox.com">Mapbox</a>',
		id: 'mapbox.streets'
	}).addTo(map)
  statesLayerGroup = L.featureGroup().addTo(map).on('click', function(marker) {
    displayShortInfo(marker.layer.unidade)
  })

  plotMap()
}

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

function plotMap(filter) {
  statesLayerGroup.clearLayers()
  $.each(mapData, function (uf, unidades) {
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
    // map.addLayer(stateLayer)
  })
}

function applyFilter() {
  var filterStr = stripDiacritics($('#filterInput').val())
  plotMap(filterStr)
}

$(window).ready(function(){
  createMap()
})
