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

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatExceptionOfType;

import io.kojan.dola.build.Alias;
import io.kojan.dola.build.DeclarativeBuild;
import org.fedoraproject.xmvn.artifact.Artifact;
import org.junit.jupiter.api.Test;

class BuildOptionParserTest {

    DeclarativeBuild parse(String s) throws Exception {
        return new BuildOptionParser("mypkg", s.replace('\n', ' ')).parse();
    }

    DeclarativeBuild parsed(String s) throws Exception {
        DeclarativeBuild db = parse(s);
        assertThat(db).isNotNull();
        return db;
    }

    String unindent(String s) {
        return (s + "    ").stripIndent().strip();
    }

    @Test
    void empty() throws Exception {
        parsed("");
    }

    @Test
    void whitespaceOnly() throws Exception {
        parsed("  ");
    }

    @Test
    void keywordTypo() throws Exception {
        String code =
                """
                    skipTestsss
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected global keyword, or end of build options
                    at BuildOption:
                    ~~~~~~~~~~~
                    skipTestsss
                    ~~~~~~~~~~~
                    ^--- here
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void transformBlockEmpty() throws Exception {
        String code =
                """
                    transform "foo:bar" {
                    }
                """;
        parsed(code);
    }

    @Test
    void skipTests() throws Exception {
        String code =
                """
                    skipTests
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.isSkipTests()).isTrue();
    }

    @Test
    void singletonPackaging() throws Exception {
        String code =
                """
                    singletonPackaging
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.isSingletonPackaging()).isTrue();
    }

    @Test
    void usesJavapackagesBootstrap() throws Exception {
        String code =
                """
                    usesJavapackagesBootstrap
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.usesJavapackagesBootstrap()).isTrue();
    }

    @Test
    void xmvnToolchain() throws Exception {
        String code =
                """
                    xmvnToolchain "openjdk25"
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getXmvnToolchain()).isEqualTo("openjdk25");
    }

    @Test
    void mavenOption() throws Exception {
        String code =
                """
                    mavenOption "-Prun-its"
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getMavenOptions()).containsExactly("-Prun-its");
    }

    @Test
    void mavenOptions() throws Exception {
        String code =
                """
                    mavenOptions {
                        "-X"
                        "-Dfoo=bar"
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getMavenOptions()).containsExactly("-X", "-Dfoo=bar");
    }

    @Test
    void buildRequire() throws Exception {
        String code =
                """
                    buildRequire "foo:bar"
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getExtraBuildReqs()).containsExactlyInAnyOrder(Artifact.of("foo:bar"));
        assertThat(db.getFilteredBuildReqs()).isEmpty();
    }

    @Test
    void buildRequireFilter() throws Exception {
        String code =
                """
                    buildRequireFilter "foo:bar"
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getExtraBuildReqs()).isEmpty();
        assertThat(db.getFilteredBuildReqs()).containsExactlyInAnyOrder(Artifact.of("foo:bar"));
    }

    @Test
    void buildRequireVersion() throws Exception {
        String code =
                """
                    buildRequireVersion "foo:bar" "1.2.3"
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getBuildReqVersions()).containsEntry(Artifact.of("foo:bar"), "1.2.3");
    }

    @Test
    void buildRequiresOne() throws Exception {
        String code =
                """
                    buildRequires {
                        "foo:bar"
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getExtraBuildReqs()).containsExactlyInAnyOrder(Artifact.of("foo:bar"));
        assertThat(db.getFilteredBuildReqs()).isEmpty();
    }

    @Test
    void buildRequiresTwo() throws Exception {
        String code =
                """
                    buildRequires {
                        "foo:bar"
                        "com.example:eee:2.5"
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getExtraBuildReqs())
                .containsExactlyInAnyOrder(
                        Artifact.of("foo:bar"), Artifact.of("com.example:eee:2.5"));
        assertThat(db.getFilteredBuildReqs()).isEmpty();
    }

    @Test
    void buildRequiresCombined() throws Exception {
        String code =
                """
                    buildRequires {
                        "foo:bar"
                        filter "*:baz"
                        version "org.xyzzy:*" "42"
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getExtraBuildReqs()).containsExactlyInAnyOrder(Artifact.of("foo:bar"));
        assertThat(db.getFilteredBuildReqs()).containsExactlyInAnyOrder(Artifact.of("*:baz"));
        assertThat(db.getBuildReqVersions()).containsEntry(Artifact.of("org.xyzzy:*"), "42");
    }

    @Test
    void testExclude() throws Exception {
        String code =
                """
                    testExclude "BadTest"
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTestExcludes()).containsExactly("BadTest");
    }

    @Test
    void testExcludesOne() throws Exception {
        String code =
                """
                    testExcludes {
                        "BadTest"
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTestExcludes()).containsExactly("BadTest");
    }

    @Test
    void testExcludesThree() throws Exception {
        String code =
                """
                    testExcludes {
                        "BadTest"
                        "AnotherBadOne"
                        "YetAnother"
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTestExcludes()).containsExactly("BadTest", "AnotherBadOne", "YetAnother");
    }

    @Test
    void artifactEmpty() throws Exception {
        String code =
                """
                    artifact "some:thing" {}
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getPackagingOptions()).hasSize(1);
        assertThat(db.getPackagingOptions().getFirst().getGroupIdGlob()).isEqualTo("some");
        assertThat(db.getPackagingOptions().getFirst().getArtifactIdGlob()).isEqualTo("thing");
    }

    @Test
    void artifactPackage() throws Exception {
        String code =
                """
                    artifact "some:thing" {
                        package "sub1"
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getPackagingOptions()).hasSize(1);
        assertThat(db.getPackagingOptions().getFirst().getTargetPackage()).isEqualTo("sub1");
    }

    @Test
    void artifactNoInstall() throws Exception {
        String code =
                """
                    artifact "some:thing" {noInstall}
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getPackagingOptions()).hasSize(1);
        assertThat(db.getPackagingOptions().getFirst().getTargetPackage()).isEqualTo("__noinstall");
    }

    @Test
    void artifactRepository() throws Exception {
        String code =
                """
                    artifact "some:thing" {
                        repository "my-repo"
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getPackagingOptions()).hasSize(1);
        assertThat(db.getPackagingOptions().getFirst().getTargetRepository()).isEqualTo("my-repo");
    }

    @Test
    void artifactFile() throws Exception {
        String code =
                """
                    artifact "some:thing" {
                        file "foo/bar"
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getPackagingOptions()).hasSize(1);
        assertThat(db.getPackagingOptions().getFirst().getFiles()).containsExactly("foo/bar");
    }

    @Test
    void artifactFilesOne() throws Exception {
        String code =
                """
                    artifact "some:thing" {
                        files { "foo/bar" }
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getPackagingOptions()).hasSize(1);
        assertThat(db.getPackagingOptions().getFirst().getFiles()).containsExactly("foo/bar");
    }

    @Test
    void artifactFilesThree() throws Exception {
        String code =
                """
                    artifact "some:thing" {
                        files {
                            "foo/bar"
                            "baz" "xyzzy" }
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getPackagingOptions()).hasSize(1);
        assertThat(db.getPackagingOptions().getFirst().getFiles())
                .containsExactly("foo/bar", "baz", "xyzzy");
    }

    @Test
    void artifactCompatVersion() throws Exception {
        String code =
                """
                    artifact "some:thing" {
                        compatVersion "1.2.3"
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getPackagingOptions()).hasSize(1);
        assertThat(db.getPackagingOptions().getFirst().getCompatVersions())
                .containsExactly("1.2.3");
    }

    @Test
    void artifactCompatVersionsOne() throws Exception {
        String code =
                """
                    artifact "some:thing" {
                        compatVersions { "1.2.3" }
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getPackagingOptions()).hasSize(1);
        assertThat(db.getPackagingOptions().getFirst().getCompatVersions())
                .containsExactly("1.2.3");
    }

    @Test
    void artifactCompatVersionsThree() throws Exception {
        String code =
                """
                    artifact "some:thing" {
                        compatVersions {
                            "1.2.3"
                            "1.2.4"
                            "1.0"
                        }
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getPackagingOptions()).hasSize(1);
        assertThat(db.getPackagingOptions().getFirst().getCompatVersions())
                .containsExactly("1.2.3", "1.2.4", "1.0");
    }

    @Test
    void artifactAlias() throws Exception {
        String code =
                """
                    artifact "some:thing" {
                        alias ":aid-alias"
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getPackagingOptions()).hasSize(1);
        assertThat(db.getPackagingOptions().getFirst().getAliases())
                .containsExactly(Alias.of("", "aid-alias"));
    }

    @Test
    void artifactAliasesOne() throws Exception {
        String code =
                """
                    artifact "some:thing" {
                        aliases { ":aid-alias" }
                    }
                """;
        DeclarativeBuild db = parse(code);
        assertThat(db.getPackagingOptions()).hasSize(1);
        assertThat(db.getPackagingOptions().getFirst().getAliases())
                .containsExactly(Alias.of("", "aid-alias"));
        assertThat(db).isNotNull();
    }

    @Test
    void artifactAliasesThree() throws Exception {
        String code =
                """
                    artifact "some:thing" {
                        aliases {
                            ":aid-alias"
                            "com.foo:my-art"
                            "another:alias"
                        }
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getPackagingOptions()).hasSize(1);
        assertThat(db.getPackagingOptions().getFirst().getAliases())
                .containsExactly(
                        Alias.of("", "aid-alias"),
                        Alias.of("com.foo", "my-art"),
                        Alias.of("another", "alias"));
    }

    @Test
    void transformEmpty() throws Exception {
        String code =
                """
                    transform "some:thing" {}
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTransformOptions()).hasSize(0);
    }

    @Test
    void transformRemoveParentLone() throws Exception {
        String code =
                """
                    transform "some:thing" {
                        removeParent
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTransformOptions()).hasSize(1);
    }

    @Test
    void transformRemoveParentArg() throws Exception {
        String code =
                """
                    transform "some:thing" {
                        removeParent "com.foo:my-parent"
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTransformOptions()).hasSize(1);
    }

    @Test
    void transformRemoveDependency() throws Exception {
        String code =
                """
                    transform "some:thing" {
                        removeDependency ":foo"
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTransformOptions()).hasSize(1);
    }

    @Test
    void transformRemoveDependenciesOne() throws Exception {
        String code =
                """
                    transform "some:thing" {
                        removeDependencies { "foo:bar" }
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTransformOptions()).hasSize(1);
    }

    @Test
    void transformRemoveDependenciesMultiple() throws Exception {
        String code =
                """
                    transform "some:thing" {
                        removeDependencies {
                            ":dep1"
                            ":dep2"
                            "biz.ness:proprietary-lib"
                        }
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTransformOptions()).hasSize(3);
    }

    @Test
    void transformRemovePlugin() throws Exception {
        String code =
                """
                    transform "some:thing" {
                        removePlugin ":maven-compiler-plugin"
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTransformOptions()).hasSize(1);
    }

    @Test
    void transformRemovePluginsOne() throws Exception {
        String code =
                """
                    transform "some:thing" {
                        removePlugins {
                            ":maven-compiler-plugin"
                        }
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTransformOptions()).hasSize(1);
    }

    @Test
    void transformRemovePluginsThree() throws Exception {
        String code =
                """
                    transform "some:thing" {
                        removePlugins {
                            ":*rat*"
                            ":*sonar*"
                            ":exec-maven-plugin"
                        }
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTransformOptions()).hasSize(3);
    }

    @Test
    void transformRemoveSubproject() throws Exception {
        String code =
                """
                    transform "some:thing" {
                        removeSubproject "its"
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTransformOptions()).hasSize(1);
    }

    @Test
    void transformRemoveSubprojectsOne() throws Exception {
        String code =
                """
                    transform "some:thing" {
                        removeSubprojects {
                            "extensions"
                        }
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTransformOptions()).hasSize(1);
    }

    @Test
    void transformRemoveSubprojectsThree() throws Exception {
        String code =
                """
                    transform "some:thing" {
                        removeSubprojects {
                            "spring"
                            "mail"
                            "integration-tests"
                        }
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTransformOptions()).hasSize(3);
    }

    @Test
    void transformAddDependency() throws Exception {
        String code =
                """
                    transform "some:thing" {
                        addDependency "junit:junit:4.12:test"
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTransformOptions()).hasSize(1);
    }

    @Test
    void transformAddDependenciesOne() throws Exception {
        String code =
                """
                    transform "some:thing" {
                        addDependencies {
                            "org.foo:dep1"
                        }
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTransformOptions()).hasSize(1);
    }

    @Test
    void transformAddDependenciesThree() throws Exception {
        String code =
                """
                    transform "some:thing" {
                        addDependencies {
                            "org.foo:dep1"
                            "org.foo:dep2"
                            "org.foo:dep3"
                        }
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTransformOptions()).hasSize(3);
    }

    @Test
    void artifactBadKeyword() throws Exception {
        String code =
                """
                    artifact "some:thing" {
                       boom
                    }
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected keyword related to artifact packaging, or closing brace
                    at BuildOption: artifact "some:thing" ->
                    ~~~~~~~~~~~~~~~~~~~~~~~
                    artifact "some:thing" {
                        boom
                    ~~~~~~~~~~~~~~~~~~~~~~~
                        ^--- here
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void transformBadKeyword() throws Exception {
        String code =
                """
                    transform "some:thing" {
                        boom
                    }
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected transformation keyword, or closing brace
                    at BuildOption: transform "some:thing" ->
                    ~~~~~~~~~~~~~~~~~~~~~~~~
                    transform "some:thing" {
                        boom
                    ~~~~~~~~~~~~~~~~~~~~~~~~
                        ^--- here
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void globalBadKeyword() throws Exception {
        String code =
                """
                    mavenOption "foo" boom
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected global keyword, or end of build options
                    at BuildOption: [...]
                    ~~~~~~~~~~~~~~~~~
                    mavenOption "foo"
                    boom
                    ~~~~~~~~~~~~~~~~~
                    ^--- here
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void combined() throws Exception {
        String code =
                """
                    usesJavapackagesBootstrap
                    mavenOption "-DjavaVersion=8"
                    mavenOptions {
                        "-X"
                        "-Prun-its"
                    }
                    testExclude "BadTest"
                    testExcludes {
                        "MyTest"
                        "AnotherTest"
                    }
                    artifact "foo:bar" {
                        aliases { ":other" }
                        compatVersion "1.2.3"
                        files {
                          "foo/bar"
                          "yyy"
                        }
                        package "my-subpackage"
                    }
                    artifact ":aggregator" {
                        noInstall
                    }
                    transform "com.foo:*" {
                        removeParent
                        removeDependency ":foo"
                        removeDependency ":junit"
                        addDependency "com.bar:baz:1.2.3"
                        addDependencies {
                            "org.junit:junit:4.12:test"
                            "org.easymock:easymock:4.3:test"
                        }
                    }
                    transform "*:*" {
                        removePlugins {
                            ":first-bad-plugin"
                            "biz.proprietary:another-bad-one"
                        }
                    }
                """;
        parsed(code);
    }

    @Test
    void unclosedBraceShouldFail() throws Exception {
        String code = "artifact \"some:thing\" { package \"foo\"";
        String expectedErrorMessage =
                """
                    Syntax error: expected keyword related to artifact packaging, or closing brace
                    at BuildOption: artifact "some:thing" -> [...]
                    ~~~~~~~~~~~~~~~~~~~~~~~
                    artifact "some:thing" {
                        package "foo"
                    ~~~~~~~~~~~~~~~~~~~~~~~
                      here ----------^
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void duplicateKeywordInArtifactShouldFail() throws Exception {
        String code =
                """
                    artifact "com.foo:bar" {
                        package "sub1"
                        package "sub2"
                    }
                """;
        String expectedErrorMessage =
                """
                    Semantic error: duplicate target package specified
                    at BuildOption: artifact "com.foo:bar" -> [...] package
                    ~~~~~~~~~~~~~~~~~~~~~~~~
                    artifact "com.foo:bar" {
                        package "sub1"
                        package
                    ~~~~~~~~~~~~~~~~~~~~~~~~
                        ^--- here
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void illegalKeywordInBlockShouldFail() throws Exception {
        String code =
                """
                    artifact "com.foo:bar" {
                        unexpectedKeyword "value"
                    }
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected keyword related to artifact packaging, or closing brace
                    at BuildOption: artifact "com.foo:bar" ->
                    ~~~~~~~~~~~~~~~~~~~~~~~~
                    artifact "com.foo:bar" {
                        unexpectedKeyword
                    ~~~~~~~~~~~~~~~~~~~~~~~~
                        ^--- here
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void artifactWithInvalidAliasFormatShouldFail() throws Exception {
        String code =
                """
                    artifact "com.foo:bar" {
                        alias "noColon"
                    }
                """;
        String expectedErrorMessage =
                """
                    Syntax error: alias specifier must contain a colon
                    at BuildOption: artifact "com.foo:bar" -> alias "noColon"
                    ~~~~~~~~~~~~~~~~~~~~~~~~
                    artifact "com.foo:bar" {
                        alias "noColon"
                    ~~~~~~~~~~~~~~~~~~~~~~~~
                      here ---^
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void transformWithAllRemovals() throws Exception {
        String code =
                """
                    transform "group:artifact" {
                        removeParent "some:parent"
                        removePlugin ":plugin"
                        removeDependency "dep:one"
                        removeSubproject "sub"
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTransformOptions()).hasSize(4);
    }

    @Test
    void emptyBuildRequiresBlock() throws Exception {
        String code = "buildRequires {}";
        DeclarativeBuild db = parsed(code);
        assertThat(db.getExtraBuildReqs()).isEmpty();
        assertThat(db.getFilteredBuildReqs()).isEmpty();
    }

    @Test
    void emptyAliasesBlock() throws Exception {
        String code =
                """
                    artifact "x:y" {
                        aliases {}
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getPackagingOptions().getFirst().getAliases()).isEmpty();
    }

    @Test
    void emptyFilesBlock() throws Exception {
        String code =
                """
                    artifact "x:y" {
                        files {}
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getPackagingOptions().getFirst().getFiles()).isEmpty();
    }

    @Test
    void whitespaceBetweenKeywordsAndLiterals() throws Exception {
        String code = "mavenOption    \"-X\"";
        DeclarativeBuild db = parsed(code);
        assertThat(db.getMavenOptions()).containsExactly("-X");
    }

    @Test
    void illegalCharacter() throws Exception {
        String code =
                """
                    mavenOption @
                """;
        String expectedErrorMessage =
                """
                    Lexical error: illegal character
                    at BuildOption: mavenOption
                    ~~~~~~~~~~~~~
                    mavenOption @
                    ~~~~~~~~~~~~~
                      here -----^
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void capitalKeyword() throws Exception {
        String code =
                """
                    MavenOption "-X"
                """;
        String expectedErrorMessage =
                """
                    Lexical error: illegal character
                    at BuildOption:
                    ~~~~~~~~~~
                    M
                    ~~~~~~~~~~
                    ^--- here
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void alphanumericKeyword() throws Exception {
        String code =
                """
                    mavenOption2 "-X"
                """;
        String expectedErrorMessage =
                """
                    Lexical error: illegal character
                    at BuildOption: mavenOption
                    ~~~~~~~~~~~~
                    mavenOption2
                    ~~~~~~~~~~~~
                      here ----^
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void commentHash() throws Exception {
        String code =
                """
                    mavenOption "-X"  # this enables debugging
                """;
        String expectedErrorMessage =
                """
                    Lexical error: illegal character
                    at BuildOption: mavenOption "-X"
                    ~~~~~~~~~~~~~~~~~~
                    mavenOption "-X" #
                    ~~~~~~~~~~~~~~~~~~
                      here ----------^
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void parentheses() throws Exception {
        String code =
                """
                    artifact "foo:bar" ( alias "a:b" )
                """;
        String expectedErrorMessage =
                """
                    Lexical error: illegal character
                    at BuildOption: artifact "foo:bar"
                    ~~~~~~~~~~~~~~~~~~~~
                    artifact "foo:bar" (
                    ~~~~~~~~~~~~~~~~~~~~
                      here ------------^
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void unclosedLiteral() throws Exception {
        String code =
                """
                    mavenOption "-X
                """;
        String expectedErrorMessage =
                """
                    Lexical error: unterminated string literal
                    at BuildOption: mavenOption
                    ~~~~~~~~~~~~~~~~~
                    mavenOption "-X $
                    ~~~~~~~~~~~~~~~~~
                      here ---------^
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void tabs() throws Exception {
        String code = "foo\tbar";
        String expectedErrorMessage =
                """
                    Lexical error: TAB characters are not allowed, replace them with spaces
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void expectedKeywordFoundLiteral() throws Exception {
        String code =
                """
                    mavenOption "-X" "-Dfoo=bar"
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected global keyword, or end of build options
                    at BuildOption: [...]
                    ~~~~~~~~~~~~~~~~
                    mavenOption "-X"
                    "-Dfoo=bar"
                    ~~~~~~~~~~~~~~~~
                    ^--- here
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void expectedKeywordFoundLiteralAtTransform() throws Exception {
        String code =
                """
                    transform "foo:bar" { "xxx"
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected transformation keyword, or closing brace
                    at BuildOption: transform "foo:bar" ->
                    ~~~~~~~~~~~~~~~~~~~~~
                    transform "foo:bar" {
                        "xxx"
                    ~~~~~~~~~~~~~~~~~~~~~
                        ^--- here
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void expectedKeywordFoundOpeningBrace() throws Exception {
        String code =
                """
                    mavenOption {
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected literal (quoted string)
                    at BuildOption: mavenOption
                    ~~~~~~~~~~~~~
                    mavenOption {
                    ~~~~~~~~~~~~~
                      here -----^
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void expectedKeywordFoundClosingBrace() throws Exception {
        String code =
                """
                    mavenOption }
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected literal (quoted string)
                    at BuildOption: mavenOption
                    ~~~~~~~~~~~
                    mavenOption
                    }
                    ~~~~~~~~~~~
                    ^--- here
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void expectedKeywordFoundLiteralInner() throws Exception {
        String code =
                """
                    artifact "foo:bar" { "-X"
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected keyword related to artifact packaging, or closing brace
                    at BuildOption: artifact "foo:bar" ->
                    ~~~~~~~~~~~~~~~~~~~~
                    artifact "foo:bar" {
                        "-X"
                    ~~~~~~~~~~~~~~~~~~~~
                        ^--- here
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void expectedKeywordFoundOpeningBraceInner() throws Exception {
        String code =
                """
                    artifact "foo:bar" { {
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected keyword related to artifact packaging, or closing brace
                    at BuildOption: artifact "foo:bar" ->
                    ~~~~~~~~~~~~~~~~~~~~
                    artifact "foo:bar" {
                            {
                    ~~~~~~~~~~~~~~~~~~~~
                            ^--- here
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void expectedClosingBraceFoundEOIInner() throws Exception {
        String code =
                """
                    artifact "foo:bar" { alias "a:b"
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected keyword related to artifact packaging, or closing brace
                    at BuildOption: artifact "foo:bar" -> [...]
                    ~~~~~~~~~~~~~~~~~~~~
                    artifact "foo:bar" {
                        alias "a:b"
                    ~~~~~~~~~~~~~~~~~~~~
                      here --------^
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void expectedKeywordFoundClosingBraceTransform() throws Exception {
        String code =
                """
                    transform "foo:bar" { "-X"
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected transformation keyword, or closing brace
                    at BuildOption: transform "foo:bar" ->
                    ~~~~~~~~~~~~~~~~~~~~~
                    transform "foo:bar" {
                        "-X"
                    ~~~~~~~~~~~~~~~~~~~~~
                        ^--- here
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void expectedClosingBraceFoundOpeningBrace() throws Exception {
        String code =
                """
                    transform "foo:bar" { {
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected transformation keyword, or closing brace
                    at BuildOption: transform "foo:bar" ->
                    ~~~~~~~~~~~~~~~~~~~~~
                    transform "foo:bar" {
                            {
                    ~~~~~~~~~~~~~~~~~~~~~
                            ^--- here
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void expectedClosingBraceFoundEOI() throws Exception {
        String code =
                """
                    transform "foo:bar" {
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected transformation keyword, or closing brace
                    at BuildOption: transform "foo:bar" ->
                    ~~~~~~~~~~~~~~~~~~~~~
                    transform "foo:bar" {
                    ~~~~~~~~~~~~~~~~~~~~~
                      here --------------^
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void unrecognizedKeyword() throws Exception {
        String code =
                """
                    mavenOption "-X" alias "foo:bar"
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected global keyword, or end of build options
                    at BuildOption: [...]
                    ~~~~~~~~~~~~~~~~
                    mavenOption "-X"
                    alias
                    ~~~~~~~~~~~~~~~~
                    ^--- here
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void unrecognizedKeywordInner() throws Exception {
        String code =
                """
                    artifact "foo:bar" { mavenOption "-X"
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected keyword related to artifact packaging, or closing brace
                    at BuildOption: artifact "foo:bar" ->
                    ~~~~~~~~~~~~~~~~~~~~
                    artifact "foo:bar" {
                        mavenOption
                    ~~~~~~~~~~~~~~~~~~~~
                        ^--- here
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void expectedLiteralFoundKeyword() throws Exception {
        String code =
                """
                    mavenOption debug
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected literal (quoted string)
                    at BuildOption: mavenOption
                    ~~~~~~~~~~~~~~~~~
                    mavenOption debug
                    ~~~~~~~~~~~~~~~~~
                      here -----^
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void expectedLiteralFoundOpeningBrace() throws Exception {
        String code =
                """
                    artifact {
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected literal (quoted string)
                    at BuildOption: artifact
                    ~~~~~~~~~~
                    artifact {
                    ~~~~~~~~~~
                             ^--- here
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void expectedOpeningBraceFoundEOI() throws Exception {
        String code =
                """
                    transform "foo:bar"
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected opening brace '{'
                    at BuildOption: transform "foo:bar"
                    ~~~~~~~~~~~~~~~~~~~
                    transform "foo:bar"
                    ~~~~~~~~~~~~~~~~~~~
                      here ------------^
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void expectedOpeningBraceFoundClosingBrace() throws Exception {
        String code =
                """
                    transform "foo:bar" }
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected opening brace '{'
                    at BuildOption: transform "foo:bar"
                    ~~~~~~~~~~~~~~~~~~~
                    transform "foo:bar"
                    }
                    ~~~~~~~~~~~~~~~~~~~
                    ^--- here
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void artifactSelectorHasMissingColon() throws Exception {
        String code =
                """
                    artifact "foo" { alias "bar:baz" }
                """;
        String expectedErrorMessage =
                """
                    Syntax error: artifact glob must contain a colon
                    at BuildOption: artifact "foo"
                    ~~~~~~~~~~~~~~
                    artifact "foo"
                    ~~~~~~~~~~~~~~
                             ^--- here
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void aliasSpecifierSelectorHasMissingColon() throws Exception {
        String code =
                """
                    artifact "foo:bar" { alias "baz" }
                """;
        String expectedErrorMessage =
                """
                    Syntax error: alias specifier must contain a colon
                    at BuildOption: artifact "foo:bar" -> alias "baz"
                    ~~~~~~~~~~~~~~~~~~~~
                    artifact "foo:bar" {
                        alias "baz"
                    ~~~~~~~~~~~~~~~~~~~~
                      here ---^
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }

    @Test
    void longErrorSnippetTrimmed() throws Exception {
        String code =
                """
                    usesJavapackagesBootstrap
                    mavenOption "-DjavaVersion=8"
                    mavenOptions {
                        "-X"
                        "-Prun-its"
                    }
                    testExclude "BadTest"
                    testExcludes {
                        "MyTest"
                        "AnotherTest"
                    }
                    artifact "foo:bar" {
                        aliases { ":other" }
                        compatVersion "1.2.3"
                        files {
                          "foo/bar"
                          baz
                          "yyy"
                        }
                        package "my-subpackage"
                    }
                """;
        String expectedErrorMessage =
                """
                    Syntax error: expected literal (quoted string)
                    at BuildOption: [...] artifact "foo:bar" -> [...] files -> [...]
                    ~~~~~~~~~~~~~~~~~~~~~~~~~
                    [...]
                        }
                        compatVersion "1.2.3"
                        files {
                            "foo/bar"
                            baz
                    ~~~~~~~~~~~~~~~~~~~~~~~~~
                            ^--- here
                """;
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> parse(code))
                .withMessage(unindent(expectedErrorMessage));
    }
}
