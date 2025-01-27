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
package io.kojan.dola.spec;

import java.util.List;

public class BuildSys extends AbstractCommentable {
    private final List<BuildOpt> buildOpts;

    private BuildSys(List<BuildOpt> buildOpts, List<String> comment) {
        super(comment);
        this.buildOpts = buildOpts;
    }

    public static BuildSys of(List<BuildOpt> buildOpts, List<String> comment) {
        return new BuildSys(List.copyOf(buildOpts), List.copyOf(comment));
    }

    public List<BuildOpt> getBuildOpts() {
        return buildOpts;
    }
}
