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
import io.kojan.dola.build.DeclarativeBuild;
import io.kojan.dola.build.DeclarativeBuildBuilder;
import io.kojan.dola.build.PackagingOption;
import io.kojan.dola.build.TransformOption;
import org.fedoraproject.xmvn.artifact.Artifact;

public class BuildOptionParser {
    private final Lexer lx;
    private final DeclarativeBuildBuilder db;

    public BuildOptionParser(String rpmName, String str) throws BuildOptionParseException {
        this.lx = new Lexer(str);
        this.db = new DeclarativeBuildBuilder(rpmName);
    }

    private boolean tryParseFlag() {
        if (lx.isKeyword("skipTests")) {
            db.skipTests(true);
            return true;
        }
        if (lx.isKeyword("singletonPackaging")) {
            db.singletonPackaging(true);
            return true;
        }
        if (lx.isKeyword("usesJavapackagesBootstrap")) {
            db.usesJavapackagesBootstrap(true);
            return true;
        }
        return false;
    }

    private boolean tryParseMavenOptions() throws BuildOptionParseException {
        if (lx.isKeyword("mavenOption")) {
            db.mavenOption(lx.next().expectLiteral());
            return true;
        }
        if (lx.isKeyword("mavenOptions")) {
            lx.next().expectBlockBegin();
            while (!lx.next().isBlockEnd()) {
                db.mavenOption(lx.expectLiteral());
            }
            return true;
        }
        return false;
    }

    private boolean tryParseToolchainOptions() throws BuildOptionParseException {
        if (lx.isKeyword("xmvnToolchain")) {
            db.xmvnToolchain(lx.next().expectLiteral());
            return true;
        }
        return false;
    }

    private boolean tryParseTestExcludes() throws BuildOptionParseException {
        if (lx.isKeyword("testExclude")) {
            db.testExclude(lx.next().expectLiteral());
            return true;
        }
        if (lx.isKeyword("testExcludes")) {
            lx.next().expectBlockBegin();
            while (!lx.next().isBlockEnd()) {
                db.testExclude(lx.expectLiteral());
            }
            return true;
        }
        return false;
    }

    private boolean tryParseBuildRequires() throws BuildOptionParseException {
        if (lx.isKeyword("buildRequire")) {
            db.extraBuildReq(Artifact.of(lx.next().expectLiteral()));
            return true;
        }
        if (lx.isKeyword("buildRequireFilter")) {
            db.filteredBuildReq(Artifact.of(lx.next().expectLiteral()));
            return true;
        }
        if (lx.isKeyword("buildRequires")) {
            lx.next().expectBlockBegin();
            while (!lx.next().isBlockEnd()) {
                if (lx.isKeyword("filter")) {
                    db.filteredBuildReq(Artifact.of(lx.next().expectLiteral()));
                } else {
                    db.extraBuildReq(Artifact.of(lx.expectLiteral()));
                }
            }
            return true;
        }
        return false;
    }

    private PackagingOption parseArtifactSelectorLiteral(String globLiteral)
            throws BuildOptionParseException {
        if (globLiteral.indexOf(':') < 0) {
            lx.error("Syntax error: artifact glob must contain a colon");
        }
        String[] globArray = globLiteral.split(":", 2);
        return PackagingOption.of(globArray[0], globArray[1]);
    }

    private Alias parseAliasLiteral(String aliasLiteral) throws BuildOptionParseException {
        if (aliasLiteral.indexOf(':') < 0) {
            lx.error("Syntax error: alias specifier must contain a colon");
        }
        String[] aliasArray = aliasLiteral.split(":", 2);
        return Alias.of(aliasArray[0], aliasArray[1]);
    }

    private boolean tryParsePackagingOptions() throws BuildOptionParseException {
        if (!lx.isKeyword("artifact")) {
            return false;
        }
        PackagingOption po = parseArtifactSelectorLiteral(lx.next().expectLiteral());
        lx.next().expectBlockBegin();
        while (!lx.next().isBlockEnd()) {
            if (lx.isKeyword("package")) {
                if (!po.getTargetPackage().isEmpty()) {
                    lx.error("Semantic error: duplicate target package specified");
                }
                po = po.withTargetPackage(lx.next().expectLiteral());
            } else if (lx.isKeyword("noInstall")) {
                if (!po.getTargetPackage().isEmpty()) {
                    lx.error("Semantic error: duplicate target package specified");
                }
                po = po.withTargetPackage("__noinstall");
            } else if (lx.isKeyword("repository")) {
                if (!po.getTargetRepository().isEmpty()) {
                    lx.error("Semantic error: duplicate target repository specified");
                }
                po = po.withTargetRepository(lx.next().expectLiteral());
            } else if (lx.isKeyword("file")) {
                po = po.withFile(lx.next().expectLiteral());
            } else if (lx.isKeyword("files")) {
                lx.next().expectBlockBegin();
                while (!lx.next().isBlockEnd()) {
                    po = po.withFile(lx.expectLiteral());
                }
            } else if (lx.isKeyword("compatVersion")) {
                po = po.withCompatVersion(lx.next().expectLiteral());
            } else if (lx.isKeyword("compatVersions")) {
                lx.next().expectBlockBegin();
                while (!lx.next().isBlockEnd()) {
                    po = po.withCompatVersion(lx.expectLiteral());
                }
            } else if (lx.isKeyword("alias")) {
                po = po.withAlias(parseAliasLiteral(lx.next().expectLiteral()));
            } else if (lx.isKeyword("aliases")) {
                lx.next().expectBlockBegin();
                while (!lx.next().isBlockEnd()) {
                    po = po.withAlias(parseAliasLiteral(lx.expectLiteral()));
                }
            } else {
                lx.error(
                        "Syntax error: expected keyword related to artifact packaging, or closing brace");
            }
        }
        db.packagingOption(po);
        return true;
    }

