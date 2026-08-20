#!/usr/bin/env python3
"""Small concept diagrams for Observability, Evaluations, Prompt Management."""
from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import User, Users
from diagrams.generic.blank import Blank
from diagrams.programming.language import Python
from diagrams.onprem.database import PostgreSQL
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

GRAPH = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.4",
    "splines": "spline",
    "nodesep": "0.4",
    "ranksep": "0.55",
}

OUT = Path(__file__).resolve().parent

# Palette aligned with product-overview PDF accent
BLUE = "#2563EB"
BLUE_LIGHT = "#DBEAFE"
BLUE_EDGE = "#93C5FD"
SLATE = "#0F172A"
MUTED = "#475569"
GREEN = "#059669"
GREEN_LIGHT = "#D1FAE5"
AMBER = "#D97706"
AMBER_LIGHT = "#FEF3C7"
WHITE = "#FFFFFF"


def _rounded(ax, x, y, w, h, facecolor, edgecolor, lw=1.4, radius=0.02):
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.012,rounding_size={radius}",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=lw,
        zorder=2,
    )
    ax.add_patch(box)
    return box


def _text(ax, x, y, s, *, size=9, weight="normal", color=SLATE, ha="center", va="center", wrap=None):
    ax.text(
        x,
        y,
        s,
        fontsize=size,
        fontweight=weight,
        color=color,
        ha=ha,
        va=va,
        zorder=3,
        linespacing=1.25,
        wrap=False,
    )


def _arrow(ax, x1, y1, x2, y2, *, color=MUTED, style="-|>", lw=1.5, connectionstyle="arc3,rad=0", ls="-"):
    arr = FancyArrowPatch(
        (x1, y1),
        (x2, y2),
        arrowstyle=style,
        mutation_scale=12,
        linewidth=lw,
        color=color,
        connectionstyle=connectionstyle,
        linestyle=ls,
        zorder=4,
    )
    ax.add_patch(arr)


def _v_flow(ax, x, y_upper_bottom, y_lower_bottom, card_h, *, color):
    """Arrow from bottom of upper card down to top of lower card."""
    _arrow(ax, x, y_upper_bottom - 0.004, x, y_lower_bottom + card_h + 0.004, color=color, lw=1.5)


def _step_card(ax, x, y, w, h, title, body, *, accent=BLUE):
    _rounded(ax, x, y, w, h, WHITE, BLUE_EDGE, lw=1.2)
    ax.add_patch(Rectangle((x, y), 0.012, h, facecolor=accent, edgecolor="none", zorder=3))
    _text(ax, x + w / 2 + 0.006, y + h - 0.028, title, size=8.5, weight="bold", color=accent)
    _text(ax, x + w / 2 + 0.006, y + h / 2 - 0.012, body, size=7.5, color=MUTED)


