class Piece {
    constructor(name, color,value,symbol) {
      this.name = name;
      this.color = color;
      this.value = value;
      this.symbol = symbol;
    }
    getSymbol(){
        return this.symbol;
    }
    getName(){
        return this.name;
    }
    getColor(){
        return this.color;
    }
    getValue(){
        return this.value;
    }
  }


class Pawn extends Piece {
constructor(color,symbol) {
    super("pawn", color , 10, symbol);   
}
}
class Rook extends Piece {
constructor(color,symbol) {
    super("rook", color , 50, symbol);   
}
}
class Knight extends Piece {
constructor(color,symbol) {
    super("knight", color , 30, symbol);   
}
}
class Bishop extends Piece {
constructor(color,symbol) {
    super("bishop", color , 30, symbol);   
}
}
class King extends Piece {
constructor(color,symbol) {
    super("king", color , 900, symbol);   
}
}
class Queen extends Piece {
constructor(color,symbol) {
    super("queen", color , 90, symbol);   
}
}


BlackPawn = new Pawn("black","&#9823");
BlackRook = new Rook("black","&#9820;");
BlackKnight = new Knight("black","&#9822;");
BlackBishop = new Bishop("black","&#9821;");
BlackQueen = new Queen("black","&#9819;");
BlackKing = new King("black","&#9818;");

WhitePawn = new Pawn("white","&#9817;");
WhiteRook = new Rook("white","&#9814;");
WhiteKnight = new Knight("white","&#9816;");
WhiteBishop = new Bishop("white","&#9815;");
WhiteQueen = new Queen("white","&#9813;");
WhiteKing = new King("white","&#9812;");



function moveOnScreen(currentSquare, targetSquare){
    document.getElementById(targetSquare).setAttribute("piece",document.getElementById(currentSquare).getAttribute("piece"))
    document.getElementById(targetSquare).setAttribute("player",document.getElementById(currentSquare).getAttribute("player"))
    document.getElementById(targetSquare).innerHTML = document.getElementById(currentSquare).innerHTML
  document.getElementById(currentSquare).setAttribute("piece","")
  document.getElementById(currentSquare).setAttribute("player","")
  document.getElementById(currentSquare).innerHTML = ""
}


function resetCurrentSquare(currentSquare){
    document.getElementById(currentSquare).setAttribute("piece","")
    document.getElementById(currentSquare).setAttribute("player","")
    document.getElementById(currentSquare).innerHTML = ""
}

