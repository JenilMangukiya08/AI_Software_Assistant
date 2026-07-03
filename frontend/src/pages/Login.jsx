import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";
import "../styles/chat.css";

export default function Login() {

    const navigate = useNavigate();

    const [username, setUsername] = useState("");

    const [password, setPassword] = useState("");

    const login = async () => {

        try {

            const response = await API.post(
                "token/",
                {
                    username,
                    password
                }
            );

            localStorage.setItem(
                "access",
                response.data.access
            );

            localStorage.setItem(
                "refresh",
                response.data.refresh
            );

            navigate("/upload");

        }

        catch {

            alert("Invalid Credentials");

        }

    };

    return (

        <div className="auth-container">

            <h2>Login</h2>

            <input

                placeholder="Username"

                onChange={(e) =>
                    setUsername(e.target.value)
                }

            />

            <input

                type="password"

                placeholder="Password"

                onChange={(e) =>
                    setPassword(e.target.value)
                }

            />

            <button onClick={login}>

                Login

            </button>

        </div>

    );

}