frappe.pages['school-location'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'School Location',
		single_column: true
	});
	$(frappe.render_template('school_location')).appendTo(page.main);
	//draw_map();
	filters.add(page);
}
filters = {
	add: function (page) {
		let year = page.add_field({
			"label": "Year",
			"fieldtype": "Link",
			"fieldname": "Year",
			"options": "Year",
			"hidden": 1,
			"default": "2021-22"
		});
		let division = page.add_field({
			"label": "Division",
			"fieldtype": "Link",
			"fieldname": "division",
			"options": "Division"
		});
		let district = page.add_field({
			"label": "District",
			"fieldtype": "Link",
			"fieldname": "district",
			"options": "District",
			"get_query": function () {
				return {
					"filters": {
						"division": division.get_value("division"),
					}
				}
			}
		});
		let gender = page.add_field({
			"label": "Gender",
			"fieldtype": "Link",
			"fieldname": "gender",
			"options": "School Gender"
		});
		let level = page.add_field({
			"label": "Level",
			"fieldtype": "Link",
			"fieldname": "level",
			"options": "Level"
		});
		let status = page.add_field({
			"label": "Status",
			"fieldtype": "Link",
			"fieldname": "status",
			"options": "School Status"
		});
		let schools_having = page.add_field({
			"label": "Schools Having",
			"fieldtype": "Select",
			"fieldname": "schools_having",
			"options": ["", "SEMIS Code", "Tracking ID"]
		});

		let fiterbtn = page.add_field({
			"label": "Load Map",
			"fieldtype": "Button",
			"fieldname": "filter",
			click() {
				$('#map_container').empty();
				$('#loader').remove();
				var img = $('<img />', {
					id: 'loader',
					src: '/assets/img/loading.gif',
					alt: 'Loading',
					style: 'text-align:center; margin:0 auto; display:block'
				});
				img.appendTo($('#map_container'));
				page_data(district.get_value(), year.get_value(), division.get_value(), gender.get_value(), level.get_value(), status.get_value(), schools_having.get_value())
			}
		});
		page_data(district.get_value(), year.get_value(), division.get_value(), gender.get_value(), level.get_value(), status.get_value(), schools_having.get_value())
	}
}
function page_data(district_, year, division, gender, level, status, schools_having) {
	frappe.call({
		method: "asc.dashboards.page.school_location.school_location.get_data",
		args: {
			district: district_,
			year: year,
			division: division,
			gender: gender,
			level: level,
			status: status,
			schools_having: schools_having
		},
		freeze: true,
		callback: function (r) {
			$('#loader').remove();
			draw_map(r.message, district_);
		}
	});
}
function draw_map(data, district) {

	(async () => {
		document.getElementById('mapcardschool').innerHTML = "<div id='map_container_school' style='width:100%; height:1000px;z-index: 1;'></div>";
		// const geojsonSample = await fetch(
		// 	'/assets/semis_theme/js/sindh-district.json'
		// ).then(response => response.json()); 

		var mbAttr = '';
		var mbUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';

		var streets = L.tileLayer(mbUrl, { id: 'mapbox/streets-v11', tileSize: 512, zoomOffset: -1, attribution: mbAttr });

		var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			/* maxZoom: 30, */
			attribution: ''
		});

		var map = L.map('map_container_school', {
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

		/* 
		 var myStyle = {
						"fillColor": "transparent",
						"color": "red",
						"weight": 2.5,
						fillOpacity: 0,
						"opacity": 0.5
					};
		 
				 
				var myLayer = L.geoJSON(geojsonSample,{
						style: myStyle
					}).addTo(map);
					 
				 
				 map.fitBounds(myLayer.getBounds()); */

		/* frappe.call({
			method: "frappe.desk.search.search_link",
			args: {
				txt: district,
				page_length: 40,
				doctype: 'District',
			},
			callback: function (r) {
				var districts = r.results;
				$.each(districts, function (ind, dist) {
					var features = new Array();
					
					$.each(data, function (index, item) {
						if (dist.value == item.district) {
							var icons = '0';
							if (item.level == 'Primary') { icons = '1'; }
							if (item.level == 'Middle') { icons = '2'; }
							if (item.level == 'Secondary') { icons = '3'; }
							if (item.level == 'Higher Secondary') { icons = '4'; }
							if (item.level == 'Elementary') { icons = '5'; }
	
							features.push({ "type": "Feature", "id": index, "properties": { "color": "red","schooltype": icons, "level": item.level, "schoolInfo": '<span class="fw-bold">' + item.School_name + '</span><br />SEMIS Code: ' + item.semis_code + '<br />Level: ' + item.level + '<br />Gender: ' + item.school_gender + '<br />Status: ' + item.status + '<br />District: ' + item.district + '<br /><a class="btn btn-xs btn-default input-xs" href="/app/school-page/2021-22/' + item.semis_code + '" target="_blank">Open Profile</a>' + '  <a class="btn btn-xs btn-default input-xs" href="https://www.google.com/maps/place/' + item.gps_coordinateslatitude + "," + item.gps_coordinateslongitude + '" target="_blank">Get Direction</a>' }, "geometry": { "type": "Point", "coordinates": [item.gps_coordinateslongitude, item.gps_coordinateslatitude] } });
						}
	
					});
	
					var geoJsonData = {
						"type": "FeatureCollection",
						"features": features
					};
					var markers = L.markerClusterGroup();
	
					var geoJsonLayer = L.geoJson(geoJsonData, {
						style: function (feature) {
							return { color: feature.properties.color };
						},
						onEachFeature: function (feature, layer) {
	
							var icons = '';
							if (feature.properties.level == 'Primary') { icons = 'icon-1.png'; }
							if (feature.properties.level == 'Middle') { icons = 'icon-2.png'; }
							if (feature.properties.level == 'Secondary') { icons = 'icon-3.png'; }
							if (feature.properties.level == 'Higher Secondary') { icons = 'icon-4.png'; }
							if (feature.properties.level == 'Elementary') { icons = 'icon-5.png'; }
							var myIcon = L.icon({
								iconUrl: '/assets/img/' + icons
							});
							layer.setIcon(myIcon);
							layer.bindPopup(feature.properties.schoolInfo);
						}
					});
					markers.addLayer(geoJsonLayer);
	
					map.addLayer(markers);
	
				});	
			} 	
		});*/


		frappe.call({
			method: "asc.dashboards.page.school_location.school_location.get_districts",
			args: {
				district: district
			},
			callback: function (r) {
				var districts = r.message;
				$.each(districts, function (ind, dist) {
					var features = new Array();

					$.each(data, function (index, item) {
						if (dist.value == item.district) {
							var icons = '0';
							if (item.level == 'Primary') { icons = '1'; }
							if (item.level == 'Middle') { icons = '2'; }
							if (item.level == 'Secondary') { icons = '3'; }
							if (item.level == 'Higher Secondary') { icons = '4'; }
							if (item.level == 'Elementary') { icons = '5'; }

							features.push({ "type": "Feature", "id": index, "properties": { "color": "red", "schooltype": icons, "level": item.level, "schoolInfo": '<span class="fw-bold">' + item.School_name + '</span><br />SEMIS Code: ' + item.semis_code + '<br />Level: ' + item.level + '<br />Gender: ' + item.school_gender + '<br />Status: ' + item.status + '<br />District: ' + item.district + '<br /><a class="btn btn-xs btn-default input-xs" href="/app/school-page/2021-22/' + item.semis_code + '" target="_blank">Open Profile</a>' + '  <a class="btn btn-xs btn-default input-xs" href="https://www.google.com/maps/place/' + item.gps_coordinateslatitude + "," + item.gps_coordinateslongitude + '" target="_blank">Get Direction</a>' }, "geometry": { "type": "Point", "coordinates": [item.gps_coordinateslongitude, item.gps_coordinateslatitude] } });
						}

					});

					var geoJsonData = {
						"type": "FeatureCollection",
						"features": features
					};
					var markers = L.markerClusterGroup();

					var geoJsonLayer = L.geoJson(geoJsonData, {
						style: function (feature) {
							return { color: feature.properties.color };
						},
						onEachFeature: function (feature, layer) {

							var icons = '';
							if (feature.properties.level == 'Primary') { icons = 'icon-1.png'; }
							if (feature.properties.level == 'Middle') { icons = 'icon-2.png'; }
							if (feature.properties.level == 'Secondary') { icons = 'icon-3.png'; }
							if (feature.properties.level == 'Higher Secondary') { icons = 'icon-4.png'; }
							if (feature.properties.level == 'Elementary') { icons = 'icon-5.png'; }
							var myIcon = L.icon({
								iconUrl: '/assets/img/' + icons
							});
							layer.setIcon(myIcon);
							layer.bindPopup(feature.properties.schoolInfo);
						}
					});
					markers.addLayer(geoJsonLayer);

					map.addLayer(markers);

				});

				var cities = [];
				$.each(districts, function (index, item) {
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


	})();

}
