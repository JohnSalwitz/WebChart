
// load charts libraries...
google.charts.load('current', {'packages':['corechart']});

// creates a single chart in the "div_target"
function ChartPlus(source_url, div_target) {

    this.url = source_url
    this.div_target = div_target
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
        clonedDiv.show();
        $('#charts').append(clonedDiv);

        title = json.title
        clonedDiv.find(".chart-title").html( title );

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.PieChart(clonedDiv.find(".panel-body")[0]);
        chart.draw(data, {width: 600, height: 400});
    }

    google.charts.setOnLoadCallback(this.drawChart);
}