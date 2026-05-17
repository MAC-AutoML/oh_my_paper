"""Deterministic SVG previews for the demo."""

from __future__ import annotations

def figure_pipeline() -> str:
    return """<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"1200\" height=\"520\" viewBox=\"0 0 1200 520\">
  <rect width=\"1200\" height=\"520\" fill=\"#f8fafc\"/>
  <text x=\"60\" y=\"60\" font-size=\"32\" font-family=\"Arial\" font-weight=\"700\" fill=\"#0f172a\">Policy-MME Diagnostic Pipeline</text>
  <g font-family=\"Arial\" font-size=\"18\">
    <rect x=\"70\" y=\"110\" width=\"220\" height=\"110\" rx=\"18\" fill=\"#dbeafe\" stroke=\"#2563eb\" stroke-width=\"3\"/>
    <text x=\"95\" y=\"150\" fill=\"#1e3a8a\" font-weight=\"700\">Input Material</text>
    <text x=\"95\" y=\"180\" fill=\"#1e40af\">PPO + RL evaluation</text>
    <text x=\"95\" y=\"205\" fill=\"#1e40af\">problem statement</text>

    <rect x=\"370\" y=\"110\" width=\"240\" height=\"110\" rx=\"18\" fill=\"#dcfce7\" stroke=\"#16a34a\" stroke-width=\"3\"/>
    <text x=\"395\" y=\"145\" fill=\"#14532d\" font-weight=\"700\">Capability Hierarchy</text>
    <text x=\"395\" y=\"175\" fill=\"#166534\">L1 stability</text>
    <text x=\"395\" y=\"200\" fill=\"#166534\">L2 robustness · L3 faithfulness</text>

    <rect x=\"700\" y=\"110\" width=\"240\" height=\"110\" rx=\"18\" fill=\"#fef3c7\" stroke=\"#d97706\" stroke-width=\"3\"/>
    <text x=\"725\" y=\"145\" fill=\"#78350f\" font-weight=\"700\">Grouped Scoring</text>
    <text x=\"725\" y=\"175\" fill=\"#92400e\">penalize fragmented wins</text>
    <text x=\"725\" y=\"200\" fill=\"#92400e\">reward consistent evidence</text>

    <rect x=\"430\" y=\"320\" width=\"340\" height=\"110\" rx=\"18\" fill=\"#ede9fe\" stroke=\"#7c3aed\" stroke-width=\"3\"/>
    <text x=\"460\" y=\"360\" fill=\"#4c1d95\" font-weight=\"700\">Paper Output</text>
    <text x=\"460\" y=\"390\" fill=\"#5b21b6\">claim-grounded sections</text>
    <text x=\"460\" y=\"415\" fill=\"#5b21b6\">explainable writing rationale</text>

    <path d=\"M295 165 L360 165\" stroke=\"#334155\" stroke-width=\"4\" marker-end=\"url(#arrow)\"/>
    <path d=\"M615 165 L690 165\" stroke=\"#334155\" stroke-width=\"4\" marker-end=\"url(#arrow)\"/>
    <path d=\"M820 230 C790 300 720 325 650 330\" stroke=\"#334155\" stroke-width=\"4\" fill=\"none\" marker-end=\"url(#arrow)\"/>
    <path d=\"M495 230 C500 285 525 310 565 330\" stroke=\"#334155\" stroke-width=\"4\" fill=\"none\" marker-end=\"url(#arrow)\"/>
  </g>
  <defs><marker id=\"arrow\" markerWidth=\"10\" markerHeight=\"10\" refX=\"8\" refY=\"3\" orient=\"auto\"><path d=\"M0,0 L0,6 L9,3 z\" fill=\"#334155\"/></marker></defs>
</svg>
"""


