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

public class Script {
    private final ScriptType type;
    private final List<String> lines;

    private Script(ScriptType type, List<String> lines) {
        this.type = type;
        this.lines = lines;
    }

    public static Script of(ScriptType type, List<String> lines) {
        return new Script(type, List.copyOf(lines));
    }

    public String getName() {
        return type.getName();
    }

    public ScriptType getType() {
        return type;
    }

    public List<String> getLines() {
        return lines;
    }
}
