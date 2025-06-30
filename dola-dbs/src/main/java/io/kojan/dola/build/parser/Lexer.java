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

class Lexer {
    final String str;
    final int eoi;
    int lexBeg;
    int lexEnd;
    int pos;

    public Lexer(String str) {
        this.str = str + '$';
        eoi = str.length();
        // Reject TABs upfront so that we don't need to care about them in the parser code
        if (str.indexOf('\t') >= 0) {
            pos = str.indexOf('\t');
            error("Lexical error: TAB characters are not allowed, replace them with spaces");
        }
        lookahead();
    }

    public Error error(String msg) {
        // Count lines
        int lineStart = 0;
        int lineNumber = 1;
        for (int i = 0; i < lexBeg; i++) {
            if (str.charAt(i) == '\n') {
                lineStart = i + 1;
                lineNumber++;
            }
        }
        int lineEnd = eoi;
        for (int i = lexBeg; i < eoi; i++) {
            if (str.charAt(i) == '\n') {
                lineEnd = i;
                break;
            }
        }
        String line = str.substring(lineStart, lineEnd);
        String banner = "~".repeat(Math.max(10, lineEnd - lineStart));
        StringBuilder sb = new StringBuilder();
        sb.append(msg);
        sb.append("\nat line ")
                .append(lineNumber)
                .append(":\n")
                .append(banner)
                .append("\n")
                .append(line)
                .append("\n")
                .append(banner)
                .append("\n");
        if (lexBeg - lineStart >= 10) {
            sb.append("  here ");
            sb.append("-".repeat(lexBeg - lineStart - 7));
            sb.append("^");
        } else {
            sb.append(" ".repeat(lexBeg - lineStart));
            sb.append("^--- here");
        }
        throw new RuntimeException(sb.toString());
    }

    private void lookahead() {
        int ch;
        while ((ch = str.charAt(pos)) == ' ' || ch == '\n') {
            pos++;
        }
    }

    public Lexer next() {
        lexBeg = pos;
        if (pos == eoi) {
            lexEnd = pos;
            return this;
        }
        int ch = str.charAt(pos++);
        if (ch == '"') {
            while (str.charAt(pos++) != '"') {
                if (pos > eoi) {
                    error("Lexical error: unterminated string literal");
                }
            }
        } else if (ch >= 'a' && ch <= 'z') {
            while (((ch = str.charAt(pos)) >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z')) {
                pos++;
            }
        } else if (ch != '{' && ch != '}') {
            error("Lexical error: illegal character");
        }
        lexEnd = pos;
        lookahead();
        return this;
    }

    public boolean isKeyword() {
        int ch = str.charAt(lexBeg);
        return ch >= 'a' && ch <= 'z';
    }

    public boolean isKeyword(String kw) {
        return kw.length() == lexEnd - lexBeg && str.regionMatches(lexBeg, kw, 0, lexEnd - lexBeg);
    }

    public String expectLiteral() {
        if (str.charAt(lexBeg) != '"') {
            error("Syntax error: expected literal (quoted string)");
        }
        return str.substring(lexBeg + 1, lexEnd - 1);
    }

    public void expectBlockBegin() {
        if (str.charAt(lexBeg) != '{') {
            error("Syntax error: expected opening brace '{'");
        }
    }

    public boolean isBlockEnd() {
        return str.charAt(lexBeg) == '}';
    }

    public boolean isEndOfInput() {
        return lexBeg == eoi;
    }

    public boolean lookaheadIsLiteral() {
        return str.charAt(pos) == '"';
    }
}
