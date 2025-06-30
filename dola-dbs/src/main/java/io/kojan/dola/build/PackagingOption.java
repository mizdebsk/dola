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
package io.kojan.dola.build;

import java.util.ArrayList;
import java.util.List;

public class PackagingOption {
    private final String groupIdGlob;
    private final String artifactIdGlob;
    private final String extensionGlob;
    private final String classifierGlob;
    private final String versionGlob;
    private final String targetPackage;
    private final String targetRepository;
    private final List<String> files;
    private final List<String> compatVersions;
    private final List<Alias> aliases;

    private PackagingOption(
            String groupIdGlob,
            String artifactIdGlob,
            String extensionGlob,
            String classifierGlob,
            String versionGlob,
            String targetPackage,
            String targetRepository,
            List<String> files,
            List<String> compatVersions,
            List<Alias> aliases) {
        this.groupIdGlob = groupIdGlob;
        this.artifactIdGlob = artifactIdGlob;
        this.extensionGlob = extensionGlob;
        this.classifierGlob = classifierGlob;
        this.versionGlob = versionGlob;
        this.targetPackage = targetPackage;
        this.targetRepository = targetRepository;
        this.files = List.copyOf(files);
        this.compatVersions = List.copyOf(compatVersions);
        this.aliases = List.copyOf(aliases);
    }

    public static PackagingOption of(String groupIdGlob, String artifactIdGlob) {
        return new PackagingOption(
                groupIdGlob, artifactIdGlob, "", "", "", "", "", List.of(), List.of(), List.of());
    }

    public PackagingOption withTargetPackage(String newTargetPackage) {
        return new PackagingOption(
                groupIdGlob,
                artifactIdGlob,
                extensionGlob,
                classifierGlob,
                versionGlob,
                newTargetPackage,
                targetRepository,
                files,
                compatVersions,
                aliases);
    }

    public PackagingOption withTargetRepository(String newTargetRepository) {
        return new PackagingOption(
                groupIdGlob,
                artifactIdGlob,
                extensionGlob,
                classifierGlob,
                versionGlob,
                targetPackage,
                newTargetRepository,
                files,
                compatVersions,
                aliases);
    }

    public PackagingOption withFile(String file) {
        List<String> newFiles = new ArrayList<>(files);
        newFiles.add(file);
        return new PackagingOption(
                groupIdGlob,
                artifactIdGlob,
                extensionGlob,
                classifierGlob,
                versionGlob,
                targetPackage,
                targetRepository,
                List.copyOf(newFiles),
                compatVersions,
                aliases);
    }

    public PackagingOption withCompatVersion(String compatVersion) {
        List<String> newCompatVersions = new ArrayList<>(compatVersions);
        newCompatVersions.add(compatVersion);
        return new PackagingOption(
                groupIdGlob,
                artifactIdGlob,
                extensionGlob,
                classifierGlob,
                versionGlob,
                targetPackage,
                targetRepository,
                files,
                List.copyOf(newCompatVersions),
                aliases);
    }

    public PackagingOption withAlias(Alias alias) {
        List<Alias> newAliases = new ArrayList<>(aliases);
        newAliases.add(alias);
        return new PackagingOption(
                groupIdGlob,
                artifactIdGlob,
                extensionGlob,
                classifierGlob,
                versionGlob,
                targetPackage,
                targetRepository,
                files,
                compatVersions,
                List.copyOf(newAliases));
    }

    public String getGroupIdGlob() {
        return groupIdGlob;
    }

    public String getArtifactIdGlob() {
        return artifactIdGlob;
    }

    public String getExtensionGlob() {
        return extensionGlob;
    }

    public String getClassifierGlob() {
        return classifierGlob;
    }

    public String getVersionGlob() {
        return versionGlob;
    }

    public String getTargetPackage() {
        return targetPackage;
    }

    public String getTargetRepository() {
        return targetRepository;
    }

    public List<String> getFiles() {
        return files;
    }

    public List<String> getCompatVersions() {
        return compatVersions;
    }

    public List<Alias> getAliases() {
        return aliases;
    }
}
