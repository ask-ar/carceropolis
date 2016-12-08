var charts = [];
// Gender timeline chart
$(function () {
    width = $('#gender-timeline-chart').width();
    chart = Highcharts.chart('gender-timeline-chart', {
      chart: {
        width: width
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
          name: 'Homens',
          data: []
      }, {
          name: 'Mulheres',
          data: [224, 208]
      }]
    });
    charts.push(chart);

    chart = Highcharts.chart('race-timeline-chart', {
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
            valueSuffix: '°C'
        },
        legend: {
            layout: 'horizontal',
            align: 'center',
            verticalAlign: 'bottom',
            borderWidth: 0
        },
        series: [{
         name: 'Branca',
         data: [30, 32]
        }, {
         name: 'Negra',
         data: [34, 38]
        }, {
         name: 'Parda',
         data: [160, 138]
        }, {
         name: 'Amarela',
         data: [0, 0]
        }, {
         name: 'Indígena',
         data: [0, 0]
        }, {
         name: 'Outras',
         data: [0, 0]
        }, {
         name: 'Não Informado',
         data: [0, 0]
        }]
    });

    charts.push(chart);

    // BAR CHARTS
    chart = Highcharts.chart('gender-timeline-bar-chart', {
      chart: {
        width: 300,
        type: 'column'
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
          name: 'Homens',
          data: []
      }, {
          name: 'Mulheres',
          data: [224, 208]
      }]
    });

    charts.push(chart);

    chart = Highcharts.chart('race-timeline-bar-chart', {
      chart: {
        width: 300,
        type: 'column'
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
            valueSuffix: '°C'
        },
        legend: {
            layout: 'horizontal',
            align: 'center',
            verticalAlign: 'bottom',
            borderWidth: 0
        },
        series: [{
         name: 'Branca',
         data: [30, 32]
        }, {
         name: 'Negra',
         data: [34, 38]
        }, {
         name: 'Parda',
         data: [160, 138]
        }, {
         name: 'Amarela',
         data: [0, 0]
        }, {
         name: 'Indígena',
         data: [0, 0]
        }, {
         name: 'Outras',
         data: [0, 0]
        }, {
         name: 'Não Informado',
         data: [0, 0]
        }]
    });
    charts.push(chart);
});
