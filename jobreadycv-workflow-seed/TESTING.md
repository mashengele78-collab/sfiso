# Testing the JobReadyCV workflow repository

## 1. View the synthetic workflow play

Open [`examples/index.html`](examples/index.html) in a browser and select **Run the full workflow**.

The play uses fictional data and demonstrates:

1. intake and authority gate;
2. source-fact clarification;
3. truthful vacancy matching;
4. a one-column draft;
5. human QA and export checks;
6. the manual delivery gate.

It is a static demonstration. It does not generate DOCX/PDF files, send messages, score a CV, or store data.

## 2. Run the repository check

Requires Python 3 and no third-party packages:

```sh
python3 scripts/repo_check.py
```

A successful run prints the number of files checked.

## 3. Prove that a prohibited file is rejected

Test in a disposable copy so the prohibited filename never enters real Git history:

```sh
tmp="$(mktemp -d)"
cp -R . "$tmp/repo"
printf 'harmless negative test\n' > "$tmp/repo/test.pdf"
python3 "$tmp/repo/scripts/repo_check.py"
rm -rf "$tmp"
```

The check must fail with `prohibited customer/binary file type: test.pdf`.

## 4. Run the GitHub check

The **Repository hygiene** workflow runs on every push and pull request and can also be started manually from the Actions tab. It has read-only repository permissions.

## 5. Test optional Human Review

Use only a fictional temporary Markdown or HTML file. Requires Node.js 20 or newer:

```sh
node --version
npx -y human-review@0.6.1 /path/to/fictional-test-cv.md
```

Test a direct text edit, a deletion and an anchored comment. Keep the server on loopback, close it afterward, and remove the temporary file. Human Review is a feedback interface; a person still approves the final document.
