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

