import ReactMarkdown from "react-markdown";
import { CopyToClipboard } from "react-copy-to-clipboard";
import { FaCopy } from "react-icons/fa";

export default function Message({ sender, text, time,sources }) {

    return (

        <div className={`message ${sender}`}>

            <ReactMarkdown>
                {text}
            </ReactMarkdown>

            {
                sender === "ai" &&
                sources &&
                sources.length > 0 && (

                    <div className="sources">

                        <strong>Sources</strong>

                        {
                            sources.map((source, index) => (

                                <div key={index}>
                                    📄 {source}
                                </div>

                            ))
                        }

                    </div>

                )
            }
            <div className="message-actions">

    {
        sender === "ai" && (

            <>
                <button
                    className="copy-btn"
                    onClick={() => navigator.clipboard.writeText(text)}
                >
                    📋 Copy
                </button>

                <button
                    className="download-btn"
                    onClick={() => {

                        const blob = new Blob(
                            [text],
                            { type: "text/markdown" }
                        );

                        const url = URL.createObjectURL(blob);

                        const a = document.createElement("a");

                        a.href = url;

                        a.download = "answer.md";

                        a.click();

                        URL.revokeObjectURL(url);

                    }}
                >
                    ⬇ Download
                </button>

            </>

        )
    }

</div>

            <small>{time}</small>
            

        </div>

    );

}