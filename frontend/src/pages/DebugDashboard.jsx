import { useEffect, useState } from "react";
import API from "../services/api";
import Layout from "../components/Layout";
import "../styles/debug.css";

export default function DebugDashboard() {

    const [debug, setDebug] = useState(null);

    const loadDebug = () => {

        API.get("debug/")
            .then((res) => {

                setDebug(res.data);

            })
            .catch(console.error);

    };

    useEffect(() => {

        loadDebug();

    }, []);

    if (!debug) {

        return (

            <Layout>

                <div className="loading">

                    <h2>Loading AI Debug Dashboard...</h2>

                </div>

            </Layout>

        );

    }

    return (

        <Layout>

            <div className="dashboard">

                <div className="dashboard-header">

                    <h1>AI Software Assistant Debug Dashboard</h1>

                    <button
                        className="refresh-btn"
                        onClick={loadDebug}
                    >
                        Refresh
                    </button>

                </div>

                {/* ========================== */}
                {/* Metrics */}
                {/* ========================== */}

                <div className="metric-grid">

                    <div className="metric-card">

                        <h3>Workflow Latency</h3>

                        <h2>

                            {debug.metrics?.workflow_latency ?? 0}s

                        </h2>

                    </div>

                    <div className="metric-card">

                        <h3>LLM Calls</h3>

                        <h2>

                            {debug.metrics?.llm_calls ?? 0}

                        </h2>

                    </div>

                    <div className="metric-card">

                        <h3>Tool Calls</h3>

                        <h2>

                            {debug.metrics?.tool_calls ?? 0}

                        </h2>

                    </div>

                    <div className="metric-card">

                        <h3>Total Steps</h3>

                        <h2>

                            {debug.metrics?.steps ?? 0}

                        </h2>

                    </div>

                    <div className="metric-card">

                        <h3>Status</h3>

                        <h2
                            className={
                                debug.metrics?.status === "SUCCESS"
                                    ? "success"
                                    : "failed"
                            }
                        >
                            {debug.metrics?.status}
                        </h2>

                    </div>

                </div>

                {/* ========================== */}
                {/* Repository */}
                {/* ========================== */}

                <div className="section">

                    <h2>Repository Information</h2>

                    <div className="repo-card">

                        <p>

                            <strong>Repository:</strong>

                            {debug.repository || "Unknown"}

                        </p>

                        <p>

                            <strong>Question:</strong>

                            {debug.question || "Unknown"}

                        </p>

                    </div>

                </div>

                {/* ========================== */}
                {/* Execution Plan */}
                {/* ========================== */}

                <div className="section">

                    <h2>Execution Plan</h2>

                    <div className="plan-container">

                        {

                            debug.plan?.map((step, index) => (

                                <div
                                    className="plan-step"
                                    key={index}
                                >

                                    {index + 1}. {step}

                                </div>

                            ))

                        }

                    </div>

                </div>

                {/* ========================== */}
                {/* Progress */}
                {/* ========================== */}

                <div className="section">

                    <h2>Workflow Progress</h2>

                    <progress

                        value={debug.metrics?.steps || 0}

                        max={debug.metrics?.steps || 1}

                    />

                    <p>

                        Completed {debug.metrics?.steps || 0} Steps

                    </p>

                </div>

                {/* ========================== */}
                {/* Timeline */}
                {/* ========================== */}

                <div className="section">

                    <h2>Execution Timeline</h2>

                    <div className="timeline">

                        {

                            debug.trace?.map((step, index) => (

                                <div
                                    className="timeline-card"
                                    key={index}
                                >

                                    <div className="timeline-header">

                                        <h3>

                                            {step.step}

                                        </h3>

                                        <span
                                            className={
                                                step.status === "success"
                                                    ? "success"
                                                    : "failed"
                                            }
                                        >

                                            {step.status}

                                        </span>

                                    </div>

                                    <p>

                                        Latency :

                                        <strong>

                                            {step.latency}s

                                        </strong>

                                    </p>

                                    <p>

                                        Sources :

                                        <strong>

                                            {

                                                Array.isArray(step.sources)

                                                    ? step.sources.length

                                                    : step.sources || 0

                                            }

                                        </strong>

                                    </p>

                                    <p>

                                        Time :

                                        <strong>

                                            {step.timestamp || step.time}

                                        </strong>

                                    </p>

                                </div>

                            ))

                        }

                    </div>

                </div>

                {/* ========================== */}
                {/* Agent Summary */}
                {/* ========================== */}

                <div className="section">

                    <h2>Agent Summary</h2>

                    {

                        debug.history?.map((agent, index) => (

                            <div
                                className="agent-card"
                                key={index}
                            >

                                <h3>

                                    {agent.agent || agent.step}

                                </h3>

                                <p>

                                    Answer Length :

                                    <strong>

                                        {

                                            agent.answer

                                                ? agent.answer.length

                                                : 0

                                        }

                                    </strong>

                                </p>

                                <p>

                                    Sources :

                                    <strong>

                                        {

                                            Array.isArray(agent.sources)

                                                ? agent.sources.length

                                                : 0

                                        }

                                    </strong>

                                </p>

                            </div>

                        ))

                    }

                </div>

                {/* ========================== */}
                {/* Conversation */}
                {/* ========================== */}

                <div className="section">

                    <h2>Conversation History</h2>

                    {

                        debug.history?.map((item, index) => (

                            <div
                                className="history-card"
                                key={index}
                            >

                                <h3>

                                    {item.agent || item.step}

                                </h3>

                                <p>

                                    <strong>

                                        Question

                                    </strong>

                                </p>

                                <p>

                                    {item.question}

                                </p>

                                <p>

                                    <strong>

                                        Answer

                                    </strong>

                                </p>

                                <p>

                                    {

                                        item.answer

                                            ?.substring(0, 350)

                                    }

                                    ...

                                </p>

                            </div>

                        ))

                    }

                </div>

            </div>

        </Layout>

    );

}