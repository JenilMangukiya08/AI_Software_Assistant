import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import StatCard from "../components/StatCard";
import API from "../services/api";

export default function Dashboard() {

    const [stats, setStats] = useState({
        repositories: 0,
        sessions: 0,
        messages: 0,
        answers: 0,
        top_repository: "-"
    });

    useEffect(() => {

        API.get("dashboard/")
            .then((response) => {

                setStats(response.data);

            })
            .catch(console.error);

    }, []);

    return (

        <Layout>

            <h1>Dashboard</h1>

            <div className="cards">

                <StatCard
                    title="Repositories"
                    value={stats.repositories}
                />

                <StatCard
                    title="Conversations"
                    value={stats.sessions}
                />

                <StatCard
                    title="Messages"
                    value={stats.messages}
                />

                <StatCard
                    title="AI Answers"
                    value={stats.answers}
                />

            </div>

            <h2>Most Used Repository</h2>

            <div className="repository">

                {stats.top_repository}

            </div>

        </Layout>

    );

}