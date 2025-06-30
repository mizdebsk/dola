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
package io.kojan.dola.generator.stub;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatExceptionOfType;

import io.kojan.dola.generator.BuildContext;
import io.kojan.dola.generator.Hook;
import io.kojan.dola.generator.HookFactory;
import org.easymock.EasyMock;
import org.junit.jupiter.api.Test;

class TestHookFactory1 implements HookFactory {
    static Hook hook;

    @Override
    public Hook createHook(BuildContext context) {
        return hook;
    }
}

class TestHookFactory2 implements HookFactory {
    static volatile boolean hookRan;

    @Override
    public Hook createHook(BuildContext context) {
        return () -> {
            hookRan = true;
        };
    }
}

class CompoundHookTest {
    @Test
    void compoundHook() {
        BuildContext bc = EasyMock.createMock(BuildContext.class);
        EasyMock.expect(bc.eval("%{?__dolagen_post_install_hooks}"))
                .andReturn(
                        "\n "
                                + TestHookFactory1.class.getName()
                                + " \n\t   "
                                + TestHookFactory2.class.getName()
                                + " ");
        EasyMock.expect(bc.eval("%{?__dolagen_debug}")).andReturn("").anyTimes();
        EasyMock.expect(bc.eval("%{buildroot}")).andReturn("/build/root").anyTimes();
        Hook hook1 = EasyMock.createStrictMock(Hook.class);
        TestHookFactory1.hook = hook1;
        hook1.run();
        EasyMock.expectLastCall();
        EasyMock.replay(bc, hook1);
        CompoundHook ch = new CompoundHook(bc);
        ch.runHook();
        assertThat(TestHookFactory2.hookRan).isTrue();
        EasyMock.verify(bc, hook1);
    }

    @Test
    void classNotFound() throws Exception {
        BuildContext bc = EasyMock.createMock(BuildContext.class);
        EasyMock.expect(bc.eval("%{?__dolagen_post_install_hooks}")).andReturn("com.foo.Bar");
        EasyMock.expect(bc.eval("%{?__dolagen_debug}")).andReturn("").anyTimes();
        EasyMock.replay(bc);
        assertThatExceptionOfType(RuntimeException.class)
                .isThrownBy(() -> new CompoundHook(bc).runHook())
                .withCauseInstanceOf(ClassNotFoundException.class)
                .withMessageContaining("com.foo.Bar");
        EasyMock.verify(bc);
    }

    @Test
    void classIsNotFactory() throws Exception {
        BuildContext bc = EasyMock.createMock(BuildContext.class);
        EasyMock.expect(bc.eval("%{?__dolagen_post_install_hooks}"))
                .andReturn(CompoundHookTest.class.getName());
        EasyMock.expect(bc.eval("%{?__dolagen_debug}")).andReturn("").anyTimes();
        EasyMock.replay(bc);
        assertThatExceptionOfType(ClassCastException.class)
                .isThrownBy(() -> new CompoundHook(bc).runHook())
                .withMessageContaining("HookFactory");
        EasyMock.verify(bc);
    }

    @Test
    void noFactories() throws Exception {
        BuildContext bc = EasyMock.createMock(BuildContext.class);
        EasyMock.expect(bc.eval("%{?__dolagen_post_install_hooks}")).andReturn("");
        EasyMock.expect(bc.eval("%{?__dolagen_debug}")).andReturn("").anyTimes();
        EasyMock.expect(bc.eval("%{warn:dola-generator: no post-install hooks were specified}"))
                .andReturn("");
        EasyMock.replay(bc);
        new CompoundHook(bc).runHook();
        EasyMock.verify(bc);
    }
}
