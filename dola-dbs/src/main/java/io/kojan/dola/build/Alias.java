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

import java.util.Objects;

public class Alias {
    private final String groupId;
    private final String artifactId;
    private final String extension;
    private final String classifier;

    private Alias(String groupId, String artifactId, String extension, String classifier) {
        this.groupId = groupId;
        this.artifactId = artifactId;
        this.extension = extension;
        this.classifier = classifier;
    }

    public static Alias of(String groupId, String artifactId) {
        return new Alias(groupId, artifactId, "", "");
    }

    public String getGroupId() {
        return groupId;
    }

    public String getArtifactId() {
        return artifactId;
    }

    public String getExtension() {
        return extension;
    }

    public String getClassifier() {
        return classifier;
    }

    @Override
    public int hashCode() {
        return Objects.hash(artifactId, classifier, extension, groupId);
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null) return false;
        if (getClass() != obj.getClass()) return false;
        Alias other = (Alias) obj;
        return Objects.equals(artifactId, other.artifactId)
                && Objects.equals(classifier, other.classifier)
                && Objects.equals(extension, other.extension)
                && Objects.equals(groupId, other.groupId);
    }
}
