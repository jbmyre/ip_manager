function get_table(subnet, page){
    var url = "/" + subnet + "/" + page
    var a_id = "#" + subnet + "_" + page
    $("ul.pagination li").removeClass("active");
    $("#table_row").load(url);
    $(a_id).toggleClass( "active" );
}

function show_ping(net){
 var url = "/sweep/" + net
 var ping = $.get(url);
 $("#ping_wait").slideDown("fast");
 ping.done(function(data){
 $("#ping_wait").slideUp("fast");
 Materialize.toast(data, 999, "green white-text", function(){$("#show_ping").hide("fast");})
  $("#table_row").load(url);
 });

}

function edit_ip(net){
 var url = "/edit/" + net
 var history = "/history/" + net

 //get inner html for the modal- then use callback to make sure html is loaded in the dom
 $("#modal1").load(url, function() {

 var chart = $.get(history);
     //parse ping history json to a fancy chart
     chart.done(function(data){

        var options = {
        high: 1,
        low: -1,
          axisX: {
            labelInterpolationFnc: function(value, index) {
              return index % 1 === 0 ? value : null;
            }
          },
          axisY: {
            labelInterpolationFnc: function(value) {
            if (value === 1){
              return "Success"
              }
            else if (value === -1){
              return "Failed"
              }
            }
          }
        }; // end of options

        var charts = new Chartist.Bar('.ct-chart', data, options);

        // check data and change color of bar for a failed ping
        charts.on('draw', function(data) {
          // the draw callback will fire while drawing the charts grid
          if(data.type === 'bar') {
                if(data.value.y === -1){
                    data.element.attr({
                      style: 'stroke: red;'
                    });
                }
                if(data.value.y === 0){
                    data.element.attr({
                      style: 'stroke: orange;'
                    });
                }
          }
        });//end draw callback

        //finally open the modal
        $('#modal1').openModal();

     }); // end of get chart json callback

 });// end of get modal html callback
}

function open_ip(net){
 var url = "/openip/" + net
 $("#modal1").load(url, function() {
 $('#modal1').openModal();
 });
}

function ping(url, element, sub){
    var pinging = $.get(url);
    var subnet = "/" + sub + "/"
    var position = $(element).position();
     pinging.done(function( data ) {
        $("#table_row").load(subnet, function(){
         sort();
        Materialize.toast(data, 3000, "dark-gradient white-text");
        $('.tooltipped').tooltip({delay: 50});
        });
     });
}

function refresh(){
    $("#table_row").load(subnet, function(){
         //sort()
        Materialize.toast(data, 3000, "dark-gradient white-text");
        $('.tooltipped').tooltip({delay: 50});
        });
}

function ip_update(){
 var url = $("#ip_update").attr( "action" );
 var d = $("#ip_update").serialize();
 var posting = $.post( url, d );
 posting.done(function( data ) {
    $('#modal1').closeModal();
    $('#modal1').empty();
    Materialize.toast(data, 3000, "dark-gradient white-text");
    $("#table_row").load(subnet,function(){
        sort();
        $('.tooltipped').tooltip({delay: 50});
    });

 });
}

