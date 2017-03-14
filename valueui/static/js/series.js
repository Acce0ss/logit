function getSeriesListData()
{
    return $.ajax({
	method: "GET",
	url: "/api/series"
    });
}

function populateListWithSeries(list)
{
    getSeriesListData()
	.then(JSON.parse)
	.then(function (data){
	    data.series.forEach(function (serie,i,l) {
		addSerieListItem(list, serie);
	    });
	}).fail(function (data){
	    console.log("Error");
	    console.log(data);
	});
}

function addSerieListItem(parent, serie)
{
    var serieItem = $('<li></li>')
    serieItem.append(
	$('<a href="/serie/' + serie.id +
	  '" class="ui-btn">' + serie.name +
	  '</a>'));
    parent.append(serieItem)
}

function getSerieData(serieid)
{
    return $.ajax({
	method: "GET",
	url: "/api/serie/" + serieid
    });
}

function populateCanvasIfDataAvailable(canvas, serieid)
{
    getSerieData(serieid)
	.then(JSON.parse)
	.then(function (serie){
	    if(serie.values.length > 0)
	    {
		drawSerieOn(serie, canvas);
	    }
	    else
	    {
		console.log("No datapoints");
	    }
	})
	.fail(function (data){
	    console.log("getting data failed");
	});
}

function drawSerieOn(serie, canvas)
{
    var time_data = [];
    var value_data = [];

    serie.values.forEach(function (e,i,l){
	console.log(e);
	time_data.push(e.time);
	value_data.push(e.value);
    });
    
    var myChart = new Chart(canvas, {
	responsive: true,
	maintainAspectRatio: false,

	type: 'line',
	data: {
	    labels: time_data,
	    datasets: [{
		label: serie.name,
		data: value_data,
	    }]
	},
	options: {
	    layout: {
		padding: {
		    left: 30,
		    right: 30
		}
	    },
	    scales: {
		yAxes: [{
		    ticks: {
			beginAtZero:true
		    }
		}]
	    }
	}
    });
}

function postValueTo(serieid, valueform)
{    
    return $.ajax({
	method: "POST",
	data: valueform.serialize(),
	url: "/api/serie/" + serieid + "/datapoint"
    });
}
