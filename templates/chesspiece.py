

class Piece:
    def __init__(self,name,color,value,symbol):
        self.name = name
        self.color = color
        self.value = value
        self.symbol = symbol
        self.moves = []
    def getSymbol(self):
        return self.symbol
    
    def getName(self):
        return self.name

    def getValue(self):
        return self.value
    
    def getSymbol(self):
        return self.symbol
    
    def getColor(self):
        return self.color

    def addMoves(self,move):
        self.moves.append(move)
        
    def getMoves(self):
        return self.moves
        
class Pawn(Piece):
    def __init__(self,color,symbol):
        super().__init__("pawn",color,10.0,symbol)
       

class Rook(Piece):
    def __init__(self,color,symbol):
        super().__init__("rook",color,50.0,symbol)
        

class Knight(Piece):
    def __init__(self,color,symbol):
        super().__init__("knight",color,30.0,symbol)
        

class Bishop(Piece):
    def __init__(self,color,symbol):
        super().__init__("bishop",color,30.0,symbol)

class Queen(Piece):
    def __init__(self,color,symbol):
        super().__init__("queen",color,90.0,symbol)

class King(Piece):
    def __init__(self,color,symbol):
        super().__init__("king",color,900.0,symbol)


BlackPawn = Pawn("black","&#9823")
BlackRook = Rook("black","&#9820;")
BlackKnight = Knight("black","&#9822;")
BlackBishop = Bishop("black","&#9821;")
BlackQueen = Queen("black","&#9819;")
BlackKing = King("black","&#9818;")

WhitePawn = Pawn("white","&#9817;")
WhiteRook = Rook("white","&#9814;")
WhiteKnight = Knight("white","&#9816;")
WhiteBishop = Bishop("white","&#9815;")
WhiteQueen = Queen("white","&#9813;")
WhiteKing = King("white","&#9812;")

BlackPawns = ["a7","b7","c7","d7","e7","f7","g7","h7"]
WhitePawns = ["a2","b2","c2","d2","e2","f2","g2","h2"]
