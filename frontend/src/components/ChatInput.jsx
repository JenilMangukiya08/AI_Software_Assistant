import { useState } from "react";

export default function ChatInput({ onSend, loading }) {

    const [question, setQuestion] = useState("");

    const handleSubmit = (e) => {

        e.preventDefault();

        if (!question.trim()) return;

        onSend(question);

        setQuestion("");

    };

    return (

        <form className="chat-input" onSubmit={handleSubmit}>

            <input
                type="text"
                placeholder="Ask anything about the repository..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
            />

            <button disabled={loading}>
                {loading ? "Thinking..." : "Send"}
            </button>

        </form>

    );

}