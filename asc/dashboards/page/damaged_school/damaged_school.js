
var floodmap = null;
var imagesmap = null;
var years = '';
var basicfacility = '';
var divisions = '';
var districts = '';
var jsondata = [];
var imagesdata = [];

let mydistrict = null
frappe.pages['damaged-school'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Flood Damaged Schools',
		single_column: true
	});

	$(frappe.render_template('damaged_school')).appendTo(page.main);
	//draw_map();
	filters.add(page);
	const d = new Date();
	let cyear = d.getFullYear() - 1;
	let myear = new Date().getFullYear().toString().substr(-2);
	years = cyear + '-' + myear;
	years = cyear + '-' + myear;
	load_data(years)

	window.addEventListener('locationchange', function () {
		console.log('location changed!');
	});

}
filters = {
	add: function (page) {
		var basic_facility_ = "Drinking Water"
		var year_ = "2021-22"

		if (frappe.get_route().length > 1) {
			if (frappe.get_route()[1]) {
				year_ = frappe.get_route()[1]
			}
			if (frappe.get_route()[2]) {
				basic_facility_ = frappe.get_route()[2]
			}
		}
		let year = page.add_field({
			label: "Year",
			fieldtype: "Link",
			fieldname: "Year",
			options: "Year",
			default: year_,
			reqd: 1,
		});
		let division = page.add_field({
			label: "Division",
			fieldtype: "Link",
			fieldname: "division",
			options: "Division",

		});
		mydistrict = page.add_field({
			"label": "District",
			"fieldtype": "Link",
			"fieldname": "district",
			"options": "District",

		});
		let basic_facility = page.add_field({
			label: "Damaged Facility",
			fieldtype: "Select",
			fieldname: "basic_facility",
			default: basic_facility_,
			options: ["", "Fully Damaged", "Partially Damaged", "School Converted in IDP"],
			reqd: 1,
		});
		let fiterbtn = page.add_field({
			label: "Update",
			fieldtype: "Button",
			fieldname: "filter",
			click() {
				if (basic_facility.get_value() == "" || year.get_value() == "") {
					if (year.get_value() == "" && basic_facility.get_value() == "") {
						frappe.msgprint("Please Select Year and Facility");
						return;
					}
					if (year.get_value() == "") {
						frappe.msgprint("Please Select Year");
						return;
					}
					if (division.get_value() == "") {
						frappe.msgprint("Please Select Division");
						return;
					}
					/* if (basic_facility.get_value() == "") {
						frappe.msgprint("Please Select Damaged Facility");
						return;
					} */

				} else {

					years = year.get_value();
					basicfacility = basic_facility.get_value();
					divisions = division.get_value();
					districts = mydistrict.get_value();


					load_data(year.get_value(), basic_facility.get_value(), division.get_value(), mydistrict.get_value());
				}
			},
		});






	},
};//end of filters
function setmapview() {
	setTimeout(function () { flood_map(jsondata); }, 400);

}
function setimageview() {
	setTimeout(function () { images_map(imagesdata); }, 400);

}
function setviewmap() {
	setTimeout(function () {
		if (districts != '') {
			frappe.call({
				method: "asc.dashboards.page.damaged_school.damaged_school.get_data",
				freeze: true,
				args: {
					basic_facility: basicfacility,
					year: years,
					division: divisions,
					district: districts,
					freeze: true
				},

				callback: function (r) {

					var data = r.message[0];


					if (district == "") {
						draw_divisional_map(r.message, basic_facility, year, true);
					} else {
						draw_map(r.message, district);
					}

				}
			});
		}
	}, 400);
}
function downloadtable() {
	$('#flooddetail').table2excel({
		exclude: ".noExl",
		name: "Flood Affected",
		exclude_img: true,
		exclude_links: true,
		exclude_inputs: true,
		preserveColors: true,
		filename: "Flood Affected Data"
	});
}
function load_data(year, basic_facility = '', division = '', district = '') {
	frappe.call({
		method: "asc.dashboards.page.damaged_school.damaged_school.get_data",
		freeze: true,
		args: {
			basic_facility: basic_facility,
			year: year,
			division: division,
			district: district,
			freeze: true,
		},

		callback: function (r) {

			var data = r.message[0];


			if (district == "") {
				draw_divisional_map(r.message, basic_facility, year, true);
			} else {
				draw_map(r.message, district);
			}

		}
	});

	frappe.call({
		method: "asc.dashboards.page.damaged_school.damaged_school.get_schools_data",
		freeze: true,
		args: {
			basic_facility: basic_facility,
			year: year,
			division: division,
			district: district,
			freeze: true,
		},

		callback: function (r) {

			jsondata = r.message;
			flood_map(r.message);


		}
	});

	frappe.call({
		method: "asc.dashboards.page.damaged_school.damaged_school.get_images_data",
		freeze: true,
		args: {
			basic_facility: basic_facility,
			year: year,
			division: division,
			district: district,
			freeze: true,
		},

		callback: function (r) {
			console.log("Images", r.message);
			imagesdata = r.message;
			images_map(r.message);


		}
	});

	frappe.call({
		method: "asc.dashboards.page.damaged_school.damaged_school.get_data_charts",
		freeze: true,
		args: {
			basic_facility: '',//basic_facility.get_value(),
			year: year,
			division: '',//division.get_value(),
			district: '',//district.get_value(),
			freeze: true,
		},

		callback: function (r) {
			console.log("bar_data", r.message);
			legend = true

			// $(frappe.render_template('district_table', { "data": r.message })).appendTo("#barContainer");
			$('#barContainer').empty();
			$(
				frappe.render_template("district_table", { "data": r.message })
			).appendTo('#barContainerdamaged');

			/* $('#flooddetail').empty();
			$(
				frappe.render_template("flood_detail", { "data": r.message })
			).appendTo('#flooddetail'); */


		}
	});

}


