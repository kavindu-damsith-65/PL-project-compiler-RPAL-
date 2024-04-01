package ast;

/*
 * Abstract Syntax Tree
 */
public class AST {
  private String text = "";
  private ASTNode root;

  public AST(ASTNode node) {
    this.root = node;
  }

  public String getAST() {
    preOrder(root, "");
    return text;
  }

  private void preOrder(ASTNode node, String printPrefix) {
    if (node == null)
      return;

    addNodeDetails(node, printPrefix);
    preOrder(node.getChild(), printPrefix + ".");
    preOrder(node.getSibling(), printPrefix);
  }

  private void addNodeDetails(ASTNode node, String printPrefix) {
    if (node.getType() == ASTNodeType.IDENTIFIER ||
        node.getType() == ASTNodeType.INTEGER)
      text += String.format(printPrefix + node.getType().getPrintName() + "\n", node.getValue());
    else if (node.getType() == ASTNodeType.STRING)
      text += String.format(printPrefix + node.getType().getPrintName() + "\n", node.getValue());
    else
      text += String.format(printPrefix + node.getType().getPrintName() + "\n");
  }
}