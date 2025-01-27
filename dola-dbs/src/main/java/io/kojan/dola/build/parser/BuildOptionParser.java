/*-
 * Copyright (c) 2025 Red Hat, Inc.
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
package io.kojan.dola.build.parser;

import io.kojan.dola.build.Alias;
import io.kojan.dola.build.DeclarativeBuildBuilder;
import io.kojan.dola.build.PackagingOption;
import io.kojan.dola.build.TransformOption;

public class BuildOptionParser {
    private int pos;
    private final String str;
    private final DeclarativeBuildBuilder ctx;

    public BuildOptionParser(String str, DeclarativeBuildBuilder ctx) {
        this.str = str;
        this.ctx = ctx;
    }

    private RuntimeException error(String msg) {
        String p = msg + ":\n  Expr: " + str + "\n" + "  Here: " + (" ".repeat(pos)) + "^";
        System.err.println(p);
        return new RuntimeException(p);
    }

    private RuntimeException error() {
        return error("Syntax error");
    }

    private String rest() {
        return str.substring(pos);
    }

    private boolean has(String s) {
        if (rest().startsWith(s)) {
            pos += s.length();
            return true;
        }
        return false;
    }

    private boolean is(String s) {
        return str.length() - pos == s.length() && has(s);
    }

    private void parseCondition() {
        throw error("conditions not implemented yet");
    }

    private void parseTransformOption() {
        if (has("/dep=")) {
            ctx.modelTransformation(new TransformOption("removeDependency", rest()));
        } else if (has("/plug=")) {
            ctx.modelTransformation(new TransformOption("removePlugin", rest()));
        } else if (has("/parent=")) {
            ctx.modelTransformation(new TransformOption("removeParent", rest()));
        } else if (has("/mod=")) {
            ctx.modelTransformation(new TransformOption("removeSubproject", rest()));
        } else if (has("/")) {
            if (rest().contains(":")) {
                ctx.modelTransformation(new TransformOption("removeDependency", rest()));
                ctx.modelTransformation(new TransformOption("removePlugin", rest()));
                ctx.modelTransformation(new TransformOption("removeParent", rest()));
            } else {
                ctx.modelTransformation(new TransformOption("removeSubproject", rest()));
            }
        } else if (has("+dep=") || has("+")) {
            ctx.modelTransformation(new TransformOption("addDependency", rest()));
        } else {
            error();
        }
    }

    private void parseShortOption() {
        if (is("Fjpb")) {
            ctx.usesJavapackagesBootstrap(true);
        } else if (has("P") || has("D") || is("X")) {
            ctx.mavenOption(str);
        } else if (is("f")) {
            ctx.skipTests(true);
        } else if (has("B")) {
            if (has("!")) {
                ctx.filteredBuildReq(org.fedoraproject.xmvn.artifact.Artifact.of(rest()));
            } else {
                ctx.extraBuildReq(org.fedoraproject.xmvn.artifact.Artifact.of(rest()));
            }
        } else {
            throw error();
        }
    }

    private void parseLongOption() {
        throw error();
    }

    private String parseId() {
        StringBuilder sb = new StringBuilder();
        while (pos < str.length()) {
            char ch = str.charAt(pos);
            if ((ch >= 'a' && ch <= 'z')
                    || (ch >= 'A' && ch <= 'Z')
                    || (ch >= '0' && ch <= '9')
                    || ch == '-'
                    || ch == '.'
                    || ch == '/'
                    || ch == '_') {
                sb.append(ch);
                pos++;
            } else {
                break;
            }
        }
        return sb.toString();
    }

    private void parsePackagingOption() {
        String gidGlob = parseId();
        if (!has(":")) {
            throw error();
        }
        String aidGlob = parseId();
        PackagingOption po = PackagingOption.of(gidGlob, aidGlob);
        while (!is("")) {
            if (has("@")) {
                String targetPackage = parseId();
                po = po.withTargetPackage(targetPackage);
                continue;
            }
            if (has("|")) {
                String aliasGid = parseId();
                if (!has(":")) {
                    throw error();
                }
                String aliasAid = parseId();
                po = po.withAlias(Alias.of(aliasGid, aliasAid));
                continue;
            }
            if (has(">")) {
                String file = parseId();
                po = po.withFile(file);
                continue;
            }
            if (has(";")) {
                String compatVersion = parseId();
                po = po.withCompatVersion(compatVersion);
                continue;
            }
            throw error();
        }
        ctx.packagingOption(po);
    }

    private void parseTestOption() {
        ctx.testExclude(rest());
    }

    public void parse() {
        if (has("[")) {
            parseCondition();
        } else if (has("--")) {
            parseLongOption();
        } else if (has("-")) {
            parseShortOption();
        } else if (has("+") || has("/")) {
            pos--;
            parseTransformOption();
        } else if (has("=")) {
            parsePackagingOption();
        } else if (has("!")) {
            parseTestOption();
        } else {
            throw error();
        }
    }
}
