import { Routes, Route } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import Dashboard from "./pages/Dashboard";
import UploadRepository from "./pages/UploadRepository";
import Chat from "./pages/Chat";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Profile from "./pages/Profile";
import Repositories from "./pages/Repositories";
import RepositoryDetails from "./pages/RepositoryDetails";
import DebugDashboard from "./pages/DebugDashboard";
function App() {
    return (
        <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/upload" element={<ProtectedRoute><UploadRepository /></ProtectedRoute>} />
            <Route path="/chat" element={<ProtectedRoute><Chat /></ProtectedRoute>} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>}/>
            <Route path="/repositories" element={<ProtectedRoute><Repositories/></ProtectedRoute>}/>
            <Route path="/repositories/:id" element={<ProtectedRoute><RepositoryDetails/></ProtectedRoute>}/>
            <Route path="/debug" element={<DebugDashboard />} />
        </Routes>
);
}

export default App;