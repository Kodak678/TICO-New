
function resetAll(){
    document.getElementById("current").innerHTML = ""
    currentSquare = ""
    targetSquare = ""
    move = ""
    if (playerTurn == "white"){
        playerTurn = "black"
        }
        else{
            playerTurn = "white"
        }
    document.getElementById("playerTurn").innerHTML = playerTurn
}
