/*-
 * Copyright (c) 2023-2024 Red Hat, Inc.
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
package io.kojan.dola.generator.jpms;

import io.kojan.dola.generator.Collector;
import java.nio.file.Path;
import java.util.jar.Manifest;
import org.easymock.EasyMock;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class ManifestGleanerTest {
    private Collector collector;
    private Manifest manifest;
    private Path filePath;
    private ManifestGleaner gleaner;

    @BeforeEach
    void setUp() {
        collector = EasyMock.createStrictMock(Collector.class);
        manifest = new Manifest();
        filePath = Path.of("something");
        gleaner = new ManifestGleaner(filePath, collector);
    }

    private void updateManifest(String key, String value) {
        manifest.getMainAttributes().putValue(key, value);
    }

    private void expectProvides(String prov) {
        collector.addProvides(filePath, prov);
        EasyMock.expectLastCall();
    }

    private void performTest() {
        EasyMock.replay(collector);
        gleaner.glean(manifest);
        EasyMock.verify(collector);
    }

    @Test
    void emptyManifest() {
        performTest();
    }

    @Test
    void nullManifest() {
        manifest = null;
        performTest();
    }

    @Test
    void simple() {
        updateManifest("Automatic-Module-Name", "foo.bar");
        expectProvides("jpms(foo.bar)");
        performTest();
    }
}
