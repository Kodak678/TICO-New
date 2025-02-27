let currentSquare = ""

let targetSquare = ""

let playerTurn = "white"

let move = ""





 
function resetBoard(){
  $.ajax({
    url: '/resetBoard',
    type: 'get',
    async: false,
    data: {
        hide : "ResetBoard"},
  })};






function reset_game(){
    BlackPawns = ["a7","b7","c7","d7","e7","f7","g7","h7"];
    for (let i of BlackPawns) {
        document.getElementById(i).innerHTML = BlackPawn.getSymbol()
        document.getElementById(i).setAttribute("piece",BlackPawn.getName())
        document.getElementById(i).setAttribute("player",BlackPawn.getColor())
    };
    //The .innerHTML stores what is displayed to the user on the screen
    //The piece attribute stores what type of piece e.g. pawn is on the square
    //The player attribute stores whether the piece is black or white
    
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

    
    resetBoard()
}

  
    
reset_game() //Everytime the page is refreshed or left: the board resets visibly and on the back end
