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
package io.kojan.dola.build.parser;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatExceptionOfType;

import org.junit.jupiter.api.Test;

class LexerTest {

    @Test
    void empty() {
        Lexer lexer = new Lexer("");
        assertThat(lexer.next().isEndOfInput()).isTrue();
    }

    @Test
    void whitespaceOnly() {
        Lexer lexer = new Lexer(" \n");
        assertThat(lexer.next().isEndOfInput()).isTrue();
    }

    @Test
    void keywordToken() {
        Lexer lexer = new Lexer("print");
        assertThat(lexer.next().isKeyword()).isTrue();
        assertThat(lexer.isKeyword("print")).isTrue();
        assertThat(lexer.next().isEndOfInput()).isTrue();
    }

    @Test
    void literalToken() {
        Lexer lexer = new Lexer("\"hello\"");
        assertThat(lexer.next().expectLiteral()).isEqualTo("hello");
        assertThat(lexer.next().isEndOfInput()).isTrue();
    }

    @Test
    void beginToken() {
        Lexer lexer = new Lexer("{");
        lexer.next().expectBlockBegin();
        assertThat(lexer.next().isEndOfInput()).isTrue();
    }

    @Test
    void endToken() {
        Lexer lexer = new Lexer("}");
        assertThat(lexer.next().isBlockEnd()).isTrue();
        assertThat(lexer.next().isEndOfInput()).isTrue();
    }

    @Test
    void multipleTokens() {
        Lexer lexer = new Lexer("print \"value\" { }");
        assertThat(lexer.next().isKeyword("print")).isTrue();
        assertThat(lexer.next().expectLiteral()).isEqualTo("value");
        lexer.next().expectBlockBegin();
        assertThat(lexer.next().isBlockEnd()).isTrue();
        assertThat(lexer.next().isEndOfInput()).isTrue();
    }

    @Test
    void whitespaceNormalization() {
        Lexer lexer = new Lexer("  print\n \"hello\"  ");
        assertThat(lexer.next().isKeyword("print")).isTrue();
        assertThat(lexer.next().expectLiteral()).isEqualTo("hello");
        assertThat(lexer.next().isEndOfInput()).isTrue();
    }

    @Test
    void tabRejection() {
        assertThatExceptionOfType(RuntimeException.class)
                .isThrownBy(() -> new Lexer("  print\n\t\"hello\"  "))
                .withMessageContaining("TAB characters are not allowed");
    }

    @Test
    void unterminatedStringLiteral() {
        Lexer lexer = new Lexer("\"unterminated");
        assertThatExceptionOfType(RuntimeException.class)
                .isThrownBy(lexer::next)
                .withMessageContaining("unterminated string literal");
    }

    @Test
    void illegalCharacter() {
        Lexer lexer = new Lexer("$");
        assertThatExceptionOfType(RuntimeException.class)
                .isThrownBy(lexer::next)
                .withMessageContaining("illegal character");
    }

    @Test
    void expectLiteralFailure() {
        Lexer lexer = new Lexer("print");
        lexer.next();
        assertThatExceptionOfType(RuntimeException.class)
                .isThrownBy(lexer::expectLiteral)
                .withMessageContaining("expected literal");
    }
}
