
	var series = [{
		type: 'map',
		enableMouseTracking: true,
		showInLegend: false,
		animation: {
			duration: 1000
		},
		data:adata,
		dataLabels: {
			enabled: true,
			color: '#FFFFFF',
			format: '{point.name} <br />(ECCE Schools {point.ECE_Schools} )'
		},
		name: 'ECE Schools Map',
		states: {
			hover: {
				borderColor: '#FFFFFF'
			}
		},
		tooltip: {
			pointFormat: 'District: {point.name} <br /> Total Schools: {point.Total_Schools}<br />Schools with ECCE Enrollemt: {point.ECE_Schools} ({point.value}%)<br />Without ECCE Enrollemt: {point.No_ECE_Schools}<br />'
		}
	}];
	Highcharts.mapChart('map_container', {
		title: {
			text: ''
		},
		mapNavigation: {
            enabled: true,
            buttonOptions: {
                alignTo: 'spacingBox',
                x: 10
            }
        },
		colorAxis: {
            min: 0,
            stops: [
                [0, '#ff0000'], //red
                [0.2, '#ffffff'], //white
                [0.5, '#57F442'], //light green
                [1, '#064E14'] //green
            ]
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'bottom'
        },
	   credits: {
					enabled: false,
				},
		exporting: {
			enabled: true
		}, 
		series: series
	});
}
