frappe.pages['district-profile'].on_page_load = function (wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'District Profile',
        single_column: true
    });
    filters.add(page);
    // school_status();
    // piechart();
    // piechart2();
    // piechart3();
    // piechart4();
};
var print_data;
var district;
var year;

filters = {
    add: function (page) {
        let year = page.add_field({
            label: "Year",
            fieldtype: "Link",
            fieldname: "Year",
            options: "Year",
            default: "2021-22",
            reqd: 1
        });
        let district = page.add_field({
            label: "District",
            fieldtype: "Link",
            fieldname: "district",
            options: "District",
            reqd: 1
        });
        let fiterbtn = page.add_field({
            label: "View",
            fieldtype: "Button",
            fieldname: "filter",
            click() {
                if (district.get_value() == "" || year.get_value() == "") {
                    return;
                }
                $('#loader').remove();
                $('#districtProfile').remove();
                var img = $('<img />', {
                    id: 'loader',
                    src: '/assets/img/loading.gif',
                    alt: 'Loading',
                    style: 'text-align:center; margin:0 auto; display:block'
                });
                img.appendTo(page.main);
                var year_based_status;
                frappe.call({
                    method: "asc.dashboards.page.district_profile.district_profile.year_based_status",
                    args: {
                        district: district.get_value(),
                        year: year.get_value(),
                    },
                    callback: function (r) {
                        year_based_status = r.message
                    },
                });
                frappe.call({
                    method: "asc.dashboards.page.district_profile.district_profile.get_data",
                    args: {
                        district: district.get_value(),
                        year: year.get_value(),
                    },


                    callback: function (r) {
                        $('#districtProfile').remove();
                        $('#loader').remove();
                        $(
                            frappe.render_template("district_profile", r.message[0])
                        ).appendTo(page.main);
                        // year = year.get_value()
                        // district = district.get_value()
                        // print_data = r.message[0]
                        // console.log(r.message[0]);
                        // console.log("dfhjasdfh", print_data);
                        $('#drinking_water').css('width', r.message[0].water_percentage + '%')
                        $('#electricity').css('width', r.message[0].electricity_percentage + '%')
                        $('#toilet').css('width', r.message[0].toilet_percentage + '%')
                        $('#boundary_wall').css('width', r.message[0].boundary_wall_percentage + '%')
                        $('#science_lab').css('width', r.message[0].science_lab_percentage + '%')
                        $('#library').css('width', r.message[0].library_percentage + '%')
                        $('#computer_lab').css('width', r.message[0].computer_lab_percentage + '%')
                        $('#hand_wash_facility_').css('width', r.message[0].hand_wash_percentage + '%')
                        $('#soap').css('width', r.message[0].soap_percentage + '%')
                        $('#fans').css('width', r.message[0].fans_percentage + '%')
                        $('#tv').css('width', r.message[0].tv_percentage + '%')
                        $('#projector').css('width', r.message[0].proj_percentage + '%')
                        $('#comp').css('width', r.message[0].comp_percentage + '%')
                        $('#ground').css('width', r.message[0].ground_percentage + '%')
                        $('[data-bs-toggle="tooltip"]').tooltip();
                        $('#drinking_water').attr('title', r.message[0].water_percentage + '%');
                        $('#electricity').attr('title', r.message[0].electricity_percentage + '%')
                        $('#toilet').attr('title', r.message[0].toilet_percentage + '%')
                        $('#boundary_wall').attr('title', r.message[0].boundary_wall_percentage + '%')
                        $('#science_lab').attr('title', r.message[0].science_lab_percentage + '%')
                        $('#library').attr('title', r.message[0].library_percentage + '%')
                        $('#computer_lab').attr('title', r.message[0].computer_lab_percentage + '%')
                        $('#hand_wash_facility_').attr('title', r.message[0].hand_wash_percentage + '%')
                        $('#soap').attr('title', r.message[0].soap_percentage + '%')
                        $('#fans').attr('title', r.message[0].fans_percentage + '%')
                        $('#tv').attr('title', r.message[0].tv_percentage + '%')
                        $('#projector').attr('title', r.message[0].proj_percentage + '%')
                        $('#comp').attr('title', r.message[0].comp_percentage + '%')
                        $('#ground').attr('title', r.message[0].ground_percentage + '%')
                        teacherPerYear(r.message[2]);
                        enrollmentPerYear(r.message[2]);
                        schoolwise(year_based_status);
                        piechart();
                        piechart2();
                        piechart3();
                        piechart4();
                    },
                });
            },
        });
        // let print = page.add_field({
        //   label: "Print",
        //   fieldtype: "Button",
        //   fieldname: "print",
        //   click() {
        //     // html = frappe.render_template("test", print_data)
        //     // console.log(html);
        //     // piechart();
        //     // piechart2();
        //     // piechart3();
        //     // piechart4();
        //     // var WinPrint = window.open('', '', 'width=900,height=900');

        //     // WinPrint.document.write(html);
        //     // WinPrint.document.close();
        //     // WinPrint.focus();
        //     // WinPrint.print();
        //     // WinPrint.close();


        //   },
        // });
    },
};

