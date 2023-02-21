// Copyright (c) 2022, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('LSU Performance Dashboard', {
	// refresh: function(frm) {

	// }

	onload: function (frm) {
		frm.disable_save();
		frappe.call({
			method: "asc.asc.doctype.lsu_performance_dashboard.lsu_performance_dashboard.get_data",
			callback: function (r) {
				$(frm.fields_dict.dashboard_container.wrapper).empty();
				data = r.message
				var rows;
				var data;
				if (data[1].length > 0) {
					rows = get_rows(r.message)
					data = get_table(r.message, rows)
				} else {
					data = get_table(r.message, ``)
				}
				$(data).appendTo(frm.fields_dict.dashboard_container.wrapper);
			}
		});
	},



});

function get_rows(data) {
	var rows_string = "";
	for (var i = 0; i < data[1].length; i++) {
		var pending = data[1][i]['assigned'] - (data[1][i]['user_completed_schools'] + data[1][i]['user_not_completed'] + data[1][i]['user_verified_schools'])
		rows_string += `<tr class="ptr">
			<td style="border:1px solid #000000;text-align:center">` + data[1][i]['user_name'] + `</td>
			<td style="border:1px solid #000000;text-align:center">` + data[1][i]['assigned'] + `</td>
			<td style="border:1px solid #000000;text-align:center">` + data[1][i]['user_completed_schools'] + `</td>
			<td style="border:1px solid #000000;text-align:center">` + data[1][i]['user_not_completed'] + `</td>
			<td style="border:1px solid #000000;text-align:center">` + data[1][i]['user_verified_schools'] + `</td>
			<td style="border:1px solid #000000;text-align:center">` + pending + `</td></tr>`
	}
	return rows_string;
}


function get_table(data_, rows) {
	var not_assigned = data_[2]['total_schools'] - data_[0][0]['assigned_schools']
	var pending = data_[0][0]['assigned_schools'] - (data_[3]['completed'] + data_[3]['not_completed'] + data_[3]['verified'])

	var message_ = `<style>
	
	#counts{
		display: flex;
		justify-content: space-around;
		margin-bottom:2.5em;
		
	}
	.singleCount{
		text-align:center;
		border-radius: 14px;
		box-shadow: 0px 0px 7px 2px #9d9593a1;
		justify-content: center;
	
		align-item:center;
		font-size:1vw;
		padding:5px;
		margin-bottom: 35px;
	}
	.singleCount1{
	text-align:center;
    border-radius: 14px;
		box-shadow: 0px 0px 7px 2px #9d9593a1;
	
		justify-content:center;
		align-item:center;
		padding:10px;
		margin-bottom: 35px;
	}
	.value_count{
		font-size:40px;
		color:white;
		font-family: sans-serif;
	}

	.counter{
		font-size: 15px;
		color:white;
		border-top-left-radius:5px;
		border-top-right-radius:5px;
		margin-bottom:7px;
		font-family: monospace;

	}
</style>

<div class="row">
<div class="col-md-3">
<div class="singleCount1" style="background-image: linear-gradient(to left, #0db2de 0%, #005bea 100%) !important;">
<span class="value_count">`+ data_[2]['total_schools'].toLocaleString("en-US") + `</span><br>
<div class="counter" >Total Schools</div>
</div>
</div>
<div class="col-md-3">
<div class="singleCount1" style="background-image: linear-gradient(to left, #efa65f, #f76a2d) !important;">
<span class="value_count">`+ data_[0][0]['assigned_schools'].toLocaleString("en-US") + `</span><br>
<div class="counter">Assigned Schools</div>
</div>
</div>
<div class="col-md-3">
<div class="singleCount1" style="    background-image: linear-gradient( 45deg, #f31717, #f7778c) !important;">
<span class="value_count">`+ not_assigned.toLocaleString("en-US") + `</span><br>
<div class="counter" >Not Assigned Schools</div>
</div>

</div>
<div class="col-md-3">
<div class="singleCount1" style="    background-image: linear-gradient( 45deg, #19547b, #ffd89b) !important;">
<span class="value_count">`+ data_[2]['tid_schools'].toLocaleString("en-US") + `</span><br>
<div class="counter" >Schools with T.ID</div>
</div>

</div>



<div class="col-md-3">

<div class="singleCount"  style="background-color: #399951;">
<span class="value_count">`+ data_[3]['verified'].toLocaleString("en-US") + `</span><br>
<div class="counter" >Verified Form</div>
</div>
</div>

<div class="col-md-3">

<div class="singleCount"  style="background-color: #0370e7;">
<span class="value_count">`+ data_[3]['completed'].toLocaleString("en-US") + `</span><br>
<div  class="counter" >Complete Form</div>
</div>
</div>

<div class="col-md-3">

<div class="singleCount"  style="  background-color: #53585d;">
<span class="value_count">`+ data_[3]['not_completed'].toLocaleString("en-US") + `</span><br>
<div class="counter" >Incomplete Form</div>
</div>
</div>

<div class="col-md-3">

<div class="singleCount"  style="background-color:#FF0000;">
<span class="value_count">`+ pending.toLocaleString("en-US") + `</span><br>
<div class="counter" >No Data</div>
</div>
</div>

</div>

		`


	if (data_[1].length > 0) {
		message_ += `
		<div class="table-responsive">
		<table  width="100%" cellpadding="5" cellspacing="0" style="border: 1px solid #000000;padding:7px; border-spacing: 1px; border-collapse: collapse;text-align:center">
			<tr style="font-size:16px; background-color:#75b17f; color: white;">
				<th style="border:1px solid #000000;text-align:center">User Name</th>
				<th style="border:1px solid #000000;text-align:center">Assigned Schools</th>
				<th style="border:1px solid #000000;text-align:center">Complete Form</th>
				<th style="border:1px solid #000000;text-align:center">Incompleted Form</th>
				<th style="border:1px solid #000000;text-align:center">Verified</th>
				<th style="border:1px solid #000000;text-align:center">No Data</th>
			</tr>` + rows
		message_ += `</table> </div> `;
	}
	return message_;
}

