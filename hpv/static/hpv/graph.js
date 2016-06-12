jQuery(function($) {

  /*
    Line Graph
  */
  var lineGraph = (function() {
    var graphData = [];
    d3.json('/api/hpv?format=json', function(data) {
      var graphData = [{
        key: 'Today',
        values: [],
        color: '#4252ce'
      }, {
        key: 'shift1',
        values: [],
      }];
      data.sort(function(a,b){
        if (a.timestamp > b.timestamp) {
          return 1;
        }
        if (a.timestamp < b.timestamp) {
          return -1;
        }
        return 0;
      });

      for (i = 0; i < data.length; i++) {
          // unix = Math.round((new Date(data[i]["timestamp"]).getTime()) / 1000);
          time = new Date(data[i]["timestamp"]).getTime()
          // console.log(i + "/" + data[i]["timestamp"] + " || " + time)
          graphData[0].values.push([time, data[i]["PLANT_d_hpv"]]);
      };

      nv.addGraph(function() {
      var chart = nv.models.lineChart()
        .useInteractiveGuideline(false)
        .x(function(d) { return d[0] })
        .y(function(d) { return d[1] })
        ;
        
        chart.xAxis
          .axisLabel('Time')
          .tickFormat(function(d) {
              return d3.time.format('%H:%M')(new Date(d))
            });

        chart.yDomain([0, 140])
        chart.yAxis
          .axisLabel('HPV')
          .tickFormat(d3.format(',f'));

        d3.select('#linegraph svg')
          .datum(graphData)
          .call(chart);

        //TODO: Figure out a good way to do this automatically
        nv.utils.windowResize(chart.update);

        return chart;
      });
    });
    return {
        lineGraph: lineGraph
    }
  })();

  // reload page every 60 seconds
  // setTimeout(function() {location.reload(true);},6000);
});
