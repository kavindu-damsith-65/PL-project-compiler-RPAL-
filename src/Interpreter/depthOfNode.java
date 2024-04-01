package Interpreter;

/**
 * Depth of a node
 */
public class depthOfNode extends Node {
    private final int depth;

    /**
     * Intermediate nodes
     */
    depthOfNode(Node parent, String label, int depth) {
        super(label);
        this.depth = depth;
        if (parent != null) {
            parent.addChild(this);
        }
    }


    depthOfNode(Node parent, String label, String value, int depth) {
        super(label, value);
        this.depth = depth;
        if (parent != null) {
            parent.addChild(this);
        }
    }
    int getDepth() {
        return depth;
    }

    @Override
    depthOfNode getParent() {

        return (depthOfNode) super.getParent();
    }
}