# Soccer ML addition — approval guide

The existing slip-recap system and website are preserved. The new predictor is isolated under `soccer_ml/`; its dashboard files are under `soccer-ml/`.

## Publish as a reviewable pull request

```bash
./scripts/publish_soccer_ml.sh
```

The script opens GitHub’s official authentication page, securely stores the licensed odds API key, pushes an isolated branch, creates a pull request, and opens that pull request for your approval. It does **not** replace `main` directly.

## Your final links

- Repository: <https://github.com/mashengele78-collab/sfiso>
- Pull requests: <https://github.com/mashengele78-collab/sfiso/pulls>
- Daily predictor: <https://github.com/mashengele78-collab/sfiso/actions/workflows/soccer-ml-daily.yml>
- Tests: <https://github.com/mashengele78-collab/sfiso/actions/workflows/soccer-ml-tests.yml>
- Encrypted secrets: <https://github.com/mashengele78-collab/sfiso/settings/secrets/actions>
- Live dashboard: <https://mashengele78-collab.github.io/sfiso/soccer-ml/>
- Licensed odds key: <https://the-odds-api.com/>

After approving and merging the pull request, open **Daily predictor**, choose **Run workflow**, and wait for the green check. The dashboard will then show the live report.

An 80% model estimate is not a guaranteed winner. Verify all live prices and comply with local law and bookmaker terms.
