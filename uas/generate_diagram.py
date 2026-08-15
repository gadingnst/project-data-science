import subprocess

# Serpentine CRISP-DM layout:
# Row 1 (top, L→R):  [1] → [2] → [3]
#                                    ↓
# Row 2 (bot, R→L):  [6] ← [5] ← [4]
#
# Key trick: bottom row visible edges go 4→5→6 but we need
# visual order 6,5,4 (left to right). We use constraint=false
# on visible bottom edges so they don't influence rank ordering,
# and rely on invisible edges to fix the visual position.

dot_code = r"""
digraph CRISP_DM {
    graph [bgcolor="#ffffff", fontname="Helvetica,Arial,sans-serif",
           rankdir=TB, nodesep=0.8, ranksep=0.9];
    node  [shape=box, style="filled,rounded",
           fontname="Helvetica,Arial,sans-serif", fontsize=11,
           fontcolor="#1F2937", penwidth=1.5, width=1.8, height=0.7];
    edge  [fontname="Helvetica,Arial,sans-serif", fontsize=9,
           color="#4B5563", penwidth=1.2, arrowsize=0.8];

    /* ── Declare nodes in desired left-to-right order per rank ── */

    /* Top row */
    step1 [label="1. Business\nUnderstanding",       fillcolor="#EFF6FF", color="#2563EB"];
    step2 [label="2. Data\nAcquisition",             fillcolor="#EFF6FF", color="#2563EB"];
    step3 [label="3. Data Preparation\n& Management", fillcolor="#EFF6FF", color="#2563EB"];

    /* Bottom row — declared 6, 5, 4 so default order is left-to-right */
    step6 [label="6. Deployment &\nBusiness Value",  fillcolor="#FEF3C7", color="#D97706"];
    step5 [label="5. Evaluation &\nInsight",         fillcolor="#F0FDF4", color="#16A34A"];
    step4 [label="4. Modeling &\nAnalytics",         fillcolor="#F0FDF4", color="#16A34A"];

    /* ── Rank constraints ── */
    { rank=same; step1; step2; step3; }
    { rank=same; step6; step5; step4; }

    /* ── Invisible ordering edges (high weight) ── */
    step1 -> step2 [style=invis, weight=100];
    step2 -> step3 [style=invis, weight=100];
    step6 -> step5 [style=invis, weight=100];
    step5 -> step4 [style=invis, weight=100];

    /* ── Anchor: align step1↔step6, step3↔step4 vertically ── */
    step1 -> step6 [style=invis, weight=10];
    step3 -> step4 [weight=10];

    /* ── Visible flow edges ── */
    step1 -> step2;
    step2 -> step3;
    /* step3 -> step4 already declared above with weight */
    step4 -> step5 [constraint=false];
    step5 -> step6 [constraint=false];
}
"""

base = "/root/.openclaw/workspace/projects/project-data-science/uas"

with open(f"{base}/crisp_dm.dot", "w") as f:
    f.write(dot_code)

subprocess.run(["dot", "-Tsvg", f"{base}/crisp_dm.dot", "-o", f"{base}/crisp_dm.svg"], check=True)
subprocess.run(["dot", "-Tpng", "-Gdpi=200", f"{base}/crisp_dm.dot", "-o", f"{base}/crisp_dm.png"], check=True)
print("Done — crisp_dm.dot / .svg / .png regenerated")
