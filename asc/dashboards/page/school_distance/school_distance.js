frappe.pages['school-distance'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Online School Distance Checker',
		single_column: true
	});

	$(frappe.render_template('school_distance')).appendTo(page.main);

	filters.add(page);


}
let schooldistmap = null;
let route = [];
let distances = 1;
let distancetype = 1;
filters = {
	add: function (page) {
		let distancefield = page.add_field({
			label: 'Find School',
			fieldtype: 'Select',
			fieldname: 'distance',
			reqd: 1,
			options: [
				'Find School Distance',
				'Find Nearby School'
			],
			change() {
				console.log(distancefield);
				var distance = distancefield.get_value()
				if (distance == 'Find School Distance') {
					toSchoolfield.toggle(1);
					distnceoption.toggle(1);
					nearbyfield.toggle(0);
				} else {
					toSchoolfield.toggle(0);
					nearbyfield.toggle(1);
					distnceoption.toggle(0);
				}
				console.log(distancefield.get_value());
			}
		});
		let fromSchoolfield = page.add_field({
			label: "From School",
			fieldtype: "Link",
			fieldname: "FromSchool",
			options: "School",
			reqd: 1,
		});
		let toSchoolfield = page.add_field({
			label: "To School",
			fieldtype: "Link",
			fieldname: "ToSchool",
			options: "School"
		});
		let nearbyfield = page.add_field({
			label: 'Range Area (mtr)',
			fieldtype: 'Select',
			fieldname: 'nearby',
			reqd: 1,
			options: [
				'500',
				'1000',
				'1500',
				'2000'
			],
			change() {
				console.log(nearbyfield.get_value());
			}
		});
		let distnceoption = page.add_field({
			label: 'Range Area (mtr)',
			fieldtype: 'Select',
			fieldname: 'nearby',
			reqd: 1,
			options: [
				'Point to Point',
				'By Road'
			],
			change() {
				console.log(distnceoption.get_value());
			}
		});

		let fiterbtn = page.add_field({
			label: "View",
			fieldtype: "Button",
			fieldname: "filter",
			click() {

				var distance = distancefield.get_value();
				let semisfrom = fromSchoolfield.get_value();
				let semisto = toSchoolfield.get_value();
				let distancenearby = nearbyfield.get_value();
				let distanceopt = distnceoption.get_value();
				if (distanceopt == 'By Road') {
					distancetype = 2;
				} else {
					distancetype = 1;
				}
				if (distance == 'Find School Distance' && (semisfrom == '' || semisto == '')) {
					frappe.throw(__('Please select From & To School'))
				} else if (semisfrom == '' || distancenearby == '') {
					frappe.throw(__('Please select From & Range Area (mtr)'))
				}

				if (distance == 'Find School Distance') {
					distances = 1;
				} else {
					distances = 2;
				}


				loadschooldata(distances, semisfrom, semisto, distancenearby);
			}
		});

		distancefield.set_value('Find School Distance');
		distnceoption.set_value('By Road');
	}
};


function loadschooldata(distance, semisfrom, semisto, distancenearby) {

	frappe.call({
		method: "asc.dashboards.page.school_distance.school_distance.get_data",
		freeze: true,
		args: {
			distance: distance,
			semisfrom: semisfrom,
			semisto: semisto,
			nearby: semisfrom,
			distancenearby: distancenearby,
			freeze: true
		},

		callback: function (r) {
			school_distance_map(r.message)
		}
	});
}

function oldloadschooldata() {
	let distance = $('input[name="distance"]:checked').val();
	let semisfrom = $('#semisfrom').val();
	let semisto = $('#semisto').val();
	let nearby = $('#nearby').val();
	let distancenearby = $('#distancenearby').val();
	if (distance == 1) {
		if (semisfrom == '' || semisfrom == null) {
			frappe.throw(__('Please enter SEMIS From #'))
		}
		if (semisto == '' || semisto == null) {
			frappe.throw(__('Please enter SEMIS To #'))
		}
	} else if (distance == 2) {
		if (nearby == '' || nearby == null) {
			frappe.throw(__('Please enter Nearby School SEMIS From#'))
		}
		if (distancenearby == '' || distancenearby == null) {
			frappe.throw(__('Please enter Range Area (mtr)'))
		}
	}
	frappe.call({
		method: "asc.dashboards.page.school_distance.school_distance.get_data",
		freeze: true,
		args: {
			distance: distance,
			semisfrom: semisfrom,
			semisto: semisto,
			nearby: nearby,
			distancenearby: distancenearby,
			freeze: true
		},

		callback: function (r) {
			school_distance_map(r.message)
		}
	});
}


