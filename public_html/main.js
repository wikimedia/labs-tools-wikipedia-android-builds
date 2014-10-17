$( function() {
    // Fetch the latest build's data
    $.get('runs/latest/meta.json').done( function( data ) {
        var completed_on = new Date( data.completed_on );
        $( '#last-build-time' ).text( completed_on.toLocaleString() );
    });
});
