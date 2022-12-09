function getWinner(){
    return $.ajax({
      url: '/getWinner',
      type: 'get',
      async: false,
      data: {
          hide : "winner",
      }});
  }
  
function trainModel(){
    return $.ajax({
      url: '/trainModel',
      type: 'get',
      // async: false,
      data: {
          hide : "train",
      }});
  }
function gameIsOver(){  
  $.when(getWinner()).then(function successHandler(response){
   
    winner = response.winner
    document.getElementById("playerTurn").innerHTML = winner
   },
   function errorHandler(){
     console.log("Error has occurred")
   })}