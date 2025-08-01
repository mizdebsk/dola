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
package io.kojan.dola.generator.filesystem;

import io.kojan.dola.generator.BuildContext;
import io.kojan.dola.generator.Collector;
import java.nio.file.Files;
import java.nio.file.Path;
import org.easymock.EasyMock;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class FilesystemGeneratorTest {
    private Collector collector;
    private BuildContext context;

    @TempDir private Path br;

    @BeforeEach
    void setUp() {
        collector = EasyMock.createMock(Collector.class);
        context = EasyMock.createMock(BuildContext.class);
        EasyMock.expect(context.eval("%{buildroot}")).andReturn(br.toString()).anyTimes();
    }

    private void expectRequires(Path filePath, String req) {
        collector.addRequires(filePath, req);
        EasyMock.expectLastCall();
    }

    private void performTest(Path path) throws Exception {
        Files.createDirectories(path.getParent());
        Files.createFile(path);
        EasyMock.replay(collector, context);
        new FilesystemGenerator(context).generate(collector);
        EasyMock.verify(collector, context);
    }

    @Test
    void jar() throws Exception {
        Path path = br.resolve("usr/share/java/foo.jar");
        expectRequires(path, "javapackages-filesystem");
        performTest(path);
    }

    @Test
    void javadoc() throws Exception {
        Path path = br.resolve("usr/share/javadoc/foo/index.html");
        expectRequires(path.getParent(), "javapackages-filesystem");
        expectRequires(path, "javapackages-filesystem");
        performTest(path);
    }

    @Test
    void nonJava() throws Exception {
        Path path = br.resolve("usr/bin/foo");
        performTest(path);
    }

    @Test
    void directoryItself() throws Exception {
        Path path = br.resolve("usr/share/java");
        performTest(path);
    }
}
