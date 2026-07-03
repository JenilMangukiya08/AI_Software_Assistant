import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import API from "../services/api";
import { useNavigate } from "react-router-dom";
import "../styles/chat.css";
export default function Repositories() {

    const [repositories, setRepositories] = useState([]);
    const [search, setSearch] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        loadRepositories();
    }, []);

    async function loadRepositories() {
        const response = await API.get("repositories/");
        setRepositories(response.data);
    }
    async function deleteRepository(id) {
        if (!window.confirm("Delete this repository?"))
            return;
        await API.delete(`repositories/${id}/delete/`);
        loadRepositories();
    }

    const filtered = repositories.filter(repo =>
        repo.name.toLowerCase().includes(search.toLowerCase())
    );
    return (
        <Layout>
            <div className="repositories-page">
                <h2>📦 My Repositories</h2>
                <input
                    type="text"
                    placeholder="Search Repository"
                    value={search}
                    onChange={(e)=>setSearch(e.target.value)}
                    className="repo-search"
                />
                {
                    filtered.map(repo=>(
                        <div
                            key={repo.id}
                            className="repo-card"
                        >
                            <h3>
                                {repo.name}
                            </h3>
                            <p>
                                Uploaded :
                                {" "}
                                {new Date(repo.uploaded_at).toLocaleDateString()}
                            </p>
                            <p>
                                Chats :
                                {repo.chat_count}
                            </p>

                            <div className="repo-buttons">

                                <button
                                    onClick={() => navigate(`/repositories/${repo.id}`)}
                                >
                                    Details
                                </button>

                                <button
                                    className="delete"
                                    onClick={()=>deleteRepository(repo.id)}
                                >
                                    Delete
                                </button>
                            </div>
                        </div>
                    ))
                }
            </div>
        </Layout>
    );
}