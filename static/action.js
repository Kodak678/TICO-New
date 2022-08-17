
function action(event){
    const promotionPlaces = ["a8","b8","c8","d8","e8","f8","g8","h8","a1","b1","c1","d1","e1","f1","g1","h1"];
    const enPassantPositions = ["a6","b6","c6","d6","e6","f6","g6","h6","a3","b3","c3","d3","e3","f3","g3","h3"];
    let csrf = $('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
      url: '/boardStates',
      type: 'get',
      data: {
          message : "hi My name numar",
          csrfmiddlewaretoken: csrf
      },
      success: function(response) {
      
          console.log(response.response)
          console.log(response.fish)
          console.log(response.tryMe)
      }
  });
    $.ajax({
      url: '/validMove',
      type: 'get',
      data: {
          moved : "moved"
      },
      success: function(response) {
      
         
      }
  });

    if (currentSquare == ""){
    currentSquare = String(event.target.id);
    document.getElementById("current").innerHTML = currentSquare
    
    }
    else{

    targetSquare = String(event.target.id);
    
    move = currentSquare + targetSquare
      
          if (promotionPlaces.includes(move.slice(2,4)) && document.getElementById(currentSquare).getAttribute("piece") == "pawn"){
            document.getElementById("promotionDiv").setAttribute("class", "showPromotionDiv")
            document.getElementById("promotionTitle").setAttribute("class", "showPromotionTitle")
            document.getElementById("promotionOptions").setAttribute("class", "showPromotionSelection")
  
          }
       else if (document.getElementById(currentSquare).getAttribute("piece") == "pawn" && document.getElementById(targetSquare).getAttribute("piece") == "" && enPassantPositions.includes(move.slice(2,4))){
         if (document.getElementById(currentSquare).getAttribute("player") == "white"){
             document.getElementById(move.slice(2,3) + String(Number(move.slice(3))-1)).innerHTML = ""
             document.getElementById(move.slice(2,3) + String(Number(move.slice(3))-1)).setAttribute("piece","")
             document.getElementById(move.slice(2,3) + String(Number(move.slice(3))-1)).setAttribute("player","")
            }
         else if (document.getElementById(currentSquare).getAttribute("player") == "black"){
             document.getElementById(move.slice(2,3) + String(Number(move.slice(3))+1)).innerHTML = ""
             document.getElementById(move.slice(2,3) + String(Number(move.slice(3))+1)).setAttribute("piece","")
             document.getElementById(move.slice(2,3) + String(Number(move.slice(3))+1)).setAttribute("player","")
            }
         moveOnScreen(currentSquare,targetSquare)
         resetAll()   
       }
    
 
       else if (document.getElementById(currentSquare).getAttribute("piece") == "king" && document.getElementById(currentSquare).getAttribute("player") == "white" && targetSquare == "g1"){
         moveOnScreen("h1","f1")
         moveOnScreen(currentSquare,targetSquare)
         document.getElementById("move").innerHTML = move
         resetAll()
       }
       else if (document.getElementById(currentSquare).getAttribute("piece") == "king" && document.getElementById(currentSquare).getAttribute("player") == "white" && targetSquare == "c1"){
         moveOnScreen("a1","d1")
         moveOnScreen(currentSquare,targetSquare)
         document.getElementById("move").innerHTML = move
         resetAll()
       }
        
       else if (document.getElementById(currentSquare).getAttribute("piece") == "king" && document.getElementById(currentSquare).getAttribute("player") == "black" && targetSquare == "c8"){
           moveOnScreen("a8","d8")
           moveOnScreen(currentSquare,targetSquare)
           document.getElementById("move").innerHTML = move
           resetAll()
       }

       else if (document.getElementById(currentSquare).getAttribute("piece") == "king" && document.getElementById(currentSquare).getAttribute("player") == "black" && targetSquare == "g8"){
           moveOnScreen("h8","f8")
           moveOnScreen(currentSquare,targetSquare)
           document.getElementById("move").innerHTML = move
           resetAll()
       }
  
        
        else{
            document.getElementById("move").innerHTML = move
            moveOnScreen(currentSquare,targetSquare)
            resetAll()
        }

        }
    }
