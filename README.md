<!-- markdownlint-configure-file {
  "MD013": {
    "code_blocks": false,
    "tables": false
  },
  "MD033": false,
  "MD041": false
} -->

<div align="center">

# MPES BAP

Mestrado Profissional em Engenharia de Software **BAP** Project.

It remembers which directories you use most frequently, so you can "jump" to
them in just a few keystrokes.<br />
zoxide works on all major shells.

[Getting started](#getting-started) •
[Installation](#installation) •
[Configuration](#configuration) •
[Integrations](#third-party-integrations)

</div>

## Getting started

![Tutorial][tutorial]

```sh
z foo              # cd into highest ranked directory matching foo
z foo bar          # cd into highest ranked directory matching foo and bar
z foo /            # cd into a subdirectory starting with foo

z ~/foo            # z also works like a regular cd command
z foo/             # cd into relative path
z ..               # cd one level up
z -                # cd into previous directory

zi foo             # cd with interactive selection (using fzf)

z foo<SPACE><TAB>  # show interactive completions (BAP v0.8.0+, bash 4.4+/fish/zsh only)
```

Read more about the matching algorithm [here][#].

## Installation

### *Step 1: Node*

If you need support [open an issue][issues].

<details>
<summary>Table</summary>

Table example

```sh
curl -sS https://raw.githubusercontent.com/linton | bash
```

Or, you can use a package manager:

| Distribution        | Repository              | Instructions                                                                                   |
| ------------------- | ----------------------- | ---------------------------------------------------------------------------------------------- |
| ***Any***           | **[Rainforest]**         | `Go to rainforest site`                                                                       |
| *Any*               | [Another-Site]           | `conda install -c conda-forge another site`                                                   |
| *Any*               | [Linuxbrew]             | `brew install`                                                                          |

</details>

## Configuration

### Flags

Insert configuration steps here:


### Environment variables

Insert environment variables here.


## Third-party integrations

| Application        | Description                                  | Plugin                     |
| ------------------ | -------------------------------------------- | -------------------------- |
| [link]             | Insert Third-party here                      | [plugin]                   |


[link]: https://github.com/link
[Another-Site]: https://anaconda.org/conda-forge/
[Rainforest]: https://mpesrainforest.com
