// Gender timeline chart
$(function () {
    Highcharts.chart('escolaridade-timeline-chart', {
      chart: {
        width: 300
      },
      title: {
          text: '',
          x: -20 //center
      },
      subtitle: {
          text: '',
          x: -20
      },
      xAxis: {
          categories: ['Jun/2014', 'Dez/2014']
      },
      yAxis: {
          title: {
              text: 'População total'
          },
          plotLines: [{
              value: 0,
              width: 1,
              color: '#808080'
          }]
      },
      tooltip: {
          valueSuffix: ''
      },
      legend: {
          layout: 'horizontal',
          align: 'center',
          verticalAlign: 'bottom',
          borderWidth: 0
      },
      series: [{
          name: 'Analfabeta',
          data: [49,49]
      },{
          name: 'Alfabetizada (s/ cursos regulares)',
          data: [0,0]
      },{
          name: 'Ensino Fundamental Incompleto',
          data: [119,107]
      },{
          name: 'Ensino Fundamental Completo',
          data: [20,20]
      },{
          name: 'Ensino Médio Incompleto',
          data: [15,15]
      },{
          name: 'Ensino Médio Completo',
          data: [17,17]
      },{
          name: 'Ensino Superior Incompleto',
          data: [3,0]
      },{
          name: 'Ensino Superior Completo',
          data: [1,0]
      },{
          name: 'Ensino acima do Superior Completo',
          data: [0,0]
      },{
          name: 'Não informado ',
          data: [0,0]
      }]
    });
});
