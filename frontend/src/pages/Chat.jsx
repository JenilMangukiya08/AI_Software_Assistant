import { useState } from "react";
import Layout from "../components/Layout";
import Message from "../components/Messages";
import ChatInput from "../components/ChatInput";
import API from "../services/api";
import "../styles/chat.css";
import { useRef, useEffect } from "react";
import FileTree from "../components/FileTree";
import RepositoryStats from "../components/RepositoryStats";

export default function Chat() {

    const [messages, setMessages] = useState([]);
    const bottomRef = useRef(null);
    const [tree, setTree] = useState({});
    const [loading, setLoading] = useState(false);
    const [stats,setStats]=useState({});
    const loadConversation = async (id) => {
        try {
            const response = await API.get(`history/${id}/`);
            setMessages(response.data.messages);
            localStorage.setItem("session_id", id);
        }
        catch (error) {
            console.error(error);
        }
    };
    const [repositories, setRepositories] = useState([]);
    const [selectedRepo, setSelectedRepo] = useState(
        localStorage.getItem("repository") || ""
    );

    
    
    useEffect(() => {
            bottomRef.current?.scrollIntoView({
                behavior: "smooth"
            });
            }, [messages]);

    useEffect(() => {

        if (!selectedRepo) {

            setTree({});

            return;

        }

        API.get("repository-tree/", {

            params: {

                repository: selectedRepo

            }

        })
        .then((response) => {

            setTree(response.data);

        })
        .catch(console.error);

    }, [selectedRepo]);

    
    useEffect(() => {

        if (!selectedRepo) {

            setStats({});

            return;

        }

        API.get("repository-stats/", {

            params: {

                repository: selectedRepo

            }

        })
        .then((response) => {

            setStats(response.data);

        })
        .catch(console.error);

    }, [selectedRepo]);

    useEffect(() => {

        API.get("repositories/")
            .then((res) => {

                setRepositories(res.data);

            })
            .catch(console.error);

    }, []);


    const sendQuestion = async (question) => {

        setMessages((prev) => [
            ...prev,
            {
                sender: "user",
                text: question,
                time:new Date().toLocaleTimeString()
            }
        ]);

        setLoading(true);

        try {
            const repository = localStorage.getItem("repository");
            console.log("Repository =", repository);
            console.log("Question =", question);

            const response = await API.post("chat/", {
                repository,
                question
            });

            console.log(response.data);
            console.log(typeof response.data.answer);
            console.log(response.data.answer);

            setMessages((prev) => [
                ...prev,
                {
                    sender: "ai",
                    text: response.data.answer,
                    sources: response.data.sources || [],
                    
                }
            ]);

        }

        catch (error) {

            console.log("Error:", error);

            console.log("Response:", error.response);

            console.log("Data:", error.response?.data);

            setMessages((prev) => [
                ...prev,
                {
                    sender: "ai",
                    text: "Something went wrong."
                }
            ]);

        }

        setLoading(false);

    };

    return (

        <Layout onConversationSelect={loadConversation}>

            <div className="chat-layout">

                {/* LEFT SIDEBAR */}
                <div className="sidebar">
                    <div className="repo-card">
                        <h3>Repository</h3>
                        <select
                            value={selectedRepo}
                            onChange={(e) => {
                                const repo = e.target.value;
                                setSelectedRepo(repo);
                                localStorage.setItem("repository", repo);
                            }}
                        >
                            <option value="">
                                Select Repository
                            </option>
                            {repositories.map((repo) => (
                                <option
                                    key={repo.id}
                                    value={repo.collection_name}
                                >
                                    {repo.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    <FileTree
                        tree={tree}
                        onSelect={(file) =>
                            sendQuestion(`Explain ${file}`)
                        }
                    />
                    
                    
                                        

                    <div className="suggestions">

                        <button
                            onClick={() =>
                                sendQuestion("Summarize this repository")
                            }
                        >
                            Summarize Repository
                        </button>

                        <button
                            onClick={() =>
                                sendQuestion("Find bugs")
                            }
                        >
                            Find Bugs
                        </button>

                        <button
                            onClick={() =>
                                sendQuestion("Review the architecture")
                            }
                        >
                            Review Architecture
                        </button>

                    </div>
                    
                    
                    <button
                        className="clear-chat"
                        onClick={() => setMessages([])}
                    >
                        🗑 Clear Chat
                    </button>

                </div>
                

                {/* CHAT AREA */}

                <div className="chat-page">

                    <div className="chat-window">

                        {messages.map((message, index) => (

                            <Message
                                key={index}
                                sender={message.sender}
                                text={message.text}
                                time={message.time}
                                sources={message.sources}
                            />

                        ))}

                        {loading && (

                            <div className="thinking">

                                <div className="dot"></div>
                                <div className="dot"></div>
                                <div className="dot"></div>

                            </div>

                        )}

                        <div ref={bottomRef}></div>

                    </div>

                    <ChatInput
                        onSend={sendQuestion}
                        loading={loading}
                    />

                </div>

            </div>

        </Layout>

    );

}