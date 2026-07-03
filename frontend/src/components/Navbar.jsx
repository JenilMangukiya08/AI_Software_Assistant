import { Link, useNavigate } from "react-router-dom";
import "../styles/chat.css";
export default function Navbar() {

    const navigate = useNavigate();

    const token = localStorage.getItem("access");

    const logout = () => {

        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        localStorage.removeItem("repository");

        navigate("/login");

    };

    return (

        <nav className="navbar">

            <Link to="/">Home</Link>

            {
                token ? (
                    <>
                        <Link to="/upload">
                            Upload Repository
                        </Link>

                        <Link to="/chat">
                            Chat
                        </Link>

                        <Link to="/repositories">
                            Repositories
                        </Link>

                        <Link to="/profile">
                            Profile
                        </Link>

                        <button onClick={logout}>
                            Logout
                        </button>
                    </>
                ) : (
                    <>
                        <Link to="/login">
                            Login
                        </Link>

                        <Link to="/register">
                            Register
                        </Link>

                        
                    </>
                )
            }

        </nav>

    );

}