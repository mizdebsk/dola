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

import java.util.ArrayList;
import java.util.List;

public class CondDep extends AbstractCommentable {
    private final int prec;
    private final String tag;
    private final Reldep reldep;
    private final Condition cond;

    private CondDep(int prec, String tag, Reldep reldep, Condition cond, List<String> comment) {
        super(comment);
        this.prec = prec;
        this.tag = tag;
        this.reldep = reldep;
        this.cond = cond;
    }

    public static CondDep ofBuildRequires(Reldep reldep, List<String> comment) {
        return new CondDep(1, "BuildRequires", reldep, null, List.copyOf(comment));
    }

    public static CondDep ofRequires(Reldep reldep, List<String> comment) {
        return new CondDep(2, "Requires", reldep, null, List.copyOf(comment));
    }

    public static CondDep ofObsoletes(Reldep reldep, List<String> comment) {
        return new CondDep(3, "Obsoletes", reldep, null, List.copyOf(comment));
    }

    public static CondDep ofProvides(Reldep reldep, List<String> comment) {
        return new CondDep(4, "Provides", reldep, null, List.copyOf(comment));
    }

    public static CondDep ofSuggests(Reldep reldep, List<String> comment) {
        return new CondDep(5, "Suggests", reldep, null, List.copyOf(comment));
    }

    public int getPrecedence() {
        return prec;
    }

    public String getTag() {
        return tag;
    }

    public Reldep getReldep() {
        return reldep;
    }

    public Condition getCondition() {
        return cond;
    }

    public CondDep addComment(List<String> comment) {
        List<String> cc = new ArrayList<String>(getComment());
        cc.addAll(comment);
        return new CondDep(prec, tag, reldep, cond, List.copyOf(cc));
    }

    public CondDep setCondition(Condition cond) {
        if (this.cond != null) {
            throw new RuntimeException("Semantic error: nested conditions");
        }
        return new CondDep(prec, tag, reldep, cond, getComment());
    }

    @Override
    public String toString() {
        if (cond == null) {
            return tag + ": " + reldep + " (always)";
        }
        return tag + ": " + reldep + " when " + cond;
    }
}
