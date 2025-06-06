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

import io.kojan.dola.generator.Collector;
import java.nio.file.Path;
import java.util.jar.Manifest;

class ManifestGleaner {
    private final Collector collector;
    private final Path filePath;

    public ManifestGleaner(Path filePath, Collector collector) {
        this.filePath = filePath;
        this.collector = collector;
    }

    public void glean(Manifest mf) {
        if (mf != null) {
            String autoName = mf.getMainAttributes().getValue("Automatic-Module-Name");
            if (autoName != null) {
                collector.addProvides(filePath, "jpms(" + autoName + ")");
            }
        }
    }
}
