let counts = { 'positive': Number($('#pos').text()), 'negative':Number($('#negative').text()), 'total':Number($('#total').text()) };


$(window).on('load', ()=>{
  const socket = io.connect();

  socket.on( 'connect', () => {
    
    const form = $( 'form.chat' ).on( 'submit',  (e )=>{
      e.preventDefault();

      let username = $( 'input.username' ).val()
      let userMessage = $( 'input.message' ).val()
      //String the date time 
      let timestamp= new Date()

      socket.emit ( 'messaging', JSON.stringify({username:username, message:userMessage, timestamp:timestamp.toUTCString()}))
      $( 'input.message' ).val( '' ).focus()
    });
  });

  const statusCounter = (pol) => {
    //Counter of live messages and all the messages coming in per messages from async
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
    counts.total++;
    $( '#pos').html( counts.positive);
    $( '#negative').html( counts.negative);
    $( '#total' ).html( counts.total )
    socket.emit('health', {positive : counts.positive.toString(), negative : counts.negative.toString(), total: counts.total.toString()});
  
    if( typeof data.username !== 'undefined' ) {
      $( '.message_holder' ).append( '<div class="mesContainer"><b style="color: #000">'+data.username+': </b>'+data.message+'<span class="timestamp">'+data.timestamp+'</span></div>')
      $('.message_holder').scrollTop($('.message_holder')[0].scrollHeight);
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
  
  $('form.getPolar').on('submit',(e)=>{
    e.preventDefault();
    console.log($('form.getPolar').serialize())
    const polarity = $.ajax({
      url:'/getPolarity',
      type:"POST",
      data: $('form.getPolar').serialize()
    });
    
    polarity.done( (res)=>{
      $('#pClass').html(res.class);
      $('#pPolar').html(res.polarity);
      console.log(res.class)
      console.log("got a respsonse")
    });
 });


  });

