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
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.fedoraproject.xmvn.artifact.Artifact;

public class DeclarativeBuildBuilder {

    private String baseName;
    private boolean skipTests;
    private final List<String> mavenOptions = new ArrayList<>();
    private final List<PackagingOption> packagingOptions = new ArrayList<>();
    private final Set<Artifact> extraBuildReqs = new LinkedHashSet<>();
    private final Set<Artifact> filteredBuildReqs = new LinkedHashSet<>();
    private final Map<Artifact, String> buildReqVersions = new LinkedHashMap<>();
    private final List<TransformOption> modelTransformations = new ArrayList<>();
    private final List<String> testExcludes = new ArrayList<>();
    private boolean usesJavapackagesBootstrap;
    private boolean singletonPackaging;
    private String xmvnToolchain;

    public DeclarativeBuildBuilder(String baseName) {
        this.baseName = baseName;
    }

    public DeclarativeBuildBuilder baseName(String baseName) {
        this.baseName = baseName;
        return this;
    }

    public DeclarativeBuildBuilder skipTests(boolean skipTests) {
        this.skipTests = skipTests;
        return this;
    }

    public DeclarativeBuildBuilder mavenOption(String mavenOption) {
        mavenOptions.add(mavenOption);
        return this;
    }

    public DeclarativeBuildBuilder packagingOption(PackagingOption packagingOption) {
        packagingOptions.add(packagingOption);
        return this;
    }

    public DeclarativeBuildBuilder extraBuildReq(Artifact extraBuildReq) {
        extraBuildReqs.add(extraBuildReq);
        return this;
    }

    public DeclarativeBuildBuilder filteredBuildReq(Artifact filteredBuildReq) {
        filteredBuildReqs.add(filteredBuildReq);
        return this;
    }

    public DeclarativeBuildBuilder buildReqVersion(Artifact buildReq, String version) {
        buildReqVersions.put(buildReq, version);
        return this;
    }

    public DeclarativeBuildBuilder modelTransformation(TransformOption modelTransformation) {
        modelTransformations.add(modelTransformation);
        return this;
    }

    public DeclarativeBuildBuilder testExclude(String testExclude) {
        testExcludes.add(testExclude);
        return this;
    }

    public DeclarativeBuildBuilder usesJavapackagesBootstrap(boolean usesJavapackagesBootstrap) {
        this.usesJavapackagesBootstrap = usesJavapackagesBootstrap;
        return this;
    }

    public DeclarativeBuildBuilder singletonPackaging(boolean singletonPackaging) {
        this.singletonPackaging = singletonPackaging;
        return this;
    }

    public DeclarativeBuildBuilder xmvnToolchain(String xmvnToolchain) {
        this.xmvnToolchain = xmvnToolchain;
        return this;
    }

    public DeclarativeBuild build() {
        return new DeclarativeBuild(
                baseName,
                skipTests,
                mavenOptions,
                packagingOptions,
                extraBuildReqs,
                filteredBuildReqs,
                buildReqVersions,
                modelTransformations,
                testExcludes,
                usesJavapackagesBootstrap,
                singletonPackaging,
                xmvnToolchain);
    }
}