function reset_game(){
    BlackPawns = ["a7","b7","c7","d7","e7","f7","g7","h7"];
    for (let i of BlackPawns) {
        document.getElementById(i).innerHTML = BlackPawn.getSymbol()
        document.getElementById(i).setAttribute("piece",BlackPawn.getName())
        document.getElementById(i).setAttribute("player",BlackPawn.getColor())
    };
    
    
    BlackRooks = ["a8","h8"];
    for (let i of BlackRooks) {
        document.getElementById(i).innerHTML = BlackRook.getSymbol()
        document.getElementById(i).setAttribute("piece",BlackRook.getName())
        document.getElementById(i).setAttribute("player",BlackRook.getColor())
    };

    BlackKnights = ["b8","g8"];
    for (let i of BlackKnights) {
        document.getElementById(i).innerHTML = BlackKnight.getSymbol()
        document.getElementById(i).setAttribute("piece",BlackKnight.getName())
        document.getElementById(i).setAttribute("player",BlackKnight.getColor())
    };

    
    
    BlackBishops = ["c8","f8"];
    for (let i of BlackBishops) {
        document.getElementById(i).innerHTML = BlackBishop.getSymbol()
        document.getElementById(i).setAttribute("piece",BlackBishop.getName())
        document.getElementById(i).setAttribute("player",BlackBishop.getColor())
    };

    
    
    document.getElementById("d8").innerHTML = BlackQueen.getSymbol()
    document.getElementById("d8").setAttribute("piece",BlackQueen.getName())
    document.getElementById("d8").setAttribute("player",BlackQueen.getColor())
    
    document.getElementById("e8").innerHTML = BlackKing.getSymbol()
    document.getElementById("e8").setAttribute("piece",BlackKing.getName())
    document.getElementById("e8").setAttribute("player",BlackKing.getColor())
    
    
    WhitePawns = ["a2","b2","c2","d2","e2","f2","g2","h2"];
    for (let i of WhitePawns) {
        document.getElementById(i).innerHTML = WhitePawn.getSymbol()
        document.getElementById(i).setAttribute("piece",WhitePawn.getName())
        document.getElementById(i).setAttribute("player",WhitePawn.getColor())
    };
    
    
    WhiteRooks = ["a1","h1"]
    for (let i of WhiteRooks) {
        document.getElementById(i).innerHTML = WhiteRook.getSymbol()
        document.getElementById(i).setAttribute("piece",WhiteRook.getName())
        document.getElementById(i).setAttribute("player",WhiteRook.getColor())
    };
    
    
    WhiteKnights = ["b1","g1"]
    for (let i of WhiteKnights) {
        document.getElementById(i).innerHTML = WhiteKnight.getSymbol()
        document.getElementById(i).setAttribute("piece",WhiteKnight.getName())
        document.getElementById(i).setAttribute("player",WhiteKnight.getColor())
    };
    
    
    WhiteBishops = ["c1","f1"]
    for (let i of WhiteBishops) {
        document.getElementById(i).innerHTML = WhiteBishop.getSymbol()
        document.getElementById(i).setAttribute("piece",WhiteBishop.getName())
        document.getElementById(i).setAttribute("player",WhiteBishop.getColor())
    };
    
    
    document.getElementById("d1").innerHTML = WhiteQueen.getSymbol()
    document.getElementById("d1").setAttribute("piece",WhiteQueen.getName())
    document.getElementById("d1").setAttribute("player",WhiteQueen.getColor())
    
    
    document.getElementById("e1").innerHTML = WhiteKing.getSymbol()
    document.getElementById("e1").setAttribute("piece",WhiteKing.getName())
    document.getElementById("e1").setAttribute("player",WhiteKing.getColor())
    
    document.getElementById("playerTurn").innerHTML = playerTurn
}

let currentSquare = ""

let targetSquare = ""

let playerTurn = "white"

let move = ""

function resetAll(){
    currentSquare = ""
    targetSquare = ""
    move = ""
}

let selector = document.getElementById("promotionOptions") 

selector.addEventListener("change", () => {
    let pieces = document.getElementById("promotionOptions")
    let piece = pieces.options[pieces.selectedIndex].value
    move =  move + piece
    
    document.getElementById("move").innerHTML = move
    color = document.getElementById(currentSquare).getAttribute("player")
    if (color == "white"){
        if (piece == "q"){
            document.getElementById(targetSquare).setAttribute("piece","queen")
            document.getElementById(targetSquare).setAttribute("player","white")
            document.getElementById(targetSquare).innerHTML = "&#9813;"
        }
        else if (piece == "r"){
            document.getElementById(targetSquare).setAttribute("piece","rook")
            document.getElementById(targetSquare).setAttribute("player","white")
            document.getElementById(targetSquare).innerHTML = "&#9814;"
        }
        else if (piece == "b"){
            document.getElementById(targetSquare).setAttribute("piece","bishop")
            document.getElementById(targetSquare).setAttribute("player","white")
            document.getElementById(targetSquare).innerHTML = "&#9815;"
        }
        else if (piece == "n"){
            document.getElementById(targetSquare).setAttribute("piece","knight")
            document.getElementById(targetSquare).setAttribute("player","white")
            document.getElementById(targetSquare).innerHTML ="&#9816;"
          }
      }
    else if (color == "black"){
        if (piece == "q"){
            document.getElementById(targetSquare).setAttribute("piece","queen")
            document.getElementById(targetSquare).setAttribute("player","black")
            document.getElementById(targetSquare).innerHTML = "&#9819;"
          }
        else if (piece == "r"){
            document.getElementById(targetSquare).setAttribute("piece","rook")
            document.getElementById(targetSquare).setAttribute("player","black")
            document.getElementById(targetSquare).innerHTML = "&#9820;"
          }
        else if (piece == "b"){
            document.getElementById(targetSquare).setAttribute("piece","bishop")
            document.getElementById(targetSquare).setAttribute("player","black")
            document.getElementById(targetSquare).innerHTML = "&#9821;"
          }
        else if (piece == "n"){
            document.getElementById(targetSquare).setAttribute("piece","knight")
            document.getElementById(targetSquare).setAttribute("player","black")
            document.getElementById(targetSquare).innerHTML = "&#9822;"
          }
        }
    resetCurrentSquare(currentSquare)
    document.getElementById("promotionDiv").setAttribute("class", "hideromotionDiv")
    document.getElementById("promotionTitle").setAttribute("class", "hidePromotionTitle")
    document.getElementById("promotionOptions").setAttribute("class", "hidePromotionSelection")
    resetAll()
})




