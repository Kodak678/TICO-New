
# from js import document  
# from pyodide import create_proxy



# import chess


# board = chess.Board()



# def action(event):
#       global promotionPiece
#       global currentSquare
#       global playerTurn
#       global board
#       promotionPlaces = ["a8","b8","c8","d8","e8","f8","g8","h8","a1","b1","c1","d1","e1","f1","g1","h1"]
#       enPassantPositions = ["a6","b6","c6","d6","e6","f6","g6","h6","a3","b3","c3","d3","e3","f3","g3","h3"]
#       if currentSquare == "":
#         currentSquare = event.target.id
#         pyscript.write("current",currentSquare)
#       else:
#         targetSquare = event.target.id
      
#         move = currentSquare + targetSquare
#         try:
#           if (move[2]+move[3]) in promotionPlaces and document.getElementById(currentSquare).getAttribute("piece") == "pawn":
#             document.getElementById("promotionDiv").setAttribute("class", "showPromotionDiv")
#             piece = getPromotionPiece()
#             move =  move + piece
#             board.push_san(move)
#             pyscript.write("move",move)
#             color = document.getElementById(currentSquare).getAttribute("player")
#             if color == "white":
#                 if piece == "q":
#                     document.getElementById(targetSquare).setAttribute("piece","queen")
#                     document.getElementById(targetSquare).setAttribute("player","white")
#                     pyscript.write(targetSquare,"&#9813;")
#                 elif piece == "r":
#                     document.getElementById(targetSquare).setAttribute("piece","rook")
#                     document.getElementById(targetSquare).setAttribute("player","white")
#                     pyscript.write(targetSquare,"&#9814;")
#                 elif piece == "b":
#                     document.getElementById(targetSquare).setAttribute("piece","bishop")
#                     document.getElementById(targetSquare).setAttribute("player","white")
#                     pyscript.write(targetSquare,"&#9815;")
#                 elif piece == "n":
#                     document.getElementById(targetSquare).setAttribute("piece","knight")
#                     document.getElementById(targetSquare).setAttribute("player","white")
#                     pyscript.write(targetSquare,"&#9816;")
#             elif color == "black":
#                 if piece == "q":
#                     document.getElementById(targetSquare).setAttribute("piece","queen")
#                     document.getElementById(targetSquare).setAttribute("player","black")
#                     pyscript.write(targetSquare,"&#9819;")
#                 elif piece == "r":
#                     document.getElementById(targetSquare).setAttribute("piece","rook")
#                     document.getElementById(targetSquare).setAttribute("player","black")
#                     pyscript.write(targetSquare,"&#9820;")
#                 elif piece == "b":
#                     document.getElementById(targetSquare).setAttribute("piece","bishop")
#                     document.getElementById(targetSquare).setAttribute("player","black")
#                     pyscript.write(targetSquare,"&#9821;")
#                 elif piece == "n":
#                     document.getElementById(targetSquare).setAttribute("piece","knight")
#                     document.getElementById(targetSquare).setAttribute("player","black")
#                     pyscript.write(targetSquare,"&#9822;")
#             resetCurrentSquare(currentSquare)  

#           elif document.getElementById(currentSquare).getAttribute("piece") == "pawn" and document.getElementById(targetSquare).getAttribute("piece") == "" and (move[2]+move[3]) in enPassantPositions and board.has_legal_en_passant():
#             if document.getElementById(currentSquare).getAttribute("player") == "white":
#                 pyscript.write(move[2] + str(int(move[3])-1),"")
#                 document.getElementById(move[2] + str(int(move[3])-1)).setAttribute("piece","")
#                 document.getElementById(move[2] + str(int(move[3])-1)).setAttribute("player","")
#             elif document.getElementById(currentSquare).getAttribute("player") == "black":
#                 pyscript.write(move[2] + str(int(move[3])+1),"")
#                 document.getElementById(move[2] + str(int(move[3])+1)).setAttribute("piece","")
#                 document.getElementById(move[2] + str(int(move[3])+1)).setAttribute("player","")
#             board.push_san(move)
#             moveOnScreen(currentSquare,targetSquare)   

#           elif document.getElementById(currentSquare).getAttribute("piece") == "king" and document.getElementById(currentSquare).getAttribute("player") == "white" and bool(chess.BB_H1) and targetSquare == "g1":
#             board.push_san(move)
#             moveOnScreen("h1","f1")
#             moveOnScreen(currentSquare,targetSquare)
#             pyscript.write("move",move)
          
#           elif document.getElementById(currentSquare).getAttribute("piece") == "king" and document.getElementById(currentSquare).getAttribute("player") == "white" and bool(chess.BB_A1) and targetSquare == "c1":
#             board.push_san(move)
#             moveOnScreen("a1","d1")
#             moveOnScreen(currentSquare,targetSquare)
#             pyscript.write("move",move)
          
