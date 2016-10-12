
// PLUGIN TO SUBMIT FORMS WHEN USER PRESSES ENTER

// EXAMPLE USAGE::
//
//   $('#your-input-id').onEnterKey(
//      function() {
//          // Do stuff here
//     });




$.fn.onEnterKey =
    function( closure ) {
        $(this).keypress(
            function( event ) {
                var code = event.keyCode ? event.keyCode : event.which;

                if (code == 13) {
                    closure();
                    return false;
                }
            } );
    }