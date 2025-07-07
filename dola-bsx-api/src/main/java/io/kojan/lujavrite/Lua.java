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
package io.kojan.lujavrite;

/**
 * The {@code Lua} class provides static native methods that interface directly with the Lua C API.
 * These methods operate on the Lua stack and are designed to be used through the <a
 * href="https://github.com/mizdebsk/lujavrite">LuJavRite</a> bridge.
 *
 * <p><strong>Note:</strong> These methods should only be called from Java code that is running
 * within a Lua execution context (i.e., invoked from Lua via Lujavrite). Calling them from outside
 * such a context results in undefined behavior.
 *
 * <p>For more detailed documentation of Lua C API, see the <a
 * href="https://www.lua.org/manual/5.4/manual.html">Lua Reference Manual</a>.
 *
 * <p>This trivial Java class is maintained as part of Lujavrite project, but it is expected to be
 * source-bundled by projects depending on the Java->Lua calling functionality of LuJavRite. The
 * canonical copy of this class source can be found at <a
 * href="https://github.com/mizdebsk/lujavrite/blob/master/Lua.java">
 * https://github.com/mizdebsk/lujavrite/blob/master/Lua.java</a>.
 *
 * @author Mikolaj Izdebski
 */
public class Lua {

    /**
     * Pushes the global variable with the given name onto the Lua stack.
     *
     * @see <a href="https://www.lua.org/manual/5.4/manual.html#lua_getglobal">lua_getglobal</a>
     *     method documentation in Lua Reference Manual
     * @param name the name of the global variable to retrieve
     * @return the type of the value pushed onto the stack
     */
    public static native int getglobal(String name);

    /**
     * Pushes onto the stack the value of a field from a table at the given index.
     *
     * @see <a href=https://www.lua.org/manual/5.4/manual.html#lua_getfield>lua_getfield</a> method
     *     documentation in Lua Reference Manual
     * @param index the stack index of the table
     * @param name the name of the field to retrieve
     * @return the type of the value pushed onto the stack
     */
    public static native int getfield(int index, String name);

    /**
     * Pushes a Java string onto the Lua stack as a Lua string.
     *
     * @see <a href=https://www.lua.org/manual/5.4/manual.html#lua_pushstring>lua_pushstring</a>
     *     method documentation in Lua Reference Manual
     * @param string the string to push onto the stack
     */
    public static native void pushstring(String string);

    /**
     * Calls a Lua function with the specified number of arguments and expected results.
     *
     * @see <a href=https://www.lua.org/manual/5.4/manual.html#lua_pcall>lua_pcall</a> method
     *     documentation in Lua Reference Manual
     * @param nargs the number of arguments to pass to the function
     * @param nresults the number of expected return values
     * @param msgh the stack index of the error handler function, or 0 for none
     * @return 0 if the call was successful, or an error code otherwise
     */
    public static native int pcall(int nargs, int nresults, int msgh);

    /**
     * Converts the Lua value at the given stack index to a Java string.
     *
     * @see <a href=https://www.lua.org/manual/5.4/manual.html#lua_tostring>lua_tostring</a> method
     *     documentation in Lua Reference Manual
     * @param index the index of the value on the stack
     * @return the string representation of the Lua value
     */
    public static native String tostring(int index);

    /**
     * Removes the top {@code n} elements from the Lua stack.
     *
     * @see <a href=https://www.lua.org/manual/5.4/manual.html#lua_pop>lua_pop</a> method
     *     documentation in Lua Reference Manual
     * @param n the number of elements to pop
     * @return the new top index of the stack
     */
    public static native int pop(int n);

    /**
     * Removes the element at the specified index from the Lua stack, shifting elements above it
     * down.
     *
     * @see <a href=https://www.lua.org/manual/5.4/manual.html#lua_remove>lua_remove</a> method
     *     documentation in Lua Reference Manual
     * @param index the index of the element to remove
     * @return the new top index of the stack
     */
    public static native int remove(int index);
}
