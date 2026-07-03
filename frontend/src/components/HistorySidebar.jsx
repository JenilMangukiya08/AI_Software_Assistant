import { useEffect, useState } from "react";
import API from "../services/api";

export default function HistorySidebar({ onSelect }) {

    const [history, setHistory] = useState([]);

    useEffect(() => {

        loadHistory();

    }, []);

    async function loadHistory() {

        const response = await API.get("history/");

        setHistory(response.data);

    }

    return (

        <div className="history-sidebar">

            <h3>Chat History</h3>

            {

                history.map(chat => (

                    <div

                        key={chat.id}

                        className="history-item"

                        onClick={() => onSelect(chat.id)}

                    >

                        <strong>{chat.title}</strong>

                        <br />

                        <small>

                            {chat.repository}

                        </small>

                    </div>

                ))

            }

        </div>

    );

}