// const e = require("cors");
// $(window).on('load', ()=>{
//   const statusCounter = (pol) => {
//     //Count function to add into counts dictionary per every message
   
//     if (pol == "positive") {
//       counts.positive++;
//       }
//     else if (pol == "negative") {
//       counts.negative++;
//       };
//     // socket.emit( 'plant health', {positive : counts.positive, negative : counts.negative});
//     return counts;
  
//   };
  
  
//   socket.on( 'new line',( data ) => {
  
//     // if( typeof data.username !== 'undefined' ) {
//     //   $( 'h3' ).remove()
//     //   $( 'div.message_holder' ).append( '<div><b style="color: #000">'+data.username+'</b> '+data.message+'</div>' )
//     // };
//     //get my counts dictionary from the fucntion statusCounter
//     let counts = statusCounter(data.polarity);
//     // socket.emit( 'plant health', {positive : counts.positive, negative : counts.negative});
//     $( '#pos').html( counts.positive);
//     $( '#negative').html( counts.negative);
//     socket.emit('health', {positive : counts.positive.toString(), negative : counts.negative.toString()});
  
//     if( typeof data.username !== 'undefined' ) {
//       $( 'div.message_holder' ).append( '<div><b style="color: #000">'+data.username+'</b> '+data.message+'</div>' )
//     };
//   });
  
  
//   socket.on('my_image', ( data ) =>{
//     $('#plant-img img').attr('src', data.pic);
//   });
  
//   const compliment = $.ajax({
//     url:'https://complimentr.com/api',
//     type: "GET",
//     dataType: 'JSON'
//   });
  
//   $('#testPopup').on('click', (e) => {
//     e.preventDefault();
    
//     compliment.done(function(data){
//       let comps = data.compliment;
//       $('#myPopup').html(comps).toggleClass("show");
//     });
//   });




// });
// const statusCounter = (pol) => {
//   //Count function to add into counts dictionary per every message
 
//   if (pol == "positive") {
//     counts.positive++;
//     }
//   else if (pol == "negative") {
//     counts.negative++;
//     };
//   // socket.emit( 'plant health', {positive : counts.positive, negative : counts.negative});
//   return counts;

// };


// socket.on( 'new line',( data ) => {

//   // if( typeof data.username !== 'undefined' ) {
//   //   $( 'h3' ).remove()
//   //   $( 'div.message_holder' ).append( '<div><b style="color: #000">'+data.username+'</b> '+data.message+'</div>' )
//   // };
//   //get my counts dictionary from the fucntion statusCounter
//   let counts = statusCounter(data.polarity);
//   // socket.emit( 'plant health', {positive : counts.positive, negative : counts.negative});
//   $( '#pos').html( counts.positive);
//   $( '#negative').html( counts.negative);
//   socket.emit('health', {positive : counts.positive.toString(), negative : counts.negative.toString()});

//   if( typeof data.username !== 'undefined' ) {
//     $( 'div.message_holder' ).append( '<div><b style="color: #000">'+data.username+'</b> '+data.message+'</div>' )
//   };
// });


// socket.on('my_image', ( data ) =>{
//   $('#plant-img img').attr('src', data.pic);
// });

// const compliment = $.ajax({
//   url:'https://complimentr.com/api',
//   type: "GET",
//   dataType: 'JSON'
// });

// $('#testPopup').on('click', (e) => {
//   e.preventDefault();
  
//   compliment.done(function(data){
//     let comps = data.compliment;
//     $('#myPopup').html(comps).toggleClass("show");
//   });
// });

// $(window).on('load', ()=>{
//   $('.load_hide').show();
//   $(window).scrollTop(localStorage.getItem('scrollPos_scu'));
// });
// $('div.chat-container').on('scroll', () => {
//   $( "span.sentAt" ).css( "display", "inline" ).fadeOut( "slow" );
// });


