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
package io.kojan.dola.spec.generator;

import static org.assertj.core.api.Assertions.assertThat;

import io.kojan.dola.spec.Spec;
import io.kojan.dola.spec.parser.DSP;
import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class DSGTest {

    @ParameterizedTest
    @ValueSource(
            strings = {
                // "ant",
                // "antlr",
                "aopalliance",
                "apache-commons-beanutils",
                "apache-commons-cli",
                "apache-commons-codec",
                "apache-commons-collections",
                "apache-commons-compress",
                "apache-commons-io",
                "apache-commons-jxpath",
                "apache-commons-lang3",
                "apache-commons-logging",
                "apache-commons-net",
                "apache-commons-parent",
                "apache-parent",
                "apache-resource-bundles",
                "apiguardian",
                // "aqute-bnd",
                "assertj-core",
                "bcel",
                "beust-jcommander",
                "bsf",
                "build-helper-maven-plugin",
                "byte-buddy",
                "cglib",
                "disruptor",
                "dola-gleaner",
                "dola-transformer",
                "easymock",
                "extra-enforcer-rules",
                "felix-parent",
                "felix-utils",
                "fusesource-pom",
                "google-gson",
                "google-guice",
                "guava",
                "hamcrest",
                "httpcomponents-client",
                "httpcomponents-core",
                "httpcomponents-project",
                "jakarta-activation",
                "jakarta-activation1",
                "jakarta-annotations",
                "jakarta-cdi2.0",
                "jakarta-inject",
                "jakarta-inject1.0",
                "jakarta-mail",
                "jakarta-oro",
                "jakarta-servlet",
                "jansi",
                "java-rpm-macros",
                "java_cup",
                "javapackages-bootstrap",
                // "javaparser",
                // "jaxb",
                "jaxb-api",
                "jaxb-dtd-parser",
                "jaxb-fi",
                "jaxb-istack-commons",
                "jaxb-stax-ex",
                "jctools",
                "jdepend",
                "jdom",
                // "jdom2",
                "jflex",
                "jline",
                // "jna",
                "jsch",
                "jsoup",
                "jsr-305",
                "junit",
                "junit5",
                "jurand",
                "jzlib",
                "kojan-parent",
                "kojan-xml",
                // "log4j",
                // "maven",
                "maven-antrun-plugin",
                "maven-archiver",
                "maven-artifact-transfer",
                "maven-assembly-plugin",
                "maven-bundle-plugin",
                "maven-common-artifact-filters",
                "maven-compiler-plugin",
                "maven-dependency-analyzer",
                "maven-dependency-plugin",
                "maven-dependency-tree",
                "maven-enforcer",
                "maven-file-management",
                "maven-filtering",
                "maven-jar-plugin",
                "maven-mapping",
                "maven-parent",
                "maven-plugin-testing",
                "maven-plugin-tools",
                "maven-remote-resources-plugin",
                "maven-resolver",
                "maven-resolver2",
                "maven-resources-plugin",
                "maven-shared-incremental",
                "maven-shared-io",
                "maven-shared-utils",
                "maven-source-plugin",
                "maven-surefire",
                "maven-verifier",
                "maven-wagon",
                // "maven4",
                "mockito",
                "modello",
                "moditect",
                "modulemaker-maven-plugin",
                "mojo-parent",
                "msv",
                "objectweb-asm",
                "objenesis",
                "opentest4j",
                "osgi-annotation",
                "osgi-compendium",
                "osgi-core",
                // "picocli",
                "plexus-archiver",
                "plexus-build-api",
                "plexus-build-api0",
                "plexus-cipher",
                "plexus-classworlds",
                "plexus-compiler",
                "plexus-containers",
                "plexus-interactivity",
                "plexus-interpolation",
                "plexus-io",
                "plexus-languages",
                "plexus-pom",
                "plexus-resources",
                "plexus-sec-dispatcher",
                "plexus-sec-dispatcher4",
                "plexus-testing",
                "plexus-utils",
                "plexus-utils4",
                "plexus-xml",
                "qdox",
                "regexp",
                "relaxng-datatype-java",
                "sisu",
                "slf4j",
                "slf4j2",
                "stax2-api",
                "testng",
                "univocity-parsers",
                "velocity",
                "woodstox-core",
                "xalan-j2",
                "xerces-j2",
                "xml-commons-apis",
                "xml-commons-resolver",
                "xmlunit",
                // "xmvn",
                "xmvn-generator",
                // "xmvn5",
                "xz-java",
            })
    void pkg(String pkg) throws Exception {
        Path p = Path.of("src/test/resources/dsp").resolve(pkg + ".spec");
        String s = Files.readString(p);
        DSP dsp = new DSP(s);
        Spec spec = dsp.parseSpec();
        DSG dsg = new DSG();
        dsg.optSortScripts = true;
        dsg.generate(spec);
        // Files.writeString(Path.of("/tmp/ppp").resolve(pkg + ".spec"), dsg.toString());
        assertThat(dsg.toString()).isEqualTo(s);
    }
}
