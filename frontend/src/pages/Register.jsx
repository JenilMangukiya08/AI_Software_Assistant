import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";
import "../styles/chat.css";

export default function Register() {

    const navigate = useNavigate();

    const [form, setForm] = useState({

        username: "",

        email: "",

        password: ""

    });

    const register = async () => {

        try {

            await API.post("register/", form);

            alert("Registration Successful");

            navigate("/login");

        }

        catch (error) {

            alert("Registration Failed");

            console.log(error.response?.data);

        }

    };

    return (

        <div className="auth-container">

            <h2>Register</h2>

            <input

                placeholder="Username"

                onChange={(e) =>
                    setForm({

                        ...form,

                        username: e.target.value

                    })
                }

            />

            <input

                placeholder="Email"

                onChange={(e) =>
                    setForm({

                        ...form,

                        email: e.target.value

                    })
                }

            />

            <input

                type="password"

                placeholder="Password"

                onChange={(e) =>
                    setForm({

                        ...form,

                        password: e.target.value

                    })
                }

            />

            <button onClick={register}>

                Register

            </button>

        </div>

    );

}