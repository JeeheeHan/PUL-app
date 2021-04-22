let counts= {'negative': Number($('#negative').text()), 'positive': Number($('#negative').text())};

const statusCounter = (pol) => {
  //Count function to add into counts dictionary per every message
 
  if (pol == "positive") {
    counts.positive++;
    }
  else if (pol == "negative") {
    counts.negative++;
    };
  // socket.emit( 'plant health', {positive : counts.positive, negative : counts.negative});
  return counts;

};

socket.on( 'new line',( data ) => {

  // if( typeof data.username !== 'undefined' ) {
  //   $( 'h3' ).remove()
  //   $( 'div.message_holder' ).append( '<div><b style="color: #000">'+data.username+'</b> '+data.message+'</div>' )
  // };
  //get my counts dictionary from the fucntion statusCounter
  let counts = statusCounter(data.polarity);
  // socket.emit( 'plant health', {positive : counts.positive, negative : counts.negative});
  $( '#positive').html( counts.positive);
  $( '#negative').html( counts.negative);
  socket.emit('health', {positive : counts.positive.toString(), negative : counts.negative.toString()});

  if( typeof data.username !== 'undefined' ) {
    $( 'h3' ).remove()
    $( 'div.message_holder' ).append( '<div><b style="color: #000">'+data.username+'</b> '+data.message+'</div>' )
  };
});


socket.on('my_image', ( data ) =>{
  console.log(data);
  // $('#plant-img img').attr('src', data.pic);
});


