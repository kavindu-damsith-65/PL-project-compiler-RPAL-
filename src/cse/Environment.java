package cse;


import cse.ele.EleValueOrTuple;

import java.util.HashMap;

/**
 * Environment to keep entries on names and their values.
 */

public class Environment {
    private Environment parent;
    private final HashMap<String, EleValueOrTuple> memory;

    /**
     * primary environment.
     */
    Environment() {
        this.memory = new HashMap<>();
        remember("Print", null);
        remember("Isstring", null);
        remember("Isinteger", null);
        remember("Istruthvalue", null);
        remember("Istuple", null);
        remember("Isfunction", null);
        remember("Null", null);
        remember("Order", null);
        remember("Stern", null);
        remember("Stem", null);
        remember("ItoS", null);
        remember("neg", null);
        remember("not", null);
        remember("Conc", null);
    }

    /**
     * empty sub environment.
     */
    Environment(Environment parent) {
        this.memory = new HashMap<>();
        this.parent = parent;
    }

    /**
     * sub environment with one entry.
     */
    Environment(Environment parent, String key, EleValueOrTuple value) {
        this.memory = new HashMap<>();
        this.parent = parent;
        remember(key, value);
    }

    /**
     * Remember an entry. Error if already defined.
     */
    void remember(String key, EleValueOrTuple value) {
        if (memory.containsKey(key)) {
            throw new RuntimeException("Variable is already defined: " + key);
        }
        memory.put(key, value);
    }

    /**
     * Get the value of a variable.
     * Returns null if defined in primary environment.
     * Throws error if undefined.
     */
    EleValueOrTuple lookup(String id) {
        if (memory.containsKey(id)) {
            return memory.get(id);
        }
        if (parent == null) {
            // Primary Environment and not found
            throw new RuntimeException("Undefined variable: " + id);
        }
        return parent.lookup(id);
    }

    @Override
    public String toString() {
        if (parent != null) {
            String[] data = new String[memory.size()];
            int i = 0;
            for (String key : memory.keySet()) {
                data[i++] = "[" + memory.get(key) + "/" + key + "]";
            }
            return parent + " > " + String.join("", data);
        }
        return "PE";
    }
}