    private boolean tryParseRemoveParent(String selector) throws BuildOptionParseException {
        if (lx.isKeyword("removeParent")) {
            if (lx.lookaheadIsLiteral()) {
                db.modelTransformation(
                        TransformOption.ofRemoveParent(lx.next().expectLiteral(), selector));
            } else {
                db.modelTransformation(TransformOption.ofRemoveParent(selector));
            }
            return true;
        }
        return false;
    }

    private boolean tryParseRemovePlugins(String selector) throws BuildOptionParseException {
        if (lx.isKeyword("removePlugin")) {
            db.modelTransformation(
                    TransformOption.ofRemovePlugin(lx.next().expectLiteral(), selector));
            return true;
        }
        if (lx.isKeyword("removePlugins")) {
            lx.next().expectBlockBegin();
            while (!lx.next().isBlockEnd()) {
                db.modelTransformation(
                        TransformOption.ofRemovePlugin(lx.expectLiteral(), selector));
            }
            return true;
        }
        return false;
    }

    private boolean tryParseRemoveDependencies(String selector) throws BuildOptionParseException {
        if (lx.isKeyword("removeDependency")) {
            db.modelTransformation(
                    TransformOption.ofRemoveDependency(lx.next().expectLiteral(), selector));
            return true;
        }
        if (lx.isKeyword("removeDependencies")) {
            lx.next().expectBlockBegin();
            while (!lx.next().isBlockEnd()) {
                db.modelTransformation(
                        TransformOption.ofRemoveDependency(lx.expectLiteral(), selector));
            }
            return true;
        }
        return false;
    }

    private boolean tryParseRemoveSubproject(String selector) throws BuildOptionParseException {
        if (lx.isKeyword("removeSubproject")) {
            db.modelTransformation(
                    TransformOption.ofRemoveSubproject(lx.next().expectLiteral(), selector));
            return true;
        }
        if (lx.isKeyword("removeSubprojects")) {
            lx.next().expectBlockBegin();
            while (!lx.next().isBlockEnd()) {
                db.modelTransformation(
                        TransformOption.ofRemoveSubproject(lx.expectLiteral(), selector));
            }
            return true;
        }
        return false;
    }

    private boolean tryParseAddDependencies(String selector) throws BuildOptionParseException {
        if (lx.isKeyword("addDependency")) {
            db.modelTransformation(
                    TransformOption.ofAddDependency(lx.next().expectLiteral(), selector));
            return true;
        }
        if (lx.isKeyword("addDependencies")) {
            lx.next().expectBlockBegin();
            while (!lx.next().isBlockEnd()) {
                db.modelTransformation(
                        TransformOption.ofAddDependency(lx.expectLiteral(), selector));
            }
            return true;
        }
        return false;
    }

    private boolean tryParseTransformOptions() throws BuildOptionParseException {
        if (lx.isKeyword("transform")) {
            String selector = lx.next().expectLiteral();
            lx.next().expectBlockBegin();
            while (!lx.next().isBlockEnd()) {
                if (tryParseRemoveParent(selector)
                        || tryParseRemovePlugins(selector)
                        || tryParseRemoveDependencies(selector)
                        || tryParseRemoveSubproject(selector)
                        || tryParseAddDependencies(selector)) {
                } else {
                    lx.error("Syntax error: expected transformation keyword, or closing brace");
                }
            }
            return true;
        }
        return false;
    }

    public DeclarativeBuild parse() throws BuildOptionParseException {
        while (!lx.next().isEndOfInput()) {
            if (tryParseFlag()
                    || tryParseToolchainOptions()
                    || tryParseMavenOptions()
                    || tryParseTestExcludes()
                    || tryParseBuildRequires()
                    || tryParsePackagingOptions()
                    || tryParseTransformOptions()) {
            } else {
                lx.error("Syntax error: expected global keyword, or end of build options");
            }
        }
        return db.build();
    }

    public String format() {
        return lx.asString();
    }
}
