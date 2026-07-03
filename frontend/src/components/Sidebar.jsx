import { Link } from "react-router-dom";
import {
    FaHome,
    FaGithub,
    FaComments
} from "react-icons/fa";
import HistorySidebar from "./HistorySidebar";



export default function Sidebar({
    onConversationSelect
}) {
    return (

        <div className="sidebar">

            <h2>AI Assistant</h2>

            <Link to="/">
                <FaHome /> Dashboard
            </Link>

            <Link to="/upload">
                <FaGithub /> Upload Repo
            </Link>

            <Link to="/chat">
                <FaComments /> Chat
            </Link>
            
            <HistorySidebar

                        onSelect={onConversationSelect}

                    />
            

            
        </div>
        

    );
}