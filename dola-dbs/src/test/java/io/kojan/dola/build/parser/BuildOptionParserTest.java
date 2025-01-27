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

import static org.junit.jupiter.api.Assertions.*;

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
        assertEquals(1, c.getPackagingOptions().size());
        r = c.getPackagingOptions().getFirst();
    }

    @Test
    void testFile() {
        parse("=gid:aid>foo/bar");
        assertEquals("gid", r.getGroupIdGlob());
        assertEquals("aid", r.getArtifactIdGlob());
        assertEquals("", r.getExtensionGlob());
        assertEquals("", r.getClassifierGlob());
        assertEquals("", r.getVersionGlob());
        assertEquals("", r.getTargetPackage());
        assertEquals(0, r.getAliases().size());
        assertEquals(0, r.getCompatVersions().size());
        assertEquals(1, r.getFiles().size());
        assertEquals("foo/bar", r.getFiles().getFirst());
    }

    @Test
    void testPackage() {
        parse("=gid:aid@pkgg1");
        assertEquals("gid", r.getGroupIdGlob());
        assertEquals("aid", r.getArtifactIdGlob());
        assertEquals("", r.getExtensionGlob());
        assertEquals("", r.getClassifierGlob());
        assertEquals("", r.getVersionGlob());
        assertEquals("pkgg1", r.getTargetPackage());
        assertEquals(0, r.getAliases().size());
        assertEquals(0, r.getCompatVersions().size());
        assertEquals(0, r.getFiles().size());
    }

    @Test
    void testAlias() {
        parse("=gid:aid|ag:aa");
        assertEquals("gid", r.getGroupIdGlob());
        assertEquals("aid", r.getArtifactIdGlob());
        assertEquals("", r.getExtensionGlob());
        assertEquals("", r.getClassifierGlob());
        assertEquals("", r.getVersionGlob());
        assertEquals("", r.getTargetPackage());
        assertEquals(1, r.getAliases().size());
        assertEquals("ag", r.getAliases().getFirst().getGroupId());
        assertEquals("aa", r.getAliases().getFirst().getArtifactId());
        assertEquals("", r.getAliases().getFirst().getExtension());
        assertEquals("", r.getAliases().getFirst().getClassifier());
        assertEquals(0, r.getCompatVersions().size());
        assertEquals(0, r.getFiles().size());
    }

    @Test
    void testVersion() {
        parse("=gid:aid;42");
        assertEquals("gid", r.getGroupIdGlob());
        assertEquals("aid", r.getArtifactIdGlob());
        assertEquals("", r.getExtensionGlob());
        assertEquals("", r.getClassifierGlob());
        assertEquals("", r.getVersionGlob());
        assertEquals("", r.getTargetPackage());
        assertEquals(0, r.getAliases().size());
        assertEquals(1, r.getCompatVersions().size());
        assertEquals("42", r.getCompatVersions().getFirst());
        assertEquals(0, r.getFiles().size());
    }

    @Test
    void testCombined() {
        parse("=gid:aid;1.2|:aa>file1>file2@pkg;3.4");
        assertEquals("gid", r.getGroupIdGlob());
        assertEquals("aid", r.getArtifactIdGlob());
        assertEquals("", r.getExtensionGlob());
        assertEquals("", r.getClassifierGlob());
        assertEquals("", r.getVersionGlob());
        assertEquals("pkg", r.getTargetPackage());
        assertEquals(1, r.getAliases().size());
        assertEquals("", r.getAliases().getFirst().getGroupId());
        assertEquals("aa", r.getAliases().getFirst().getArtifactId());
        assertEquals("", r.getAliases().getFirst().getExtension());
        assertEquals("", r.getAliases().getFirst().getClassifier());
        assertEquals(2, r.getCompatVersions().size());
        assertEquals("1.2", r.getCompatVersions().get(0));
        assertEquals("3.4", r.getCompatVersions().get(1));
        assertEquals(2, r.getFiles().size());
        assertEquals("file1", r.getFiles().get(0));
        assertEquals("file2", r.getFiles().get(1));
    }
}