function sort(){
console.log("sorted");
$('.tablesorter').tablesorter({
    theme: 'blackice',
    widthFixed: false,
    showProcessing: false,
    headerTemplate: '{content} {icon}',
    onRenderTemplate: null, // function(index, template){ return template; },
    onRenderHeader: function (index) {
        // the span wrapper is added by default
        $(this).find('div.tablesorter-header-inner').addClass('roundedCorners');
    },
    cancelSelection: true,
    dateFormat: "mmddyyyy",
    sortMultiSortKey: "shiftKey",
    sortResetKey: 'ctrlKey',
    usNumberFormat: true,
    delayInit: false,
    serverSideSorting: false,
    headers: {
        // set "sorter : false" (no quotes) to disable the column
        0: {
            sorter: "ipAdderess"
        },
        1: {
            sorter: "text"
        },
        2: {
            sorter: "text"
        },
        3: {
            sorter: "text"
        },
        4: {
            sorter: "text"
        },
        5: {
            sorter: "text"
        },
        6: {
            sorter: "false"
        },
        7: {
            sorter: "text"
        },
        8: {
            sorter: "text"
        }
    },
    ignoreCase: true,
    sortForce: null,
    sortList: [
        [0, 0],
        [1, 0],
        [2, 0],
        [3, 0],
        [4, 0],
        [5, 0],
        [6, 0],
        [7, 0],
        [8, 0],
    ],
    sortAppend: null,
    sortInitialOrder: "asc",
    sortLocaleCompare: true,
    sortReset: false,
    sortRestart: false,
    emptyTo: "bottom",
    stringTo: "max",
    textExtraction: {
        0: function (node) {
            return $(node).text();
        },
        1: function (node) {
            return $(node).text();
        },
        '.ping': function(node, table, cellIndex){ return $(node).find("div.ping-sort").text(); },
        '.date' : function(node, table, cellIndex){ return $(node).text(); }
    },
    textSorter: null,
    initWidgets: true,
    widgets: ['columns', 'stickyHeaders'],
    widgetOptions: {
        uitheme: 'jui',
        columns: [
            "primary",
            "secondary",
            "tertiary"],
        columns_tfoot: true,
        columns_thead: true,
        filter_childRows: false,
        filter_columnFilters: true,
        filter_cssFilter: "tablesorter-filter",
        filter_functions: null,
        filter_hideFilters: false,
        filter_ignoreCase: true,
        filter_reset: null,
        filter_searchDelay: 300,
        filter_serversideFiltering: false,
        filter_startsWith: false,
        filter_useParsedData: false,
        resizable: true,
        saveSort: true,
        stickyHeaders: "tablesorter-stickyHeader",
      // number or jquery selector targeting the position:fixed element
      stickyHeaders_offset : 0,
      // added to table ID, if it exists
      stickyHeaders_cloneId : '-sticky',
      // trigger "resize" event on headers
      stickyHeaders_addResizeEvent : true,
      // if false and a caption exist, it won't be included in the sticky header
      stickyHeaders_includeCaption : true,
      // The zIndex of the stickyHeaders, allows the user to adjust this to their needs
      stickyHeaders_zIndex : 22,
      // jQuery selector or object to attach sticky header to
      stickyHeaders_attachTo : '#floater',
      // jQuery selector or object to monitor horizontal scroll position (defaults: xScroll > attachTo > window)
      stickyHeaders_xScroll : null,
      // jQuery selector or object to monitor vertical scroll position (defaults: yScroll > attachTo > window)
      stickyHeaders_yScroll : null,

      // scroll table top into view after filtering
      stickyHeaders_filteredToTop: true
    },

    initialized: function (table) {},
    tableClass: 'tablesorter',
    cssAsc: "tablesorter-headerSortUp",
    cssDesc: "tablesorter-headerSortDown",
    cssHeader: "tablesorter-header",
    cssHeaderRow: "tablesorter-headerRow",
    cssIcon: "material-icons",
    cssChildRow: "tablesorter-childRow",
    cssInfoBlock: "tablesorter-infoOnly",
    cssProcessing: "tablesorter-processing",
    selectorHeaders: '> thead th, > thead td',
    selectorSort: "th, td",
    selectorRemove: "tr.remove-me",
    debug: false
});
$.extend($.tablesorter.themes.jui, {
    table: 'ui-widget ui-widget-content ui-corner-all', // table classes
    header: 'ui-widget-header ui-corner-all ui-state-default', // header classes
    icons: 'material-icons', // icon class added to the <i> in the header
    sortNone: 'ui-icon-carat-2-n-s',
    sortAsc: 'ui-icon-carat-1-n',
    sortDesc: 'ui-icon-carat-1-s',
    active: 'ui-state-active', // applied when column is sorted
    hover: 'ui-state-hover', // hover class
    filterRow: '',
    even: 'ui-widget-content', // even row zebra striping
    odd: 'ui-state-default' // odd row zebra striping
});


}


$(document).ready(function(){
    $("#menu").load("/navigation");

    $(".button-collapse").sideNav();

    $("#logo").sideNav();

    $(".dropdown-button").dropdown();

    $('.tooltipped').tooltip({delay: 50});
});