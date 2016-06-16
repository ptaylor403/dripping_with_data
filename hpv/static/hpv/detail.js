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
  // var parseDate = d3.time.format("%Y-%m-%dT%H:%M:%SZ").parse;
  var parseDate = d3.time.format.utc("%Y-%m-%dT%H:%M:%SZ").parse;


  var datasets = [{day: "PLANT_d_hpv", shift: "PLANT_s_hpv", label: "PLANT"},
                  {day: "CIW_d_hpv", shift: "CIW_s_hpv", label: 'CIW'},
                  {day: "FCB_d_hpv", shift: "FCB_s_hpv",label: 'FCB'},
                  {day: "PNT_d_hpv", shift: "PNT_s_hpv",label: 'PNT'},
                  {day: "PCH_d_hpv", shift: "PCH_s_hpv",label: 'PCH'},
                  {day: "FCH_d_hpv", shift: "FCH_s_hpv",label: 'FCH'},
                  {day: "DAC_d_hpv", shift: "DAC_s_hpv",label: 'DAC'},
                  {day: "MAINT_d_hpv", shift: "MAINT_s_hpv",label: 'MAINT'},
                  {day: "QA_d_hpv", shift: "QA_s_hpv",label: 'QA'},
                  {day: "MAT_d_hpv", shift: "MAT_s_hpv",label: 'MAT'}];

  var detailLevel = [{query: "/api/hpv/?days=1&format=json", label: "Day"},
                     {query: "/api/hpv/?days=7&format=json", label: 'Week'},
                     {query: "/api/hpv/?days=31&format=json", label: 'Month'}];

 var url_parts = ($(location).attr("href")).split('/');
 var dept = '';

 while (dept == ''){
   dept = url_parts.pop();
 }

 dept = dept.toUpperCase();

 // create new array of available departments
 // then check to see if user selection is in them
 // if not, set to 'PLANT'
 var depts = datasets.map(function(d) { return d.label; });
 if (depts.indexOf(dept) == -1){
   dept='PLANT';
 };


  var currentDataName = dept+"_d_hpv";
  var initial_query = "/api/hpv/?days=7&format=json";
  var currentQuery = initial_query
  /***********************************
    Line Graph
  ************************************/

  var lineChart = (function() {
      // Set the dimensions of the canvas / graph
      var margin = {top: 30, right: 15, bottom: 47, left: 50},
          width = 670 - margin.left - margin.right,
          height = 297 - margin.top - margin.bottom;

      // Set the ranges
      var x = d3.time.scale().range([0, width]);
      var y = d3.scale.linear().range([height, 0]);

      // Define the axes
      var xAxis = d3.svg.axis().scale(x)
          .orient("bottom").ticks(5);

      var yAxis = d3.svg.axis().scale(y)
          .orient("left").ticks(5);

      // Adds the svg canvas
      var svg = d3.select("#line")
          .append("svg")
              .attr("width", width + margin.left + margin.right)
              .attr("height", height + margin.top + margin.bottom)
          .append("g")
              .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");
      // add legend
      var legend = svg.append("svg")
    	  .attr("class", "legend")
        .attr("x", 420)
        .attr("y", -20)
    	  .attr("height", 200)
    	  .attr("width", 200);

      // add colour square/circle
      legend.append("circle")
        .attr("cx", 35)
        .attr("cy", 6)
        .attr("r", 6)
    	  .style("fill", 'steelblue');

      legend.append("circle")
        .attr("cx", 110)
        .attr("cy", 6)
        .attr("r", 6)
    	  .style("fill", 'orange');

      // add text for colour square/circle
      legend.append("text")
  	    .attr("x", 60)
        .attr("y", 10)
    	  .text('Day');

      legend.append("text")
  	    .attr("x", 140)
        .attr("y", 10)
    	  .text('Shift');

      // create x axis grid
      function make_x_axis() {
          return d3.svg.axis()
              .scale(x)
              .orient("bottom")
              .ticks(5)
          }

      // create y axis grid
      function make_y_axis() {
          return d3.svg.axis()
              .scale(y)
              .orient("left")
              .ticks(5)
          }

      // Get the data
      var lineGraph = function(day, data) {
        // Get dataset
        var dataset = datasets.filter(function(dataset) {
            if (dataset.day == day) {
                return true;
            }
        })[0];

        var shift = dataset.shift;

        // Setup data
        data.forEach(function(d){
            d[day] = +d[day];
            d[shift] = +d[shift];
        });

        // Sort timestamp to most recent
        data.sort(timeSort);

        // Define line
        var valueline = d3.svg.line()
            .x(function(d) { return x(d.timestamp); })
            .y(function(d) { return y(d[day]); });

        // Define line1
        var valueline1 = d3.svg.line()
            .x(function(d) { return x(d.timestamp); })
            .y(function(d) { return y(d[shift]); });

        // Scale the range of the data
        x.domain(d3.extent(data, function(d) { return d.timestamp; }));
        y.domain([0, d3.max(data, function(d) { return Math.max(d[day], d[shift]); })]);

        // create grids for linegraph
        svg.append("g")
          .attr("class", "x grid")
          .attr("transform", "translate(0," + height + ")")
          .call(make_x_axis()
              .tickSize(-height, 0, 0)
              .tickFormat("")
          );

        svg.append("g")
          .attr("class", "y grid")
          .call(make_y_axis()
              .tickSize(-width, 0, 0)
              .tickFormat("")
          );

        // Add the valueline path
        svg.append("path")
            .attr("class", "line")
            .style({"stroke-width": "4px"})
            .attr("d", valueline(data));

        // Add the valueline1 path
        svg.append("path")
            .attr("class", "line1")
            .style("stroke", "orange")
            .style("stroke-dasharray", ("3, 3"))
            .attr("d", valueline1(data));

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
            .attr("y", 0 - (margin.left / 2)- 20)
            .attr("dy", "1em")
            .style("text-anchor", "middle")
            .text("HPV");

          //  Add title
          $('#depttitle').text(dataset.label);
          $('#time').text('Week');
          // svg.append("text")
          //     .classed('title', true)
          //     .attr("x", (width / 2))
          //     .attr("y", 0 - (margin.bottom / 2))
          //     // .attr("y", 0 - height)
          //     .attr("text-anchor", "middle")
          //     .style("font-size", "16px")
          //     .text(dataset.label + " vs Date");

          var dateline1 = d3.select('#line')
              .transition()
              .select('.line1')
              .duration(750)
              .attr("d", valueline1(data));
        };

      /*********
      Update line graph - remove old line and update new information/line
      **********/
      var updateLineData = function(day, data) {
          // Get dataset
          var dataset = datasets.filter(function(dataset) {
              if (dataset.day == day) {
                  return true;
              }
          })[0];

          var shift = dataset.shift;

          data.forEach(function(d){
              // d[day] = +d[day];
              d[shift] = +d[shift];
          });

          data.sort(timeSort);

          // update lines
          var valueline = d3.svg.line()
              .x(function(d) { return x(d.timestamp); })
              .y(function(d) { return y(d[day]); });

          var valueline1 = d3.svg.line()
              .x(function(d) { return x(d.timestamp); })
              .y(function(d) { return y(d[shift]); });

          // Scale the range of the data
          x.domain(d3.extent(data, function(d) { return d.timestamp; }));
          y.domain([0, d3.max(data, function(d) { return d[shift]; })]);

          // Update the x axis
          svg.select(".x.axis")
              .call(xAxis);

          // update the y axis
          svg.select(".y.axis")
              .call(yAxis);

          // // Update title
          // svg.select("text.title")
          //     .text(dataset.label + " vs Date");

          // update grid for linegraph
          svg.select(".x.grid")
            .call(make_x_axis()
                .tickSize(-height, 0, 0)
                .tickFormat("")
            );

          svg.select(".y.grid")
            .call(make_y_axis()
                .tickSize(-width, 0, 0)
                .tickFormat("")
            );

          d3.select('#line')
              .transition()
              .select('.line')
              .duration(750)
              .attr("d", valueline(data));

          d3.select('#line')
              .transition()
              .select('.line1')
              .duration(750)
              .attr("d", valueline1(data));

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
    var margin = { top: 40, right: 0, bottom: 50, left: 30 },
        width = 800 - margin.left - margin.right,
        height = 350 - margin.top - margin.bottom,
        gridSize = Math.floor(width / 24),
        legendElementWidth = gridSize * 2,
        buckets = 9,
        colors = ["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"],

        days = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],

        times = ["12a", "1a", "2a", "3a", "4a", "5a", "6a", "7a", "8a", "9a", "10a", "11a", "12p", "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p", "10p", "11p"];

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
          .attr("class", function (d, i) { return ((i >= 1 && i <= 5) ? "dayLabel mono axis axis-workweek" : "dayLabel mono axis"); });

    var timeLabels = svg.selectAll(".timeLabel")
        .data(times)
        .enter().append("text")
          .text(function(d) { return d; })
          .attr("x", function(d, i) { return i * gridSize; })
          .attr("y", 0)
          .style("text-anchor", "middle")
          .attr("transform", "translate(" + gridSize / 2 + ", -6)")
          .attr("class", function(d, i) { return ((i >= 6 && i <= 14) ? "timeLabel mono axis axis-shift1" : ((i >= 15 && i <= 23) ? "timeLabel mono axis axis-shift2" : "timeLabel mono axis")); })
          // .attr("class", function(d, i) { return ((i >= 15 && i <= 23) ? "timeLabel mono axis axis-shift2" : "timeLabel mono axis"); });

    // Create heatmap
    var heatMapChart = function(day, data) {
      var heatmapData = {};
      for (var i = 0; i < data.length; i++) {
        var timestamp = data[i]["timestamp"];
        var times = new Date(timestamp); // get date object
        var dayOfWeek = times.getDay(); // get day of week 0-7
        var hourOfDay = times.getHours(); // get hour of day
        if (!heatmapData[dayOfWeek]) { // create day of week if its not there
          heatmapData[dayOfWeek] = {};
        }
        if (!heatmapData[dayOfWeek][hourOfDay]) { // create hour of day if not in dictionary
          heatmapData[dayOfWeek][hourOfDay] = [];
        }
        heatmapData[dayOfWeek][hourOfDay].push(parseFloat(data[i][day])); // append to dictionary
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

      // format dataset to
      var newHeatMapData = []
      for (day in heatmapData) {
        for (hour in heatmapData[day]) {
          newHeatMapData.push({
            day:day,
            hour:hour,
            value:heatmapData[day][hour],
          })
        }
      };

      var colorScale = d3.scale.quantile()
          .domain([d3.min(newHeatMapData, function (d) { return d.value; }), d3.max(newHeatMapData, function (d) { return d.value; })])
          .range(colors);

      var cards = svg.selectAll(".hour")
          .data(newHeatMapData, function(d) {return d.day+':'+d.hour;});

      cards.append("title");

      cards.enter().append("rect")
          .attr("x", function(d) { return (d.hour) * gridSize; })
          .attr("y", function(d) { return (d.day) * gridSize; })
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
    };
    return {
        heatmap: heatMapChart
    }
  })();
  /********************************
    Week on Week
  *********************************/

  var weekOnWeek = (function(day, data) {
    var dayInSeconds = 24 * 3600
    var weekInSeconds = 7 * dayInSeconds
    var todayData = [];
    var previousData =[];
    var graphData = [{
      key: 'Today',
      values: [],
      color: 'steelblue'
    },
    {
      key: 'LastWeek',
      values: [],
      color: '#ff0000',
      classed: 'dashed'
    }];
    last_in_data = data[data.length-1]['timestamp'] / 1000
    first_for_day = last_in_data - dayInSeconds
    for (i = 0; i < data.length; i++) {
      time = data[i]["timestamp"] / 1000
      if(time >= first_for_day){
        todayData.push(data[i])
      }
    }
    for (i = 0; i < todayData.length; i++) {
      // unix = Math.round((new Date(data[i]["timestamp"]).getTime()) / 1000);
      time = todayData[i]["timestamp"] / 1000
      // console.log(i + "/" + data[i]["timestamp"] + " || " + time)
      graphData[0].values.push([time, todayData[i][day]]);
    };
    lastDataTime = todayData[todayData.length-1]['timestamp']
    lastDataTimestamp = lastDataTime / 1000
    previousDataTimestamp = lastDataTimestamp - weekInSeconds //- ( dayInSeconds / 6)
    var query = '/api/hpv?days=1&format=json&end='+previousDataTimestamp
    d3.json(query,function(data){
      for (i = 0; i < data.length; i++) {
          // unix = Math.round((new Date(data[i]["timestamp"]).getTime()) / 1000);
          time = parseDate(data[i]["timestamp"]) / 1000 + weekInSeconds
          // console.log(i + "/" + data[i]["timestamp"] + " || " + time)
          graphData[1].values.push([time, +data[i][day]]);
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
              return d3.time.format('%H:%M')(new Date(d * 1000))
            });

        chart.yDomain([0, d3.max(graphData, function(d){
          var y_value_max =  d3.max(d.values, function(e){return e[1]})
          console.log(y_value_max);
          return y_value_max
        })])
        chart.yAxis
          .axisLabel('HPV')
          .tickFormat(d3.format(',f'));
        d3.select('#week_on_week svg')
          .datum(graphData)
          .call(chart);

        //TODO: Figure out a good way to do this automatically
        nv.utils.windowResize(chart.update);

        return chart;
      });
      //console.log(graphData);
    })
  });

  // remove old highlighted buttons and highlight new infomation
  var updateButtons = function(label, parent) {
    parent.find('.btn-default').removeClass('selected');
    parent.find('.btn-default.' + label).addClass('selected');
  };

  var weekQueryResult = []
  var currentQueryResult = []

  // intialize charts

  d3.json(initial_query,function(error, data){
    data.forEach(function(d){
      d.timestamp = parseDate(d.timestamp);
    });
    weekQueryResult = data
    currentQueryResult = data
    heatMap.heatmap(currentDataName, data)
    lineChart.lineGraph(currentDataName, data)
    weekOnWeek(currentDataName, data)
  });

  // dataset selection
  var datasetpicker = d3.select("#dataset-picker").selectAll(".btn btn-default")
  .data(datasets);

  var detailLevelPicker = d3.select("#detaillevel-picker").selectAll(".btn btn-default")
  .data(detailLevel);

  datasetpicker.enter()
    .append("input")
    .attr("value", function(d) { return d.label })
    .attr("type", "button")
    .attr("class", function(d) { return "btn btn-default " + d.label })
    .on("click", function(d) {
      // update charts with new data
      currentDataName = d.day
      updateButtons(d.label, $(this).parent());
      $('.depttitle').text(d.label);
      heatMap.heatmap(d.day,weekQueryResult);
      lineChart.updateLineData(d.day, currentQueryResult);
      weekOnWeek(currentDataName, currentQueryResult);
    });

  detailLevelPicker.enter()
    .append("input")
    .attr("value", function(d){ return d.label })
    .attr("type", "button")
    .attr("class", function(d) { return "btn btn-default " + d.label })
    .on("click", function(d) {
      // update charts with new data
      currentQuery = d.query

      updateButtons(d.label, $(this).parent());
      $('#time').text(d.label);
      d3.json(currentQuery, function(data){
        data.forEach(function(d){
          d.timestamp = parseDate(d.timestamp);
        });
        currentQueryResult = data
        lineChart.updateLineData(currentDataName, data);
      })
    });


  // prehighlight buttons
  updateButtons(dept, $('#dataset-picker'));
  updateButtons('Week', $('#detaillevel-picker'));

  // reload page every 60 seconds
  // setTimeout(function() {location.reload(true);},6000);
  // reload page every 5 seconds
  setInterval(function() {
    d3.json(initial_query,function(error, data){
      data.forEach(function(d){
        d.timestamp = parseDate(d.timestamp);
      });
      weekQueryResult = data
      heatMap.heatmap(currentDataName, data)
      d3.json(currentQuery,function(error, data){
        data.forEach(function(d){
          d.timestamp = parseDate(d.timestamp);
        });
        currentQueryResult = data
        lineChart.updateLineData(currentDataName, data)
      })
      weekOnWeek(currentDataName, weekQueryResult)
    })
  },5000);


});
