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
package io.kojan.dola.spec;

import java.util.List;

public class Pkg {
    private final String name;
    private final BuildSys buildSys;
    private final List<Tag> tags;
    private final List<CondDep> deps;
    private final List<String> description;
    private final List<String> files;
    private final List<String> mfiles;

    private Pkg(
            String name,
            BuildSys buildSys,
            List<Tag> tags,
            List<CondDep> deps,
            List<String> description,
            List<String> files,
            List<String> mfiles) {
        this.name = name;
        this.buildSys = buildSys;
        this.tags = tags;
        this.deps = deps;
        this.description = description;
        this.files = files;
        this.mfiles = mfiles;
    }

    public static Pkg of(String name) {
        return new Pkg(name, null, List.of(), List.of(), List.of(), null, List.of());
    }

    public static Pkg ofPrefixed(String prefix, String name) {
        return Pkg.of(prefix + "-" + name);
    }

    public Pkg withTags(List<Tag> newTags) {
        return new Pkg(name, buildSys, List.copyOf(newTags), deps, description, files, mfiles);
    }

    public Pkg withDeps(List<CondDep> newDeps) {
        return new Pkg(name, buildSys, tags, List.copyOf(newDeps), description, files, mfiles);
    }

    public Pkg withBuildSys(BuildSys newBuildSys) {
        return new Pkg(name, newBuildSys, tags, deps, description, files, mfiles);
    }

    public Pkg withDescription(List<String> newDescription) {
        return new Pkg(name, buildSys, tags, deps, List.copyOf(newDescription), files, mfiles);
    }

    public Pkg withFiles(List<String> newFiles) {
        return new Pkg(name, buildSys, tags, deps, description, List.copyOf(newFiles), mfiles);
    }

    public Pkg withMFiles(List<String> newMfiles) {
        return new Pkg(name, buildSys, tags, deps, description, files, List.copyOf(newMfiles));
    }

    public String getName() {
        return name;
    }

    public BuildSys getBuildSys() {
        return buildSys;
    }

    public List<Tag> getTags() {
        return tags;
    }

    public List<CondDep> getDeps() {
        return deps;
    }

    public List<String> getDescription() {
        return description;
    }

    public List<String> getFiles() {
        return files;
    }

    public List<String> getMfiles() {
        return mfiles;
    }
}