function flood_map(data) {
	(async () => {

		const floodedAreasGeoJson = await fetch(
			'/assets/semis_theme/js/geojson/sindh_flood_geo.json'
		).then(response => response.json());
		document.getElementById('floodcard').innerHTML = "<div id='school-gis-tool-map' style='width:100%; height:1000px;'></div>";
		var mbAttr = '';
		var mbUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';

		var streets = L.tileLayer(mbUrl, { id: 'mapbox/streets-v11', tileSize: 512, zoomOffset: -1, attribution: mbAttr });

		var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution: ''
		});

		var latSindh = 26.1806083;
		var longSindh = 68.7912237;

		floodmap = L.map('school-gis-tool-map', {
			center: [latSindh, longSindh],
			zoom: 8,
			layers: [osm, streets]
		});

		var baseLayers = {
			'Street': osm
		};

		var layerControl = L.control.layers(baseLayers).addTo(floodmap);

		var satellite = L.tileLayer(mbUrl, { id: 'mapbox/satellite-v9', tileSize: 512, zoomOffset: -1, attribution: mbAttr });
		layerControl.addBaseLayer(satellite, 'Satellite');
		var myLayer = L.geoJSON().addTo(floodmap);

		var geoJsonMappingsArray = [];
		geoJsonMappingsArray.push({ "geojson": floodedAreasGeoJson, "style": { color: "red", weight: 0.5, "fillOpacity": 0.3 } });
		var geoJsonLayers = [];
		geoJsonMappingsArray.forEach(geoJson => {
			var currentGeoJsonLayer = L.geoJSON(geoJson["geojson"], geoJson["style"]).addTo(floodmap);
			geoJsonLayers.push(currentGeoJsonLayer);
		});



		frappe.call({
			method: "frappe.desk.search.search_link",
			args: {
				txt: districts,
				page_length: 40,
				doctype: 'District',
			},
			callback: function (r) {
				console.log(r.results);
				var districtsdata = r.results;
				$.each(districtsdata, function (ind, dist) {
					var features = new Array();
					$.each(data, function (index, item) {
						if (dist.value == item.district) {
							var icons = '1';
							if (item.school_converted_in_idp_camps.toLowerCase() == 'yes') { icons = '4'; }
							if (item.fully.toLowerCase() == 'yes') { icons = '2'; }
							if (item.partially.toLowerCase() == 'yes') { icons = '3'; }
							if (item.fully.toLowerCase() == 'yes' && item.school_converted_in_idp_camps.toLowerCase() == 'yes') { icons = '5'; }
							if (item.partially.toLowerCase() == 'yes' && item.school_converted_in_idp_camps.toLowerCase() == 'yes') { icons = '6'; }

							/*
							<a class="btn btn-xs btn-default input-xs" href="/app/school-page/' + item.year + '/' + item.semis_code + '" target="_blank">Open Profile</a>  tac.semis_code as semiscode,
							*/
							features.push({ "type": "Feature", "id": index, "properties": { "schooltype": icons, "gender": item.school_gender, "level": item.level, "idp": item.school_converted_in_idp_camps, "fully": item.fully, "partially": item.partially, "address": item.School_name + '<br />Level: ' + item.level + '<br />School SEMIS Code: ' + item.semiscode + '<br />Type: ' + item.school_gender + '<br />Fully Damaged: ' + item.fully + '<br />Partially Damaged: ' + item.partially + '<br />School Converted in IDP Camps: ' + item.school_converted_in_idp_camps + '<br />No of Families Accommodated in School: ' + item.no_of_families + '<br />Population Accommodated (Estimated): ' + item.population_accomodated + '<br /><br /><br /><a style="margin-right:10px;" class="btn btn-xs btn-default input-xs" href="https://www.google.com/maps/place/' + item.lat + ',' + item.lng + '" target="_blank">Open Route</a>' }, "geometry": { "type": "Point", "coordinates": [item.lng, item.lat] } });

						}

					});

					var geoJsonData = {
						"type": "FeatureCollection",
						"features": features
					};
					var markers = L.markerClusterGroup();

					var geoJsonLayer = L.geoJson(geoJsonData, {
						style: function (feature) {
							console.log(feature.properties);
							return { color: feature.properties.color };
						},
						onEachFeature: function (feature, layer) {


							var icons = 'flood1.png';
							if (feature.properties.idp.toLowerCase() == 'yes') { icons = 'flood4.png'; }
							if (feature.properties.fully.toLowerCase() == 'yes') { icons = 'flood2.png'; }
							if (feature.properties.partially.toLowerCase() == 'yes') { icons = 'flood3.png'; }
							if (feature.properties.fully.toLowerCase() == 'yes' && feature.properties.idp.toLowerCase() == 'yes') { icons = 'flood5.png'; }
							if (feature.properties.partially.toLowerCase() == 'yes' && feature.properties.idp.toLowerCase() == 'yes') { icons = 'flood6.png'; }


							var myIcon = L.icon({
								iconUrl: '/assets/img/' + icons
							});

							layer.setIcon(myIcon);
							layer.bindPopup(feature.properties.address, { closeButton: false, closeOnClick: true });
						}
					});
					markers.addLayer(geoJsonLayer);

					floodmap.addLayer(markers);

				});
			}
		});

	})();

}