function enrolmentChart(data, year) {
    var boys;
    var girls;
    var classes;

    if (year == "2021-22") {
        boys = Array(14).fill(0);
        girls = Array(14).fill(0);
        classes = [
            "ECCE",
            "Katchi",
            "Class I",
            "Class II",
            "Class III",
            "Class IV",
            "Class V",
            "Class VI",
            "Class VII",
            "Class VIII",
            "Class IX",
            "Class X",
            "Class XI",
            "Class XII",
        ]
        for (i = 0; i < data.length; i++) {
            $.each(data[i], function (key, value) {
                if (key == "order" && value == 0) {
                    boys[0] = data[i]['boys'];
                    girls[0] = data[i]['girls'];
                }
                if (key == "order" && value == 1) {
                    boys[1] = data[i]['boys'];
                    girls[1] = data[i]['girls'];
                } else if (key == "order" && value == 2) {
                    boys[2] = data[i]['boys'];
                    girls[2] = data[i]['girls'];
                } else if (key == "order" && value == 3) {
                    boys[3] = data[i]['boys'];
                    girls[3] = data[i]['girls'];
                } else if (key == "order" && value == 4) {
                    boys[4] = data[i]['boys'];
                    girls[4] = data[i]['girls'];
                } else if (key == "order" && value == 5) {
                    boys[5] = data[i]['boys'];
                    girls[5] = data[i]['girls'];
                } else if (key == "order" && value == 6) {
                    boys[6] = data[i]['boys'];
                    girls[6] = data[i]['girls'];
                } else if (key == "order" && value == 7) {
                    boys[7] = data[i]['boys'];
                    girls[7] = data[i]['girls'];
                } else if (key == "order" && value == 8) {
                    boys[8] = data[i]['boys'];
                    girls[8] = data[i]['girls'];
                } else if (key == "order" && value == 9) {
                    boys[9] = data[i]['boys'];
                    girls[9] = data[i]['girls'];
                } else if (key == "order" && value == 10) {
                    boys[10] = data[i]['boys'];
                    girls[10] = data[i]['girls'];
                } else if (key == "order" && value == 11) {
                    boys[11] = data[i]['boys'];
                    girls[11] = data[i]['girls'];
                } else if (key == "order" && value == 12) {
                    boys[12] = data[i]['boys'];
                    girls[12] = data[i]['girls'];
                } else if (key == "order" && value == 13) {
                    boys[13] = data[i]['boys'];
                    girls[13] = data[i]['girls'];
                }
            });
        }
    } else {
        boys = Array(13).fill(0);
        girls = Array(13).fill(0);
        classes = [
            "Katchi",
            "Class I",
            "Class II",
            "Class III",
            "Class IV",
            "Class V",
            "Class VI",
            "Class VII",
            "Class VIII",
            "Class IX",
            "Class X",
            "Class XI",
            "Class XII",
        ]
        for (i = 0; i < data.length; i++) {
            $.each(data[i], function (key, value) {
                if (key == "order" && value == 1) {
                    boys[0] = data[i]['boys'];
                    girls[0] = data[i]['girls'];
                }
                if (key == "order" && value == 2) {
                    boys[1] = data[i]['boys'];
                    girls[1] = data[i]['girls'];
                } else if (key == "order" && value == 3) {
                    boys[2] = data[i]['boys'];
                    girls[2] = data[i]['girls'];
                } else if (key == "order" && value == 4) {
                    boys[3] = data[i]['boys'];
                    girls[3] = data[i]['girls'];
                } else if (key == "order" && value == 5) {
                    boys[4] = data[i]['boys'];
                    girls[4] = data[i]['girls'];
                } else if (key == "order" && value == 6) {
                    boys[5] = data[i]['boys'];
                    girls[5] = data[i]['girls'];
                } else if (key == "order" && value == 7) {
                    boys[6] = data[i]['boys'];
                    girls[6] = data[i]['girls'];
                } else if (key == "order" && value == 8) {
                    boys[7] = data[i]['boys'];
                    girls[7] = data[i]['girls'];
                } else if (key == "order" && value == 9) {
                    boys[8] = data[i]['boys'];
                    girls[8] = data[i]['girls'];
                } else if (key == "order" && value == 10) {
                    boys[9] = data[i]['boys'];
                    girls[9] = data[i]['girls'];
                } else if (key == "order" && value == 11) {
                    boys[10] = data[i]['boys'];
                    girls[10] = data[i]['girls'];
                } else if (key == "order" && value == 12) {
                    boys[11] = data[i]['boys'];
                    girls[11] = data[i]['girls'];
                } else if (key == "order" && value == 13) {
                    boys[12] = data[i]['boys'];
                    girls[12] = data[i]['girls'];
                }
            });
        }
    }





    Highcharts.chart("containergender", {
        chart: {
            type: "bar",
        },
        colors: ["#0091F7", "#F740A9"],
        title: {
            text: "Class and Gender wise Enrollments",
        },
        credits: {
            enabled: false,
        },
        exporting: {
            enabled: false,
        },
        xAxis: {
            categories: classes,
            title: {
                text: null,
            },
        },
        yAxis: {
            min: 0,
            title: {
                text: "",
                align: "high",
            },
            labels: {
                overflow: "justify",
            },
        },
        tooltip: {
            valueSuffix: "",
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true,
                    crop: false,
                    padding: 5,
                    allowOverlap: true,
                },
            },
        },
        legend: {
            layout: "vertical",
            align: "right",
            verticalAlign: "top",
            x: -20,
            y: -10,
            floating: true,
            borderWidth: 1,
            backgroundColor:
                Highcharts.defaultOptions.legend.backgroundColor || "#FFFFFF",
            shadow: true,
        },
        credits: {
            enabled: false,
        },
        series: [
            {
                name: "Boys",
                data: boys,
            },
            {
                name: "Girls",
                data: girls,
            },
        ],
        filter: {
            property: 'x',
            operator: '>',
            value: 0
        },
    });
}


