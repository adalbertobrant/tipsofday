# DEV.to post — draft & publishing notes

This is the **publishing wrapper** for the Hacktoberfest Week 2 submission. The post body
itself lives in one place so it cannot drift:

> **Canonical post body → [`../project_submit.md`](../project_submit.md)**

Copy `project_submit.md` into a new DEV post (or stage it with DevRelay
`create_article`), then apply the metadata and checklist below.

---

## 1. Title options (pick one)

- **tipsofday — a daily crypto briefing written on your own laptop by a local Gemma model**
  *(recommended: leads with the product, then the open-weight angle)*
- I replaced my morning news-tab ritual with a local Gemma model and $0.00 of API spend
- A $7/month side-hustle tool that only works because the model is open-weight

## 2. Tags

Required by the challenge, must be present:

```
devchallenge, hf26challenge
```

Add up to two more from this set (skip anything that does not apply):

```
ai, opensource, python, machinelearning, gemma, ollama, showdev
```

## 3. Front matter (already in `project_submit.md`)

```yaml
---
title: tipsofday — a daily crypto briefing written on your own laptop by a local Gemma model
published: false
tags: devchallenge, hf26challenge, ai, opensource
---
```

## 4. AI disclosure (required by DEV)

The post was written by a human **with meaningful AI/agent assistance** (drafting, the
evaluation write-up, editing). That is `some_ai`. Disclose it either:

- add the tag **`#ABotWroteThis`**, or
- keep this line at the end of the post:

  > *This article was written by me with help from an AI coding agent, and I have checked
  > every number in it against the committed files in the repository.*

Every number in the post is traceable to `eval/RESULTS.md` and the raw JSON in `eval/`;
that is what "checked for factual accuracy" means here.

## 5. Repo URL

The body links to `https://github.com/tipsofday/tipsofday`. **Replace every occurrence with
your real repository URL** before publishing (the README, `pipx install` instructions and the
`{% embed %}` tag all point at it).

The GitHub embed renders the repo card:

```text
{% embed https://github.com/<your-user>/tipsofday %}
```

## 6. Cover image

Suggested: a screenshot of the rendered briefing panel next to `ollama ps` output (proves the
model is local). 1000×420, under 2 MB. Keep the disclaimer footer visible.

## 7. Checklist against the challenge requirements

- [ ] Post uses the **Side Hustle submission template** sections
      (What I Built / Demo / Code / How I Built It / Why Does Open Innovation Matter /
      My Agent Session / My First User / Prize Categories). *(present in `project_submit.md`)*
- [ ] Required tag **`#hf26challenge`** present.
- [ ] Tag **`devchallenge`** present.
- [ ] Opening line identifies it as a submission for
      [Week 2: Side Hustle](https://dev.to/challenges/hacktoberfest-week2-2026-10-12).
- [ ] **Demo** section shows or links a video/GIF (the post currently has a TODO marker —
      fill it before publishing).
- [ ] **Code** section links the public repo **and** the repo is actually public.
- [ ] **Why Does Open Innovation Matter?** answers the prompt's question with real numbers.
- [ ] **Prize Categories** lists every category entered — currently **Best Use of Gemma**
      only (do not claim categories the project does not genuinely use).
- [ ] **My Agent Session** (optional): save the build session with DevRelay and paste the
      embed / link. Remove the `.TODO` comment once done.
- [ ] **My First User** (optional): update if a real user appears before the deadline;
      otherwise the current honest "not yet" wording stays.
- [ ] AI disclosure added (tag `#ABotWroteThis` or the disclosure line).
- [ ] Disclaimer line kept at the end (**not financial advice**).
- [ ] Published before **October 18, 2026, 11:59 PM PDT**.

## 8. Optional: stage it with DevRelay

Instead of pasting manually, the post can be created as a **draft** through the gateway
(`create_article`), which sends `ai_disclosure_level: some_ai` by default. Nothing is
published without an explicit yes. See the `devrelay-publishing` skill for the workflow.

## 9. After publishing

- Reply to your own post with the demo video if it is not embedded yet.
- Save the submission as an agent session and add it to the post (judges like it).
- Keep the repo's `eval/RESULTS.md` updated if you run more real days — the post's claims
  depend on it, and the report is honest about `n = 1`.
