# Tag: does this reuse row or divergence note belong to the issue "the ground of obligation"?

The collection traces how questions travel from text to text. The pilot issue is **the ground of obligation**: what obligation is and what makes it binding. Grotius, Pufendorf, Leibniz (*Jugement d'un anonyme*), Barbeyrac (notes and *Réflexions*), Wolff, Burlamaqui and Vattel (the *Essai sur le fondement du droit naturel*, 1747, and *Le droit des gens*, 1758/1773) answer it differently.

## Input (JSON, path given)

A list of items. Each is either a reuse row (`kind` "row": `passage` of the edition, `source_passage` of the source, `label` such as translation, close paraphrase, shared argument, citation, open disagreement) or a divergence note (`kind` "note": the source answers the same question differently; `question`, `comment`, `label` diverges or partly). `edition` is the later text (`vattel-essai-1747`, `burlamaqui-1747`, `vattel-1773`), `source` and `locus` the earlier one. `french` is a working French rendering of a Latin source passage.

## Sub-issues

Tag an item with the one sub-issue its two passages share:

- `definition`: what obligation is (a moral quality, a moral necessity, active and passive obligation, the connection of a motive with an action).
- `superior`: whether obligation needs the will or command of a superior, and what gives a superior that right.
- `utility`: whether our own good, utility or happiness grounds obligation; the motive of obligation against its ground.
- `reason`: whether reason, the nature of things or the fitness of actions obliges by itself.
- `god`: obligation without God or before his command; whether an atheist is obliged.
- `self`: whether one can oblige oneself, and whether an obligation known by reason can cease at will.
- `law`: what a law is, and in what sense natural law is a law.
- `sanction`: rewards and punishments as motives or as the sanction of natural law.

An item belongs to the issue only if both passages speak to one of these sub-issues. A row that shares wording on another topic (the definition of natural law as a science, sociability as such, a duty to others, the law of nations, the state of nature) is off the issue. Be strict: a passage that mentions "obligation" in passing is off.

## Output

Write with python3 a JSON file (path given): `{"items":[{"key","on_issue":true|false,"sub":"<sub-issue or empty>","why":"one short sentence"}]}`, one entry per input item, in order. Reply with one line: items read, on the issue by sub-issue.
