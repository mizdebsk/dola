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
package io.kojan.dola.generator.stub;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.fail;

import io.kojan.dola.generator.BuildContext;
import io.kojan.dola.generator.Collector;
import io.kojan.dola.generator.Generator;
import io.kojan.dola.generator.GeneratorFactory;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.stream.Stream;
import org.easymock.EasyMock;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class TestGeneratorFactory1 implements GeneratorFactory {
    static Generator gen;

    @Override
    public Generator createGenerator(BuildContext context) {
        return gen;
    }
}

class TestGeneratorFactory2 implements GeneratorFactory {
    @Override
    public Generator createGenerator(BuildContext context) {
        return (Collector collector) -> {
            List<Path> filePaths;
            try (Stream<Path> paths =
                    Files.find(
                            Path.of(context.eval("%{buildroot}")),
                            42,
                            (path, attr) -> attr.isRegularFile())) {
                filePaths = paths.toList();
            } catch (IOException e) {
                throw new UncheckedIOException(e);
            }
            for (Path filePath : filePaths) {
                collector.addProvides(filePath, filePath.getFileName().toString());
                collector.addProvides(filePath, "prov2 = 1.2.3");
                collector.addRequires(filePath, "somereq");
                collector.addRequires(filePath, "anotherdep >= 42");
            }
        };
    }
}

abstract class AbstractTestGeneratorFactory implements GeneratorFactory {
    private final String id;

    public AbstractTestGeneratorFactory(String id) {
        this.id = id;
    }

    @Override
    public Generator createGenerator(BuildContext context) {
        return (Collector collector) -> {
            List<Path> filePaths;
            try (Stream<Path> paths =
                    Files.find(
                            Path.of(context.eval("%{buildroot}")),
                            42,
                            (path, attr) -> attr.isRegularFile())) {
                filePaths = paths.toList();
            } catch (IOException e) {
                throw new UncheckedIOException(e);
            }
            for (Path filePath : filePaths) {
                collector.addProvides(filePath, "Prov" + id + "1");
                collector.addProvides(filePath, "Prov" + id + "2");
                collector.addRequires(filePath, "Req" + id + "1");
                collector.addRequires(filePath, "Req" + id + "2");
            }
        };
    }
}

class TGFA extends AbstractTestGeneratorFactory {
    public TGFA() {
        super("A");
    }
}

class TGFB extends AbstractTestGeneratorFactory {
    public TGFB() {
        super("B");
    }
}

class TGFC extends AbstractTestGeneratorFactory {
    public TGFC() {
        super("C");
    }
}

class TestGeneratorFactory3 implements GeneratorFactory {
    @Override
    public Generator createGenerator(BuildContext context) {
        return (Collector collector) -> {
            List<Path> filePaths;
            try (Stream<Path> paths =
                    Files.find(
                            Path.of(context.eval("%{buildroot}")),
                            42,
                            (path, attr) -> attr.isRegularFile())) {
                filePaths = paths.toList();
            } catch (IOException e) {
                throw new UncheckedIOException(e);
            }
            for (Path filePath : filePaths) {
                collector.addProvides(
                        filePath, "prov" + filePath.getFileName().toString().length());
                if (filePath.toString().endsWith("3")) {
                    collector.addRequires(filePath, "req");
                }
            }
        };
    }
}

class CompoundGeneratorTest {
    @TempDir Path br;

