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
package io.kojan.dola.generator.transformer;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.AssertionsForClassTypes.assertThatExceptionOfType;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.FileOutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.nio.file.attribute.PosixFilePermission;
import java.util.Arrays;
import java.util.jar.Attributes;
import java.util.jar.JarInputStream;
import java.util.jar.Manifest;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class JarTransformerTest {
    @TempDir private Path workDir;

    private Path testResource;
    private Path testJar;
    private Path backupPath;
    private JarTransformer jarTransformer =
            new JarTransformer(mf -> mf.getMainAttributes().putValue("X-Key", "X-Value"));

    @BeforeEach
    void setUp() throws Exception {
        prepare("example.jar");
    }

    private void prepare(String testResourceName) throws Exception {
        testResource = Path.of("src/test/resources").resolve(testResourceName);
        assertThat(Files.isRegularFile(testResource)).isTrue();
        testJar = workDir.resolve("test.jar");
        Files.copy(
                testResource,
                testJar,
                StandardCopyOption.COPY_ATTRIBUTES,
                StandardCopyOption.REPLACE_EXISTING);
        backupPath = Path.of(testJar + "-backup");
    }

    private void performTest() throws Exception {
        jarTransformer.transformJar(testJar);
        try (JarInputStream jis = new JarInputStream(Files.newInputStream(testJar))) {
            Manifest mf = jis.getManifest();
            assertThat(mf).isNotNull();
            Attributes attr = mf.getMainAttributes();
            assertThat(attr).isNotNull();
            assertThat(attr.getValue("X-Key")).isEqualTo("X-Value");
        }
    }

    /**
     * Test JAR if manifest injection works as expected.
     *
     * @throws Exception
     */
    @Test
    void manifestInjection() throws Exception {
        performTest();
    }

    /**
     * Test JAR if manifest injection works when MANIFEST.MF file appears later in the file (for
     * example produced by adding manifest to existing jar with plain zip)
     *
     * @throws Exception
     */
    @Test
    void manifestInjectionLateManifest() throws Exception {
        prepare("late-manifest.jar");
        performTest();
    }

    /**
     * Regression test for a jar which contains an entry that can recompress with a different size,
     * which caused a mismatch in sizes.
     *
     * @throws Exception
     */
    @Test
    void manifestInjectionRecompressionCausesSizeMismatch() throws Exception {
        prepare("recompression-size.jar");
        performTest();
    }

    /**
     * Test JAR if manifest injection works when MANIFEST.MF entry is duplicated
     *
     * @throws Exception
     */
    @Test
    void manifestInjectionDuplicateManifest() throws Exception {
        prepare("duplicate-manifest.jar");
        performTest();
    }

    /**
     * Test JAR if manifest injection preserves sane file perms.
     *
     * @throws Exception
     */
    @Test
    void manifestInjectionSanePermissions() throws Exception {
        assumeTrue(
                Files.getPosixFilePermissions(testJar).contains(PosixFilePermission.OTHERS_READ),
                "sane umask");
        performTest();
        assertThat(Files.getPosixFilePermissions(testJar).contains(PosixFilePermission.OTHERS_READ))
                .isTrue();
    }

    /**
     * Test if any of utility functions throws exception when trying to access invalid JAR file.
     *
     * @throws Exception
     */
    @Test
    void invalidJar() throws Exception {
        prepare("invalid.jar");
        jarTransformer.transformJar(testJar);
        byte[] testJarContent = Files.readAllBytes(testJar);
        byte[] testResourceContent = Files.readAllBytes(testResource);
        assertThat(Arrays.equals(testJarContent, testResourceContent)).isTrue();
    }

    /**
     * Test that the manifest file retains the same i-node after being injected into
     *
     * @throws Exception
     */
    @Test
    void sameINode() throws Exception {
        long oldInode = (Long) Files.getAttribute(testJar, "unix:ino");
        performTest();
        long newInode = (Long) Files.getAttribute(testJar, "unix:ino");
        assertThat(newInode).as("Different manifest I-node after injection").isEqualTo(oldInode);
    }

    /**
     * Test that the backup file created during injectManifest was deleted after a successful
     * operation
     *
     * @throws Exception
     */
    @Test
    void backupDeletion() throws Exception {
        performTest();
        assertThat(Files.exists(backupPath)).isFalse();
    }

    /**
     * Test that the backup file created during injectManifest remains after an unsuccessful
     * operation and its content is identical to the original file
     *
     * @throws Exception
     */
    @Test
    void backupOnFailure() throws Exception {
        byte[] content = Files.readAllBytes(testJar);
        jarTransformer =
                new JarTransformer(
                        mf -> {
                            throw new RuntimeException("boom");
                        });
        Exception ex =
                assertThatExceptionOfType(Exception.class).isThrownBy(this::performTest).actual();
        assertThat(ex.getMessage().contains(backupPath.toString()))
                .as(
                        "An exception thrown when injecting manifest does not mention stored backup file")
                .isTrue();
        assertThat(Files.exists(backupPath)).isTrue();
        byte[] backupContent = Files.readAllBytes(backupPath);
        assertThat(backupContent)
                .as("Content of the backup file is different from the content of the original file")
                .containsExactly(content);
        Files.copy(
                testResource,
                testJar,
                StandardCopyOption.COPY_ATTRIBUTES,
                StandardCopyOption.REPLACE_EXISTING);
        try (FileOutputStream os = new FileOutputStream(testJar.toFile(), true)) {
            /// Append garbage to the original file to check if the content of the backup
            /// will be retained
            os.write(0);
        }
        assertThatExceptionOfType(Exception.class).isThrownBy(this::performTest);
        assertThat(Files.readAllBytes(backupPath))
                .as("Backup file content was overwritten after an unsuccessful injection")
                .containsExactly(backupContent);
        Files.delete(backupPath);
    }

    /**
     * Test that injectManifest fails if the backup file already exists
     *
     * @throws Exception
     */
    @Test
    void failWhenBachupPresent() throws Exception {
        Files.writeString(backupPath, "something");
        assertThatExceptionOfType(Exception.class)
                .as("Expected failure because the the backup file already exists")
                .isThrownBy(this::performTest);
        assertThat(Files.exists(backupPath)).isTrue();
    }
}
