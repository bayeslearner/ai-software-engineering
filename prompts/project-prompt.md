---
title: "AI-Powered Software Engineering — Project-Specific Prompt"
subtitle: "Layers on top of the lecture-notes skill"
---

# Project-specific rules

## Source material

Primary sources:
- `ralph1-4.pptx` — Four iterations of Geoffrey Huntley's "Ralph, Gas Town, and the New Software Engineering" presentation
- `claude.pptx` — Claude Code advanced tutorial (agentic runtime, sessions, memory, extensions)
- Author's own experience building and using autonomous coding agents

## Audience

Software engineers (mid to senior) who use LLMs for coding but haven't built or understood autonomous coding loops. They've used ChatGPT/Claude interactively but don't understand context engineering, harness design, or multi-agent orchestration. They need to shift from "using AI tools" to "engineering AI systems."

## Voice and depth

- Opinionated and direct — this is a practitioner's guide, not a survey
- Use concrete examples: show actual prompts, actual harness code, actual failure modes
- When Huntley makes a claim (e.g., "coding is being commoditized"), present the evidence AND the counterargument, then take a position
- Code examples in Python using Claude Code / Claude API where applicable
- Reference the companion "Agentic Design Patterns" book for deeper pattern coverage

## Quarto conventions

- YAML front matter: `subtitle` = topic, `author` = "AI-Powered SE Tutorial", `date: today`
- Section anchors: `{#sec-topic-subtopic}` format
- Cross-references inline between chapters
