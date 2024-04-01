package Interpreter;

/**
 * When standardizing the abstract syntax tree, handle Exception.
 */
public class ExceptionHandlerOfAST extends RuntimeException {
    ExceptionHandlerOfAST(String message) {
        super(message);
    }
}
