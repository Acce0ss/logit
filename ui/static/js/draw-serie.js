
// expect value_data and time_data variables
// to exists with the serie data in them.

document.addEventListener('DOMContentLoaded', function() {
  var ctx = document.getElementById("serie-graph");
  var myChart = new Chart(ctx, {
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
}, false);
