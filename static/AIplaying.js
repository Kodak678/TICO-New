function getAImove(){
    return $.ajax({
      url: '/AiMove',
      type: 'get',
      async: true,
      data: {
          stuff : "getting Aimove",
      }});
  }
  



function AIPlay(){
    $.when(getAImove()).then(function successHandler(response){
      legalEnPassant = response.legalEnPassant
      whiteKingSide = response.whiteKingSide
      whiteQueenSide = response.whiteQueenSide
      blackQueenSide = response.blackQueenSide
      blackKingSide = response.blackKingSide
      AImove = response.moveAI
      gameOver = response.gameOver
      const promotionPlaces = ["a8","b8","c8","d8","e8","f8","g8","h8","a1","b1","c1","d1","e1","f1","g1","h1"];
      const enPassantPositions = ["a6","b6","c6","d6","e6","f6","g6","h6","a3","b3","c3","d3","e3","f3","g3","h3"];
  AIsquare = AImove.substring(0, 2)
  AIsquareTarget = AImove.substring(2, 4)
  if (document.getElementById(AIsquare).getAttribute("piece") == "pawn" && document.getElementById(AIsquareTarget).getAttribute("piece") == "" && enPassantPositions.includes(AImove.slice(2,4)) && legalEnPassant){
             if (document.getElementById(AIsquare).getAttribute("player") == "white"){
                 document.getElementById(AImove.slice(2,3) + String((Number(AImove.slice(3,4))-1))).innerHTML = ""
                 document.getElementById(AImove.slice(2,3) + String((Number(AImove.slice(3,4))-1))).setAttribute("piece","")
                 document.getElementById(AImove.slice(2,3) + String((Number(AImove.slice(3,4))-1))).setAttribute("player","")
             }
             else if (document.getElementById(AIsquare).getAttribute("player") == "black"){
                 document.getElementById(AImove.slice(2,3) + String((Number(AImove.slice(3,4))+1))).innerHTML = ""
                 document.getElementById(AImove.slice(2,3) + String((Number(AImove.slice(3,4))+1))).setAttribute("piece","")
                 document.getElementById(AImove.slice(2,3) + String((Number(AImove.slice(3,4))+1))).setAttribute("player","")
                }
                 
  }
  //The above if statement deals with en passent captures on the GUI side
  
  
  else if (document.getElementById(AIsquare).getAttribute("piece") == "king" && document.getElementById(AIsquare).getAttribute("player") == "white" && AIsquareTarget == "g1" && whiteKingSide){
  moveOnScreen("h1","f1")
  moveOnScreen(AIsquare,AIsquareTarget)
  document.getElementById("AImove").innerHTML = AImove
  }
  else if (document.getElementById(AIsquare).getAttribute("piece") == "king" && document.getElementById(AIsquare).getAttribute("player") == "white" && AIsquareTarget == "c1" && whiteQueenSide){
  moveOnScreen("a1","d1")
  moveOnScreen(AIsquare,AIsquareTarget)
  document.getElementById("AImove").innerHTML = AImove
  }
  
  else if (document.getElementById(AIsquare).getAttribute("piece") == "king" && document.getElementById(AIsquare).getAttribute("player") == "black" && AIsquareTarget == "c8" && blackQueenSide){
  moveOnScreen("a8","d8")
  moveOnScreen(AIsquare,AIsquareTarget)
  document.getElementById("AImove").innerHTML = AImove
  }
  
  else if (document.getElementById(AIsquare).getAttribute("piece") == "king" && document.getElementById(AIsquare).getAttribute("player") == "black" && AIsquareTarget == "g8" && blackKingSide){
  moveOnScreen("h8","f8")
  moveOnScreen(AIsquare,AIsquareTarget)
  document.getElementById("AImove").innerHTML = AImove
  }  
  
  else{
    moveOnScreen(AIsquare,AIsquareTarget)
  }
  if (playerTurn == "white"){
    playerTurn = "black"
    
  }
  else{
  
      playerTurn = "white"
  }

  if (!(gameOver)){
    document.getElementById("playerTurn").innerHTML = playerTurn
    document.getElementById("board").setAttribute("class", "chessboard")
  
    }
    else{
      gameIsOver()
      console.log(gameOver)
    }
  


  


    },
    function errorHandler(){
      console.log("Error has occurred")
    })
  
  
  }