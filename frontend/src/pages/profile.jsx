import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import API from "../services/api";
import "../styles/chat.css";
export default function Profile() {

    const [profile, setProfile] = useState(null);

    useEffect(() => {
        loadProfile();
    }, []);

    async function loadProfile() {

        const response = await API.get("profile/");

        setProfile(response.data);

    }

    if (!profile)
        return <h2>Loading...</h2>;

    return (

        <Layout>

            <div className="profile-page">

                <h2>👤 My Profile</h2>

                <div className="profile-card">

                    <h3>{profile.username}</h3>

                    <p>Email : {profile.email}</p>

                    <p>Joined : {new Date(profile.date_joined).toLocaleDateString()}</p>

                </div>

                <div className="stats-grid">

                    <div className="stat-card">

                        <h3>{profile.repositories}</h3>

                        <p>Repositories</p>

                    </div>

                    <div className="stat-card">

                        <h3>{profile.chat_sessions}</h3>

                        <p>Chat Sessions</p>

                    </div>

                    <div className="stat-card">

                        <h3>{profile.messages}</h3>

                        <p>Messages</p>

                    </div>

                </div>

            </div>

        </Layout>

    );

}