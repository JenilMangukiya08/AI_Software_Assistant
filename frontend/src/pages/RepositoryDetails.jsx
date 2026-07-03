import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Layout from "../components/Layout";
import API from "../services/api";
import "../styles/chat.css";
export default function RepositoryDetails() {

    const { id } = useParams();

    const navigate = useNavigate();

    const [repo, setRepo] = useState(null);

    useEffect(() => {

        loadRepository();

    }, []);

    async function loadRepository() {

        const response = await API.get(

            `repositories/${id}/stats/`

        );

        setRepo(response.data);

    }

    async function deleteRepository() {

        if (!window.confirm("Delete this repository?"))
            return;

        await API.delete(

            `repositories/${id}/delete/`

        );

        navigate("/repositories");

    }

    if (!repo)

        return (

            <Layout>

                <h2>Loading...</h2>

            </Layout>

        );

    return (

        <Layout>

            <div className="repository-details">

                <h1>📦 {repo.repository}</h1>

                <div className="details-card">

                    <p>

                        <strong>GitHub URL</strong>

                    </p>

                    <a

                        href={repo.github_url}

                        target="_blank"

                        rel="noreferrer"

                    >

                        {repo.github_url}

                    </a>

                    <hr />

                    <p>

                        <strong>Uploaded</strong>

                    </p>

                    <p>

                        {new Date(
                            repo.uploaded_at
                        ).toLocaleDateString()}

                    </p>

                    <hr />

                    <div className="stats-grid">

                        <div className="stat-card">

                            <h2>

                                {repo.chat_sessions}

                            </h2>

                            <p>Chat Sessions</p>

                        </div>

                        <div className="stat-card">

                            <h2>

                                {repo.messages}

                            </h2>

                            <p>Messages</p>

                        </div>

                    </div>

                </div>

                <div className="recent-chat-card">

                    <h2>

                        Recent Chats

                    </h2>

                    {

                        repo.recent_chats.length === 0 ?

                        (

                            <p>

                                No chats yet.

                            </p>

                        )

                        :

                        repo.recent_chats.map(chat=>(

                            <div

                                key={chat.id}

                                className="recent-chat"

                            >

                                💬 {chat.title}

                            </div>

                        ))

                    }

                </div>

                <div className="action-buttons">

                    <button

                        className="open-btn"

                        onClick={()=>{

                            localStorage.setItem(

                                "repository",

                                repo.repository

                            );

                            navigate("/chat");

                        }}

                    >

                        Open Chat

                    </button>

                    <button

                        className="delete-btn"

                        onClick={deleteRepository}

                    >

                        Delete Repository

                    </button>

                </div>

            </div>

        </Layout>

    );

}