function teacherPerYear(data) {
    var year = Array(data.length).fill(0);
    var teachers = Array(data.length).fill(0);
    for (i = 0; i < data.length; i++) {
        $.each(data[i], function (key, value) {
            if (key == "year") {
                year[i] = data[i]['year'];
            } else if (key == "teachers") {
                teachers[i] = data[i]['teachers']
            }
        });
    }
    // console.log(year);

    Highcharts.chart('teachercontainer', {
        chart: {
            type: 'line',
            style: { fontFamily: "'Roboto', sans-serif" },
        },
        title: {
            text: 'Teachers Per Year',
            align: 'left',
            style: {
                fontWeight: 'bold',
                fontSize: '14px'
            }
        },
        colors: ["#309975 "],
        subtitle: {
            text: ''
        },
        credits: {
            enabled: false,
        },
        exporting: {
            enabled: false,
        },
        yAxis: {

            title: {
                text: 'Number of Teachers'
            },
        },

        xAxis: {
            allowDecimals: false,
            accessibility: {
                // rangeDescription: 'Range: 2019 to 2020'

            },
            categories: year,


        },
        plotOptions: {
            series: {
                label: {
                    connectorAllowed: false
                },
                // pointStart: 2019
            }
        },

        series: [{
            name: 'Teachers',
            data: teachers
        }],

        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'bottom'
                    }
                }
            }]
        }

    });
}

function enrollmentPerYear(data) {

    var year = Array(data.length).fill(0);
    var enrollment = Array(data.length).fill(0);
    for (i = 0; i < data.length; i++) {
        $.each(data[i], function (key, value) {
            if (key == "year") {
                year[i] = data[i]['year'];
            } else if (key == "enrollment") {
                enrollment[i] = data[i]['enrollment']
            }
        });
    }


    Highcharts.chart('enrollmentcontainer', {
        chart: {
            type: 'line',
            style: { fontFamily: "'Roboto', sans-serif" },
        },
        title: {
            text: 'Enrollment Per Year',
            align: 'left',
            style: {
                fontWeight: 'bold',
                fontSize: '14px',
            }
        },

        colors: ["#304C73"],

        credits: {
            enabled: false,
        },
        exporting: {
            enabled: false,
        },
        yAxis: {
            title: {
                text: 'Enrollments'
            }
        },

        xAxis: {
            allowDecimals: false,
            accessibility: {
                //rangeDescription: 'Range: 2010 to 2020'
            },
            categories: year,

        },



        plotOptions: {
            series: {
                label: {
                    connectorAllowed: false
                },
                //pointStart: 2019
            }
        },

        series: [{
            name: 'Enrollments',
            data: enrollment
        }],
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'bottom'
                    }
                }
            }]
        }

    });
}

