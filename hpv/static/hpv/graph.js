jQuery(function($) {
  var graphData = [];

  // $.ajax({
  //   url: '/api/hpv/?format=json',
  //   success: function(data) {
  //     for (i = 0; i < data.length; i++) {
  //       unix = Math.round((new Date(data[i]["timestamp"]).getTime()) / 1000);
  //       graphData.push([unix, data[i]["hpv_plant"]]);
  //     }
  //     console.log("2", graphData);
  //   }
  // });

  d3.json('/api/hpv/?date=1&format=json', function(data) {
    var graphData = [{
      key: 'Today',
      values: [],
      color: '#4252ce'
    }];
    for (i = 0; i < data.length; i++) {
      // unix = Math.round((new Date(data[i]["timestamp"]).getTime()) / 1000);
      unix = new Date(data[i]["timestamp"]).getTime()
      graphData[0].values.push([unix, data[i]["hpv_plant"]]);
    }
    console.log(graphData);
    nv.addGraph(function() {
    var chart = nv.models.lineChart()
      .useInteractiveGuideline(false)
      .x(function(d) { return d[0] })
      .y(function(d) { return d[1] })
      ;
    // nv.addGraph(function() {
    //   var chart = nv.models.cumulativeLineChart()
    //                 .x(function(d) { return d[0] })
    //                 .y(function(d) { return d[1]/100 }) //adjusting, 100% is 1.00, not 100 as it is in the data
    //                 .color(d3.scale.category10().range())
    //                 .useInteractiveGuideline(true)
    //                 ;
      chart.xAxis
        .axisLabel('Time')
        .tickFormat(function(d) {
            return d3.time.format('%H:%M')(new Date(d))
          });

      chart.yDomain([70, 110])
      chart.yAxis
          .axisLabel('HPV')
          .tickFormat(d3.format(',f'));

      d3.select('#chart svg')
          .datum(graphData)
          .call(chart);

      //TODO: Figure out a good way to do this automatically
      nv.utils.windowResize(chart.update);

      return chart;
    });
  });
  // reload page every 60 seconds
  // setTimeout(function() {location.reload(true);},60000);
});
