import Layout from "../components/Layout";
import StatCard from "../components/StatCard";

export default function Dashboard() {

    return (

        <Layout>

            <h1>Dashboard</h1>

            <div className="cards">

                <StatCard
                    title="Repositories"
                    value="1"
                />

                <StatCard
                    title="Documents"
                    value="320"
                />

                <StatCard
                    title="Chats"
                    value="15"
                />

                <StatCard
                    title="AI Answers"
                    value="54"
                />

            </div>

            <h2>Recent Repository</h2>

            <div className="repository">

                AI_ROUTE_PLANNER

            </div>

        </Layout>

    );

}