function schoolwise(data) {

    var year = Array(data.length).fill(0);
    var functional = Array(data.length).fill(0);
    var closed = Array(data.length).fill(0);
    var merged = Array(data.length).fill(0);
    for (i = 0; i < data.length; i++) {
        $.each(data[i], function (key, value) {
            if (key == "year") {
                year[i] = data[i]['year'];
            } else if (key == "functional") {
                functional[i] = data[i]['functional']
            } else if (key == "closed") {
                closed[i] = data[i]['closed']
            } else if (key == "merged") {
                merged[i] = data[i]['merged']
            }
        });
    }


    // console.log(year);


    Highcharts.chart('schoolcontainer', {

        chart: {
            type: 'column'
        },
        colors: ["#309975", "#454d66", "#EFD446"],
        credits: {
            enabled: false,
        },
        exporting: {
            enabled: false,
        },
        title: {
            text: 'Yearly Based School Status'
        },

        xAxis: {
            categories: year
        },

        yAxis: {
            allowDecimals: false,
            min: 0,
            title: {
                text: ''
            }
        },

        tooltip: {
            formatter: function () {
                return '<b>' + this.x + '</b><br/>' +
                    this.series.name + ': ' + this.y + '<br/>' +
                    'Total: ' + this.point.stackTotal;
            }
        },

        plotOptions: {
            column: {
                stacking: 'normal'
            },
            series: {
                pointWidth: 50
            }
        },

        series: [{
            name: 'Functional',
            data: functional

        }, {
            name: 'Non-Functional',
            data: closed

        }, {
            name: 'Merged Schools',
            data: merged
        }]
    });






    // Highcharts.chart('schoolcontainer', {
    //   chart: {
    //     type: 'column',
    //     style: { fontFamily: "'Roboto', sans-serif" },
    //   },
    //   colors: ["#454d66", "#309975", "#58b368"],
    //   credits: {
    //     enabled: false,
    //   },
    //   exporting: {
    //     enabled: false,
    //   },
    //   title: {
    //     text: 'Yearly Based School Status'
    //   },
    //   subtitle: {
    //     text: ''
    //   },
    //   xAxis: {
    //     categories: year,
    //     crosshair: true
    //   },
    //   yAxis: {
    //     min: 0,
    //     title: {
    //       text: ''
    //     }
    //   },
    //   tooltip: {
    //     headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
    //     pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
    //       '<td style="padding:0"><b>{point.y}</b></td></tr>',
    //     footerFormat: '</table>',
    //     shared: true,
    //     useHTML: true
    //   },
    //   plotOptions: {
    //     column: {
    //       pointPadding: 0.2,
    //       borderWidth: 0
    //     }
    //   },
    //   series: [{
    //     name: 'Functional',
    //     data: functional

    //   }, {
    //     name: 'Non Functional',
    //     data: closed

    //   }, {
    //     name: 'Merged Schools',
    //     data: merged

    //   }]
    // });
}

function school_status() {
    // Make monochrome colors
    var pieColors = (function () {
        var colors = ["#309975", "#454d66"],
            base = Highcharts.getOptions().colors[0],
            i;

        for (i = 0; i < 10; i += 1) {
            // Start out with a darkened base color (negative brighten), and end
            // up with a much brighter color
            colors.push(Highcharts.color(base).brighten((i - 3) / 7).get());
        }
        return colors;
    }());

    // Build the chart
    Highcharts.chart('school-status-container', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie',
            height: 300
        },
        credits: {
            enabled: false,
        },
        exporting: {
            enabled: false,
        },
        title: {
            text: ''
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        accessibility: {
            point: {
                valueSuffix: '%'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                colors: pieColors,
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b><br>{point.percentage:.1f} %',
                    distance: -50,
                    filter: {
                        property: 'percentage',
                        operator: '>',
                        value: 4
                    }
                }
            }
        },
        series: [{
            name: 'Share',
            data: [
                { name: 'Functional', y: 61.41 },
                { name: 'Closed', y: 11.84 },

            ]
        }]
    });
}
function piechart() {
    $(".donut-lg").peity("donut", {
        fill: ["#309975", "#fff"],
        width: "150",
        height: "150",
        innerRadius: 60,
        radius: 10
    });
}

function piechart2() {
    $(".donut-lg2").peity("donut", {
        fill: ["#CD113B", "#fff"],
        width: "150",
        height: "150",
        innerRadius: 60,
        radius: 10
    });
}

function piechart3() {
    $(".donut-lg3").peity("donut", {
        fill: ["#454D66", "#fff"],
        width: "150",
        height: "150",
        innerRadius: 60,
        radius: 10
    });
}

function piechart4() {
    $(".donut-lg4").peity("donut", {
        fill: ["#EFD446", "#fff"],
        width: "150",
        height: "150",
        innerRadius: 60,
        radius: 10
    });
}

