

function moveOnScreen(currentSquare, targetSquare){
    document.getElementById(targetSquare).setAttribute("piece",document.getElementById(currentSquare).getAttribute("piece"))
    document.getElementById(targetSquare).setAttribute("player",document.getElementById(currentSquare).getAttribute("player"))
    document.getElementById(targetSquare).innerHTML = document.getElementById(currentSquare).innerHTML
  document.getElementById(currentSquare).setAttribute("piece","")
  document.getElementById(currentSquare).setAttribute("player","")
  document.getElementById(currentSquare).innerHTML = ""
}