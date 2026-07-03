import Sidebar from "./Sidebar";
import Navbar from "./Navbar";
import "../styles/layout.css";

export default function Layout({children,onConversationSelect}) {
    return (
        <div className="app">
            <Sidebar onConversationSelect={onConversationSelect}/>

            <div className="main">

                <Navbar />

                <div className="content">
                    {children}
                </div>

            </div>
        </div>
    );
}