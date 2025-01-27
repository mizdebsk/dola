/*-
 * Copyright (c) 2024 Red Hat, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package io.kojan.dola.spec;

public class Condition {
    private final String expr;
    private final boolean negated;

    private Condition(String expr, boolean negated) {
        this.expr = expr;
        this.negated = negated;
    }

    public static Condition of(String expr) {
        return new Condition(expr, false);
    }

    public String getExpr() {
        return expr;
    }

    public boolean isNegated() {
        return negated;
    }

    public Condition negate() {
        return new Condition(expr, !negated);
    }

    @Override
    public String toString() {
        if (negated) {
            return "NOT [" + expr + "]";
        }
        return "[" + expr + "]";
    }

    @Override
    public boolean equals(Object obj) {
        return obj instanceof Condition c && expr.equals(c.expr) && negated == c.negated;
    }
}
