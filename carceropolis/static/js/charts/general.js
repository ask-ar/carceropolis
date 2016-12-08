
$(window).resize(function(){
  for chart in charts{
    height = chart.height
    width = $("#chartRow").width() / 2
    chart.setSize(width, height, doAnimation = true);
  }
});
