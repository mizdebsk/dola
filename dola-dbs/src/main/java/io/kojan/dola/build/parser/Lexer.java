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

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.stream.Collectors;

class Lexer {
    final String str;
    final int eoi;
    int lexBeg;
    int lexEnd;
    int pos;

    private int indentLevel;
    private boolean whiteSpaceBefore;
    private boolean newLineBefore;
    private final StringBuilder buffer = new StringBuilder();
    private String currentToken;
    private Deque<String> path = new ArrayDeque<>();
    private Deque<Integer> pathForks = new ArrayDeque<>();

    public Lexer(String str) throws BuildOptionParseException {
        this.str = str + '$';
        eoi = str.length();
        // Reject TABs upfront so that we don't need to care about them in the parser code
        if (str.indexOf('\t') >= 0) {
            pos = str.indexOf('\t');
            throw new BuildOptionParseException(
                    "Lexical error: TAB characters are not allowed, replace them with spaces");
        }
        lookahead();
    }

    // number of context lines to show in code snippets
    final int nLinesInContext = 5;

    public BuildOptionParseException error(String msg) throws BuildOptionParseException {

        token();
        String canonStr = buffer.toString();

        int[] lineStart = new int[nLinesInContext];
        int lineNum = 0;
        int curLineBeg = 0;
        for (int i = 0; i < canonStr.length(); i++) {
            if (canonStr.charAt(i) == '\n') {
                curLineBeg = i + 1;
                lineStart[lineNum] = i + 1;
                lineNum = (lineNum + 1) % nLinesInContext;
            }
        }

        int snipMaxLen = lineStart[0] - lineStart[nLinesInContext - 1];
        for (int i = 1; i < nLinesInContext; i++) {
            snipMaxLen = Math.max(snipMaxLen, lineStart[i] - lineStart[i - 1]);
        }
        int snipBeg = lineStart[lineNum];
        int errLoc = canonStr.length() - (lexEnd - lexBeg) - curLineBeg;

        String banner = "~".repeat(Math.min(72, Math.max(10, snipMaxLen - 1)));
        StringBuilder sb = new StringBuilder();
        sb.append(msg)
                .append("\n")
                .append("at BuildOption:")
                .append(path.stream().map(x -> " " + x).collect(Collectors.joining()))
                .append("\n")
                .append(banner)
                .append("\n")
                .append(snipBeg > 0 ? "[...]\n" : "")
                .append(canonStr.substring(snipBeg))
                .append("\n")
                .append(banner)
                .append("\n");
        if (errLoc >= 10) {
            sb.append("  here ");
            sb.append("-".repeat(errLoc - 7));
            sb.append("^");
        } else {
            sb.append(" ".repeat(errLoc));
            sb.append("^--- here");
        }
        throw new BuildOptionParseException(sb.toString());
    }

    private void lookahead() {
        int ch;
        while ((ch = str.charAt(pos)) == ' ' || ch == '\n') {
            pos++;
        }
    }

    private void token() {
        if (currentToken != null) {
            boolean newLineAfter;
            if (currentToken.equals("{")) {
                indentLevel++;
                newLineAfter = true;
            } else if (currentToken.equals("}")) {
                indentLevel--;
                newLineBefore = true;
                newLineAfter = true;
            } else {
                newLineAfter = false;
            }
            if (whiteSpaceBefore) {
                if (newLineBefore) {
                    buffer.append('\n').append("    ".repeat(Math.max(indentLevel, 0)));
                } else {
                    buffer.append(' ');
                }
            }
            buffer.append(currentToken);
            newLineBefore = newLineAfter;
            whiteSpaceBefore = true;
        }
    }

    private void pathAppend(String tok) {
        path.addLast(tok);
    }

    public Lexer next() throws BuildOptionParseException {
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
        token();
        currentToken = str.substring(lexBeg, lexEnd);
        lookahead();
        return this;
    }

    public boolean isKeyword(String kw) {
        boolean isKw =
                kw.length() == lexEnd - lexBeg && str.regionMatches(lexBeg, kw, 0, lexEnd - lexBeg);
        if (isKw) {
            pathAppend(currentToken);
        }
        return isKw;
    }

    public String expectLiteral() throws BuildOptionParseException {
        if (str.charAt(lexBeg) != '"') {
            error("Syntax error: expected literal (quoted string)");
        }
        pathAppend(currentToken);
        return str.substring(lexBeg + 1, lexEnd - 1);
    }

    private void markPathFork() {
        pathForks.addLast(path.size());
    }

    public void expectBlockBegin() throws BuildOptionParseException {
        if (str.charAt(lexBeg) != '{') {
            error("Syntax error: expected opening brace '{'");
        }
        pathAppend("->");
        markPathFork();
    }

    private boolean pathUnwind(boolean reset) {
        int mark = pathForks.size() > 0 ? pathForks.removeLast() : 0;
        boolean dots = false;
        while (path.size() > mark) {
            path.removeLast();
            dots = true;
        }
        if (dots && (path.isEmpty() || !path.peekLast().equals("[...]"))) {
            path.addLast("[...]");
        }
        if (!reset) {
            markPathFork();
        }
        return reset;
    }

    public boolean isBlockEnd() {
        newLineBefore = true;
        return pathUnwind(str.charAt(lexBeg) == '}');
    }

    public boolean isEndOfInput() {
        newLineBefore = true;
        return pathUnwind(lexBeg == eoi);
    }

    public boolean lookaheadIsLiteral() {
        return str.charAt(pos) == '"';
    }

    public String asString() {
        return buffer.toString();
    }
}