function action(event){
    const promotionPlaces = ["a8","b8","c8","d8","e8","f8","g8","h8","a1","b1","c1","d1","e1","f1","g1","h1"];
    const enPassantPositions = ["a6","b6","c6","d6","e6","f6","g6","h6","a3","b3","c3","d3","e3","f3","g3","h3"];
  
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
            console.log(move.slice(2) + String(Number(move.slice(3))-1))
            //  document.getElementById(move.slice(2) + String(Number(move.slice(3))-1)).innerHTML = ""
            //  document.getElementById(move.slice(2) + String(Number(move.slice(3))-1)).setAttribute("piece","")
            //  document.getElementById(move.slice(2) + String(Number(move.slice(3))-1)).setAttribute("player","")
            }
         else if (document.getElementById(currentSquare).getAttribute("player") == "black"){
             document.getElementById(move.slice(2) + String(Number(move.slice(3))+1)).innerHTML = ""
             document.getElementById(move.slice(2) + String(Number(move.slice(3))+1)).setAttribute("piece","")
             document.getElementById(move.slice(2) + String(Number(move.slice(3))+1)).setAttribute("player","")
            }
         moveOnScreen(currentSquare,targetSquare)
         resetAll()   
       }
    
 
//        elif document.getElementById(currentSquare).getAttribute("piece") == "king" and document.getElementById(currentSquare).getAttribute("player") == "white" and bool(chess.BB_H1) and targetSquare == "g1":
//          board.push_san(move)
//          moveOnScreen("h1","f1")
//          moveOnScreen(currentSquare,targetSquare)
//          document.getElementById.innerHTML("move",move)
        
//        elif document.getElementById(currentSquare).getAttribute("piece") == "king" and document.getElementById(currentSquare).getAttribute("player") == "white" and bool(chess.BB_A1) and targetSquare == "c1":
//          board.push_san(move)
//          moveOnScreen("a1","d1")
//          moveOnScreen(currentSquare,targetSquare)
//          document.getElementById.innerHTML("move",move)
        
//        elif document.getElementById(currentSquare).getAttribute("piece") == "king" and document.getElementById(currentSquare).getAttribute("player") == "black" and bool(chess.BB_A8) and targetSquare == "c8":
//            board.push_san(move)
//            moveOnScreen("a8","d8")
//            moveOnScreen(currentSquare,targetSquare)
//            document.getElementById.innerHTML("move",move)

//        elif document.getElementById(currentSquare).getAttribute("piece") == "king" and document.getElementById(currentSquare).getAttribute("player") == "black" and bool(chess.BB_H8) and targetSquare == "g8":
//            board.push_san(move)
//            moveOnScreen("h8","f8")
//            moveOnScreen(currentSquare,targetSquare)
//            document.getElementById.innerHTML("move",move)
  
        
        else{
            document.getElementById("move").innerHTML = move
            moveOnScreen(currentSquare,targetSquare)
            resetAll()
        }
        }
    }
        
//        currentSquare = ""
//        promotionPiece = ""
//        if board.is_checkmate():
//          document.getElementById.innerHTML("playerTurn", "playerTurn" + " wins!")
//        if playerTurn == "white":
//          playerTurn = "black"
//        else:
//          playerTurn = "white"
//        document.getElementById.innerHTML("playerTurn",playerTurn)
     
//      if board.is_checkmate():
//        if playerTurn == "white":
//          playerTurn = "black"
//        else:
//          playerTurn = "white"
//        document.getElementById.innerHTML("playerTurn", playerTurn + " wins!")            
          
//     }
// }        

    
// reset_game()
move = "d7d5"
console.log(move.slice(2) + String(Number(move.slice(3))-1))