#           elif document.getElementById(currentSquare).getAttribute("piece") == "king" and document.getElementById(currentSquare).getAttribute("player") == "black" and bool(chess.BB_A8) and targetSquare == "c8":
#               board.push_san(move)
#               moveOnScreen("a8","d8")
#               moveOnScreen(currentSquare,targetSquare)
#               pyscript.write("move",move)

#           elif document.getElementById(currentSquare).getAttribute("piece") == "king" and document.getElementById(currentSquare).getAttribute("player") == "black" and bool(chess.BB_H8) and targetSquare == "g8":
#               board.push_san(move)
#               moveOnScreen("h8","f8")
#               moveOnScreen(currentSquare,targetSquare)
#               pyscript.write("move",move)
    
          
#           else:
#             board.push_san(move)
#             pyscript.write("move",move)
#             moveOnScreen(currentSquare,targetSquare)

            
          
#           currentSquare = ""
#           promotionPiece = ""
#           if board.is_checkmate():
#             pyscript.write("playerTurn", "playerTurn" + " wins!")
#           if playerTurn == "white":
#             playerTurn = "black"
#           else:
#             playerTurn = "white"
#           pyscript.write("playerTurn",playerTurn)
#         except ValueError:
#           currentSquare = ""
#           promotionPiece = ""
#           pyscript.write("current","")
       
#         if board.is_checkmate():
#           if playerTurn == "white":
#             playerTurn = "black"
#           else:
#             playerTurn = "white"
#           pyscript.write("playerTurn", playerTurn + " wins!")            
        

        
#         ActivePositions = []
#         BlackPositions = ["a7","b7","c7","d7","e7","f7","g7","h7","a8","b8","c8","d8","e8","f8","g8","h8"]
#         WhitePositions = ["a2","b2","c2","d2","e2","f2","g2","h2","a1","b1","c1","d1","e1","f1","g1","h1"]
#         BlackPawnNum = 8
#         BlackRookNum = 2
#         BlackKnightNum = 2
#         BlackBishopnum = 2
#         BlackQueenNum = 1
#         BlackKingNum = 1

#         WhitePawnNum = 8
#         WhiteRookNum = 8
#         WhiteBishopNum = 8
#         WhiteKnightNum = 8
#         WhiteQueenNum = 8
#         WhiteKingNum = 8
 
# def promoter(event):
#   global promotionPiece
#   promotionPiece = document.getElementById(event.target.id).getAttribute("choice")
#   document.getElementById("promotionDiv").setAttribute("class", "hidePromotionDiv")

# def getPromotionPiece():
#   global promotionPiece
#   return promotionPiece

# cc = create_proxy(action)
# pp = create_proxy(promoter)
# reset_game()











  

# if (document.getElementById(currentSquare).getAttribute("piece") == "king" && document.getElementById(currentSquare).getAttribute("player") == "white" && targetSquare == "g1" && whiteKingSide){
# moveOnScreen("h1","f1")
# moveOnScreen(currentSquare,targetSquare)
# document.getElementById("move").innerHTML = move
# resetAll()
# }
# else if (document.getElementById(currentSquare).getAttribute("piece") == "king" && document.getElementById(currentSquare).getAttribute("player") == "white" && targetSquare == "c1" && whiteQueenSide){
# moveOnScreen("a1","d1")
# moveOnScreen(currentSquare,targetSquare)
# document.getElementById("move").innerHTML = move
# resetAll()
# }

# else if (document.getElementById(currentSquare).getAttribute("piece") == "king" && document.getElementById(currentSquare).getAttribute("player") == "black" && targetSquare == "c8" && blackQueenSide){
#  moveOnScreen("a8","d8")
#  moveOnScreen(currentSquare,targetSquare)
#  document.getElementById("move").innerHTML = move
#  resetAll()
# }

# else if (document.getElementById(currentSquare).getAttribute("piece") == "king" && document.getElementById(currentSquare).getAttribute("player") == "black" && targetSquare == "g8" && blackKingSide){
#  moveOnScreen("h8","f8")
#  moveOnScreen(currentSquare,targetSquare)
#  document.getElementById("move").innerHTML = move
#  resetAll()
# }


# else{
#   document.getElementById("move").innerHTML = move
#   moveOnScreen(currentSquare,targetSquare)
#   resetAll()
# }
# if (playerTurn == "white"){
#   playerTurn = "black"
#   }
#   else{
#       playerTurn = "white"
#   }
# document.getElementById("playerTurn").innerHTML = playerTurn
#       }