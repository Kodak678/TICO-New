class Piece {
    constructor(name, color,symbol) {
      this.name = name;
      this.color = color;
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
  }


class Pawn extends Piece {
constructor(color,symbol) {
    super("pawn", color , symbol);   
}
}
class Rook extends Piece {
constructor(color,symbol) {
    super("rook", color , symbol);   
}
}
class Knight extends Piece {
constructor(color,symbol) {
    super("knight", color , symbol);   
}
}
class Bishop extends Piece {
constructor(color,symbol) {
    super("bishop", color , symbol);   
}
}
class King extends Piece {
constructor(color,symbol) {
    super("king", color , symbol);   
}
}
class Queen extends Piece {
constructor(color,symbol) {
    super("queen", color , symbol);   
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

