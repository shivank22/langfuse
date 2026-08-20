#!/usr/bin/env python3
"""High-level architecture for Central Langfuse Platform (icon/PNG via diagrams)."""
from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import Users
from diagrams.onprem.container import Docker
from diagrams.onprem.database import Clickhouse, PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.generic.storage import Storage
from diagrams.generic.blank import Blank
from diagrams.programming.framework import Nextjs
from diagrams.programming.language import Nodejs

GRAPH_ATTR = {
    "fontsize": "20",
    "bgcolor": "white",
    "pad": "0.5",
    "splines": "spline",
    "nodesep": "0.55",
    "ranksep": "0.7",
}

with Diagram(
    "Central Langfuse Platform",
    filename="architecture",
    outformat="png",
    show=False,
    direction="LR",
    graph_attr=GRAPH_ATTR,
):
    teams = Users("App teams\n(agents & apps)")

    with Cluster("Central Langfuse (Compose build)"):
        compose = Docker("docker-compose\n.build.yml")
        with Cluster("Application"):
            web = Nextjs("langfuse-web\nUI + API")
            worker = Nodejs("langfuse-worker\nevals & jobs")
        with Cluster("Data plane"):
            pg = PostgreSQL("PostgreSQL")
            ch = Clickhouse("ClickHouse")
            redis = Redis("Redis")
            minio = Storage("MinIO")

        compose >> Edge(label="builds/runs") >> web
        compose >> Edge(label="builds/runs") >> worker
        web >> Edge(label="metadata") >> pg
        web >> Edge(label="traces") >> ch
        worker >> Edge(label="queues") >> redis
        web >> Edge(label="events/media") >> minio
        worker >> Edge(label="reads/writes") >> pg
        worker >> Edge(label="analytics") >> ch

    openai = Blank("OpenAI API")

    teams >> Edge(label="traces, scores,\nprompt fetch") >> web
    teams >> Edge(label="LLM calls") >> openai
    worker >> Edge(label="LLM-as-Judge") >> openai