def render_build_runtime_figure(filename: str, *, title: str, eval_detail: bool):
    """
    Deb-style lifecycle: Build-time (left) vs Runtime (right, primary).
    Drawn with matplotlib so arrows stay intentional (not Graphviz spaghetti).
    """
    fig, ax = plt.subplots(figsize=(12.4, 8.0 if eval_detail else 7.0), dpi=160)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor(WHITE)

    _text(ax, 0.5, 0.97, title, size=13, weight="bold", color=SLATE)

    # Column frames
    _rounded(ax, 0.03, 0.10, 0.40, 0.82, "#F8FAFC", "#CBD5E1", lw=1.5, radius=0.025)
    _rounded(ax, 0.57, 0.10, 0.40, 0.82, BLUE_LIGHT, BLUE, lw=2.0, radius=0.025)

    # Headers
    _rounded(ax, 0.055, 0.83, 0.35, 0.065, AMBER_LIGHT, AMBER, lw=1.2)
    _text(ax, 0.23, 0.862, "BUILD-TIME  (pre-ship)", size=10, weight="bold", color=AMBER)

    _rounded(ax, 0.595, 0.83, 0.35, 0.065, BLUE, BLUE, lw=1.2)
    _text(ax, 0.77, 0.862, "RUNTIME  — primary focus", size=10, weight="bold", color=WHITE)

    _text(ax, 0.23, 0.805, "Validate agent changes before deploy", size=7.5, color=MUTED)
    _text(
        ax,
        0.77,
        0.805,
        "Central Langfuse: live traces + online scores",
        size=7.5,
        color=BLUE,
        weight="bold",
    )

    card_w = 0.32
    lx, rx = 0.07, 0.61
    cx_l, cx_r = 0.23, 0.77

    if eval_detail:
        card_h = 0.105
        build_ys = [0.68, 0.545, 0.41, 0.275]
        build_steps = [
            ("B1  Artifacts under change", "prompts · tools · agent logic\nmodel / config versions"),
            ("B2  Langfuse dataset", "gold cases + promoted failures\ninput · expected_output · expected_tools"),
            ("B3  Offline experiment", "task = your agent on every item\nLangfuse Experiments (SDK / UI)"),
            ("B4  Score + metrics gate", "code evaluators · OpenAI LLM-as-Judge\ngoal_achieved · tool_correctness\ntrajectory_ok · faithfulness"),
        ]
        for y, (title_s, body) in zip(build_ys, build_steps):
            _step_card(ax, lx, y, card_w, card_h, title_s, body, accent=AMBER)
        for yu, yl in zip(build_ys, build_ys[1:]):
            _v_flow(ax, cx_l, yu, yl, card_h, color=AMBER)

        _text(ax, cx_l, 0.24, "Pass gate → ready to ship", size=7.5, weight="bold", color=AMBER)
        _text(ax, cx_l, 0.195, "Optional CI: fail build on regressions", size=7, color=MUTED)

        runtime_ys = [0.68, 0.545, 0.41, 0.275]
        runtime_steps = [
            ("R1  Agent runs in prod / staging", "user turns · tool loops · OpenAI calls"),
            ("R2  Nested traces → Langfuse", "agent-run → plan / tool-* / openai-*\nsession · env · team + service tags"),
            ("R3  Online scoring (sampled)", "Langfuse worker + OpenAI judge\ncode checks · user_thumbs"),
            ("R4  Review in Langfuse UI", "latency · cost · failures\ngoal drift / loops visible only live"),
        ]
        for y, (title_s, body) in zip(runtime_ys, runtime_steps):
            _step_card(ax, rx, y, card_w, card_h, title_s, body, accent=BLUE)
        for yu, yl in zip(runtime_ys, runtime_ys[1:]):
            _v_flow(ax, cx_r, yu, yl, card_h, color=BLUE)

        _text(ax, cx_r, 0.24, "Hard failures → promote to B2 dataset", size=7.5, weight="bold", color=BLUE)
        _text(ax, cx_r, 0.195, "Same score names online & offline", size=7, color=MUTED)

        # Gutter bridges — no crossing diagonals:
        # top: promote failures (runtime → build) at B2 height
        _arrow(ax, 0.57, 0.597, 0.43, 0.597, color=MUTED, lw=1.8, ls="--")
        _text(ax, 0.50, 0.625, "promote failures", size=7.5, weight="bold", color=MUTED)

        # bottom: ship if pass (build → runtime)
        _arrow(ax, 0.43, 0.145, 0.57, 0.145, color=GREEN, lw=2.2)
        _text(ax, 0.50, 0.168, "ship if pass", size=8, weight="bold", color=GREEN)
    else:
        card_h = 0.125
        build_ys = [0.64, 0.46, 0.28]
        build_steps = [
            ("B1  Design & artifacts", "agent code · prompts · tools\npipeline structure checks"),
            ("B2  Simulation / offline runs", "Langfuse datasets + experiments\ncode evals · OpenAI LLM-as-Judge"),
            ("B3  Pre-ship gate", "catalog metrics must pass\noptional CI experiment job"),
        ]
        for y, (title_s, body) in zip(build_ys, build_steps):
            _step_card(ax, lx, y, card_w, card_h, title_s, body, accent=AMBER)
        for yu, yl in zip(build_ys, build_ys[1:]):
            _v_flow(ax, cx_l, yu, yl, card_h, color=AMBER)
        _text(ax, cx_l, 0.22, "Catch issues early — before users see them", size=7.5, color=MUTED)

        runtime_ys = [0.64, 0.46, 0.28]
        runtime_steps = [
            ("R1  Live agent execution", "non-deterministic plans & tool paths\ngoal drift / loops appear here"),
            ("R2  Central Langfuse tracing", "traces · observations · sessions\nenvironments · tags · cost / tokens"),
            ("R3  Online scores & review", "LLM-as-Judge · code · thumbs\nUI review → feed build-time datasets"),
        ]
        for y, (title_s, body) in zip(runtime_ys, runtime_steps):
            _step_card(ax, rx, y, card_w, card_h, title_s, body, accent=BLUE)
        for yu, yl in zip(runtime_ys, runtime_ys[1:]):
            _v_flow(ax, cx_r, yu, yl, card_h, color=BLUE)
        _text(ax, cx_r, 0.22, "Primary focus of this platform", size=7.5, weight="bold", color=BLUE)

        _arrow(ax, 0.57, 0.522, 0.43, 0.522, color=MUTED, lw=1.8, ls="--")
        _text(ax, 0.50, 0.55, "promote failures", size=7.5, weight="bold", color=MUTED)

        _arrow(ax, 0.43, 0.145, 0.57, 0.145, color=GREEN, lw=2.2)
        _text(ax, 0.50, 0.168, "ship if pass", size=8, weight="bold", color=GREEN)

    # Footer legend
    _rounded(ax, 0.03, 0.015, 0.94, 0.055, "#F1F5F9", "#CBD5E1", lw=1.0)
    _text(
        ax,
        0.5,
        0.042,
        "Tools: Langfuse (traces · datasets · experiments · scores)  ·  OpenAI (app LLM + LLM-as-a-Judge)  ·  code evaluators  ·  CI",
        size=7,
        color=MUTED,
    )

    out = OUT / filename
    fig.savefig(out, bbox_inches="tight", facecolor=WHITE, pad_inches=0.15)
    plt.close(fig)
    print(f"Wrote {out.name}")


