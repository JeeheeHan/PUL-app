const socket = io.connect();

socket.on( 'connect', () => {
  
    //pt 1; emit login timestamp first to server
    
    // socket.emit('messaging', {
    //   data: "A new user connected!"
    // });

    
    //pt2: jquery ajax to get the values from the form 
    const form = $( 'form.chat' ).on( 'submit',  (e )=>{
      e.preventDefault();
      //ignore the action 
      let username = $( 'input.username' ).val()
      let userMessage = $( 'input.message' ).val()
      //String the date time 
      let timestamp= new Date()
      //Sean complimented me here: user point time stamp accuracy 
      //Call for messaging decorator
      socket.emit ( 'messaging', {username : username, message : userMessage,timestamp : timestamp.toISOString()})
      //pt3: remove the message in the input line and focus to add the click there
      $( 'input.message' ).val( '' ).focus()
    });
  });
  