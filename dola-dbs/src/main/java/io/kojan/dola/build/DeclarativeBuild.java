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

import java.util.List;
import java.util.Map;
import java.util.Set;
import org.fedoraproject.xmvn.artifact.Artifact;

public class DeclarativeBuild {

    private final String baseName;
    private final boolean skipTests;
    private final List<String> mavenOptions;
    private final List<PackagingOption> packagingOptions;
    private final Set<Artifact> extraBuildReqs;
    private final Set<Artifact> filteredBuildReqs;
    private final Map<Artifact, String> buildReqVersions;
    private final List<TransformOption> transformOptions;
    private final List<String> testExcludes;
    private final boolean usesJavapackagesBootstrap;
    private final boolean singletonPackaging;
    private final String xmvnToolchain;

    public DeclarativeBuild(
            String baseName,
            boolean skipTests,
            List<String> mavenOptions,
            List<PackagingOption> packagingOptions,
            Set<Artifact> extraBuildReqs,
            Set<Artifact> filteredBuildReqs,
            Map<Artifact, String> buildReqVersions,
            List<TransformOption> transformOptions,
            List<String> testExcludes,
            boolean usesJavapackagesBootstrap,
            boolean singletonPackaging,
            String xmvnToolchain) {
        this.baseName = baseName;
        this.skipTests = skipTests;
        this.mavenOptions = List.copyOf(mavenOptions);
        this.packagingOptions = List.copyOf(packagingOptions);
        this.extraBuildReqs = Set.copyOf(extraBuildReqs);
        this.filteredBuildReqs = Set.copyOf(filteredBuildReqs);
        this.buildReqVersions = Map.copyOf(buildReqVersions);
        this.transformOptions = List.copyOf(transformOptions);
        this.testExcludes = List.copyOf(testExcludes);
        this.usesJavapackagesBootstrap = usesJavapackagesBootstrap;
        this.singletonPackaging = singletonPackaging;
        this.xmvnToolchain = xmvnToolchain;
    }

    public String getBaseName() {
        return baseName;
    }

    public boolean isSkipTests() {
        return skipTests;
    }

    public List<String> getMavenOptions() {
        return mavenOptions;
    }

    public List<PackagingOption> getPackagingOptions() {
        return packagingOptions;
    }

    public Set<Artifact> getExtraBuildReqs() {
        return extraBuildReqs;
    }

    public Set<Artifact> getFilteredBuildReqs() {
        return filteredBuildReqs;
    }

    public Map<Artifact, String> getBuildReqVersions() {
        return buildReqVersions;
    }

    public List<TransformOption> getTransformOptions() {
        return transformOptions;
    }

    public List<String> getTestExcludes() {
        return testExcludes;
    }

    public boolean usesJavapackagesBootstrap() {
        return usesJavapackagesBootstrap;
    }

    public boolean isSingletonPackaging() {
        return singletonPackaging;
    }

    public String getXmvnToolchain() {
        return xmvnToolchain;
    }
}