function school_distance_map(data) {
	if (distances == 1) {
		document.getElementById('result_div').innerHTML = "<div id='ContentPlaceHolder1_result_div' class='alert alert-success'></div><div id='school-distance-map' style='width:100%; height:1000px;z-index:0;'></div>";
	} else {
		document.getElementById('result_div').innerHTML = "<div id='school-distance-map' style='width:100%; height:1000px;z-index:0;'></div>";
	}

	var mbAttr = '';
	var mbUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';

	var streets = L.tileLayer(mbUrl, { id: 'mapbox/streets-v11', tileSize: 512, zoomOffset: -1, attribution: mbAttr });

	var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		attribution: ''
	});

	let frommapschool = data[0];
	var latSindh = parseFloat(frommapschool[0].latn);
	var longSindh = parseFloat(frommapschool[0].lone);

	schooldistmap = L.map('school-distance-map', {
		center: [longSindh, latSindh],
		zoom: 16,
		layers: [osm, streets]
	});

	var baseLayers = {
		'Street': osm
	};

	var layerControl = L.control.layers(baseLayers).addTo(schooldistmap);

	var satellite = L.tileLayer(mbUrl, { id: 'mapbox/satellite-v9', tileSize: 512, zoomOffset: -1, attribution: mbAttr });
	layerControl.addBaseLayer(satellite, 'Satellite');

	// show the scale bar on the lower left corner
	L.control.scale({ imperial: true, metric: true }).addTo(schooldistmap);


	let fromschool = data[0];
	let toschools = data[1];
	let address = fromschool[0].school_name + " <br /> Type: " + fromschool[0].gender + " <br /> Level: " + fromschool[0].level + " <br /> SEMIS: " + fromschool[0].name;
	add_mapmarker(fromschool[0].latn, fromschool[0].lone, address, 'targetschool.png');

	/* schooldistmap.setCenter([fromschool[0].latn, fromschool[0].lone]); */
	if (distances == 2) {
		var rad = 1500;
		var circle = L.circle([parseFloat(fromschool[0].lone), parseFloat(fromschool[0].latn)], {
			radius: rad,
			color: 'green',
			fillColor: 'green',
			fillRule: 'nonzero',
			fillOpacity: 1,
			opacity: 1
		}).addTo(schooldistmap);


		var rad = 1000;
		var circle = L.circle([parseFloat(fromschool[0].lone), parseFloat(fromschool[0].latn)], {
			radius: rad,
			color: 'yellow',
			fillColor: 'yellow',
			fillRule: 'nonzero',
			fillOpacity: 1,
			opacity: 1
		}).addTo(schooldistmap);

		var rad = 500;

		/*  L.circleMarker([parseFloat(fromschool[0].lone), parseFloat(fromschool[0].latn)], {
		  radius: rad,
		  color: '#5d78ff',
		  fillColor: '#f03',
		  fillOpacity: 0.2,
		  opacity: 1   
		}).addTo(schooldistmap);  */

		var circle = L.circle([parseFloat(fromschool[0].lone), parseFloat(fromschool[0].latn)], {
			radius: rad,
			color: '#5d78ff',
			fillColor: '#f03',
			fillRule: 'nonzero',
			fillOpacity: 1,
			opacity: 1
		}).addTo(schooldistmap);

	}

	$.each(toschools, function (index, item) {
		var popup = item.school_name + " <br /> Type: " + item.gender + " <br /> Level: " + item.level + " <br /> Status: " + item.status + " <br /> SEMIS: <strong>" + item.name + "</strong> <br /> Distance From SEMIS #: <strong>" + fromschool[0].name + "</strong> - in  <strong>" + (item.distance.toFixed(2) / 1000).toFixed(2) + "</strong> Kilometers or  <strong>" + item.distance.toFixed(2) + "</strong> Meters.";
		var icon = 'distance1.png';
		if (item.status == 'Closed') {
			icon = 'distance2.png';
		}
		add_mapmarker(item.lats, item.lngs, popup, icon);

		if (distances == 1) {
			document.getElementById('ContentPlaceHolder1_result_div').innerHTML = 'Total Distance  in <strong>' + (item.distance.toFixed(2) / 1000).toFixed(2) + '</strong> Kilometers or  <strong>' + item.distance.toFixed(2) + '</strong> Meters.';


		}
	});
	if (distances == 1) {
		$.each(toschools, function (index, item) {
			if (distancetype == 2) {
				L.Routing.Line = L.Routing.Line.extend({
					options: {
						styles: [
							{ color: 'black', opacity: 0.15, weight: 9 },
							{ color: 'white', opacity: 0.8, weight: 6 },
							{ color: 'red', opacity: 1, weight: 2 }
						],
						missingRouteStyles: [
							{ color: 'black', opacity: 0.15, weight: 7 },
							{ color: 'white', opacity: 0.6, weight: 4 },
							{ color: 'gray', opacity: 0.8, weight: 2, dashArray: '7,12' }
						],
						addWaypoints: false,
						extendToWaypoints: true,
						missingRouteTolerance: 10
					}
				});

				L.Routing.control({
					lineOptions: {
						addWaypoints: false
					},
					draggableWaypoints: false,
					showAlternatives: true,
					/* autoRoute:false, */
					waypoints: [
						L.latLng(parseFloat(item.lone), parseFloat(item.latn)),
						L.latLng(parseFloat(item.lngs), parseFloat(item.lats))
					]
				}).addTo(schooldistmap);
			} else {
				var pointA = new L.latLng(parseFloat(item.lone), parseFloat(item.latn));
				var pointB = new L.latLng(parseFloat(item.lngs), parseFloat(item.lats));
				var pointList = [pointA, pointB];

				var firstpolyline = new L.polyline(pointList, {
					color: 'red',
					weight: 3,
					opacity: 0.5,
					smoothFactor: 1
				});
				firstpolyline.addTo(schooldistmap);
			}

		});
	}
}

function add_mapmarker(latitude, longitude, detail, icons) {
	var myIcon = L.icon({
		iconSize: [24, 24],
		iconUrl: '/assets/img/' + icons
	});
	L.marker([parseFloat(longitude), parseFloat(latitude)], { icon: myIcon }).addTo(schooldistmap).bindPopup(detail);
}