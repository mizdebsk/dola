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

import static org.assertj.core.api.Assertions.assertThat;

import io.kojan.dola.generator.Collector;
import java.io.InputStream;
import java.io.StringWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;
import java.util.stream.Collectors;
import javax.tools.JavaCompiler;
import javax.tools.JavaCompiler.CompilationTask;
import javax.tools.JavaFileObject;
import javax.tools.StandardJavaFileManager;
import javax.tools.ToolProvider;
import org.easymock.EasyMock;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class ModuleInfoGleanerTest {
    @TempDir private Path srcDir;

    @TempDir private Path binDir;

    private final Deque<Path> modulePath = new ArrayDeque<>();
    private Collector collector;
    private Path filePath;
    private ModuleInfoGleaner gleaner;

    @BeforeEach
    void setUp() {
        collector = EasyMock.createStrictMock(Collector.class);
        filePath = Path.of("something");
        gleaner = new ModuleInfoGleaner(filePath, collector);
    }

    private ModuleInfoBuilder mod(String name, String version) {
        return new ModuleInfoBuilder(name, version);
    }

    private void expectProvides(String dep) {
        collector.addProvides(filePath, dep);
        EasyMock.expectLastCall();
    }

    private void expectRequires(String dep) {
        collector.addRequires(filePath, dep);
        EasyMock.expectLastCall();
    }

    private void performTest() throws Exception {
        EasyMock.replay(collector);
        try (InputStream is =
                Files.newInputStream(modulePath.getFirst().resolve("module-info.class"))) {
            gleaner.glean(is);
        }
        EasyMock.verify(collector);
    }

    @Test
    void noRequires() throws Exception {
        mod("mymod", "1.2.3").build();
        expectProvides("jpms(mymod) = 1.2.3");
        performTest();
    }

    @Test
    void noVersion() throws Exception {
        mod("mymod", null).build();
        expectProvides("jpms(mymod)");
        performTest();
    }

    @Test
    void requireIntransitive() throws Exception {
        mod("dep", "1").build();
        mod("mymod", "2").req("dep").build();
        expectProvides("jpms(mymod) = 2");
        performTest();
    }

    @Test
    void requireTransitive() throws Exception {
        mod("dep", "1").build();
        mod("mymod", "2").req("transitive dep").build();
        expectProvides("jpms(mymod) = 2");
        expectRequires("jpms(dep)");
        performTest();
    }

    @Test
    void requireStatic() throws Exception {
        mod("dep", "1").build();
        mod("mymod", "2").req("static dep").build();
        expectProvides("jpms(mymod) = 2");
        performTest();
    }

    @Test
    void requireStaticTransitive() throws Exception {
        mod("dep", "1").build();
        mod("mymod", "2").req("static transitive dep").build();
        expectProvides("jpms(mymod) = 2");
        performTest();
    }

    @Test
    void twoRequires() throws Exception {
        mod("a", "1").build();
        mod("b", null).build();
        mod("c", "3").req("transitive a").req("transitive b").build();
        expectProvides("jpms(c) = 3");
        expectRequires("jpms(a)");
        expectRequires("jpms(b)");
        performTest();
    }

    class ModuleInfoBuilder {
        private final String name;
        private final String version;
        private final StringBuilder sb = new StringBuilder();

        public ModuleInfoBuilder(String name, String version) {
            this.name = name;
            this.version = version;
            sb.append("module ").append(name).append(" {").append("\n");
        }

        public ModuleInfoBuilder req(String s) {
            sb.append("requires ").append(s).append(";\n");
            return this;
        }

        public void build() throws Exception {
            Path moduleInfoJava = srcDir.resolve("module-info.java");
            Files.writeString(moduleInfoJava, sb.append("}").append("\n"));
            Path outDir = binDir.resolve(name);
            List<String> opts = new ArrayList<>();
            if (version != null) {
                opts.add("--module-version");
                opts.add(version);
            }
            opts.add("-d");
            opts.add(outDir.toString());
            opts.add("-p");
            opts.add(modulePath.stream().map(Path::toString).collect(Collectors.joining(":")));
            JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
            try (StandardJavaFileManager fileManager =
                    compiler.getStandardFileManager(null, null, null)) {
                Iterable<? extends JavaFileObject> compilationUnits =
                        fileManager.getJavaFileObjectsFromFiles(List.of(moduleInfoJava.toFile()));
                StringWriter compilerOutput = new StringWriter();
                CompilationTask task =
                        compiler.getTask(
                                compilerOutput, fileManager, null, opts, null, compilationUnits);
                assertThat(task.call())
                        .as("module-info compilation failed with output:\n" + compilerOutput)
                        .isTrue();
            }
            modulePath.addFirst(outDir);
        }
    }
}