def figure_results() -> str:
    bars = [("PPO", 52.4, "#2563eb"), ("SAC", 58.2, "#16a34a"), ("TD3", 49.7, "#f97316"), ("Oracle", 88.9, "#7c3aed")]
    parts = ["<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"1200\" height=\"620\" viewBox=\"0 0 1200 620\">", "<rect width=\"1200\" height=\"620\" fill=\"#ffffff\"/>", "<text x=\"70\" y=\"60\" font-size=\"32\" font-family=\"Arial\" font-weight=\"700\" fill=\"#111827\">Synthetic Policy-MME Score Comparison</text>", "<text x=\"70\" y=\"95\" font-size=\"18\" font-family=\"Arial\" fill=\"#6b7280\">Demo numbers only: illustrate diagnostic reporting, not empirical claims.</text>"]
    x0, y0, width, maxv = 150, 500, 780, 100
    for i, (name, score, color) in enumerate(bars):
        y = y0 - i * 90
        bar_w = width * score / maxv
        parts.append(f"<text x=\"70\" y=\"{y-8}\" font-size=\"22\" font-family=\"Arial\" font-weight=\"700\" fill=\"#111827\">{name}</text>")
        parts.append(f"<rect x=\"{x0}\" y=\"{y-38}\" width=\"{bar_w:.1f}\" height=\"42\" rx=\"10\" fill=\"{color}\"/>")
        parts.append(f"<text x=\"{x0+bar_w+18:.1f}\" y=\"{y-10}\" font-size=\"22\" font-family=\"Arial\" fill=\"#111827\">{score}</text>")
    parts.append("<line x1=\"150\" y1=\"520\" x2=\"930\" y2=\"520\" stroke=\"#d1d5db\" stroke-width=\"2\"/>")
    parts.append("<text x=\"150\" y=\"560\" font-size=\"16\" font-family=\"Arial\" fill=\"#6b7280\">0</text><text x=\"910\" y=\"560\" font-size=\"16\" font-family=\"Arial\" fill=\"#6b7280\">100</text>")
    parts.append("<rect x=\"975\" y=\"155\" width=\"150\" height=\"170\" rx=\"16\" fill=\"#f3f4f6\" stroke=\"#d1d5db\"/>")
    parts.append("<text x=\"995\" y=\"195\" font-size=\"18\" font-family=\"Arial\" font-weight=\"700\" fill=\"#111827\">Takeaway</text>")
    parts.append("<text x=\"995\" y=\"230\" font-size=\"15\" font-family=\"Arial\" fill=\"#374151\">Average return can</text>")
    parts.append("<text x=\"995\" y=\"255\" font-size=\"15\" font-family=\"Arial\" fill=\"#374151\">hide robustness and</text>")
    parts.append("<text x=\"995\" y=\"280\" font-size=\"15\" font-family=\"Arial\" fill=\"#374151\">faithfulness failures.</text>")
    parts.append("</svg>\n")
    return "".join(parts)


def figure_hierarchy() -> str:
    return """<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"1200\" height=\"700\" viewBox=\"0 0 1200 700\">
  <rect width=\"1200\" height=\"700\" fill=\"#f8fafc\"/>
  <text x=\"70\" y=\"60\" font-size=\"32\" font-family=\"Arial\" font-weight=\"700\" fill=\"#0f172a\">Policy-MME Three-Level Capability Hierarchy</text>
  <text x=\"70\" y=\"95\" font-size=\"18\" font-family=\"Arial\" fill=\"#64748b\">Higher levels depend on lower-level optimization reliability.</text>
  <g font-family=\"Arial\">
    <rect x=\"120\" y=\"470\" width=\"960\" height=\"120\" rx=\"24\" fill=\"#dbeafe\" stroke=\"#2563eb\" stroke-width=\"3\"/>
    <text x=\"160\" y=\"515\" font-size=\"25\" font-weight=\"700\" fill=\"#1e3a8a\">Level 1 · Optimization Stability</text>
    <text x=\"160\" y=\"550\" font-size=\"18\" fill=\"#1e40af\">seed variance · training collapse · destructive updates · hyperparameter sensitivity</text>
    <rect x=\"190\" y=\"310\" width=\"820\" height=\"120\" rx=\"24\" fill=\"#dcfce7\" stroke=\"#16a34a\" stroke-width=\"3\"/>
    <text x=\"230\" y=\"355\" font-size=\"25\" font-weight=\"700\" fill=\"#14532d\">Level 2 · Robustness and Generalization</text>
    <text x=\"230\" y=\"390\" font-size=\"18\" fill=\"#166534\">reward noise · dynamics shift · observation corruption · delayed reward</text>
    <rect x=\"260\" y=\"150\" width=\"680\" height=\"120\" rx=\"24\" fill=\"#fef3c7\" stroke=\"#d97706\" stroke-width=\"3\"/>
    <text x=\"300\" y=\"195\" font-size=\"25\" font-weight=\"700\" fill=\"#78350f\">Level 3 · Decision Faithfulness</text>
    <text x=\"300\" y=\"230\" font-size=\"18\" fill=\"#92400e\">counterfactual probes · action support · shortcut detection</text>
    <path d=\"M600 470 L600 430\" stroke=\"#334155\" stroke-width=\"5\" marker-end=\"url(#arrow3)\"/>
    <path d=\"M600 310 L600 270\" stroke=\"#334155\" stroke-width=\"5\" marker-end=\"url(#arrow3)\"/>
    <text x=\"745\" y=\"455\" font-size=\"17\" fill=\"#475569\">instability propagates upward</text>
    <text x=\"745\" y=\"295\" font-size=\"17\" fill=\"#475569\">brittleness undermines faithfulness</text>
  </g>
  <defs><marker id=\"arrow3\" markerWidth=\"10\" markerHeight=\"10\" refX=\"8\" refY=\"3\" orient=\"auto\"><path d=\"M0,0 L0,6 L9,3 z\" fill=\"#334155\"/></marker></defs>
</svg>
"""