function images_map(data) {
	(async () => {

		const floodedAreasGeoJson = await fetch(
			'/assets/semis_theme/js/geojson/sindh_flood_geo.json'
		).then(response => response.json());
		document.getElementById('imagescard').innerHTML = "<div id='school-gis-table-map' style='width:100%; height:1000px;'></div>";
		var mbAttr = '';
		var mbUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';

		var streets = L.tileLayer(mbUrl, { id: 'mapbox/streets-v11', tileSize: 512, zoomOffset: -1, attribution: mbAttr });

		var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution: ''
		});

		var latSindh = 26.1806083;
		var longSindh = 68.7912237;

		imagesmap = L.map('school-gis-table-map', {
			center: [latSindh, longSindh],
			zoom: 8,
			layers: [osm, streets]
		});

		var baseLayers = {
			'Street': osm
		};

		var layerControl = L.control.layers(baseLayers).addTo(imagesmap);

		var satellite = L.tileLayer(mbUrl, { id: 'mapbox/satellite-v9', tileSize: 512, zoomOffset: -1, attribution: mbAttr });
		layerControl.addBaseLayer(satellite, 'Satellite');
		var myLayer = L.geoJSON().addTo(imagesmap);

		var geoJsonMappingsArray = [];
		geoJsonMappingsArray.push({ "geojson": floodedAreasGeoJson, "style": { color: "red", weight: 0.5, "fillOpacity": 0.3 } });
		var geoJsonLayers = [];
		geoJsonMappingsArray.forEach(geoJson => {
			var currentGeoJsonLayer = L.geoJSON(geoJson["geojson"], geoJson["style"]).addTo(imagesmap);
			geoJsonLayers.push(currentGeoJsonLayer);
		});



		frappe.call({
			method: "frappe.desk.search.search_link",
			args: {
				txt: districts,
				page_length: 40,
				doctype: 'District',
			},
			callback: function (r) {
				console.log(r.results);
				var districtsdata = r.results;
				$.each(districtsdata, function (ind, dist) {
					var features = new Array();
					$.each(data, function (index, item) {
						if (dist.value == item.district) {
							var icons = '1';
							// if (item.school_converted_in_idp_camps.toLowerCase() == 'yes') { icons = '4'; }
							// if (item.fully.toLowerCase() == 'yes') { icons = '2'; }
							// if (item.partially.toLowerCase() == 'yes') { icons = '3'; }
							// if (item.fully.toLowerCase() == 'yes' && item.school_converted_in_idp_camps.toLowerCase() == 'yes') { icons = '5'; }
							// if (item.partially.toLowerCase() == 'yes' && item.school_converted_in_idp_camps.toLowerCase() == 'yes') { icons = '6'; }

							/*
							<a class="btn btn-xs btn-default input-xs" href="/app/school-page/' + item.year + '/' + item.semis_code + '" target="_blank">Open Profile</a>  tac.semis_code as semiscode,
							*/
							features.push({ "type": "Feature", "id": index, "properties": { "schooltype": icons, "Name": item.name1, "address": '<img width="300" style="width:300px" src="' + item.image + '" alt="' + item.name1 + '" />' }, "geometry": { "type": "Point", "coordinates": [item.lng, item.lat] } });

						}

					});

					var geoJsonData = {
						"type": "FeatureCollection",
						"features": features
					};
					var markers = L.markerClusterGroup();

					var geoJsonLayer = L.geoJson(geoJsonData, {
						style: function (feature) {
							console.log(feature.properties);
							return { color: feature.properties.color };
						},
						onEachFeature: function (feature, layer) {


							var icons = 'flood-img-pin.png';
							// if (feature.properties.idp.toLowerCase() == 'yes') { icons = 'flood4.png'; }
							// if (feature.properties.fully.toLowerCase() == 'yes') { icons = 'flood2.png'; }
							// if (feature.properties.partially.toLowerCase() == 'yes') { icons = 'flood3.png'; }
							// if (feature.properties.fully.toLowerCase() == 'yes' && feature.properties.idp.toLowerCase() == 'yes') { icons = 'flood5.png'; }
							// if (feature.properties.partially.toLowerCase() == 'yes' && feature.properties.idp.toLowerCase() == 'yes') { icons = 'flood6.png'; }


							var myIcon = L.icon({
								iconUrl: '/assets/img/' + icons
							});

							layer.setIcon(myIcon);
							layer.bindPopup(feature.properties.address, { closeButton: false, closeOnClick: true });
						}
					});
					markers.addLayer(geoJsonLayer);

					imagesmap.addLayer(markers);

				});
			}
		});

	})();

}
function draw_map(data, district) {

	(async () => {
		document.getElementById('mapcard').innerHTML = "<div id='map_container_damaged' style='width:100%; height:1000px;'></div>";
		/* const geojsonSample = await fetch(
			'/assets/semis_theme/js/sindh-district.json'
		).then(response => response.json()); */

		var mbAttr = '';
		var mbUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';

		var streets = L.tileLayer(mbUrl, { id: 'mapbox/streets-v11', tileSize: 512, zoomOffset: -1, attribution: mbAttr });

		var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			/* maxZoom: 30, */
			attribution: ''
		});

		var map = L.map('map_container_damaged', {
			zoom: 10,
			layers: [osm, streets]
		});

		var baseLayers = {
			'Street': osm/* ,
			'Streets': streets */
		};

		var layerControl = L.control.layers(baseLayers).addTo(map);
		var satellite = L.tileLayer(mbUrl, { id: 'mapbox/satellite-v9', tileSize: 512, zoomOffset: -1, attribution: mbAttr });
		layerControl.addBaseLayer(satellite, 'Satellite');
		/* var myLayer = L.geoJSON().addTo(map);
		myLayer.addData(geojsonSample);
		 
		map.fitBounds(myLayer.getBounds()); */


		frappe.call({
			method: "asc.dashboards.page.damaged_school.damaged_school.get_districts",
			args: {
				district: district
			},
			callback: function (r) {
				var districtsdata = r.message;
				$.each(districtsdata, function (ind, dist) {
					var features = new Array();
					$.each(data, function (index, item) {
						if (dist.value == item.district) {

							var icons = '6';
							if (item.school_converted_in_idp_camps.toLowerCase() == 'yes') { icons = '9'; }
							if (item.fully.toLowerCase() == 'yes') { icons = '7'; }
							if (item.partially.toLowerCase() == 'yes') { icons = '8'; }


							features.push({ "type": "Feature", "id": index, "properties": { "schooltype": icons, "gender": item.school_gender, "level": item.level, "idp": item.school_converted_in_idp_camps, "fully": item.fully, "partially": item.partially, "address": item.School_name + '<br />Level: ' + item.level + 'School SEMIS Code: ' + item.semiscode + '<br /><br />Type: ' + item.school_gender + '<br />Fully Damaged: ' + item.fully + '<br />Partially Damaged: ' + item.partially + '<br />School Converted in IDP Camps: ' + item.school_converted_in_idp_camps + '<br />No of Families Accommodated in School: ' + item.no_of_families + '<br />Population Accommodated (Estimated): ' + item.population_accomodated + '<br /><br /><br /><a style="margin-right:10px;" class="btn btn-xs btn-default input-xs" href="https://www.google.com/maps/place/' + item.lat + ',' + item.lng + '" target="_blank">Open Route</a>' }, "geometry": { "type": "Point", "coordinates": [item.lng, item.lat] } });

						}

					});

					var geoJsonData = {
						"type": "FeatureCollection",
						"features": features
					};
					var markers = L.markerClusterGroup();

					var geoJsonLayer = L.geoJson(geoJsonData, {
						style: function (feature) {
							console.log(feature.properties);
							return { color: feature.properties.color };
						},
						onEachFeature: function (feature, layer) {
							var icons = 'flood1.png';
							if (feature.properties.idp.toLowerCase() == 'yes') { icons = 'flood4.png'; }
							if (feature.properties.fully.toLowerCase() == 'yes') { icons = 'flood2.png'; }
							if (feature.properties.partially.toLowerCase() == 'yes') { icons = 'flood3.png'; }
							if (feature.properties.fully.toLowerCase() == 'yes' && feature.properties.idp.toLowerCase() == 'yes') { icons = 'flood5.png'; }
							if (feature.properties.partially.toLowerCase() == 'yes' && feature.properties.idp.toLowerCase() == 'yes') { icons = 'flood6.png'; }

							var myIcon = L.icon({
								iconUrl: '/assets/img/' + icons
							});

							layer.setIcon(myIcon);
							layer.bindPopup(feature.properties.address, { closeButton: false, closeOnClick: true });
						}
					});
					markers.addLayer(geoJsonLayer);

					map.addLayer(markers);

				});
				var cities = [];
				$.each(districtsdata, function (index, item) {
					cities.push({
						"type": "Feature",
						"properties": { "color": "red", "fillColor": "transparent", "Id": item.code, "District": item.value, "Division": item.value, "Schools": 0 },
						"geometry": {
							"type": item.type,
							"coordinates": JSON.parse(item.coordinates)
						}
					});
				});

				var myStyle = {
					"fillColor": "transparent",
					"color": "red",
					"weight": 2.5,
					fillOpacity: 0,
					"opacity": 0.5
				};
				var districtsdetail = {
					"type": "FeatureCollection",
					"name": "B_Dist_Data30",
					"crs": {
						"type": "name",
						"properties": {
							"name": "urn:ogc:def:crs:OGC:1.3:CRS84"
						}
					},
					"features": cities
				};
				var myLayer = L.geoJSON(districtsdetail, {
					style: myStyle
				}).addTo(map);

				map.fitBounds(myLayer.getBounds());

			}
		});

		/* frappe.call({
			method: "frappe.desk.search.search_link",
			args: {
				txt: district,
				page_length:40,
				doctype: 'District',
			},
			callback: function (r) {
				console.log(r.results);
				var districtsdata = r.results;
				$.each(districtsdata, function (ind, dist) {
					var features = new Array();
					$.each(data, function (index, item) {
						if (dist.value == item.district) {
							 
							var icons = '6';
							if (item.school_converted_in_idp_camps.toLowerCase() == 'yes') { icons = '9'; }
							if (item.fully.toLowerCase() == 'yes') { icons = '7'; }
							if (item.partially.toLowerCase() == 'yes') { icons = '8'; }
 
							features.push({ "type": "Feature", "id": index, "properties": { "schooltype": icons, "gender": item.school_gender, "level": item.level, "idp": item.school_converted_in_idp_camps, "fully": item.fully, "partially": item.partially, "address": item.School_name + '<br />Level: ' + item.level + 'School SEMIS Code: ' + item.semiscode + '<br /><br />Type: ' + item.school_gender + '<br />Fully Damaged: ' + item.fully + '<br />Partially Damaged: ' + item.partially + '<br />School Converted in IDP Camps: ' + item.school_converted_in_idp_camps + '<br />No of Families Accommodated in School: ' + item.no_of_families + '<br />Population Accommodated (Estimated): ' + item.population_accomodated + '<br /><br /><br /><a style="margin-right:10px;" class="btn btn-xs btn-default input-xs" href="https://www.google.com/maps/place/' + item.lat + ',' + item.lng + '" target="_blank">Open Route</a>' }, "geometry": { "type": "Point", "coordinates": [item.lng, item.lat] } });

						}

					});

					var geoJsonData = {
						"type": "FeatureCollection",
						"features": features
					};
					var markers = L.markerClusterGroup();

					var geoJsonLayer = L.geoJson(geoJsonData, {
						style: function (feature) {
							console.log(feature.properties);
							return { color: feature.properties.color };
						},
						onEachFeature: function (feature, layer) {
 
							var icons = 'flood1.png';
							if (feature.properties.idp.toLowerCase() == 'yes') { icons = 'flood4.png'; }
							if (feature.properties.fully.toLowerCase() == 'yes') { icons = 'flood2.png'; }
							if (feature.properties.partially.toLowerCase() == 'yes') { icons = 'flood3.png'; }
							if (feature.properties.fully.toLowerCase() == 'yes' && feature.properties.idp.toLowerCase() == 'yes') { icons = 'flood5.png'; }
							if (feature.properties.partially.toLowerCase() == 'yes' && feature.properties.idp.toLowerCase() == 'yes') { icons = 'flood6.png'; }

							var myIcon = L.icon({
								iconUrl: '/assets/img/' + icons
							});

							layer.setIcon(myIcon);
							layer.bindPopup(feature.properties.address, { closeButton: false, closeOnClick: true });
						}
					});
					markers.addLayer(geoJsonLayer);

					map.addLayer(markers);

				}); 
			}
		});*/


	})();

}
function draw_divisional_map(adata, facility, year, page, basic_facility) {
	var series = [{
		type: 'map',
		enableMouseTracking: true,
		showInLegend: false,
		animation: {
			duration: 1000
		},
		borderColor: '#000000',
		data: adata,
		dataLabels: {
			enabled: true,
			color: '#FFFFFF',
			format: '{point.name} <br />( {point.value} )'
		},
		name: 'Schools Damaged',
		states: {
			hover: {
				borderColor: '#000000'
			}
		},
		tooltip: {
			pointFormat: 'District: {point.name} <br /> Total Schools: {point.totalschool}<br /> Fully Damaged Schools: {point.fulvalue}<br /> Partially Damaged Schools: {point.parvalue}<br /> School Converted in IDP: {point.idpvalue}<br /> No of Families Accommodated in School: {point.no_of_families}<br /> Population Accommodated (Estimated): {point.population_accomodated}<br /><br />'
		}
	}];
	Highcharts.mapChart('map_container_damaged', {
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
			dataClasses: [{
				color: "#cfc9c9",
				from: 0,
				name: "0-4",
				to: 4
			}, {
				color: "#ecfccd",
				from: 5,
				name: "4-142",
				to: 142
			}, {
				color: "#d5ed8e",
				from: 143,
				name: "143-318",
				to: 318
			}, {
				color: "#b9db51",
				from: 319,
				name: "319-505",
				to: 505
			}, {
				color: "#9ecd06",
				from: 506,
				name: "506 and above"
			}]
		},
		legend: {
			layout: 'vertical',
			align: 'left',
			verticalAlign: 'bottom',
			floating: true,

		},
		plotOptions: {
			series: {
				events: {
					click: function (e) {
						districts = e.point.name;
						mydistrict.set_value(districts);

						load_data(years, basicfacility, divisions, districts);

						/* frappe.call({
							method: "asc.dashboards.page.damaged_school.damaged_school.get_data",
							freeze: true,
							args: {
								basic_facility: facility,
								year: year,
								division: '',
								district: districts,
								freeze: true,
							},

							callback: function (r) {
								 
								draw_map(r.message, districts); 
							}
						}); */
					}
				}
			}
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


function barChart2(data_, facility_name, container, legend, type, height) {

	categoery = []
	facility_yes = []
	facility_no = []
	facility_safe = []
	facility_available = []
	facility_not_available = []
	for (let i = 0; i < data_.length; i++) {
		categoery[i] = data_[i].name;
		facility_yes[i] = data_[i].fulvalue;
		facility_no[i] = data_[i].parvalue;
		facility_safe[i] = parseFloat((parseFloat(data_[i].totalschool) - parseFloat(data_[i].value)).toFixed(1));
		facility_available[i] = data_[i].value;
		facility_not_available[i] = parseFloat((parseFloat(data_[i].totalschool) - parseFloat(data_[i].value)).toFixed(1));
	}

	Highcharts.chart(container, {
		chart: {
			type: type,
			// width: 450,
		},
		credits: {
			enabled: false,
		},
		title: {
			text: facility_name,
			align: 'left',
			style: {
				fontWeight: 'bold',
				fontSize: '16px',
			}
		},
		xAxis: {
			categories: categoery,
			crosshair: true
		},
		yAxis: {
			min: 0,
			title: {
				text: ""
			}
		},
		legend: {
			reversed: true,
			enabled: legend,
		},

		plotOptions: {
			series: {
				pointWidth: 28,
				stacking: 'percent',
				dataLabels: {
					enabled: true,
					formatter: function () {
						if (this.y) {
							return this.y;
						}
					},
					position: "left",
					allowOverlap: true,
					crop: false,
					padding: 0,

				},
			}
		},
		series: [{
			name: "Fully Damaged",
			data: facility_yes,
			color: 'red',
		}, {
			name: "Partially Damaged",
			data: facility_no,
			color: 'yellow',
		}, {
			name: 'Safe Schools',
			data: facility_safe,
			color: 'green',


		}]
	});




}