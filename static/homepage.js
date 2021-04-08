// This the JS for chat room

const socket = io.connect(); 

socket.on('connect', function () {
    //pt 1; emit login timestamp first to server
    socket.emit('login timestamp', {
        username: SESSION['username']
    })
    //pt2: jquery ajax to get the values from the form 
    const generalChat = $( 'form' ).on( 'submit', function ( e ){
      e.preventDefault()
      let username = $( 'input.username' ).val()
      let userMessage = $( 'input.message' ).val()
      let timestamp= Date.now()
      //Call for messaging decorator
      socket.emit ( 'messaging', {
        username = username, 
        message = userMessage,
        timestamp = timestamp
      })
      //pt3: remove the message in the input line and focus to add the click there
      $( 'input.message' ).val( '' ).focus()
    })
})