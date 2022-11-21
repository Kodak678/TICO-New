if (AImove.length == 5){
  piece = AImove.substr(4,5)
if (piece == "q"){
    document.getElementById(AIsquareTarget).setAttribute("piece","queen")
    document.getElementById(AIsquareTarget).setAttribute("player","black")
    document.getElementById(AIsquareTarget).innerHTML = "&#9819;"
  }
else if (piece == "r"){
    document.getElementById(AIsquareTarget).setAttribute("piece","rook")
    document.getElementById(AIsquareTarget).setAttribute("player","black")
    document.getElementById(AIsquareTarget).innerHTML = "&#9820;"
  }
else if (piece == "b"){
    document.getElementById(AIsquareTarget).setAttribute("piece","bishop")
    document.getElementById(AIsquareTarget).setAttribute("player","black")
    document.getElementById(AIsquareTarget).innerHTML = "&#9821;"
  }
else if (piece == "n"){
    document.getElementById(AIsquareTarget).setAttribute("piece","knight")
    document.getElementById(AIsquareTarget).setAttribute("player","black")
    document.getElementById(AIsquareTarget).innerHTML = "&#9822;"
  }
}
