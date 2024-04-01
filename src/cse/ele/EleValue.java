package cse.ele;

import Interpreter.Node;

import java.util.Objects;

/**
 * EleValue which will store all elements except tuples.
 */
public class EleValue extends EleValueOrTuple {
    private final String value;

    /**
     * Create element from labels
     */
    public EleValue(String label) {
        super(label);
        this.value = null;
    }

    /**
     * Create element from label and value
     */
    public EleValue(String label, String value) {
        super(label);
        this.value = value;
    }

    /**
     * Create element from node
     */
    public EleValue(Node node) {
        super(node.getLabel());
        this.value = node.getValue();
    }

    public String getValue() {
        return value;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        EleValue that = (EleValue) o;
        return Objects.equals(value, that.value);
    }

    @Override
    public int hashCode() {
        return Objects.hash(value);
    }

    @Override
    public String toString() {
        if (value == null) return getLabel();
        return String.format("%s(%s)", getLabel(), getValue());
    }
}