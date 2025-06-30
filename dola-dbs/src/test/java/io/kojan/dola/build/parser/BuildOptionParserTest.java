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

import io.kojan.dola.build.DeclarativeBuild;
import io.kojan.dola.build.DeclarativeBuildBuilder;
import io.kojan.dola.build.PackagingOption;
import org.junit.jupiter.api.Test;

class BuildOptionParserTest {

    private DeclarativeBuild c;
    private PackagingOption r;

    private void parse(String s) {
        DeclarativeBuildBuilder cb = new DeclarativeBuildBuilder("mypkg");
        BuildOptionParser p = new BuildOptionParser(s, cb);
        p.parse();
        c = cb.build();
        assertThat(c.getPackagingOptions().size()).isEqualTo(1);
        r = c.getPackagingOptions().getFirst();
    }

    @Test
    void file() {
        parse("=gid:aid>foo/bar");
        assertThat(r.getGroupIdGlob()).isEqualTo("gid");
        assertThat(r.getArtifactIdGlob()).isEqualTo("aid");
        assertThat(r.getExtensionGlob()).isEqualTo("");
        assertThat(r.getClassifierGlob()).isEqualTo("");
        assertThat(r.getVersionGlob()).isEqualTo("");
        assertThat(r.getTargetPackage()).isEqualTo("");
        assertThat(r.getAliases().size()).isEqualTo(0);
        assertThat(r.getCompatVersions().size()).isEqualTo(0);
        assertThat(r.getFiles().size()).isEqualTo(1);
        assertThat(r.getFiles().getFirst()).isEqualTo("foo/bar");
    }

    @Test
    void testPackage() {
        parse("=gid:aid@pkgg1");
        assertThat(r.getGroupIdGlob()).isEqualTo("gid");
        assertThat(r.getArtifactIdGlob()).isEqualTo("aid");
        assertThat(r.getExtensionGlob()).isEqualTo("");
        assertThat(r.getClassifierGlob()).isEqualTo("");
        assertThat(r.getVersionGlob()).isEqualTo("");
        assertThat(r.getTargetPackage()).isEqualTo("pkgg1");
        assertThat(r.getAliases().size()).isEqualTo(0);
        assertThat(r.getCompatVersions().size()).isEqualTo(0);
        assertThat(r.getFiles().size()).isEqualTo(0);
    }

    @Test
    void alias() {
        parse("=gid:aid|ag:aa");
        assertThat(r.getGroupIdGlob()).isEqualTo("gid");
        assertThat(r.getArtifactIdGlob()).isEqualTo("aid");
        assertThat(r.getExtensionGlob()).isEqualTo("");
        assertThat(r.getClassifierGlob()).isEqualTo("");
        assertThat(r.getVersionGlob()).isEqualTo("");
        assertThat(r.getTargetPackage()).isEqualTo("");
        assertThat(r.getAliases().size()).isEqualTo(1);
        assertThat(r.getAliases().getFirst().getGroupId()).isEqualTo("ag");
        assertThat(r.getAliases().getFirst().getArtifactId()).isEqualTo("aa");
        assertThat(r.getAliases().getFirst().getExtension()).isEqualTo("");
        assertThat(r.getAliases().getFirst().getClassifier()).isEqualTo("");
        assertThat(r.getCompatVersions().size()).isEqualTo(0);
        assertThat(r.getFiles().size()).isEqualTo(0);
    }

    @Test
    void version() {
        parse("=gid:aid;42");
        assertThat(r.getGroupIdGlob()).isEqualTo("gid");
        assertThat(r.getArtifactIdGlob()).isEqualTo("aid");
        assertThat(r.getExtensionGlob()).isEqualTo("");
        assertThat(r.getClassifierGlob()).isEqualTo("");
        assertThat(r.getVersionGlob()).isEqualTo("");
        assertThat(r.getTargetPackage()).isEqualTo("");
        assertThat(r.getAliases().size()).isEqualTo(0);
        assertThat(r.getCompatVersions().size()).isEqualTo(1);
        assertThat(r.getCompatVersions().getFirst()).isEqualTo("42");
        assertThat(r.getFiles().size()).isEqualTo(0);
    }

    @Test
    void combined() {
        parse("=gid:aid;1.2|:aa>file1>file2@pkg;3.4");
        assertThat(r.getGroupIdGlob()).isEqualTo("gid");
        assertThat(r.getArtifactIdGlob()).isEqualTo("aid");
        assertThat(r.getExtensionGlob()).isEqualTo("");
        assertThat(r.getClassifierGlob()).isEqualTo("");
        assertThat(r.getVersionGlob()).isEqualTo("");
        assertThat(r.getTargetPackage()).isEqualTo("pkg");
        assertThat(r.getAliases().size()).isEqualTo(1);
        assertThat(r.getAliases().getFirst().getGroupId()).isEqualTo("");
        assertThat(r.getAliases().getFirst().getArtifactId()).isEqualTo("aa");
        assertThat(r.getAliases().getFirst().getExtension()).isEqualTo("");
        assertThat(r.getAliases().getFirst().getClassifier()).isEqualTo("");
        assertThat(r.getCompatVersions().size()).isEqualTo(2);
        assertThat(r.getCompatVersions().get(0)).isEqualTo("1.2");
        assertThat(r.getCompatVersions().get(1)).isEqualTo("3.4");
        assertThat(r.getFiles().size()).isEqualTo(2);
        assertThat(r.getFiles().get(0)).isEqualTo("file1");
        assertThat(r.getFiles().get(1)).isEqualTo("file2");
    }
}
