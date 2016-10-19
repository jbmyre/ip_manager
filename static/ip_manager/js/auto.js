/**
 * Created by cbssneng on 10/19/2016.
 */
            $.getJSON("{% url 'ip_manager:search_subnet' subnet_name %} ", function(d){
                    $('#search').autocomplete("destroy")
                    .autocomplete({
                        data: d
                    });
             });

             $("#search_form").submit(function () {
                 event.preventDefault();
                 $("#host_details").empty();
                  var search_form = $("#search_form").serialize()
                  var url = $("#search_form").attr( "action" );

                  // Send the query using post
                  var posting = $.post( url, search_form );

                  // Put the results in a modal
                  posting.done(function( data ) {
                      console.log(data)
                      $("#host_details").html(data);
                      $("#host_modal").openModal();
                  });
             })