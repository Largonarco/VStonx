const width_threshold = 480;

function drawLineChart() {
  if ($("#lineChart").length) {
    ctxLine = document.getElementById("lineChart").getContext("2d");
    optionsLine = {
      scales: {
        yAxes: [
          {
            scaleLabel: {
              display: true,
              labelString: "Hits"
            }
          }
        ]
      }
    };

    // Set aspect ratio based on window width
    optionsLine.maintainAspectRatio =
      $(window).width() < width_threshold ? false : true;

    configLine = {
      type: "line",
      data: {
        labels: [
          "January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July"
        ],
        datasets: [
          {
            label: "Latest Hits",
            data: [88, 68, 79, 57, 56, 55, 70],
            fill: false,
            borderColor: "rgb(75, 192, 192)",
            lineTension: 0.1
          },
          {
            label: "Popular Hits",
            data: [33, 45, 37, 21, 55, 74, 69],
            fill: false,
            borderColor: "rgba(255,99,132,1)",
            lineTension: 0.1
          },
          {
            label: "Featured",
            data: [44, 19, 38, 46, 85, 66, 79],
            fill: false,
            borderColor: "rgba(153, 102, 255, 1)",
            lineTension: 0.1
          }
        ]
      },
      options: optionsLine
    };

    lineChart = new Chart(ctxLine, configLine);
  }
}

function updateChartOptions() {
  if ($(window).width() < width_threshold) {
    if (optionsLine) {
      optionsLine.maintainAspectRatio = false;
    }
  } else {
    if (optionsLine) {
      optionsLine.maintainAspectRatio = true;
    }
  }
}

function updateLineChart() {
  if (lineChart) {
    lineChart.options = optionsLine;
    lineChart.update();
  }
}

function reloadPage() {
  setTimeout(function() {
    window.location.reload();
  }); // Reload the page so that charts will display correctly
}

function drawCalendar() {
  if ($("#calendar").length) {
    $("#calendar").fullCalendar({
      height: 400,
      events: [
        {
          title: "Meeting",
          start: "2018-09-1",
          end: "2018-09-2"
        },
        {
          title: "Marketing trip",
          start: "2018-09-6",
          end: "2018-09-8"
        },
        {
          title: "Follow up",
          start: "2018-10-12"
        },
        {
          title: "Team",
          start: "2018-10-17"
        },
        {
          title: "Company Trip",
          start: "2018-10-25",
		  end: "2018-10-27"
        },
        {
          title: "Review",
          start: "2018-11-12"
        },
        {
          title: "Plan",
          start: "2018-11-18"
        }
      ],
      eventColor: "rgba(54, 162, 235, 0.4)"
    });
  }
}
