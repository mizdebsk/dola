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
package io.kojan.dola.spec.generator;

import io.kojan.dola.spec.BuildOpt;
import io.kojan.dola.spec.CondDep;
import io.kojan.dola.spec.Condition;
import io.kojan.dola.spec.MacroDef;
import io.kojan.dola.spec.Pkg;
import io.kojan.dola.spec.Reldep;
import io.kojan.dola.spec.Script;
import io.kojan.dola.spec.ScriptType;
import io.kojan.dola.spec.Spec;
import io.kojan.dola.spec.Tag;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Objects;

public class DSG {
    private final StringBuilder sb = new StringBuilder();

    // Put each %files right after corresponding %package and %description
    public boolean optInlineFiles;
    // Sort tags
    public boolean optSortTags;
    // Sort dependencies
    public boolean optSortDeps;
    // Sort dependencies
    public boolean optSortScripts;

    private void nl() {
        sb.append('\n');
    }

    private void genComment(List<String> comment) {
        for (String line : comment) {
            sb.append('#');
            if (!line.isBlank()) {
                sb.append(' ').append(line);
            }
            nl();
        }
    }

    private void genTags(List<Tag> tags) {
        Comparator<Tag> tagCmp =
                (a, b) -> {
                    int pa = a.getPrecedence();
                    int pb = b.getPrecedence();
                    return Integer.compare(pa, pb);
                };

        List<Tag> taga = new ArrayList<>(tags);
        if (optSortTags) {
            Collections.sort(taga, tagCmp);
        }

        boolean seenSource = false;
        boolean seenPatch = false;
        for (Tag tag : taga) {
            if (tag.getName().startsWith("Source") && !seenSource) {
                seenSource = true;
                nl();
            }
            if (tag.getName().equals("Patch") && !seenPatch) {
                seenPatch = true;
                nl();
            }
            genComment(tag.getComment());
            String n = tag.getName();
            sb.append(n).append(':');
            sb.append(" ".repeat(Math.max(15 - n.length(), 0)));
            sb.append(tag.getValue());
            nl();
        }
    }

    private boolean isSpecialDep(Reldep r) {
        return r.getName().startsWith("maven-local")
                || r.getName().startsWith("javapackages-local")
                || r.getName().startsWith("dola");
    }

    private void genDeps(List<CondDep> deps) {

        Comparator<Condition> condCmp =
                (a, b) -> {
                    if (!a.getExpr().equals(b.getExpr())) {
                        return a.getExpr().compareTo(b.getExpr());
                    }
                    return Boolean.compare(a.isNegated(), b.isNegated());
                };

        Comparator<CondDep> depCmp =
                (a, b) -> {
                    int pa = a.getPrecedence();
                    int pb = b.getPrecedence();
                    if (pa != pb) {
                        return Integer.compare(pa, pb);
                    }
                    Condition ca = a.getCondition();
                    Condition cb = b.getCondition();
                    if (!Objects.equals(ca, cb)) {
                        if (ca == null) {
                            return -1;
                        }
                        if (cb == null) {
                            return +1;
                        }
                        return condCmp.compare(ca, cb);
                    }
                    Reldep ra = a.getReldep();
                    Reldep rb = b.getReldep();
                    if (isSpecialDep(ra) != isSpecialDep(rb)) {
                        if (isSpecialDep(ra)) {
                            return -1;
                        }
                        return +1;
                    }
                    if (a.getComment().isEmpty() != b.getComment().isEmpty()) {
                        if (a.getComment().isEmpty()) {
                            return -1;
                        }
                        return +1;
                    }
                    return ra.getRpmStr().compareTo(rb.getRpmStr());
                };

        List<CondDep> depa = new ArrayList<>(deps);
        if (optSortDeps) {
            Collections.sort(depa, depCmp);
        }

        Condition cc = null;
        for (CondDep dep : depa) {
            Condition c = dep.getCondition();
            if (c == null) {
                if (cc != null) {
                    sb.append("%endif");
                    nl();
                }
            } else {
                if (cc == null) {
                    sb.append("%if " + c.getExpr());
                    nl();
                    if (c.isNegated()) {
                        throw new IllegalStateException("initial cond negated");
                    }
                } else {
                    if (c.getExpr().equals(cc.getExpr())) {
                        if (!cc.isNegated() && c.isNegated()) {
                            sb.append("%else");
                            nl();
                        } else if (cc.isNegated() != c.isNegated()) {
                            throw new IllegalStateException("cond negated to not negated");
                        }
                    } else {
                        sb.append("%endif");
                        nl();
                        sb.append("%if " + c.getExpr());
                        nl();
                        if (c.isNegated()) {
                            throw new IllegalStateException("initial cond negated");
                        }
                    }
                }
            }
            cc = c;
            genComment(dep.getComment());
            String n = dep.getTag();
            sb.append(n).append(':');
            sb.append(" ".repeat(Math.max(15 - n.length(), 0)));
            sb.append(dep.getReldep().getRpmStr());
            nl();
        }
        if (cc != null) {
            sb.append("%endif");
            nl();
        }
    }

