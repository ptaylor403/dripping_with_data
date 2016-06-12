jQuery(function($) {
  // sort on timestamp
  var timeSort = function(a,b){
      if (a.timestamp > b.timestamp) {
          return 1;
      }
      if (a.timestamp < b.timestamp) {
          return -1;
      }
      return 0;
  };

  var datasets = [{key: "PLANT_d_hpv", label: "Plant Day HPV"},
                  {key: "CIW_d_hpv", label: 'CIW Day HPV'},
                  {key: "FCB_d_hpv", label: 'FCB Day HPV'}];
  var detailLevel = [{key: "?format=json&days=1", label: "Day"},
                     {key: "?format=json&days=7", label: 'Week'},
                     {key: "?format=json&days=31", label: 'Month'}];
  /*
    Line Graph
  */
  var lineChart = (function() {
      // Set the dimensions of the canvas / graph
      var margin = {top: 30, right: 50, bottom: 30, left: 50},
          width = 700 - margin.left - margin.right,
          height = 270 - margin.top - margin.bottom;

      // Set the ranges
      var x = d3.time.scale().range([0, width]);
      var y = d3.scale.linear().range([height, 0]);

      // Define the axes
      var xAxis = d3.svg.axis().scale(x)
          .orient("bottom").ticks(5);

      var yAxis = d3.svg.axis().scale(y)
          .orient("left").ticks(5);

      // Define the div for the tooltip
      var div = d3.select("#line").append("div")
          .attr("class", "tooltip")
          .style("opacity", 0);

      // Adds the svg canvas
      var svg = d3.select("#line")
          .append("svg")
              .attr("width", width + margin.left + margin.right)
              .attr("height", height + margin.top + margin.bottom)
          .append("g")
              .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");

      // Get the data
      var lineGraph = function(key) {
        d3.json('/api/hpv?format=json',
        function(error, data) {

          // setup and order data
          data.forEach(function(d){
              d.timestamp = new Date(d.timestamp);
              d[key] = +d[key];
          });

          // sort timestamp to most recent
          data.sort(timeSort);

          // Define the line
          var valueline = d3.svg.line()
              .interpolate("basis")
              .x(function(d) { return x(d.timestamp); })
              .y(function(d) { return y(d[key]); });

          // Scale the range of the data
          x.domain(d3.extent(data, function(d) { return d.timestamp; }));
          y.domain([0, d3.max(data, function(d) { return d[key]; })]);
          // var yDomain = d3.extent(data, function(d) { return d[key]; });
          // y.domain(yDomain);

          // Add the valueline path.
          svg.append("path")
              .attr("class", "line")
              .attr("d", valueline(data));

          // Add the X Axis
          svg.append("g")
              .attr("class", "x axis")
              .attr("transform", "translate(0," + height + ")")
              .call(xAxis);

          // Add X Axis Label
          svg.append("text")
              .classed('xLabel', true)
              .attr("x", width / 2)
              .attr("y", height + margin.bottom)
              .style("text-anchor", "middle")
              .text("Date");

          // Add the Y Axis
          svg.append("g")
              .attr("class", "y axis")
              .call(yAxis);

          // Add Y Axis Label
          svg.append("text")
              .classed('yLabel', true)
              .attr("transform", "rotate(-90)")
              .attr("x", 0 - (height / 2))
              // .attr("y", 0 – margin.left)
              .attr("dy", "1em")
              .style("text-anchor", "middle")
              .text("HPV");

          // Get label
          var getLabel = datasets.filter(function(getLabel) {
              if (getLabel.key == key) {
                  return true;
              }
          })[0];

          // Add title
          svg.append("text")
              .classed('title', true)
              .attr("x", (width / 2))
              .attr("y", 0 - (margin.bottom / 2))
              // .attr("y", 0 - height)
              .attr("text-anchor", "middle")
              .style("font-size", "16px")
              .text(getLabel.label + " vs Date");

          // line transition or animation
          var dateline = d3.select('#line')
              .transition()
              .select('.line')
              .duration(750)
              .attr("d", valueline(data));
        })
      };

      var updateLineData = function(key) {
        d3.json('/api/hpv?format=json',
        function(error, data) {

          data.forEach(function(d){
              d.timestamp = new Date(d.timestamp);
              d[key] = +d[key];
          });
          data.sort(timeSort);

          // Define the line
          var valueline = d3.svg.line()
              .interpolate("basis")
              .x(function(d) { return x(d.timestamp); })
              .y(function(d) { return y(d[key]); });

          // Scale the range of the data
          x.domain(d3.extent(data, function(d) { return d.timestamp; }));
          y.domain([0, d3.max(data, function(d) { return d[key]; })]);

          // Get dataset
          var getLabel = datasets.filter(function(getLabel) {
              if (getLabel.key == key) {
                  return true;
              }
          })[0];

          // Update title
          svg.select("text.title")
              .text(getLabel.label + " vs Date");

          var dateline = d3.select('#line')
              .transition()
              .select('.line')
              .duration(750)
              .attr("d", valueline(data));

        }) // function close
      }; // updateLineData close

      return {
          lineGraph: lineGraph,
          updateLineData: updateLineData
      }
  })(); // linechart close

  /********************************
    Heat Map
  *********************************/
  var heatMap = (function() {
    var margin = { top: 50, right: 0, bottom: 50, left: 30 },
        width = 700 - margin.left - margin.right,
        height = 300 - margin.top - margin.bottom,
        gridSize = Math.floor(width / 24),
        legendElementWidth = gridSize*2,
        buckets = 9,
        colors = ["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"], // alternatively colorbrewer.YlGnBu[9]
        days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"],
        times = ["1a", "2a", "3a", "4a", "5a", "6a", "7a", "8a", "9a", "10a", "11a", "12p", "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p", "10p", "11p", "12a"];

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
          var hourOfDay = times.getHours(); // get hour of day
          if (!heatmapData[dayOfWeek]) { // create day of week if not there
            heatmapData[dayOfWeek] = {};
          }
          if (!heatmapData[dayOfWeek][hourOfDay]) { // create hour of day if not in dictionary
            heatmapData[dayOfWeek][hourOfDay] = [];
          }
          heatmapData[dayOfWeek][hourOfDay].push(parseFloat(data[i][key])); // append to dictionary
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
    return {
        heatmap: heatmapChart
    }
  })();

  // intialize charts
  heatMap.heatmap("PLANT_d_hpv");
  lineChart.lineGraph("PLANT_d_hpv");

  // dataset selection
  var datasetpicker = d3.select("#dataset-picker").selectAll(".btn btn-default")
  .data(datasets);

  var detailLevelPicker = d3.select("#detaillevel-picker").selectAll(".btn btn-default")
  .data(detailLevel);

  datasetpicker.enter()
      .append("input")
      .attr("value", function(d){ return d.label })
      .attr("type", "button")
      .attr("class", "btn btn-default")
      .on("click", function(d) {
        // update charts with new data
        heatMap.heatmap(d.key);
        lineChart.updateLineData(d.key);
      });

  detailLevelPicker.enter()
    .append("input")
    .attr("value", function(d){ return d.label })
    .attr("type", "button")
    .attr("class", "btn btn-default")
    .on("click", function(d) {
      // update charts with new data
      lineChart.updateLineData(d.key);
    });

  // reload page every 60 seconds
  // setTimeout(function() {location.reload(true);},6000);
});
