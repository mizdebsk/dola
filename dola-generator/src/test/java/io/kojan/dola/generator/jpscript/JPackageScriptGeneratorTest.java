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
package io.kojan.dola.generator.jpscript;

import io.kojan.dola.generator.BuildContext;
import io.kojan.dola.generator.Collector;
import java.nio.file.Files;
import java.nio.file.Path;
import org.easymock.EasyMock;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class JPackageScriptGeneratorTest {
    private Collector collector;
    private BuildContext context;

    @TempDir private Path br;

    @BeforeEach
    void setUp() {
        collector = EasyMock.createMock(Collector.class);
        context = EasyMock.createMock(BuildContext.class);
        EasyMock.expect(context.eval("%{buildroot}")).andReturn(br.toString()).anyTimes();
    }

    private void expectRequires(String req) {
        collector.addRequires(EasyMock.anyObject(Path.class), EasyMock.eq(req));
        EasyMock.expectLastCall();
    }

    private void performTest(String script) throws Exception {
        Path scriptPath = Path.of("src/test/resources/usr/bin").resolve(script);
        Path binDir = br.resolve("usr/bin");
        Files.createDirectories(binDir);
        Files.copy(scriptPath, binDir.resolve(script));
        EasyMock.replay(collector, context);
        new JPackageScriptGenerator(context).generate(collector);
        EasyMock.verify(collector, context);
    }

    @Test
    void jPackage() throws Exception {
        expectRequires("javapackages-tools");
        expectRequires("java-21-openjdk-headless");
        performTest("jflex");
    }

    @Test
    void nonJPackage() throws Exception {
        performTest("xmvn");
    }

    @Test
    void invalidUtf8() throws Exception {
        performTest("invalid-utf8");
    }
}