def render_observability():
    with Diagram(
        "Observability concepts",
        filename="diagram-observability",
        outformat="png",
        show=False,
        direction="TB",
        graph_attr=GRAPH,
    ):
        user = User("End user")
        with Cluster("One session (multi-turn)"):
            t1 = Blank("Trace\nturn 1")
            t2 = Blank("Trace\nturn 2")
        with Cluster("Inside a trace"):
            root = Blank("agent-run\n(span)")
            plan = Blank("plan\n(span)")
            tool = Blank("tool-*\n(tool)")
            gen = Blank("openai-*\n(generation)")
        lf = PostgreSQL("Central\nLangfuse")

        user >> Edge(label="turns") >> t1
        user >> t2
        t1 >> Edge(label="nested steps") >> root
        root >> plan
        root >> tool
        root >> gen
        t1 >> Edge(label="async export") >> lf
        t2 >> lf


def render_evaluations():
    render_build_runtime_figure(
        "diagram-evaluations.png",
        title="Agent evaluation — build-time vs runtime (Central Langfuse)",
        eval_detail=True,
    )


def render_agentic_observability():
    render_build_runtime_figure(
        "diagram-agentic-observability.png",
        title="Agentic observability — build-time vs runtime",
        eval_detail=False,
    )


def render_prompts():
    with Diagram(
        "Prompt management",
        filename="diagram-prompts",
        outformat="png",
        show=False,
        direction="LR",
        graph_attr=GRAPH,
    ):
        owners = Users("Product /\ndomain")
        with Cluster("Langfuse prompts"):
            versions = Blank("Versions\nv1 v2 v3")
            labels = Blank("Labels\nstaging /\nproduction")
        app = Python("Team app\nSDK fetch")
        trace = Blank("Trace +\ngeneration\n(linked)")

        owners >> Edge(label="edit / promote") >> versions
        versions >> labels
        labels >> Edge(label="get_prompt\nlabel=production") >> app
        app >> Edge(label="link prompt\nto generation") >> trace


if __name__ == "__main__":
    render_observability()
    render_evaluations()
    render_agentic_observability()
    render_prompts()
    print(
        "Wrote diagram-observability.png, diagram-evaluations.png, "
        "diagram-agentic-observability.png, diagram-prompts.png"
    )
