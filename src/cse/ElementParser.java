package cse;

import cse.ele.EleValue;
import Interpreter.Node;

import java.util.ArrayList;

/**
 * Preorder traversal is used by the parser to transform ast to Element stacks.
 */
public class ElementParser {
    /**
     * By preorder traversal, the control structure array is created.
     */
    public static ArrayList<Stack<EleValue>> generateCS(Node root) {
        ArrayList<Stack<EleValue>> controls = new ArrayList<>();
        Stack<EleValue> control = new Stack<>();
        controls.add(control);
        generateCS(root, controls, control);
        return controls;
    }

    /**
     * Generates the control structure array by preorder traversal.
     */
    private static void generateCS(Node node, ArrayList<Stack<EleValue>> controls,
                                   Stack<EleValue> currentControl) {
        if (node.isLabel("lambda")) {
            generateCSLambda(node, controls, currentControl);
        } else if (node.isLabel("->")) {
            generateCSIf(node, controls, currentControl);
        } else if (node.isLabel("tau")) {
            generateCSTau(node, controls, currentControl);
        } else {
            // Add this node and recurse on children
            currentControl.push(new EleValue(node));
            node.forEachChild(child -> generateCS(child, controls, currentControl));
        }
    }

    /**
     *Divide the control structure on lambda nodes and navigate the sub tree using a delta node.
     */
    private static void generateCSLambda(Node node, ArrayList<Stack<EleValue>> controls,
                                         Stack<EleValue> currentControl) {
        // Get right and left children
        int newIndex = controls.size();
        Node leftChild = node.getChild(0);
        Node rightChild = node.getChild(1);

        if (leftChild.isLabel(",")) {
            ArrayList<String> children = new ArrayList<>();
            leftChild.forEachChild(child -> children.add(child.getValue()));
            String combinedParams = String.join(",", children);
            leftChild = new Node("id", combinedParams);
        }

        //control element
        String controlValue = String.format("%s %s", newIndex, leftChild.getValue());
        EleValue newControlElem = new EleValue("lambda", controlValue);
        currentControl.push(newControlElem);

        // new control structure
        Stack<EleValue> newControl = new Stack<>();
        controls.add(newControl);

        // Traverse in new structure
        generateCS(rightChild, controls, newControl);
    }

    /**
     * Split if node to then and else delta nodes and traverse in subtrees.
     */
    private static void generateCSIf(Node node, ArrayList<Stack<EleValue>> controls,
                                     Stack<EleValue> currentControl) {
        Node conditionNode = node.getChild(0);
        Node thenNode = node.getChild(1);
        Node elseNode = node.getChild(2);

        
        int thenIndex = controls.size();
        EleValue thenElem = new EleValue("delta", Integer.toString(thenIndex));
        currentControl.push(thenElem);
        Stack<EleValue> thenControl = new Stack<>();
        controls.add(thenControl);
        generateCS(thenNode, controls, thenControl);

        
        int elseIndex = controls.size();
        EleValue elseElem = new EleValue("delta", Integer.toString(elseIndex));
        currentControl.push(elseElem);
        Stack<EleValue> elseControl = new Stack<>();
        controls.add(elseControl);
        generateCS(elseNode, controls, elseControl);

        currentControl.push(new EleValue("beta"));
        generateCS(conditionNode, controls, currentControl);
    }

    /**
     * Add the amount of elements to the tau node, then walk through each subtree.
     */
    private static void generateCSTau(Node node, ArrayList<Stack<EleValue>> controls,
                                      Stack<EleValue> currentControl) {
        currentControl.push(new EleValue("tau", Integer.toString(node.getNumChild())));
        node.forEachChild(child -> generateCS(child, controls, currentControl));
    }
}
