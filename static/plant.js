
const statusCounter = (pol) => {
  //Count function to add into counts dictionary per every message
 
  if (pol == "positive") {
    counts.positive++;
    }
  else if (pol == "negative") {
    counts.negative++;
    };
  return counts;

};

let counts= {'negative': Number($('#negative').text()), 'positive': Number($('#negative').text())};


socket.on( 'new line', function( data ) {

    if( typeof data.username !== 'undefined' ) {
    $( 'h3' ).remove()
    $( 'div.message_holder' ).append( '<div><b style="color: #000">'+data.username+'</b> '+data.message+'</div>' )
    // let positiveCount = Number($('#positive').val());  //{{count["positive"]}}
    // let negativeCount = Number($('#negative').val());
    //get my counts dictionary from the fucntion statusCounter
    let counts = statusCounter(data.polarity);
    $( '#positive').html( counts.positive)
    $( '#negative').html( counts.negative)
    };
});


