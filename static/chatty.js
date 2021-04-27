let counts = { 'positive': Number($('#pos').text()), 'negative':Number($('#negative').text()) };

  $('form.getPolar').on('submit',(e)=>{
    e.preventDefault();
    console.log($('form.getPolar').serialize())
    const polarity = $.ajax({
      url:'/getPolarity',
      type:"POST",
      data: $('form.getPolar').serialize()
    });
    
    polarity.done( (res)=>{
      console.log(res.polarity)
      console.log("got a respsonse")
    });
    console.log("TEstING")});


$(window).on('load', ()=>{
  const socket = io.connect();

  socket.on( 'connect', () => {
    
    const form = $( 'form.chat' ).on( 'submit',  (e )=>{
      e.preventDefault();

      let username = $( 'input.username' ).val()
      let userMessage = $( 'input.message' ).val()
      //String the date time 
      let timestamp= new Date()

      socket.emit ( 'messaging', JSON.stringify({username:username, message:userMessage, timestamp:timestamp.toISOString()}))
      $( 'input.message' ).val( '' ).focus()
    });
  });

  const statusCounter = (pol) => {
    if (pol == "positive") {
      counts.positive++;
      }
    else if (pol == "negative") {
      counts.negative++;
      };
    return counts;
  };

  socket.on( 'new line',( data ) => {
    //get my counts dictionary from the fucntion statusCounter
    let counts = statusCounter(data.polarity);
    $( '#pos').html( counts.positive);
    $( '#negative').html( counts.negative);
    socket.emit('health', {positive : counts.positive.toString(), negative : counts.negative.toString()});
  
    if( typeof data.username !== 'undefined' ) {
      $( 'div.message_holder' ).append( '<div><b style="color: #000">'+data.username+'</b> '+data.message+'</div>' )
    };
  });

  socket.on('my_image', ( data ) =>{
    $('#plant-img img').attr('src', data.pic);
  });
    
  const compliment = $.ajax({
    url:'https://complimentr.com/api',
    type: "GET",
    dataType: 'JSON'
  });
  
  $('#testPopup').on('click', (e) => {
    e.preventDefault();
    
    compliment.done(function(data){
      let comps = data.compliment;
      $('#myPopup').html(comps).toggleClass("show");
    });
  });

  });

