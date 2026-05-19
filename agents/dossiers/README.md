# Dossiers

Each file in this directory is a *system prompt* for one actor. It is
synthesised from the corresponding `data/actors/<actor>.md` profile plus
the `_template.md` skeleton.

The runner instantiates one Claude session per actor with that actor's
dossier as system prompt. Each session is independent — no shared memory —
which keeps actors honestly partial-information.

When `data/actors/<actor>.md` changes, regenerate the dossier with:

```bash
python -m agents.runner --regenerate-dossiers
```

The 12 dossier files mirror the 12 actor files. Heuristic mode does not
need them; API mode does.
