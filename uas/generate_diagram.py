import subprocess

# We build exact graphviz layout where:
# Row 1 (top, left to right): step1 -> step2 -> step3
# Row 2 (bottom, right to left visually): step6 <- step5 <- step4
# Link: step3 (top-right) -> step4 (bottom-right)

dot_code = """
digraph CRISP_DM {
    graph [bgcolor="#ffffff", fontname="Helvetica,Arial,sans-serif", nodesep=0.7, ranksep=0.6];
    node [shape=box, style="filled,rounded", fontname="Helvetica,Arial,sans-serif", fontsize=11, fontcolor="#1F2937", penwidth=1.5];
    edge [fontname="Helvetica,Arial,sans-serif", fontsize=9, color="#4B5563", penwidth=1.2, arrowsize=0.8];

    subgraph cluster_top {
        color=none;
        rank=same;
        step1 [label="1. Business\\nUnderstanding", fillcolor="#EFF6FF", color="#2563EB"];
        step2 [label="2. Data\\nAcquisition", fillcolor="#EFF6FF", color="#2563EB"];
        step3 [label="3. Data Preparation\\n& Management", fillcolor="#EFF6FF", color="#2563EB"];
    }

    subgraph cluster_bottom {
        color=none;
        rank=same;
        step6 [label="6. Deployment &\\nBusiness Value", fillcolor="#FEF3C7", color="#D97706"];
        step5 [label="5. Evaluation &\\nInsight", fillcolor="#F0FDF4", color="#16A34A"];
        step4 [label="4. Modeling &\\nAnalytics", fillcolor="#F0FDF4", color="#16A34A"];
    }

    step1 -> step2 -> step3;
    step3 -> step4;
    step5 -> step4 [dir=back];
    step6 -> step5 [dir=back];
}
"""

with open("/root/.openclaw/workspace/projects/project-data-science/uas/crisp_dm.dot", "w") as f:
    f.write(dot_code)

subprocess.run(["dot", "-Tsvg", "/root/.openclaw/workspace/projects/project-data-science/uas/crisp_dm.dot", "-o", "/root/.openclaw/workspace/projects/project-data-science/uas/crisp_dm.svg"])
subprocess.run(["dot", "-Tpng", "/root/.openclaw/workspace/projects/project-data-science/uas/crisp_dm.dot", "-o", "/root/.openclaw/workspace/projects/project-data-science/uas/crisp_dm.png"])
print("Fixed direction!")
