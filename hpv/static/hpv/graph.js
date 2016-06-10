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

  /*
    Line Graph
  */

  d3.json('/api/hpv?format=json', function(data) {
    var graphData = [{
      key: 'Today',
      values: [],
      color: '#4252ce'
    }];
    for (i = 0; i < data.length; i++) {
      // unix = Math.round((new Date(data[i]["timestamp"]).getTime()) / 1000);
      unix = new Date(data[i]["timestamp"]).getTime()
      graphData[0].values.push([unix, data[i]["PLANT_d_hpv"]]);
    }

    nv.addGraph(function() {
    var chart = nv.models.lineChart()
      .useInteractiveGuideline(false)
      .x(function(d) { return d[0] })
      .y(function(d) { return d[1] })
      ;

      chart.xAxis
        .axisLabel('Time')
        .tickFormat(function(d) {
            return d3.time.format('%H')(new Date(d))
          });

      // chart.yDomain([70, 120])
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

  /*
    Heat Map
  */

  var margin = { top: 50, right: 0, bottom: 100, left: 30 },
      width = 1100 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom,
      gridSize = Math.floor(width / 24),
      legendElementWidth = gridSize*2,
      buckets = 9,
      colors = ["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"], // alternatively colorbrewer.YlGnBu[9]
      days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"],
      times = ["1a", "2a", "3a", "4a", "5a", "6a", "7a", "8a", "9a", "10a", "11a", "12p", "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p", "10p", "11p", "12a"];
      datasets = [{key: "PLANT_d_hpv", label: "Plant Day HPV"}, {key: "CIW_d_hpv", label: 'CIW Day HPV'}, {key: "FCB_d_hpv", label: 'FCB Day HPV'}];

  var svg = d3.select("#heatmap").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var dayLabels = svg.selectAll(".dayLabel")
      .data(days)
      .enter().append("text")
        .text(function (d) { return d; })
        .attr("x", 0)
        .attr("y", function (d, i) { return i * gridSize; })
        .style("text-anchor", "end")
        .attr("transform", "translate(-6," + gridSize / 1.5 + ")")
        .attr("class", function (d, i) { return ((i >= 0 && i <= 4) ? "dayLabel mono axis axis-workweek" : "dayLabel mono axis"); });

  var timeLabels = svg.selectAll(".timeLabel")
      .data(times)
      .enter().append("text")
        .text(function(d) { return d; })
        .attr("x", function(d, i) { return i * gridSize; })
        .attr("y", 0)
        .style("text-anchor", "middle")
        .attr("transform", "translate(" + gridSize / 2 + ", -6)")
        .attr("class", function(d, i) { return ((i >= 5 && i <= 12) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis"); });

  // Create heatmap
  var heatmapChart = function(key) {
    d3.json('/api/hpv?format=json',
    function(error, data) {
      var heatmapData = {};
      for (var i = 0; i < data.length; i++) {
        var timestamp = data[i]["timestamp"];
        var times = new Date(timestamp); // get date object
        var dayOfWeek = times.getDay() + 1; // get day of week 0-7
        var hourOfDay = times.getHours(); // get hour
        if (!heatmapData[dayOfWeek]) { // create day of week if not there
          heatmapData[dayOfWeek] = {};
        }
        if (!heatmapData[dayOfWeek][hourOfDay]) { // create hour of day if not there
          heatmapData[dayOfWeek][hourOfDay] = [];
        }
        heatmapData[dayOfWeek][hourOfDay].push(parseFloat(data[i][key])); // append to dataset
      }

      // get average of value per hour
      for (day in heatmapData) {
        if (heatmapData.hasOwnProperty(day)) {
          for (hour in heatmapData[day]) {
            if (heatmapData[day].hasOwnProperty(hour)) {
              var values = heatmapData[day][hour],
                  sum = 0;
              for (var i = 0; i < values.length; i++) {
                sum += values[i];
              }
              heatmapData[day][hour] = sum / values.length;
            }
          }
        }
      }

      // format new dataset
      var newHeatMapData = []
      for (day in heatmapData) {
        for (hour in heatmapData[day]) {
          newHeatMapData.push({
            day:day,
            hour:hour,
            value:heatmapData[day][hour],
          })
        }
      }

      var colorScale = d3.scale.quantile()
          .domain([d3.min(newHeatMapData, function (d) { return d.value; }) - 3, d3.max(newHeatMapData, function (d) { return d.value; })])
          .range(colors);

      var cards = svg.selectAll(".hour")
          .data(newHeatMapData, function(d) {return d.day+':'+d.hour;});

      cards.append("title");

      cards.enter().append("rect")
          .attr("x", function(d) { return (d.hour - 1) * gridSize; })
          .attr("y", function(d) { return (d.day - 1) * gridSize; })
          .attr("rx", 4)
          .attr("ry", 4)
          .attr("class", "hour bordered")
          .attr("width", gridSize)
          .attr("height", gridSize)
          .style("fill", colors[0]);

      cards.transition().duration(1000)
          .style("fill", function(d) { return colorScale(d.value); });

      cards.select("title").text(function(d) { return d.value; });

      cards.exit().remove();

      var legend = svg.selectAll(".legend")
          .data([0].concat(colorScale.quantiles()), function(d) { return d; });

      legend.enter().append("g")
          .attr("class", "legend");

      legend.append("rect")
          .attr("x", function(d, i) { return legendElementWidth * i; })
          .attr("y", height)
          .attr("width", legendElementWidth)
          .attr("height", gridSize / 2)
          .style("fill", function(d, i) { return colors[i]; });

      legend.append("text")
          .attr("class", "mono scale")
          .text(function(d) { return "≥ " + Math.round(d); })
          .attr("x", function(d, i) { return legendElementWidth * i; })
          .attr("y", height + gridSize);

      legend.exit().remove();

    });
  };

  heatmapChart("PLANT_d_hpv");

  // dataset selection
  var datasetpicker = d3.select("#dataset-picker").selectAll(".btn btn-default")
  .data(datasets);

  datasetpicker.enter()
      .append("input")
      .attr("value", function(d){ return d.label })
      .attr("type", "button")
      .attr("class", "btn btn-default")
      .on("click", function(d) {
        heatmapChart(d.key);
    });

  // reload page every 60 seconds
  // setTimeout(function() {location.reload(true);},60000);
});
