

function resetCurrentSquare(currentSquare){
    document.getElementById(currentSquare).setAttribute("piece","")
    document.getElementById(currentSquare).setAttribute("player","")
    document.getElementById(currentSquare).innerHTML = ""
}
