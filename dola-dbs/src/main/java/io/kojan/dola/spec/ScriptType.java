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

public enum ScriptType {
    PREP_P(1, "prep -p"),
    PREP(2, "prep"),
    PREP_A(3, "prep -a"),
    GENERATE_BUILDREQUIRES_P(4, "generate_buildrequires -p"),
    GENERATE_BUILDREQUIRES(5, "generate_buildrequires"),
    GENERATE_BUILDREQUIRES_A(6, "generate_buildrequires -a"),
    CONF_P(7, "conf -p"),
    CONF(8, "conf"),
    CONF_A(9, "conf -a"),
    BUILD_P(10, "build -p"),
    BUILD(11, "build"),
    BUILD_A(12, "build -a"),
    INSTALL_P(13, "install -p"),
    INSTALL(14, "install"),
    INSTALL_A(15, "install -a");

    private final int prec;
    private final String name;

    ScriptType(int prec, String name) {
        this.prec = prec;
        this.name = name;
    }

    public int getPrecedence() {
        return prec;
    }

    public String getName() {
        return name;
    }
}