    @Test
    void compoundGenerator() throws IOException {
        BuildContext bc = EasyMock.createMock(BuildContext.class);
        String generators =
                "\n"
                        + " "
                        + TestGeneratorFactory1.class.getName()
                        + " \n"
                        + "\t   "
                        + TestGeneratorFactory2.class.getName()
                        + " ";
        EasyMock.expect(bc.eval("%{?__dolagen_provides_generators}")).andReturn(generators);
        EasyMock.expect(bc.eval("%{?__dolagen_requires_generators}")).andReturn(generators);
        EasyMock.expect(bc.eval("%{?__dolagen_debug}")).andReturn("").anyTimes();
        EasyMock.expect(bc.eval("%{?__dolagen_protocol}")).andReturn("").anyTimes();
        EasyMock.expect(bc.eval("%{buildroot}")).andReturn(br.toString()).anyTimes();
        EasyMock.expect(bc.eval("%#")).andReturn("1").times(2);
        EasyMock.expect(bc.eval("%1")).andReturn(br + "/some/file/one").times(2);
        Generator gen1 = EasyMock.createStrictMock(Generator.class);
        TestGeneratorFactory1.gen = gen1;
        gen1.generate(EasyMock.isA(Collector.class));
        EasyMock.expectLastCall();
        EasyMock.replay(bc, gen1);
        Files.createDirectories(br.resolve("some/file"));
        Files.createFile(br.resolve("some/file/one"));
        Files.createFile(br.resolve("some/file/two"));
        CompoundGenerator cg = new CompoundGenerator(bc);
        String prov = cg.runGenerator("provides");
        assertThat(prov).isEqualTo("one\n" + "prov2 = 1.2.3\n" + "");
        String req = cg.runGenerator("requires");
        assertThat(req).isEqualTo("anotherdep >= 42\n" + "somereq\n" + "");
        EasyMock.verify(bc, gen1);
    }

    @Test
    void classNotFound() throws Exception {
        BuildContext bc = EasyMock.createMock(BuildContext.class);
        EasyMock.expect(bc.eval("%{?__dolagen_provides_generators}")).andReturn("com.foo.Bar");
        EasyMock.expect(bc.eval("%{?__dolagen_requires_generators}")).andReturn("com.foo.Bar");
        EasyMock.expect(bc.eval("%{?__dolagen_debug}")).andReturn("").anyTimes();
        EasyMock.expect(bc.eval("%{?__dolagen_protocol}")).andReturn("").anyTimes();
        EasyMock.replay(bc);
        try {
            new CompoundGenerator(bc).runGenerator("provides");
            fail("ClassNotFoundException expected");
        } catch (RuntimeException e) {
            Throwable c = e.getCause();
            assertThat(c).isInstanceOf(ClassNotFoundException.class);
            assertThat(c.getMessage()).isEqualTo("com.foo.Bar");
        }
        EasyMock.verify(bc);
    }

    @Test
    void classIsNotFactory() throws Exception {
        BuildContext bc = EasyMock.createMock(BuildContext.class);
        EasyMock.expect(bc.eval("%{?__dolagen_provides_generators}"))
                .andReturn(CompoundGeneratorTest.class.getName());
        EasyMock.expect(bc.eval("%{?__dolagen_requires_generators}"))
                .andReturn(CompoundGeneratorTest.class.getName());
        EasyMock.expect(bc.eval("%{?__dolagen_debug}")).andReturn("").anyTimes();
        EasyMock.expect(bc.eval("%{?__dolagen_protocol}")).andReturn("").anyTimes();
        EasyMock.replay(bc);
        try {
            new CompoundGenerator(bc).runGenerator("provides");
            fail("ClassCastException expected");
        } catch (ClassCastException e) {
            assertThat(e.getMessage().contains("GeneratorFactory")).isTrue();
        }
        EasyMock.verify(bc);
    }

    @Test
    void noFactories() throws Exception {
        BuildContext bc = EasyMock.createMock(BuildContext.class);
        EasyMock.expect(bc.eval("%{?__dolagen_provides_generators}")).andReturn("");
        EasyMock.expect(bc.eval("%{?__dolagen_requires_generators}")).andReturn("");
        EasyMock.expect(bc.eval("%{?__dolagen_debug}")).andReturn("").anyTimes();
        EasyMock.expect(bc.eval("%{?__dolagen_protocol}")).andReturn("").anyTimes();
        EasyMock.expect(bc.eval("%{buildroot}")).andReturn(br.toString()).anyTimes();
        EasyMock.expect(bc.eval("%#")).andReturn("1");
        EasyMock.expect(bc.eval("%1")).andReturn(br + "/some/file/one");
        EasyMock.expect(bc.eval("%{warn:dola-generator: no generators were specified}"))
                .andReturn("");
        EasyMock.replay(bc);
        Files.createDirectories(br.resolve("some/file"));
        Files.createFile(br.resolve("some/file/one"));
        String prov = new CompoundGenerator(bc).runGenerator("provides");
        assertThat(prov).isEqualTo("");
        EasyMock.verify(bc);
    }

