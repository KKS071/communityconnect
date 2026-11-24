# Contribution statement: Milestone 2

Name / UCID: Sandeep Garg / sg2938

## Personal authorship
I primarily coordinated AI-agent prompts, ran mutation-testing comparisons, and maintained Git documentation and traceability for CommunityConnect Milestone 2. I organized baseline and post-regression mutation runs, reviewed some patches, and helped record test evidence and commit references. Relevant artifacts include `LEDGER.md`, `docs/audits/mutation-summary.md`, `evidence/mutation-baseline.txt`, `evidence/mutation-properties.txt`, and `evidence/mutation-after.txt`. The recorded workflow appears in `LEDGER.md` Entries 69–75.

## AI-assisted authorship
I used Claude Code agents to assist with mutation-testing planning, configuration, survivor analysis, regression-test proposals, and evidence documentation. Specific examples include `prompts/83-Milestone-2-Mutation-Testing-Plan.md`, `prompts/84-Milestone-2-Mutation-Configuration.md`, `prompts/85-Milestone-2-Controlled-Mutation-Comparison.md`, `prompts/87-AGENT-21-Prepare-Three-Mutation-Killing-Regression-Tests.md`, and `prompts/88-AGENT-22-M2-Mutation-Evidence-Ledger-Final-Audit.md`. See `LEDGER.md` Entries 69–75. The two baselines each killed 25/30 selected mutants; after three deterministic regression tests, 28/30 were killed. These results do not describe all 603 generated mutants.

## Review
I reviewed some AI-generated patches and documentation against the S-6 design, locked acceptance tests, and mutation evidence. In particular, the survivor analysis distinguished three test gaps from an unresolved concurrency-policy mutant and a mutant equivalent through the public API. Relevant records include `docs/audits/mutation-summary.md`, `agent-patches/AGENT-21-M2-mutation-killing-tests.patch`, and `LEDGER.md` Entries 72–75. 

Signed:  Sandeep Garg   Date: 11/23/2026
