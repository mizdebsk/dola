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

    DeclarativeBuild parse(String s) {
        return new BuildOptionParser("mypkg", s.replace('\n', ' ')).parse();
    }

    DeclarativeBuild parsed(String s) {
        DeclarativeBuild db = parse(s);
        assertThat(db).isNotNull();
        return db;
    }

    @Test
    void empty() {
        parsed("");
    }

    @Test
    void whitespaceOnly() {
        parsed("  ");
    }

    @Test
    void lexicalError() {
        assertThatExceptionOfType(RuntimeException.class)
                .isThrownBy(() -> parse("skipTests%bar"))
                .withMessageContaining("Lexical error");
    }

    @Test
    void capitalKeyword() {
        assertThatExceptionOfType(RuntimeException.class)
                .isThrownBy(() -> parse("SkipTests"))
                .withMessageContaining("Lexical error");
    }

    @Test
    void alphanumericKeyword() {
        assertThatExceptionOfType(RuntimeException.class)
                .isThrownBy(() -> parse("skipTests2"))
                .withMessageContaining("Lexical error");
    }

    @Test
    void keywordTypo() {
        assertThatExceptionOfType(RuntimeException.class)
                .isThrownBy(() -> parse("skipTestsss"))
                .withMessageContaining("unrecognized keyword");
    }

    @Test
    void transformBlockEmpty() {
        String code =
                """
                    transform "foo:bar" {
                    }
                """;
        parsed(code);
    }

    @Test
    void skipTests() {
        String code =
                """
                    skipTests
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.isSkipTests()).isTrue();
    }

    @Test
    void singletonPackaging() {
        String code =
                """
                    singletonPackaging
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.isSingletonPackaging()).isTrue();
    }

    @Test
    void usesJavapackagesBootstrap() {
        String code =
                """
                    usesJavapackagesBootstrap
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.usesJavapackagesBootstrap()).isTrue();
    }

    @Test
    void mavenOption() {
        String code =
                """
                    mavenOption "-Prun-its"
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getMavenOptions()).containsExactly("-Prun-its");
    }

    @Test
    void mavenOptions() {
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
    void buildRequire() {
        String code =
                """
                    buildRequire "foo:bar"
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getExtraBuildReqs()).containsExactlyInAnyOrder(Artifact.of("foo:bar"));
        assertThat(db.getFilteredBuildReqs()).isEmpty();
    }

    @Test
    void buildRequireFilter() {
        String code =
                """
                    buildRequireFilter "foo:bar"
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getExtraBuildReqs()).isEmpty();
        assertThat(db.getFilteredBuildReqs()).containsExactlyInAnyOrder(Artifact.of("foo:bar"));
    }

    @Test
    void buildRequiresOne() {
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
    void buildRequiresTwo() {
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
    void buildRequiresFilter() {
        String code =
                """
                    buildRequires {
                        "foo:bar"
                        filter "*:baz"
                    }
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getExtraBuildReqs()).containsExactlyInAnyOrder(Artifact.of("foo:bar"));
        assertThat(db.getFilteredBuildReqs()).containsExactlyInAnyOrder(Artifact.of("*:baz"));
    }

    @Test
    void testExclude() {
        String code =
                """
                    testExclude "BadTest"
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTestExcludes()).containsExactly("BadTest");
    }

    @Test
    void testExcludesOne() {
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
    void testExcludesThree() {
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
    void artifactEmpty() {
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
    void artifactPackage() {
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
    void artifactNoInstall() {
        String code =
                """
                    artifact "some:thing" {noInstall}
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getPackagingOptions()).hasSize(1);
        assertThat(db.getPackagingOptions().getFirst().getTargetPackage()).isEqualTo("__noinstall");
    }

    @Test
    void artifactRepository() {
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
    void artifactFile() {
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
    void artifactFilesOne() {
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
    void artifactFilesThree() {
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
    void artifactCompatVersion() {
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
    void artifactCompatVersionsOne() {
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
    void artifactCompatVersionsThree() {
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
    void artifactAlias() {
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
    void artifactAliasesOne() {
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
    void artifactAliasesThree() {
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
    void transformEmpty() {
        String code =
                """
                    transform "some:thing" {}
                """;
        DeclarativeBuild db = parsed(code);
        assertThat(db.getTransformOptions()).hasSize(0);
    }

    @Test
    void transformRemoveParentLone() {
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
    void transformRemoveParentArg() {
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
    void transformRemoveDependency() {
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
    void transformRemoveDependenciesOne() {
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
    void transformRemoveDependenciesMultiple() {
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
    void transformRemovePlugin() {
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
    void transformRemovePluginsOne() {
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
    void transformRemovePluginsThree() {
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
    void transformRemoveSubproject() {
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
    void transformRemoveSubprojectsOne() {
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
    void transformRemoveSubprojectsThree() {
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
    void transformAddDependency() {
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
    void transformAddDependenciesOne() {
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
    void transformAddDependenciesThree() {
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
    void artifactBadKeyword() {
        String code =
                """
                    artifact "some:thing" {
                       boom
                    }
                """;
        assertThatExceptionOfType(RuntimeException.class).isThrownBy(() -> parse(code));
    }

    @Test
    void transformBadKeyword() {
        String code =
                """
                    transform "some:thing" {
                        boom
                    }
                """;
        assertThatExceptionOfType(RuntimeException.class).isThrownBy(() -> parse(code));
    }

    @Test
    void globalBadKeyword() {
        String code =
                """
                    boom
                """;
        assertThatExceptionOfType(RuntimeException.class).isThrownBy(() -> parse(code));
    }

    @Test
    void combined() {
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
    void unclosedBraceShouldFail() {
        String code = "artifact \"some:thing\" { package \"foo\"";
        assertThatExceptionOfType(RuntimeException.class)
                .isThrownBy(() -> parse(code))
                .withMessageContaining("Syntax error");
    }

    @Test
    void unclosedStringLiteralShouldFail() {
        String code = "mavenOption \"-X";
        assertThatExceptionOfType(RuntimeException.class)
                .isThrownBy(() -> parse(code))
                .withMessageContaining("Lexical error");
    }

    @Test
    void duplicateKeywordInArtifactShouldFail() {
        String code =
                """
                    artifact "com.foo:bar" {
                        package "sub1"
                        package "sub2"
                    }
                """;
        assertThatExceptionOfType(RuntimeException.class)
                .isThrownBy(() -> parse(code))
                .withMessageContaining("duplicate target package");
    }

    @Test
    void illegalKeywordInBlockShouldFail() {
        String code =
                """
                    artifact "com.foo:bar" {
                        unexpectedKeyword "value"
                    }
                """;
        assertThatExceptionOfType(RuntimeException.class)
                .isThrownBy(() -> parse(code))
                .withMessageContaining("Syntax error");
    }

    @Test
    void artifactWithInvalidAliasFormatShouldFail() {
        String code =
                """
                    artifact "com.foo:bar" {
                        alias "noColon"
                    }
                """;
        assertThatExceptionOfType(RuntimeException.class)
                .isThrownBy(() -> parse(code))
                .withMessageContaining("Syntax error");
    }

    @Test
    void transformWithAllRemovals() {
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
    void emptyBuildRequiresBlock() {
        String code = "buildRequires {}";
        DeclarativeBuild db = parsed(code);
        assertThat(db.getExtraBuildReqs()).isEmpty();
        assertThat(db.getFilteredBuildReqs()).isEmpty();
    }

    @Test
    void emptyAliasesBlock() {
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
    void emptyFilesBlock() {
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
    void whitespaceBetweenKeywordsAndLiterals() {
        String code = "mavenOption    \"-X\"";
        DeclarativeBuild db = parsed(code);
        assertThat(db.getMavenOptions()).containsExactly("-X");
    }
}
