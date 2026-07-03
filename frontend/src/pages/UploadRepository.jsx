import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
import API from "../services/api";
import "../styles/upload.css";

export default function UploadRepository() {

    const navigate = useNavigate();

    const [url, setUrl] = useState("");
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");
    const [repository, setRepository] = useState("");

    const handleSubmit = async (e) => {

        e.preventDefault();

        if (!url) {
            setMessage("Please enter a GitHub repository URL.");
            return;
        }

        setLoading(true);
        setMessage("");

        try {
            const response = await API.post("upload-repository/", {
                url: url,
            });
            console.log(response.data);

            setMessage(response.data.message);
            setRepository(response.data.repository);
            localStorage.setItem(
                "repository",
                response.data.repository
            );
            console.log("Saved:", localStorage.getItem("repository"));

            setTimeout(() => {
                navigate("/chat");
            }, 1500);

        } 
        catch (error) {

            console.log(error);

            console.log(error.response);

            console.log(error.response?.data);

            setMessage(
                error.response?.data?.message ||
                error.response?.data?.error ||
                error.message
            );

        }

        setLoading(false);
    };

    return (

        <Layout>

            <div className="upload-container">

                <h1>Upload GitHub Repository</h1>

                <form onSubmit={handleSubmit}>

                    <input
                        type="text"
                        placeholder="https://github.com/username/project"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                    />

                    <button
                        type="submit"
                        disabled={loading}
                    >

                        {loading ? "Indexing..." : "Index Repository"}

                    </button>

                </form>

                {message && (
                    <p className="message">
                        {message}
                    </p>
                )}

            </div>

        </Layout>

    );

}