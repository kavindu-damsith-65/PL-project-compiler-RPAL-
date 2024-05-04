import ast.AST;
import cse.CSEMachine;
import cse.ElementParser;
import cse.ExceptionHandlerOfCSE;
import cse.ele.EleValue;
import cse.Stack;
import scanner.*;
import parser.*;

import java.io.IOException;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

import Interpreter.Node;
import Interpreter.ASTtoST;
import Interpreter.CreateTree;
import Interpreter.ExceptionHandlerOfAST;

public class rpal20 {
    public static void main(String[] args) throws Exception {
        String fileName = "";
        try {
            // fileName = args[0];
            fileName ="C:\\PROGRAMMING\\compilerDesign\\PL-project-compiler-RPAL-\\src\\conc.1";
            // if (args.length == 0) {
            //     String error = "You shold give the AST file name as a argument...";
            //     throw new Exception(error);
            // } else {


                AST ast = null;
                Scanner scanner = new Scanner(fileName);
                Parser parser = new Parser(scanner);
                ast = parser.buildAST();
                String text[] = ast.getAST().split("\n");
                List<String> lines = new LinkedList<>();

                for (int i = 0; i < text.length; i++) {
                    lines.add(text[i]);
                }

                Node root = CreateTree.nodeFromFile(lines);
                ASTtoST.astToSt(root);

                // System.out.println(root.getNumChild());


                ArrayList<Stack<EleValue>> controls = ElementParser.generateCS(root);
                CSEMachine cseMachine = new CSEMachine(controls);
                cseMachine.evaluateTree();
            // }

        } catch (ExceptionHandlerOfAST exception) {
            System.out.println("Error occurred while standardizing ast:\n" + exception.getMessage());
        } catch (ExceptionHandlerOfCSE exception) {
            System.out.println("Error occurred while evaluating cse:\n" + exception.getMessage());
        } catch (IOException e) {
            throw new ParseException("ERROR: Could not read from file: " + fileName);
        } catch (RuntimeException exception) {
            System.out.println("Runtime Exception:\n" + exception.getMessage());
        } catch (Exception exception) {
            System.out.println(exception.getMessage());
        }
    }

}