    @Test
    void filtering() throws Exception {
        BuildContext bc = EasyMock.createMock(BuildContext.class);
        EasyMock.expect(bc.eval("%{?__dolagen_provides_generators}"))
                .andReturn(TGFA.class.getName() + " " + TGFC.class.getName());
        EasyMock.expect(bc.eval("%{?__dolagen_requires_generators}"))
                .andReturn(TGFB.class.getName() + " " + TGFC.class.getName());
        EasyMock.expect(bc.eval("%{?__dolagen_debug}")).andReturn("").anyTimes();
        EasyMock.expect(bc.eval("%{?__dolagen_protocol}")).andReturn("").anyTimes();
        EasyMock.expect(bc.eval("%{buildroot}")).andReturn(br.toString()).anyTimes();
        EasyMock.expect(bc.eval("%#")).andReturn("1").times(2);
        EasyMock.expect(bc.eval("%1")).andReturn(br + "/some/file/one").times(2);
        EasyMock.replay(bc);
        Files.createDirectories(br.resolve("some/file"));
        Files.createFile(br.resolve("some/file/one"));
        CompoundGenerator cg = new CompoundGenerator(bc);
        String prov = cg.runGenerator("provides");
        assertThat(prov).isEqualTo("ProvA1\n" + "ProvA2\n" + "ProvC1\n" + "ProvC2\n" + "");
        String req = cg.runGenerator("requires");
        assertThat(req).isEqualTo("ReqB1\n" + "ReqB2\n" + "ReqC1\n" + "ReqC2\n" + "");
        EasyMock.verify(bc);
    }

    @Test
    void multifile() throws Exception {
        BuildContext bc = EasyMock.createMock(BuildContext.class);
        EasyMock.expect(bc.eval("%{?__dolagen_provides_generators}"))
                .andReturn(TestGeneratorFactory3.class.getName());
        EasyMock.expect(bc.eval("%{?__dolagen_requires_generators}"))
                .andReturn(TestGeneratorFactory3.class.getName());
        EasyMock.expect(bc.eval("%{?__dolagen_debug}")).andReturn("").anyTimes();
        EasyMock.expect(bc.eval("%{?__dolagen_protocol}")).andReturn("multifile").anyTimes();
        EasyMock.expect(bc.eval("%{buildroot}")).andReturn("" + br + "").anyTimes();
        EasyMock.expect(bc.eval("%#")).andReturn("5").times(2);
        EasyMock.expect(bc.eval("%1")).andReturn(br + "/f").times(2);
        EasyMock.expect(bc.eval("%2")).andReturn(br + "/f2").times(2);
        EasyMock.expect(bc.eval("%3")).andReturn(br + "/ff3").times(2);
        EasyMock.expect(bc.eval("%4")).andReturn(br + "/file").times(2);
        EasyMock.expect(bc.eval("%5")).andReturn(br + "/file5").times(2);
        EasyMock.replay(bc);
        Files.createDirectories(br);
        Files.createFile(br.resolve("f"));
        Files.createFile(br.resolve("f2"));
        Files.createFile(br.resolve("ff3"));
        Files.createFile(br.resolve("file"));
        Files.createFile(br.resolve("file5"));
        Files.createFile(br.resolve("file66"));
        CompoundGenerator cg = new CompoundGenerator(bc);
        String prov = cg.runGenerator("provides");
        assertThat(prov)
                .isEqualTo(
                        ";"
                                + br
                                + "/f\n"
                                + "prov1\n"
                                + //
                                ";"
                                + br
                                + "/f2\n"
                                + "prov2\n"
                                + //
                                ";"
                                + br
                                + "/ff3\n"
                                + "prov3\n"
                                + //
                                ";"
                                + br
                                + "/file\n"
                                + "prov4\n"
                                + //
                                ";"
                                + br
                                + "/file5\n"
                                + "prov5\n");
        String req = cg.runGenerator("requires");
        assertThat(req).isEqualTo(";" + br + "/ff3\n" + "req\n" + "");
        EasyMock.verify(bc);
    }
}