    private void genSection(List<String> lines) {
        for (String line : lines) {
            sb.append(line);
            nl();
        }
    }

    private void genMainFiles(Pkg main) {
        if (main.getFiles() != null) {
            sb.append("%files");
            for (String mfiles : main.getMfiles()) {
                sb.append(" -f ").append(mfiles);
            }
            nl();
            genSection(main.getFiles());
            nl();
        }
    }

    private void genSubFiles(Spec spec, Pkg pkg) {
        String pn = pkg.getName();
        String pnn =
                pn.startsWith(spec.getMainPkg().getName() + "-")
                        ? pn.substring(spec.getMainPkg().getName().length() + 1)
                        : "-n " + pn;
        sb.append("%files " + pnn);
        for (String mfiles : pkg.getMfiles()) {
            sb.append(" -f ").append(mfiles);
        }
        nl();
        genSection(pkg.getFiles());
        nl();
    }

    public void generate(Spec spec) {
        if (!spec.getMacros().isEmpty()) {
            for (MacroDef macro : spec.getMacros()) {
                genComment(macro.getComment());
                sb.append(macro.getLine());
                nl();
            }
            nl();
        }
        Pkg main = spec.getMainPkg();
        genTags(main.getTags());
        nl();
        if (!main.getDeps().isEmpty()) {
            genDeps(main.getDeps());
            nl();
        }
        if (main.getBuildSys() != null) {
            genComment(main.getBuildSys().getComment());
            sb.append("BuildSystem:    maven");
            nl();
            for (BuildOpt bopt : main.getBuildSys().getBuildOpts()) {
                genComment(bopt.getComment());
                sb.append("BuildOption:    ").append(bopt.getOpt());
                nl();
            }
            nl();
        }
        sb.append("%description");
        nl();
        genSection(main.getDescription());
        nl();
        if (optInlineFiles) {
            genMainFiles(main);
        }
        for (Pkg pkg : spec.getSubpkgs()) {
            String pn = pkg.getName();
            String pnn =
                    pn.startsWith(main.getName() + "-")
                            ? pn.substring(main.getName().length() + 1)
                            : "-n " + pn;
            sb.append("%package " + pnn);
            nl();
            genTags(pkg.getTags());
            genDeps(pkg.getDeps());
            nl();
            sb.append("%description " + pnn);
            nl();
            genSection(pkg.getDescription());
            nl();
            if (optInlineFiles) {
                genSubFiles(spec, pkg);
            }
        }
        Comparator<ScriptType> scriptTypeCmp =
                (a, b) -> {
                    int pa = a.getPrecedence();
                    int pb = b.getPrecedence();
                    return Integer.compare(pa, pb);
                };
        Collection<Script> scripts = spec.getScripts().values();
        if (optSortScripts) {
            List<ScriptType> types = new ArrayList<>(spec.getScripts().keySet());
            Collections.sort(types, scriptTypeCmp);
            scripts = new ArrayList<>();
            for (ScriptType type : types) {
                scripts.add(spec.getScripts().get(type));
            }
        }
        for (Script script : scripts) {
            sb.append("%" + script.getName());
            nl();
            genSection(script.getLines());
            nl();
        }
        if (!optInlineFiles) {
            genMainFiles(main);
            for (Pkg pkg : spec.getSubpkgs()) {
                genSubFiles(spec, pkg);
            }
        }
        sb.append("%changelog");
        nl();
        genSection(spec.getChangelog());
    }

    @Override
    public String toString() {
        return sb.toString();
    }
}
