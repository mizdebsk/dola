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
package io.kojan.dola.rpm;

import io.kojan.lujavrite.Lua;

/**
 * Provides a Java interface for interacting with the RPM system via Lua. It uses the Lujavrite
 * library to bridge between Java and Lua and allows execution of RPM macros.
 */
public class RPM {

    // Load the Lujavrite native shared library necessary to interface with Lua.
    // This library provides native support for the Lua-Java bridge.
    static {
        System.load("/usr/lib64/lua/5.4/lujavrite.so");
    }

    /**
     * Expands an RPM macro expression using the embedded Lua interpreter.
     *
     * <p>This method invokes the {@code rpm.expand} function in Lua, passing the provided
     * expression and returning the result of its evaluation.
     *
     * <p><strong>Important:</strong> This method <em>must</em> be called from Java code that was
     * invoked from Lua via the Lujavrite bridge. Specifically, <strong>the current thread must be
     * the exact thread that was originally called from Lua</strong>. Lujavrite is not thread-safe
     * and depends on thread-local state established by the Lua runtime when it enters the Java
     * layer.
     *
     * <p>Calling this method from a different thread or outside the Lua-to-Java call context will
     * result in <strong>undefined behavior</strong> — including potential JVM crashes, segmentation
     * faults, or silent data corruption.
     *
     * @param expr the RPM macro expression to be expanded (e.g., {@code "%{_bindir}"})
     * @return the result of expanding the given RPM macro expression
     */
    public static String rpmExpand(String expr) {
        Lua.getglobal("rpm"); //       Stack: rpm(-1)
        Lua.getfield(-1, "expand"); // Stack: rpm(-2), expand(-1)
        Lua.pushstring(expr); //       Stack: rpm(-3), expand(-2), expr(-1)
        Lua.pcall(1, 1, 0); //         Stack: rpm(-2), val(-1)
        String val = Lua.tostring(-1);
        Lua.pop(2); //                 Stack: (empty)
        return val;
    }
}
