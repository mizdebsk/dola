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

public class TransformOption {

    private final String opcode;
    private final String argument;
    private final String selector;

    public static TransformOption ofRemoveParent(String selector) {
        return new TransformOption("removeParent", ":", selector);
    }

    public static TransformOption ofRemoveParent(String matcher, String selector) {
        return new TransformOption("removeParent", matcher, selector);
    }

    public static TransformOption ofRemovePlugin(String matcher, String selector) {
        return new TransformOption("removePlugin", matcher, selector);
    }

    public static TransformOption ofRemoveDependency(String matcher, String selector) {
        return new TransformOption("removeDependency", matcher, selector);
    }

    public static TransformOption ofRemoveSubproject(String matcher, String selector) {
        return new TransformOption("removeSubproject", matcher, selector);
    }

    public static TransformOption ofAddDependency(String matcher, String selector) {
        return new TransformOption("addDependency", matcher, selector);
    }

    private TransformOption(String opcode, String argument, String selector) {
        this.opcode = opcode;
        this.argument = argument;
        this.selector = selector;
    }

    public String getOpcode() {
        return opcode;
    }

    public String getArgument() {
        return argument;
    }

    public String getSelector() {
        return selector;
    }
}
