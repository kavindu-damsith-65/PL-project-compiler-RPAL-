package scanner;

/** Token types **/

public enum TokenType{
  IDENTIFIER,
  INTEGER,
  STRING,
  OPERATOR,
  DELETE,
  L_PAREN,
  R_PAREN,
  SEMICOLON,
  COMMA,
  RESERVED; // For distinguish reserveed RPAL keywords from othe identifiers
}
