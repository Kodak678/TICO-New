
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



