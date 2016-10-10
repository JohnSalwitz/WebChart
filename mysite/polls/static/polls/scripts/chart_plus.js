
// load charts libraries...
google.charts.load('current', {'packages':['corechart']});

// creates a single chart in the "div_target"
function ChartPlus(source_url, div_target, chart_type) {

    this.url = source_url
    this.div_target = div_target
    this.chart_type = chart_type
    var self = this

    this.drawChart = function() {
        var jsonData = $.ajax({
              url: self.url,
              dataType: "json",
              async: false
              }).responseText;

        // Create our data table out of JSON data loaded from server.
        var data = new google.visualization.DataTable(jsonData);
        var json = jQuery.parseJSON(jsonData)

        var clonedDiv = $('#chart_box_template').clone();
        clonedDiv.attr("id", self.div_target);
        //clonedDiv.show();
        $('#charts').append(clonedDiv);

        if (json.header.title != undefined)
            clonedDiv.find(".chart-title").html(json.header.title );

        if (json.header.subtotal != undefined)
            clonedDiv.find(".chart-subtotal").html(json.header.subtotal );

        // Instantiate and draw our chart, passing in some options.
        if (self.chart_type == "line") {
            var chart = new google.visualization.LineChart(clonedDiv.find(".panel-body")[0]);
        }
        else if (self.chart_type == "pie") {
            var chart = new google.visualization.PieChart(clonedDiv.find(".panel-body")[0]);
        }
        else if (self.chart_type == "bar") {
            var chart = new google.visualization.BarChart(clonedDiv.find(".panel-body")[0]);
        }
        chart.draw(data, {width: 500, height: 400});
    }

    google.charts.setOnLoadCallback(this.drawChart);
}