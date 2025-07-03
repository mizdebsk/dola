Dola BuildOption Syntax Reference Manual
========================================

This manual documents the declarative DSL used to define BuildOption
tags for Dola declarative builds.

It includes explanations of each language feature, supported syntax,
grammar fragments in BNF, and many examples.


Overview
--------

A **Declarative Build** is a sequence of instructions, called *build
options*, written in a structured, human-readable DSL.  These describe
how Maven packages are handled, how tests are excluded, what
dependencies are required, and how project metadata is transformed.

Each line in the DSL starts with a **keyword** and may optionally be
followed by a **literal** or a **block** of sub-options.


Grammar Notation
----------------

We use a simplified BNF-like format:

- Non-terminals are in angle brackets: `<NonTerminal>`
- Terminals (keywords or symbols) are in quotes: `"keyword"`
- `ε` means the production can be empty


Top-Level Structure
-------------------

```bnf
<DeclarativeBuild> ::= <DeclarativeBuildPartList>

<DeclarativeBuildPartList> ::= ε
                             | <DeclarativeBuildPart> <DeclarativeBuildPartList>

<DeclarativeBuildPart> ::= <Flag>
                         | <Toolchainptions>
                         | <MavenOptions>
                         | <TestExcludes>
                         | <BuildRequires>
                         | <PackagingOptions>
                         | <TransformOptions>
```

A build is a sequence of zero or more parts.

Examples:

```dsl
skipTests
mavenOption "-DskipTests"
```


Flags
-----

```bnf
<Flag> ::= "skipTests"
         | "singletonPackaging"
         | "usesJavapackagesBootstrap"
```

Each flag is just a standalone keyword that sets a boolean flag to true.

Examples:

```dsl
singletonPackaging
```


Toolchain Options
-----------------

```bnf
<ToolchainOptions> ::= "xmvnToolchain" <Literal>
```

Specifies which XMvn toolchain to use during package build.

Examples:

```dsl
xmvnToolchain "openjdk25"
```


Maven Options
-------------

```bnf
<MavenOptions> ::= "mavenOption" <Literal>
                 | "mavenOptions" "{" <LiteralSequence> "}"
```

Maven options can be defined one-by-one or in a block.

Examples:

```dsl
mavenOption "-DskipTests"
```

```dsl
mavenOptions {
    "-X"
    "-Pfast"
}
```


Test Excludes
-------------

```bnf
<TestExcludes> ::= "testExclude" <Literal>
                 | "testExcludes" "{" <LiteralSequence> "}"
```

Used to exclude specific tests.

Examples:

```dsl
testExclude "BrokenTest"
```

```dsl
testExcludes {
    "BadOne"
    "AnotherBad"
}
```


Build Requirements
------------------

```bnf
<BuildRequires> ::= "buildRequire" <Literal>
                  | "buildRequireFilter" <Literal>
                  | "buildRequires" "{" <BuildRequiresPartSequence> "}"

<BuildRequiresPartSequence> ::= ε
                              | <BuildRequiresPart> <BuildRequiresPartSequence>

<BuildRequiresPart> ::= <Literal>
                      | "filter" <Literal>
```

You can specify build-time dependencies and filters to remove them.

Examples:

```dsl
buildRequire "org.slf4j:slf4j-api"
buildRequireFilter "com.thirdparty:*"
```

```dsl
buildRequires {
    "org.apache:commons-lang3"
    filter "com.unwanted:*"
}
```


Packaging Options
-----------------

```bnf
<PackagingOptions> ::= "artifact" <Literal> "{" <PackagingOptionPartSequence> "}"

<PackagingOptionPartSequence> ::= ε
                                | <PackagingOptionPart> <PackagingOptionPartSequence>

<PackagingOptionPart> ::= "package" <Literal>
                        | "noInstall"
                        | "repository" <Literal>
                        | "file" <Literal>
                        | "files" "{" <LiteralSequence> "}"
                        | "compatVersion" <Literal>
                        | "compatVersions" "{" <LiteralSequence> "}"
                        | "alias" <Literal>
                        | "aliases" "{" <LiteralSequence> "}"
```

Each `artifact` block describes how an artifact is packaged.

Examples:

```dsl
artifact "com.foo:lib" {
    package "subpackage"
    repository "repo"
    files {
        "com/foo/lib"
        "resources"
    }
    compatVersions {
        "1.0"
        "1.1"
    }
    aliases {
        ":lib-alias"
        "org.other:lib-alt"
    }
}
```


Transform Options
-----------------

```bnf
<TransformOptions> ::= "transform" <Literal> "{" <TransformOptionPartSequence> "}"

<TransformOptionPartSequence> ::= ε
                                | <TransformOptionPart> <TransformOptionPartSequence>

<TransformOptionPart> ::= "removeParent"
                        | "removeParent" <Literal>
                        | "removePlugin" <Literal>
                        | "removePlugins" "{" <LiteralSequence> "}"
                        | "removeDependency" <Literal>
                        | "removeDependencies" "{" <LiteralSequence> "}"
                        | "removeSubproject" <Literal>
                        | "removeSubprojects" "{" <LiteralSequence> "}"
                        | "addDependency" <Literal>
                        | "addDependencies" "{" <LiteralSequence> "}"
```

These modify the Maven POMs on the fly during the build.

Examples:

```dsl
transform "com.example:*" {
    removeParent
    removeDependency "com.obsolete:lib"
    addDependencies {
        "org.test:lib:1.0"
        "org.util:tool:2.1"
    }
}
```


Literal Syntax
--------------

```bnf
<Literal> ::= """ <LiteralChars> """
<LiteralChars> ::= ε | <LiteralChar> <LiteralChars>
<LiteralChar> ::= any non-whitespace character except '"'

<LiteralSequence> ::= ε
                    | <Literal> <LiteralSequence>
```

Literals must be quoted. Whitespace or `"` characters are not allowed inside.


Full Example
------------

```dsl
skipTests
mavenOption "-DjavaVersion=11"
testExclude "FailingTest"
buildRequire "org.apache.commons:commons-lang3"
artifact "com.example:my-lib" {
    package "subpackage"
    files {
        "myproject/myartifact"
    }
    aliases {
        ":my-alias"
    }
}
transform "com.example:*" {
    removePlugins {
        ":maven-site-plugin"
    }
    addDependency "org.junit:junit:4.13.2"
}
```


Declarative Spec File Template
------------------------------

```
Name:           ...
Version:        ...
Release:        %autorelease
Summary:        ...
License:        ...
URL:            ...
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source:         ...

BuildSystem:    maven
BuildOption:    ...

%description
...

%files -f .mfiles
%license ...

%changelog
%autochangelog
```

Example:

```
Name:           maven-dependency-tree
Version:        3.2.1
Release:        %autorelease
Summary:        Maven dependency tree artifact
License:        Apache-2.0
URL:            https://maven.apache.org/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/apache/maven/shared/%{name}/%{version}/%{name}-%{version}-source-release.zip

BuildSystem:    maven
BuildOption:    transform ":maven-dependency-tree" {
BuildOption:        removeParent
BuildOption:        removePlugins {
BuildOption:            ":apache-rat-plugin"
BuildOption:            ":maven-invoker-plugin"
BuildOption:        }
BuildOption:    }

%description
Apache Maven dependency tree artifact. Originally part of maven-shared.

%files -f .mfiles
%license LICENSE NOTICE

%changelog
%autochangelog
```
