$( function() {
    // Fetch the latest build's data
    $.get('/wikipedia-android-builds/runs/latest/meta.json').done( function( data ) {
        $( '#last-build-time' ).text( data.completed_on );
    });
});
