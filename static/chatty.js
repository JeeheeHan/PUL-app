const socket = io.connect();


socket.on( 'connect', function () {
  
    //pt 1; emit login timestamp first to server
    
    // socket.emit('messaging', {
    //   data: "A new user connected!"
    // });
    
    
    //pt2: jquery ajax to get the values from the form 
    const form = $( 'form.chat' ).on( 'submit', function ( e ){
      e.preventDefault();
      //ignore the action 
      let username = $( 'input.username' ).val()
      let userMessage = $( 'input.message' ).val()
      //String the date time 
      let timestamp= new Date()
      //Sean complimented me here: user point time stamp accuracy 
      //Call for messaging decorator
      socket.emit ( 'messaging', {username : username,message : userMessage,timestamp : timestamp.toISOString()})
      //pt3: remove the message in the input line and focus to add the click there
      $( 'input.message' ).val( '' ).focus()
    });
    //pt4: adding the message into the screen waiting for emit 'my response'   
});
  
  
// let positiveCount = 0;
// let negativeCount = 0;
  
// socket.on( 'new line', function( data ) {
//       // console.log( data )
//   function statusCounter(counter){
  
//     if (counter == "positive") {
//       positiveCount++;
//       return positiveCount;
//     }
//     else if (counter == "negative") {
//       negativeCount++;
//       return negativeCount;
//       }; 
//       };
  
//     if( typeof data.username !== 'undefined' ) {
//       $( 'h3' ).remove()
//       $( 'div.message_holder' ).append( '<div><b style="color: #000">'+data.username+'</b> '+data.message+'</div>' )
//       statusCounter(data.polarity)
//       $( 'div.counter').html( '<div>'+positiveCount+'</div>' )      
//     }
//   });
  

