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
