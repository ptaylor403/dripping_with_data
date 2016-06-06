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

  d3.json('/api/hpv/?format=json', function(data) {
    var graphData = [{
      key: 'Today',
      values: [],
      color: '#ff7f0e'
    }];
    for (i = 0; i < data.length; i++) {
      // unix = Math.round((new Date(data[i]["timestamp"]).getTime()) / 1000);
      unix = new Date(data[i]["timestamp"]).getTime()
      graphData[0].values.push([unix, data[i]["hpv_plant"]]);
    }
    console.log(graphData);

    nv.addGraph(function() {
    var chart = nv.models.lineChart()
      .useInteractiveGuideline(true)
      .x(function(d) { return d[0] })
      .y(function(d) { return d[1] }) //adjusting, 100% is 1.00, not 100 as it is in the data
      ;
    // nv.addGraph(function() {
    //   var chart = nv.models.cumulativeLineChart()
    //                 .x(function(d) { return d[0] })
    //                 .y(function(d) { return d[1]/100 }) //adjusting, 100% is 1.00, not 100 as it is in the data
    //                 .color(d3.scale.category10().range())
    //                 .useInteractiveGuideline(true)
    //                 ;
      //
       chart.xAxis
          .axisLabel('Time')
          .tickFormat(function(d) {
              return d3.time.format('%H:%M')(new Date(d))
            });
      //
      // chart.yAxis
      //     .tickFormat(d3.format(',f'));

      d3.select('#chart svg')
          .datum(graphData)
          .call(chart);

      //TODO: Figure out a good way to do this automatically
      nv.utils.windowResize(chart.update);

      return chart;
    });
  });
});
