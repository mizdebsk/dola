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
package io.kojan.dola.bsx;

import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Set;
import java.util.TreeSet;
import org.codehaus.plexus.classworlds.ClassWorld;
import org.codehaus.plexus.classworlds.launcher.Configurator;
import org.codehaus.plexus.classworlds.realm.ClassRealm;
import org.codehaus.plexus.classworlds.realm.NoSuchRealmException;

public class BSX {

    private static final boolean debugEnabled = "1".equals(System.getProperty("dola.bsx.debug"));
    private static final ClassWorld classWorld = new ClassWorld();
    private static final ClassLoader systemClassLoader =
            Thread.currentThread().getContextClassLoader();

    private static void debug(Object... msg) {
        if (debugEnabled) {
            System.err.print("BSX: ");
            for (Object s : msg) {
                System.err.print(s.toString());
            }
            System.err.println();
        }
    }

    public static String configureClassWorld(String confDir) throws Throwable {
        Configurator cc = new Configurator(classWorld);
        Set<Path> confPaths = new TreeSet<>();
        try (var dirStream = Files.newDirectoryStream(Path.of(confDir), "*.conf")) {
            dirStream.forEach(confPaths::add);
        }
        for (Path confPath : confPaths) {
            debug("Configuring class world with ", confPath);
            try (var is = Files.newInputStream(confPath)) {
                cc.configure(is);
            }
        }
        if (debugEnabled) {
            for (ClassRealm cr : classWorld.getRealms()) {
                cr.display(System.err);
            }
        }
        // XXX load org.objectweb.asm.ClassVisitor now
        // I don't know why, but loading it later from the same realm results in
        // ClassNotFoundException
        try {
            ClassRealm cr = classWorld.getRealm("Realm:generator");
            Thread.currentThread().setContextClassLoader(cr);
            cr.loadClassFromSelf("org.objectweb.asm.ClassVisitor");
            Thread.currentThread().setContextClassLoader(systemClassLoader);
        } catch (NoSuchRealmException e) {
            // Ignore
        }
        return "";
    }

    public static String call0S(String realmName, String className, String methodName)
            throws Throwable {
        debug("call0S: realm=", realmName, ", className=", className, ", methodName=", methodName);
        ClassRealm classRealm = classWorld.getClassRealm(realmName);
        try {
            Thread.currentThread().setContextClassLoader(classRealm);
            Class<?> cls = classRealm.loadClass(className);
            Method method = cls.getDeclaredMethod(methodName);
            Object ret = method.invoke(null);
            return (String) ret;
        } finally {
            Thread.currentThread().setContextClassLoader(systemClassLoader);
        }
    }

    public static String call1S(
            String realmName, String className, String methodName, String param1) throws Throwable {
        debug(
                "call1S: realm=",
                realmName,
                ", className=",
                className,
                ", methodName=",
                methodName,
                ", param1=",
                param1);
        ClassRealm classRealm = classWorld.getClassRealm(realmName);
        try {
            Thread.currentThread().setContextClassLoader(classRealm);
            Class<?> cls = classRealm.loadClass(className);
            Method method = cls.getDeclaredMethod(methodName, String.class);
            Object ret = method.invoke(null, param1);
            return (String) ret;
        } finally {
            Thread.currentThread().setContextClassLoader(systemClassLoader);
        }
    }
}
